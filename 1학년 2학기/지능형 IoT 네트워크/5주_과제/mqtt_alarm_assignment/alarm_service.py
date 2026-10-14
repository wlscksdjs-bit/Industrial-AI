"""
alarm_service.py — 설비 이상 알람 서비스 (과제 구현 파일)

이상 탐지 모델(anomaly_model.py)은 이미 주어져 있다.
이 파일에서 TODO 1~5를 채워, 모델이 판정한 이상을 MQTT 알람으로 내보낸다.

  TODO 1 (Step 1 Pub/Sub)   : 텔레메트리와 시뮬레이터 신호 구독
  TODO 2 (상태 전이)         : NORMAL ↔ ALARM 상태 판단
  TODO 3 (Step 2 토픽 계층)  : 이상 유형별 알람 토픽으로 발행
  TODO 4 (Step 3 Retained)  : 현재 설비 상태(health)를 retain으로 발행
  TODO 5 (Step 4 LWT)       : 서비스 상태 ONLINE 발행 + OFFLINE Will 메시지 등록

토픽과 메시지 형식은 과제 안내 문서의 표를 따른다.
"""
import json
import os
import sys
import paho.mqtt.client as mqtt
from anomaly_model import AnomalyModel

if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')

USER_ID = "2026254019"  # 본인 ID로 변경 (simulator, check_alarms와 동일)
BROKER = os.environ.get("MQTT_BROKER", "broker.emqx.io")
PORT = 1883

BASE = f"{USER_ID}/factory/line1"
TOPIC_TELEMETRY = f"{BASE}/press01/telemetry"          # 구독: 센서 값
TOPIC_SIM = f"{BASE}/press01/sim"                      # 구독: 시뮬레이터 START / END
TOPIC_ALARM = f"{BASE}/press01/alarm"                  # 발행: 알람 → {TOPIC_ALARM}/{이상 유형}
TOPIC_HEALTH = f"{BASE}/press01/health"                # 발행: 현재 설비 상태 (retain)
TOPIC_STATUS = f"{BASE}/alarm_service/status"          # 발행: 서비스 상태 (retain + Will)

n_warmup = 600    # 학습 구간 샘플 수 (시뮬레이터 START 메시지 값으로 갱신)
CLEAR_COUNT = 10  # 정상 판정이 연속 10회 나오면 NORMAL로 복귀

# ---------------- 제공: 모델 학습·판정 ----------------
model = AnomalyModel()
warmup = []
ready = False

# ---------------- 상태 변수 ----------------
state = "NORMAL"   # "NORMAL" 또는 "ALARM"
normal_run = 0     # 연속 정상 판정 횟수


def reset(client):
    """시뮬레이터가 새로 시작하면 모든 상태를 초기화한다."""
    global model, warmup, ready, state, normal_run
    model, warmup, ready = AnomalyModel(), [], False
    state, normal_run = "NORMAL", 0
    publish_health(client, "NORMAL", None, None)


def publish_health(client, state_value, anomaly_type, seq):
    # TODO 4: TOPIC_HEALTH에 현재 상태를 retain=True, qos=1로 발행한다.
    #   메시지 예: {"state": "ALARM", "type": "stuck", "seq": 1412}
    #             {"state": "NORMAL", "type": null, "seq": 1500}
    payload = {
        "state": state_value,
        "type": anomaly_type,
        "seq": seq
    }
    client.publish(TOPIC_HEALTH, json.dumps(payload), qos=1, retain=True)


def publish_alarm(client, sample, result):
    # TODO 3: f"{TOPIC_ALARM}/{result['type']}" 토픽에 qos=1로 알람을 발행한다.
    #   메시지 예: {"seq": 1412, "ts": 1790751430.2, "type": "stuck", "score": 12.5}
    #   seq, ts는 sample에서, type, score는 result에서 가져온다.
    payload = {
        "seq": sample["seq"],
        "ts": sample["ts"],
        "type": result["type"],
        "score": result["score"]
    }
    topic = f"{TOPIC_ALARM}/{result['type']}"
    client.publish(topic, json.dumps(payload), qos=1)


def on_connect(client, userdata, flags, rc, properties=None):
    # TODO 1: TOPIC_TELEMETRY와 TOPIC_SIM을 qos=1로 구독한다.
    if rc == 0:
        client.subscribe([(TOPIC_TELEMETRY, 1), (TOPIC_SIM, 1)])
        print("[알람 서비스] 브로커 연결 완료 및 텔레메트리/시뮬레이터 신호 구독 시작")
    else:
        print(f"[알람 서비스] 브로커 연결 실패 (코드: {rc})")


