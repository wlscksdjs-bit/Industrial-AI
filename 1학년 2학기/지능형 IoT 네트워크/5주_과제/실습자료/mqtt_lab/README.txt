MQTT 4단계 실습 코드

[준비]
  pip install paho-mqtt
  5개 파일의 USER_ID = "myname" 을 동일한 본인 ID(이니셜 또는 학번)로 수정

[실행 순서]
  터미널 1: python sub_console.py          (실습 내내 실행 유지)
  터미널 2: python pub_step1_basic.py      Step 1 Pub/Sub (Ctrl + C로 종료)
            python pub_step2_wildcard.py   Step 2 와일드카드
            python pub_step3_retained.py   Step 3 Retained Message -> 이후 sub_console.py 재실행
            python pub_step4_lwt.py        Step 4 LWT (Will 메시지)

[Step 2 비교]
  sub_console.py의 TOPIC_ALL을 line1/+/temp 또는 line1/# 로 변경하여 수신 범위를 비교한다.

[Step 4 확인 절차] 터미널 1의 sub_console.py를 실행해 둔 상태로 진행
  ① pub_step4_lwt.py 실행 직후 : 관제 콘솔에 status = ONLINE 수신 (센서가 직접 발행)
  ② 5초 후 자동 강제 종료     : 관제 콘솔에 status = CRITICAL_OFFLINE 수신
                                (센서 코드에 OFFLINE 발행 구문 없음 -> 브로커의 대리 발행)
  ③ sub_console.py 재실행     : [RETAINED] CRITICAL_OFFLINE 즉시 수신
                                (Will 메시지가 브로커에 보관되어 ONLINE을 대체)

[정리]
  Step 3·4의 Retained 메시지는 브로커에 남는다.
  같은 토픽에 빈 페이로드를 retain=True로 발행하여 삭제한다.
