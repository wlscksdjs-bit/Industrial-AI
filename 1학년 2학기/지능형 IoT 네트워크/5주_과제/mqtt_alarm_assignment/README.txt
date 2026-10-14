과제: MQTT 기반 설비 이상 알람 서비스 구현

[파일]
  sensor_simulator.py  센서 시뮬레이터        (USER_ID, RUN_MODE만 수정)
  anomaly_model.py     이상 탐지 모델(제공)   (수정 금지)
  alarm_service.py     알람 서비스            (과제 구현 파일, TODO 1~5)
  watch_alarms.py      개발용 실시간 모니터   (USER_ID만 수정)
  check_alarms.py      제출용 자동 검사기     (USER_ID만 수정)

[준비]
  pip install paho-mqtt numpy
  네 파일(sensor_simulator, alarm_service, watch_alarms, check_alarms)의 USER_ID를 동일한 본인 ID로 수정

[개발 중] quick 모드: 1회 약 1분 30초, 이상 4건
  sensor_simulator.py의 RUN_MODE = "quick" (기본값)
  터미널 1: python watch_alarms.py     (계속 켜 둠, 알람·상태만 표시하고 정답과 바로 비교)
  터미널 2: python alarm_service.py    (코드를 고칠 때마다 다시 실행)
  터미널 3: python sensor_simulator.py
  -> 터미널 1에 OK / 오탐 / 놓침 / 중복이 바로 표시됨

[제출 전] full 모드: 1회 약 10분, 이상 12건
  sensor_simulator.py의 RUN_MODE = "full"
  터미널 1: python check_alarms.py
  터미널 2: python alarm_service.py
  터미널 3: python sensor_simulator.py
  -> 시뮬레이터 종료 후 검사 [1]~[7] 출력
  -> 안내가 나오면 60초 안에 터미널 2에서 Ctrl + C  (검사 [8] Will 메시지)
  -> check_result.json 저장 (mode가 "full"이어야 제출 가능)

[로컬 브로커 사용 시]
  환경 변수 MQTT_BROKER 로 브로커 주소 지정 (예: MQTT_BROKER=127.0.0.1)
