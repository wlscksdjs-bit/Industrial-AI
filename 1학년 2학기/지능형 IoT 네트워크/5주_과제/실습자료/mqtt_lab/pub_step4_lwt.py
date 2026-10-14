"""
pub_step4_lwt.py — [Step 4] LWT 등록과 비정상 종료 재현 (터미널 2)

Will 메시지(LWT)를 등록하고 status 토픽에 ONLINE을 발행한 뒤,
DISCONNECT 없이 프로세스를 강제 종료하여 브로커의 Will 메시지 대리 발행을 확인한다.

[확인 절차] 터미널 1에서 sub_console.py를 실행해 둔 상태로 진행
 ① 실행 직후   : 관제 콘솔에 status = ONLINE 수신 (이 코드가 직접 발행)
 ② 강제 종료 후: 관제 콘솔에 status = CRITICAL_OFFLINE 수신
                 → 이 코드에는 OFFLINE 발행 구문이 없으므로 브로커가 대리 발행한 것
 ③ 콘솔 재실행 : [RETAINED] 표시와 함께 CRITICAL_OFFLINE 즉시 수신
                 → Will 메시지가 브로커에 보관되어 있음

실습 후 정리: status 토픽에 빈 페이로드를 retain=True로 발행하여 보관 메시지 삭제
  client.publish(TOPIC_STATUS, "", qos=1, retain=True)
"""
import time
import json
import os
import sys
import paho.mqtt.client as mqtt

USER_ID = "2026254019"
BROKER = "broker.emqx.io"
PORT = 1883
TOPIC_TELEMETRY = f"{USER_ID}/factory/line1/press01/telemetry"
TOPIC_STATUS = f"{USER_ID}/factory/line1/press01/status"


def get_mqtt_client():
    try:
        return mqtt.Client(mqtt.CallbackAPIVersion.VERSION2)
    except AttributeError:
        return mqtt.Client()


client = get_mqtt_client()

# ========================================================
# [핵심] 브로커 연결 전에 Will 메시지(LWT) 등록
# DISCONNECT 없이 연결이 종료되면 브로커가 이 메시지를 대신 발행한다.
# ========================================================
lwt_payload = json.dumps({
    "equipment": "press01",
    "status": "CRITICAL_OFFLINE",
    "reason": "Sudden Power Cut / Network Lost"
})

client.will_set(TOPIC_STATUS, payload=lwt_payload, qos=1, retain=True)

print("[Step 4] Will 메시지 등록 (CONNECT 패킷에 포함되어 브로커에 전달)")
print(f"  토픽    : {TOPIC_STATUS}")
print(f"  페이로드: {lwt_payload}\n")

# Keep-Alive 주기를 5초로 짧게 설정하여 단절 감지 시간 단축
client.connect(BROKER, PORT, keepalive=5)
client.loop_start()
time.sleep(1)  # 연결 대기

# 접속 직후 정상 상태(ONLINE) 발행 — 이 코드가 status 토픽에 직접 발행하는 유일한 메시지
online_payload = json.dumps({"equipment": "press01", "status": "ONLINE"})
client.publish(TOPIC_STATUS, online_payload, qos=1, retain=True)
print("① status = ONLINE 발행 완료. 관제 콘솔에서 수신을 확인하십시오.\n")

for i in range(1, 6):
    data = {"power_kw": 45.2, "count": i}
    client.publish(TOPIC_TELEMETRY, json.dumps(data))
    print(f"[{i}/5] telemetry 발행 중...")
    time.sleep(1)

print(f"\n② [장애 재현] {time.strftime('%H:%M:%S')} DISCONNECT 없이 프로세스를 강제 종료합니다.")
print("   관제 콘솔에 status = CRITICAL_OFFLINE이 수신되는지 확인하십시오.")
print("③ 이어서 관제 콘솔을 재실행하여 [RETAINED] 표시와 함께 다시 수신되는지 확인하십시오.")
sys.stdout.flush()  # os._exit()는 출력 버퍼를 비우지 않으므로 먼저 출력

# disconnect() 없이 프로세스 강제 종료 (finally 블록도 실행되지 않음)
os._exit(1)