def on_message(client, userdata, msg):
    global ready, state, normal_run, n_warmup
    data = json.loads(msg.payload.decode("utf-8"))

    if msg.topic == TOPIC_SIM:
        if data.get("event") == "START":
            n_warmup = data.get("n_warmup", n_warmup)
            reset(client)
            print("[알람 서비스] 시뮬레이터 시작. 상태를 초기화합니다.")
        return
    if "seq" not in data:
        return  # 형식이 다른 메시지는 무시

    # 학습 구간: 제공 코드가 모델을 학습한다
    if not ready:
        if data["seq"] < n_warmup:
            warmup.append(data)
            if len(warmup) % 50 == 0 or len(warmup) == n_warmup:
                print(f"[알람 서비스] 학습 구간 수집 중... ({len(warmup)}/{n_warmup})")
            if len(warmup) >= n_warmup:
                model.fit(warmup)
                ready = True
                print(f"[알람 서비스] 모델 준비 완료 (학습 샘플 {len(warmup)}개). 이상 판정을 시작합니다.")
            return
        else:
            # seq >= n_warmup 인데 아직 ready가 안 된 경우 (패킷 누락 대비)
            if len(warmup) >= 50:
                model.fit(warmup)
                ready = True
                print(f"[알람 서비스] 모델 준비 완료 (수집 샘플 {len(warmup)}개로 학습 완료). 이상 판정을 시작합니다.")
            else:
                return

    result = model.predict(data)  # {"anomaly": bool, "type": str|None, "score": float}

    # TODO 2: 상태 전이를 구현한다.
    #   - result["anomaly"]가 True이면 normal_run = 0
    #       · state가 "NORMAL"이면 → state = "ALARM",
    #         publish_alarm()과 publish_health(..., "ALARM", ...) 호출, 화면에 알람 출력
    #   - result["anomaly"]가 False이면 normal_run += 1
    #       · state가 "ALARM"이고 normal_run >= CLEAR_COUNT이면 → state = "NORMAL",
    #         publish_health(..., "NORMAL", ...) 호출, 화면에 복귀 출력
    #   (ALARM 상태가 이어지는 동안에는 알람을 다시 보내지 않는다)
    if result["anomaly"]:
        normal_run = 0
        if state == "NORMAL":
            state = "ALARM"
            publish_alarm(client, data, result)
            publish_health(client, "ALARM", result["type"], data["seq"])
            print(f"[알람 서비스] [알람 발생] seq {data['seq']}  유형: {result['type']:<9} (score: {result['score']})")
    else:
        normal_run += 1
        if state == "ALARM" and normal_run >= CLEAR_COUNT:
            state = "NORMAL"
            publish_health(client, "NORMAL", None, data["seq"])
            print(f"[알람 서비스] [상태 복귀] seq {data['seq']}  정상(NORMAL) 상태 복귀")


if __name__ == "__main__":
    client = mqtt.Client(mqtt.CallbackAPIVersion.VERSION2) if hasattr(mqtt, "CallbackAPIVersion") else mqtt.Client()
    client.on_connect = on_connect
    client.on_message = on_message

    # TODO 5-1: 연결 전에 TOPIC_STATUS로 Will 메시지를 등록한다 (qos=1, retain=True).
    #   메시지: {"service": "alarm_service", "status": "OFFLINE"}
    lwt_payload = json.dumps({"service": "alarm_service", "status": "OFFLINE"})
    client.will_set(TOPIC_STATUS, payload=lwt_payload, qos=1, retain=True)

    client.connect(BROKER, PORT, keepalive=10)

    # TODO 5-2: 연결 직후 TOPIC_STATUS에 ONLINE을 발행한다 (qos=1, retain=True).
    #   메시지: {"service": "alarm_service", "status": "ONLINE"}
    online_payload = json.dumps({"service": "alarm_service", "status": "ONLINE"})
    client.publish(TOPIC_STATUS, online_payload, qos=1, retain=True)

    print("[알람 서비스] 시뮬레이터보다 먼저 실행해야 학습 구간을 받을 수 있습니다.")
    try:
        client.loop_forever()
    except KeyboardInterrupt:
        # disconnect() 없이 종료 → 브로커가 Will 메시지를 발행한다 (검사 [8])
        print("\n[알람 서비스] 종료합니다.")
