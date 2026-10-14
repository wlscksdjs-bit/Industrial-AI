"""
sensor_simulator.py — 프레스 설비(press01) 센서 시뮬레이터 (수정하지 말 것)

온도·진동·전류 3채널 텔레메트리를 발행한다. 실행 모드는 RUN_MODE로 고른다.
  - "quick" (개발용) : 10 Hz · 900개 · 약 1분 30초. 학습 구간 300개, 이상 4건(유형별 1건)
  - "full"  (제출용) : 5 Hz · 3,000개 · 약 10분. 학습 구간 600개, 이상 12건(유형별 3건)
정답은 실행 폴더의 ground_truth.json에 저장되며, 검사 도구만 이 파일을 읽는다.
"""
import json
import math
import os
import sys
import random
import time
import paho.mqtt.client as mqtt

if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')

USER_ID = "2026254019"  # 본인 ID로 변경 (alarm_service, check_alarms, watch_alarms와 동일)
RUN_MODE = "full"  # 개발 중에는 "quick", 제출용 검사는 "full"
BROKER = os.environ.get("MQTT_BROKER", "broker.emqx.io")
PORT = 1883
SEED = 2026  # 같은 SEED = 같은 데이터. 최종 평가는 공개되지 않은 SEED로 수행

MODES = {"quick": {"rate_hz": 10, "n_samples": 900, "n_warmup": 300, "n_per_type": 1},
         "full": {"rate_hz": 5, "n_samples": 3000, "n_warmup": 600, "n_per_type": 3}}
_m = MODES[RUN_MODE]
RATE_HZ = float(os.environ.get("SIM_RATE_HZ", _m["rate_hz"]))  # 발행 주기 [Hz]
N_SAMPLES = _m["n_samples"]
N_WARMUP = _m["n_warmup"]
CYCLE = 300  # 부하 사이클 길이 [샘플]

TOPIC_TELEMETRY = f"{USER_ID}/factory/line1/press01/telemetry"
TOPIC_SIM = f"{USER_ID}/factory/line1/press01/sim"
GT_FILE = "ground_truth.json"

# 이상 유형: (최소 길이, 최대 길이) [샘플]
ANOMALY_SPECS = {"spike": (1, 3), "drift": (150, 150), "vib_noise": (100, 100), "stuck": (80, 80)}
N_PER_TYPE = _m["n_per_type"]
MIN_GAP = 40  # 이상 사이 최소 간격 [샘플]


def make_schedule(rng):
    """학습 구간 이후에 이상을 겹치지 않게 배치한다."""
    types = [t for t in ANOMALY_SPECS for _ in range(N_PER_TYPE)]
    rng.shuffle(types)
    durations = [rng.randint(*ANOMALY_SPECS[t]) for t in types]
    region_start, region_end = N_WARMUP + MIN_GAP, N_SAMPLES - MIN_GAP
    slack = (region_end - region_start) - sum(durations) - MIN_GAP * (len(types) - 1)
    weights = [rng.random() for _ in range(len(types) + 1)]
    extra = [slack * w / sum(weights) for w in weights]

    events, pos = [], region_start + extra[0]
    for i, (t, d) in enumerate(zip(types, durations)):
        start = int(pos)
        events.append({"type": t, "start": start, "end": start + d - 1})
        pos = start + d + MIN_GAP + extra[i + 1]
    return events


def generate(rng, events):
    """정상 신호를 만든 뒤 이상을 주입한다. 반환: 샘플 리스트"""
    samples = []
    for i in range(N_SAMPLES):
        load = 1.5 * math.sin(2 * math.pi * i / CYCLE)  # 부하 사이클
        current = 12.0 + load + rng.gauss(0, 0.15)
        temp = 26.0 + 0.4 * load + rng.gauss(0, 0.08)
        vib = 0.40 + 0.02 * load + rng.gauss(0, 0.015)
        samples.append({"load": load, "temp": temp, "vib_rms": vib, "current": current})

    for ev in events:
        s, e, t = ev["start"], ev["end"], ev["type"]
        length = e - s + 1
        stuck_value = samples[s - 1]["temp"]
        for k, i in enumerate(range(s, e + 1)):
            x = samples[i]
            if t == "spike":
                x["vib_rms"] += 0.35
            elif t == "drift":
                x["temp"] += 4.0 * (k + 1) / length
            elif t == "vib_noise":
                x["vib_rms"] = 0.40 + 0.02 * x["load"] + rng.gauss(0, 0.075)
            elif t == "stuck":
                x["temp"] = stuck_value

    return [{"seq": i,
             "temp": round(x["temp"], 3),
             "vib_rms": round(x["vib_rms"], 4),
             "current": round(x["current"], 3)} for i, x in enumerate(samples)]


def get_mqtt_client():
    try:
        return mqtt.Client(mqtt.CallbackAPIVersion.VERSION2)
    except AttributeError:
        return mqtt.Client()


if __name__ == "__main__":
    rng = random.Random(SEED)
    events = make_schedule(rng)
    data = generate(rng, events)

    with open(GT_FILE, "w", encoding="utf-8") as f:
        json.dump({"mode": RUN_MODE, "seed": SEED, "rate_hz": RATE_HZ, "n_samples": N_SAMPLES,
                   "n_warmup": N_WARMUP, "events": events}, f, indent=2)

    client = get_mqtt_client()
    client.connect(BROKER, PORT, keepalive=60)
    client.loop_start()
    time.sleep(1)

    info = {"event": "START", "mode": RUN_MODE, "seed": SEED, "n_samples": N_SAMPLES,
            "n_warmup": N_WARMUP, "rate_hz": RATE_HZ}
    client.publish(TOPIC_SIM, json.dumps(info), qos=1)
    print(f"[시뮬레이터] {RUN_MODE} 모드 발행 시작: {N_SAMPLES}개, {RATE_HZ:g} Hz, 약 {N_SAMPLES / RATE_HZ / 60:.1f}분")
    print(f"[시뮬레이터] 처음 {N_WARMUP}개 샘플은 학습 구간입니다.\n")

    period = 1.0 / RATE_HZ
    t_next = time.time()
    for x in data:
        msg = dict(x, ts=round(time.time(), 3))
        client.publish(TOPIC_TELEMETRY, json.dumps(msg), qos=1)
        if x["seq"] == N_WARMUP - 1:
            print("[시뮬레이터] 학습 구간 종료. 이후 구간에 이상이 주입됩니다.")
        if (x["seq"] + 1) % 300 == 0:
            print(f"[시뮬레이터] {x['seq'] + 1}/{N_SAMPLES} 발행")
        t_next += period
        time.sleep(max(0.0, t_next - time.time()))

    time.sleep(1)
    client.publish(TOPIC_SIM, json.dumps({"event": "END"}), qos=1)
    time.sleep(1)
    print("\n[시뮬레이터] 발행 완료.")
    client.loop_stop()
    client.disconnect()
