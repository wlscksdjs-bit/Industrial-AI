"""
sub_console.py — 통합 관제 수신기 (터미널 1)

실습 전 과정에서 터미널 1에 실행해 두는 중앙 관제 콘솔이다.
와일드카드(#)로 본인 ID 하위의 모든 토픽을 구독하고, 수신 메시지를 출력한다.
"""
import time
import json
import sys
import paho.mqtt.client as mqtt

if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')

# ==========================================
# [설정] 본인의 이니셜 또는 학번으로 변경 (토픽 충돌 방지)
# ==========================================
USER_ID = "2026254019"
BROKER = "broker.emqx.io"
PORT = 1883
TOPIC_ALL = f"{USER_ID}/factory/#"
# Step 2 와일드카드 비교 시 아래 토픽 필터로 변경하여 실행
#   단일 레벨(+): f"{USER_ID}/factory/line1/+/temp"
#   다중 레벨(#): f"{USER_ID}/factory/line1/#"


def get_mqtt_client():
    """paho-mqtt v2.0+ / v1.x 호환 클라이언트 생성 함수"""
    try:
        # paho-mqtt v2.0 이상
        return mqtt.Client(mqtt.CallbackAPIVersion.VERSION2)
    except AttributeError:
        # paho-mqtt v1.x 구버전
        return mqtt.Client()


def on_connect(client, userdata, flags, rc, properties=None):
    if rc == 0:
        print("\n==========================================")
        print(f"[관제 콘솔] 브로커({BROKER}) 연결 성공")
        print(f"[관제 콘솔] 토픽 필터 구독 시작: {TOPIC_ALL}")
        print("==========================================\n")
        client.subscribe(TOPIC_ALL)
    else:
        print(f"[오류] 브로커 연결 실패 (코드: {rc})")


def on_message(client, userdata, msg):
    timestamp = time.strftime("%H:%M:%S")
    topic = msg.topic
    retained_flag = "[RETAINED] " if msg.retain else ""

    try:
        # JSON 형식으로 파싱
        payload = json.loads(msg.payload.decode("utf-8"))
        formatted_payload = json.dumps(payload, ensure_ascii=False)
    except Exception:
        # 파싱 실패 시 문자열로 출력
        formatted_payload = msg.payload.decode("utf-8", errors="replace")

    print(f"[{timestamp}] {retained_flag}토픽: {topic}")
    print(f"  └─ 페이로드: {formatted_payload}\n")


if __name__ == "__main__":
    client = get_mqtt_client()
    client.on_connect = on_connect
    client.on_message = on_message

    print("[시스템] 브로커 연결 시도 중...")
    client.connect(BROKER, PORT, keepalive=60)

    try:
        client.loop_forever()
    except KeyboardInterrupt:
        print("\n[관제 콘솔] 모니터링을 종료합니다.")
