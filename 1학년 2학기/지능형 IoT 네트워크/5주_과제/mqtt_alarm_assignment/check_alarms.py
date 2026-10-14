"""
check_alarms.py — 알람 서비스 자동 검사기 (수정하지 말 것, USER_ID만 수정)

알람·상태 토픽을 구독하여 alarm_service.py가 요구사항대로 동작하는지 검사한다.
시뮬레이터 종료(END) 후 [1]~[7]을 검사하고, 마지막으로 [8] Will 메시지 검사를 위해
알람 서비스를 강제 종료하도록 안내한다. 결과는 check_result.json에 저장된다.
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
TOPIC_SIM = f"{BASE}/press01/sim"
TOPIC_ALARM_ALL = f"{BASE}/press01/alarm/+"
TOPIC_HEALTH = f"{BASE}/press01/health"
TOPIC_STATUS = f"{BASE}/alarm_service/status"
GT_FILE = "ground_truth.json"
RESULT_FILE = "check_result.json"
TYPES = {"spike", "drift", "vib_noise", "stuck"}
TOLERANCE = 10     # 이상 종료 후 허용 샘플 수
WILL_TIMEOUT = 60  # [8] OFFLINE 대기 시간 [s]

alarms = []  # (topic, payload dict 또는 None, qos)
state = {"end_time": None}


def new_client():
    return mqtt.Client(mqtt.CallbackAPIVersion.VERSION2) if hasattr(mqtt, "CallbackAPIVersion") else mqtt.Client()


def parse(payload):
    try:
        return json.loads(payload.decode("utf-8"))
    except Exception:
        return None


def on_connect(client, userdata, flags, rc, properties=None):
    client.subscribe([(TOPIC_SIM, 1), (TOPIC_ALARM_ALL, 1)])
    print("[검사기] 대기 중... 시뮬레이터 실행을 기다립니다.")


def on_message(client, userdata, msg):
    if msg.topic == TOPIC_SIM:
        data = parse(msg.payload) or {}
        if data.get("event") == "START":
            alarms.clear()
            state["end_time"] = None
            print("[검사기] 시뮬레이터 시작 감지. 알람 수집을 시작합니다.")
        elif data.get("event") == "END":
            state["end_time"] = time.time()
        return
    alarms.append((msg.topic, parse(msg.payload), msg.qos))
    print(f"[검사기] 알람 수신: {msg.topic}")


def read_retained(topic, wait=3.0):
    """새 클라이언트로 구독하여 retain된 메시지를 읽는다."""
    got = {}
    c = new_client()
    c.on_connect = lambda cl, u, f, rc, p=None: cl.subscribe(topic, 1)
    c.on_message = lambda cl, u, m: got.update(msg=parse(m.payload), retain=m.retain)
    c.connect(BROKER, PORT, keepalive=30)
    c.loop_start()
    t0 = time.time()
    while "msg" not in got and time.time() - t0 < wait:
        time.sleep(0.1)
    c.loop_stop()
    c.disconnect()
    return got


def check_alarms(gt):
    events = gt["events"]
    windows = [(e["start"], e["end"] + TOLERANCE) for e in events]
    items = []

    ok_topic = bool(alarms) and all(t.rsplit("/", 1)[-1] in TYPES and p and p.get("type") == t.rsplit("/", 1)[-1]
                                    for t, p, _ in alarms)
    items.append(("[1] 알람 토픽이 .../alarm/{유형}이고 payload의 type과 일치", ok_topic))

    ok_fields = bool(alarms) and all(p and {"seq", "ts", "type", "score"} <= set(p) for _, p, _ in alarms)
    items.append(("[2] 알람 payload에 seq, ts, type, score 포함", ok_fields))

    ok_qos = bool(alarms) and all(q == 1 for _, _, q in alarms)
    items.append(("[3] 알람을 QoS 1로 발행", ok_qos))

    seqs = [p["seq"] for _, p, _ in alarms if p and "seq" in p]
    detected, per_event = 0, []
    for e, (s, w) in zip(events, windows):
        hits = sorted(q for q in seqs if s <= q <= w)
        detected += bool(hits)
        per_event.append({"type": e["type"], "start": e["start"], "alarms": len(hits)})
    items.append((f"[4] 이상 이벤트 알람 ({detected}/{len(events)}건, {len(events) - 1}건 이상이면 통과)",
                  detected >= len(events) - 1))

    extra = len(seqs) - detected
    items.append((f"[5] 이벤트당 알람 1건 (전체 알람 {len(seqs)}건, 초과 {extra}건, 2건 이하면 통과)",
                  bool(seqs) and extra <= 2))
    return items, per_event


def report(items):
    print("\n================ 검사 결과 ================")
    for name, ok in items:
        print(f"{'PASS' if ok else 'FAIL'}  {name}")
    print("===========================================")


if __name__ == "__main__":
    client = new_client()
    client.on_connect = on_connect
    client.on_message = on_message
    client.connect(BROKER, PORT, keepalive=60)
    client.loop_start()
    try:
        while state["end_time"] is None or time.time() - state["end_time"] < 3:
            time.sleep(0.2)
    except KeyboardInterrupt:
        raise SystemExit("\n[검사기] 중단되었습니다.")
    client.loop_stop()
    client.disconnect()

    if not os.path.exists(GT_FILE):
        raise SystemExit(f"[검사기] {GT_FILE}이 없습니다. 시뮬레이터와 같은 폴더에서 실행하십시오.")
    with open(GT_FILE, encoding="utf-8") as f:
        gt = json.load(f)
    items, per_event = check_alarms(gt)
    mode = gt.get("mode", "full")

    health = read_retained(TOPIC_HEALTH)
    ok = bool(health.get("retain")) and (health.get("msg") or {}).get("state") == "NORMAL"
    items.append(("[6] health가 retain으로 보관되고 종료 시점 상태가 NORMAL", ok))

    status = read_retained(TOPIC_STATUS)
    ok = bool(status.get("retain")) and (status.get("msg") or {}).get("status") == "ONLINE"
    items.append(("[7] 서비스 상태 ONLINE이 retain으로 보관됨", ok))
    report(items)

    print(f"\n[8] Will 메시지 검사: {WILL_TIMEOUT}초 안에 alarm_service.py 터미널에서 Ctrl + C를 누르십시오.")
    offline = {}
    c = new_client()
    c.on_connect = lambda cl, u, f, rc, p=None: cl.subscribe(TOPIC_STATUS, 1)

    def on_status(cl, u, m):
        msg = parse(m.payload) or {}
        if not m.retain and msg.get("status") == "OFFLINE":
            offline["t"] = time.time()
    c.on_message = on_status
    c.connect(BROKER, PORT, keepalive=30)
    c.loop_start()
    t0 = time.time()
    while "t" not in offline and time.time() - t0 < WILL_TIMEOUT:
        time.sleep(0.2)
    c.loop_stop()
    c.disconnect()
    items.append(("[8] 서비스 비정상 종료 시 OFFLINE Will 메시지 발행", "t" in offline))

    report(items)
    passed = sum(ok for _, ok in items)
    print(f"통과 {passed}/{len(items)}  ·  실행 모드 {mode}  ·  결과 저장: {RESULT_FILE}")
    if mode != "full":
        print('※ 개발용(quick) 결과입니다. 제출용 결과는 시뮬레이터를 RUN_MODE = "full"로 실행하여 만드십시오.')
    with open(RESULT_FILE, "w", encoding="utf-8") as f:
        json.dump({"user_id": USER_ID, "mode": mode, "passed": passed, "total": len(items),
                   "items": [{"check": n, "pass": ok} for n, ok in items],
                   "events": per_event}, f, indent=2, ensure_ascii=False)
