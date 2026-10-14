"""
pub_step3_retained.py — [Step 3] Retained 상태 발행기 (터미널 2)

retain=True로 최신 상태 1건을 발행한 후 종료한다.
이후 sub_console.py를 재실행하면 [RETAINED] 표시와 함께 상태가 즉시 수신되는지 확인한다.

실습 후 보관 메시지 삭제:
  client.publish(TOPIC_STATE, "", qos=1, retain=True)
"""
import json
import time
import paho.mqtt.client as mqtt

USER_ID = "2026254019"
BROKER = "broker.emqx.io"
PORT = 1883
TOPIC_STATE = f"{USER_ID}/factory/line1/press01/state"


def get_mqtt_client():
    try:
        return mqtt.Client(mqtt.CallbackAPIVersion.VERSION2)
    except AttributeError:
        return mqtt.Client()


client = get_mqtt_client()
client.connect(BROKER, PORT)
client.loop_start()
time.sleep(1)

state_payload = {
    "equipment": "press01",
    "status": "RUNNING",
    "operator": "Kim_HJ",
    "timestamp": time.strftime("%Y-%m-%d %H:%M:%S")
}

print(f"[Step 3] 토픽({TOPIC_STATE})에 Retained 메시지 발행 중...")
# retain=True: 브로커가 이 메시지를 메모리에 보관
client.publish(TOPIC_STATE, json.dumps(state_payload), qos=1, retain=True)

print("발행 완료. 프로그램을 종료합니다.")
print(">>> 확인: 관제 콘솔(sub_console.py) 재실행 시 이 상태가 [RETAINED] 표시와 함께 즉시 수신되는지 확인하십시오.")

time.sleep(1)  # 전송 완료 대기
client.loop_stop()
client.disconnect()
