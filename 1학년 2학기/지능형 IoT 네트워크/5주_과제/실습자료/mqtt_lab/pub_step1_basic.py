"""
pub_step1_basic.py — [Step 1] 주기적 온도 발행기 (터미널 2)

1호기 프레스의 온도 센서가 1초 주기로 가상 온도를 발행한다.
단일 Publisher–Subscriber 간 메시지 전달을 확인한다.
"""
import time
import json
import random
import sys
import paho.mqtt.client as mqtt

USER_ID = "2026254019"  # sub_console.py와 동일해야 함
BROKER = "broker.emqx.io"
PORT = 1883
TOPIC = f"{USER_ID}/factory/line1/press01/temp"
MAX_COUNT = int(sys.argv[1]) if len(sys.argv) > 1 else None


def get_mqtt_client():
    try:
        return mqtt.Client(mqtt.CallbackAPIVersion.VERSION2)
    except AttributeError:
        return mqtt.Client()


client = get_mqtt_client()
client.connect(BROKER, PORT, keepalive=60)
client.loop_start()  # 네트워크 처리를 백그라운드 스레드에서 실행

print(f"[Step 1] 1호기 프레스 온도 센서 발행 시작 (토픽: {TOPIC})")
print("종료하려면 Ctrl + C를 누르십시오.\n")

try:
    count = 1
    while MAX_COUNT is None or count <= MAX_COUNT:
        # 가상 온도 데이터 생성 (25.0 ~ 28.0 °C)
        current_temp = round(random.uniform(25.0, 28.0), 2)
        payload = {
            "sensor_id": "press01_temp",
            "sequence": count,
            "temperature": current_temp,
            "unit": "Celsius"
        }

        # QoS 0 등급으로 발행
        client.publish(TOPIC, json.dumps(payload), qos=0)
        print(f"[{count}회차] 온도 발행 완료: {current_temp} °C")

        count += 1
        time.sleep(1)
except KeyboardInterrupt:
    print("\n[Step 1] 발행을 중지합니다. (정상 종료: DISCONNECT 전송)")
finally:
    client.loop_stop()
    client.disconnect()
