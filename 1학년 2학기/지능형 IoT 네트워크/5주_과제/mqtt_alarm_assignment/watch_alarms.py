"""
watch_alarms.py — 개발용 실시간 모니터 (제공, USER_ID만 수정)

센서 값(telemetry)은 한 줄씩 출력하지 않고, 알람 서비스가 발행한 결과만 골라 보여준다.
알람이 들어오는 즉시 정답(ground_truth.json)과 비교하여 일치·오탐·놓침을 표시한다.

  출력 예
    [정답] seq 412  stuck 이상 시작
    [알람] seq 415  stuck   OK 정답과 일치 (0.3 s 후)
    [health] ALARM · stuck  (retain)
    [놓침] seq 600  drift 이상에 알람 없음

시뮬레이터를 여러 번 다시 실행해도 계속 동작한다. 종료는 Ctrl + C.
"""
import json
import os
import sys
import time
import paho.mqtt.client as mqtt

if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')

USER_ID = "2026254019"  # 본인 ID로 변경 (simulator, alarm_service와 동일)
BROKER = os.environ.get("MQTT_BROKER", "broker.emqx.io")
PORT = 1883

BASE = f"{USER_ID}/factory/line1"
TOPIC_TELEMETRY = f"{BASE}/press01/telemetry"
TOPIC_SIM = f"{BASE}/press01/sim"
TOPIC_ALARM_ALL = f"{BASE}/press01/alarm/+"
TOPIC_HEALTH = f"{BASE}/press01/health"
TOPIC_STATUS = f"{BASE}/alarm_service/status"
GT_FILE = "ground_truth.json"
TOLERANCE = 10  # 이상 종료 후 허용 샘플 수

run = {"events": [], "n_samples": 0, "n_warmup": 0, "rate": 5.0, "fp": 0, "dup": 0, "wrong": 0}


def now():
    return time.strftime("%H:%M:%S")


def parse(payload):
    try:
        return json.loads(payload.decode("utf-8"))
    except Exception:
        return None


def start_run(info):
    events = []
    if os.path.exists(GT_FILE):
        with open(GT_FILE, encoding="utf-8") as f:
            events = [dict(e, alarm_seq=None) for e in json.load(f)["events"]]
    run.update(events=events, n_samples=info.get("n_samples", 0), n_warmup=info.get("n_warmup", 0),
               rate=float(info.get("rate_hz", 5)), fp=0, dup=0, wrong=0)
    print(f"\n[{now()}] ===== 시뮬레이터 시작 · {info.get('mode', 'full')} 모드 · "
          f"{run['n_samples']}개 샘플 · 이상 {len(events)}건 =====")
    if not events:
        print("  (ground_truth.json이 없어 정답 비교 없이 알람만 표시합니다. 시뮬레이터와 같은 폴더에서 실행하십시오.)")


def on_telemetry(seq):
    step = max(run["n_samples"] // 9, 1)
    if seq < run["n_warmup"] and seq % step == 0:
        print(f"[{now()}] [진행] {seq}/{run['n_samples']} · 학습 구간")
    if seq == run["n_warmup"]:
        print(f"[{now()}] [진행] 학습 구간 종료 · 이상 판정 구간 시작 (seq {seq})")
    for e in run["events"]:
        if seq == e["start"]:
            print(f"[{now()}] [정답] seq {seq}  {e['type']} 이상 시작")
        if seq == e["end"] + TOLERANCE and e["alarm_seq"] is None:
            print(f"[{now()}] [놓침] seq {e['start']}  {e['type']} 이상에 알람 없음")


def on_alarm(topic, data):
    if not data or "seq" not in data:
        print(f"[{now()}] [알람] {topic}  형식 오류: {data}")
        return
    seq, typ = data["seq"], data.get("type")
    topic_type = topic.rsplit("/", 1)[-1]
    note = "" if topic_type == typ else f"  (토픽 유형 {topic_type} ≠ payload 유형 {typ})"
    match = next((e for e in run["events"] if e["start"] <= seq <= e["end"] + TOLERANCE), None)
    if match is None:
        run["fp"] += 1
        verdict = "오탐 (정답 이상 없음)" if run["events"] else ""
    elif match["alarm_seq"] is not None:
        run["dup"] += 1
        verdict = "중복 알람 (같은 이상에 두 번째 알람)"
    else:
        match["alarm_seq"] = seq
        delay = (seq - match["start"]) / run["rate"]
        if match["type"] == typ:
            verdict = f"OK 정답과 일치 ({delay:.1f} s 후)"
        else:
            run["wrong"] += 1
            verdict = f"유형 불일치 (정답 {match['type']})"
    print(f"[{now()}] [알람] seq {seq}  {typ:<9} {verdict}{note}")


def on_end():
    ev = run["events"]
    hit = sum(e["alarm_seq"] is not None for e in ev)
    print(f"[{now()}] ===== 종료 · 탐지 {hit}/{len(ev)} · 오탐 {run['fp']} · 중복 {run['dup']} · "
          f"유형 불일치 {run['wrong']} =====\n")


def on_connect(client, userdata, flags, rc, properties=None):
    client.subscribe([(TOPIC_SIM, 1), (TOPIC_TELEMETRY, 0), (TOPIC_ALARM_ALL, 1),
                      (TOPIC_HEALTH, 1), (TOPIC_STATUS, 1)])
    print(f"[{now()}] 모니터 시작 · 알람·health·status만 표시합니다. 시뮬레이터 실행을 기다립니다.")


def on_message(client, userdata, msg):
    data = parse(msg.payload)
    retained = "  (retain)" if msg.retain else ""
    if msg.topic == TOPIC_SIM and data:
        if data.get("event") == "START":
            start_run(data)
        elif data.get("event") == "END":
            on_end()
    elif msg.topic == TOPIC_TELEMETRY and data and "seq" in data:
        on_telemetry(data["seq"])
    elif msg.topic == TOPIC_HEALTH:
        if data:
            extra = f" · {data.get('type')}" if data.get("type") else ""
            print(f"[{now()}] [health] {data.get('state')}{extra}{retained}")
    elif msg.topic == TOPIC_STATUS:
        if data:
            print(f"[{now()}] [status] {data.get('status')}{retained}")
    else:
        on_alarm(msg.topic, data)


if __name__ == "__main__":
    client = mqtt.Client(mqtt.CallbackAPIVersion.VERSION2) if hasattr(mqtt, "CallbackAPIVersion") else mqtt.Client()
    client.on_connect = on_connect
    client.on_message = on_message
    client.connect(BROKER, PORT, keepalive=60)
    try:
        client.loop_forever()
    except KeyboardInterrupt:
        print("\n[모니터] 종료합니다.")
