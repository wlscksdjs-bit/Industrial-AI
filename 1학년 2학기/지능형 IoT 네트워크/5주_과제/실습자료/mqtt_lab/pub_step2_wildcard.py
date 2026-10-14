"""
pub_step2_wildcard.py — [Step 2] 와일드카드 검증 발행기 (터미널 2)

설비(press01, press02, press03)와 센서 종류(temp, vibration)별 토픽에 1회씩 발행한다.
line2/press03/temp는 line1 토픽 필터와 비교하기 위한 비교군이다.

+ / # 의 차이를 확인하려면 sub_console.py의 TOPIC_ALL을
  f"{USER_ID}/factory/line1/+/temp" 또는 f"{USER_ID}/factory/line1/#" 로 변경하여 실행한다.
"""
import time
import json
import paho.mqtt.client as mqtt

USER_ID = "2026254019"
BROKER = "broker.emqx.io"
PORT = 1883


def get_mqtt_client():
    try:
        return mqtt.Client(mqtt.CallbackAPIVersion.VERSION2)
    except AttributeError:
        return mqtt.Client()


client = get_mqtt_client()
client.connect(BROKER, PORT)
client.loop_start()

time.sleep(1)  # 연결 안정화 대기

# 설비·센서별 토픽과 페이로드
data_samples = [
    (f"{USER_ID}/factory/line1/press01/temp", {"machine": "press01", "temp": 26.5}),
    (f"{USER_ID}/factory/line1/press02/temp", {"machine": "press02", "temp": 27.8}),
    (f"{USER_ID}/factory/line1/press01/vibration", {"machine": "press01", "vibe_rms": 0.42}),
    (f"{USER_ID}/factory/line2/press03/temp", {"machine": "press03", "temp": 24.1})  # 비교군
]

print("[Step 2] 설비·센서별 토픽 발행 시작 (0.5초 간격)\n")

for topic, payload in data_samples:
    client.publish(topic, json.dumps(payload), qos=0)
    print(f"발행 완료 ──> 토픽: {topic}")
    time.sleep(0.5)

print("\n[Step 2] 4개 토픽 발행 완료. 관제 콘솔의 수신 범위를 확인하십시오.")
client.loop_stop()
client.disconnect()
