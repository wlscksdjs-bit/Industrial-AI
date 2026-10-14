# 🌐 지능형 IoT 네트워크 (Intelligent IoT Network)

본 저장소는 충북대학교 일반대학원 산업인공지능학과 **지능형 IoT 네트워크** 교과의 강의 자료(PDF), 주차별 연구 보고서, 실습 코드(Jupyter Notebook & Python Script) 및 과제 산출물을 체계적으로 관리하는 공간입니다.

---

## 📌 교과 개요 및 목표
* **교과목명**: 지능형 IoT 네트워크 (Intelligent IoT Network)
* **담당 교수**: 이혁로 교수님
* **소속**: 충북대학교 일반대학원 산업인공지능학과 (석사과정)
* **연구자**: 진찬언 (학번: 2026254019)
* **주요 내용**: 스마트팩토리 및 산업 인공지능 인프라를 뒷받침하는 사물인터넷(IoT) 아키텍처, OSI 7계층 네트워크 프로토콜, 무선 센서 네트워크(WSN), 엣지 컴퓨팅, 산업용 메시징 프로토콜(MQTT, OPC UA) 및 암호화 네트워크 트래픽 분류를 위한 딥러닝 모델링 기술을 학습합니다.

---

## 📂 주차별 강의 자료 및 산출물 일람

| 주차 / 주제 | 강의 자료 | 실습 및 산출물 폴더 | 주요 학습 내용 및 핵심 기술 |
| :--- | :--- | :--- | :--- |
| **1주차** | [`지능형 IoT 네트워크(1주차 - 오리엔테이션).pdf`](./지능형%20IoT%20네트워크(1주차%20-%20오리엔테이션).pdf) | - | • IoT 개념, 발전사 및 산업 인공지능과의 융합<br>• 센서 노드, 게이트웨이, 클라우드 연계 아키텍처 |
| **2주차** | [`지능형 IoT 네트워크(2주차 - 지능형 IoT 개요).pdf`](./지능형%20IoT%20네트워크(2주차%20-%20지능형%20IoT%20개요).pdf) | - | • 지능형 IoT 시스템 구성 요소 및 스마트 센싱<br>• 온디바이스 AI, 엣지 AI와 네트워크 대역폭 최적화 |
| **3주차** | [`지능형 IoT 네트워크(3주차 - 지능형 IoT와 OSI 7계층).pdf`](./지능형%20IoT%20네트워크(3주차%20-%20지능형%20IoT%20와%20OSI%207계층).pdf) | [`3주_과제/`](./3주_과제/) | • OSI 7계층 및 TCP/IP 5계층 프로토콜 스택<br>• 네트워크 패킷 캡처(PCAP) 및 플로우(Flow) 통계 추출<br>• **[연구 과제]** ISCXVPN2016 암호화 트래픽 다중 분류 딥러닝 모델 성능 개선 |
| **4주차** | [`지능형 IoT 네트워크(4주차 - 지능형 IoT를 위한 무선 통신 기술).pdf`](./지능형%20IoT%20네트워크(4주차%20-%20지능형%20IoT를%20위한%20무선%20통신%20기술).pdf) | - | • 근거리 무선 통신: Bluetooth, BLE, Zigbee, Wi-Fi<br>• 저전력 광역 통신망(LPWAN): LoRaWAN, Sigfox, NB-IoT<br>• 산업용 무선 IoT 프로토콜 비교 및 토폴로지 분석 |
| **5주차** | [`지능형 IoT 네트워크(5주차 - 지능형 IoT 데이터 수집, MQTT).pdf`](./지능형%20IoT%20네트워크(5주차%20-%20지능형%20IoT%20데이터%20수집,%20MQTT).pdf) | [`5주_과제/`](./5주_과제/) | • 산업용 경량 메시징 프로토콜 MQTT (Publish/Subscribe 구조)<br>• Topic 설계, QoS 레벨(0, 1, 2), Retain 및 LWT(Last Will & Testament)<br>• **[실무 과제]** MQTT 기반 실시간 설비 센서 이상 탐지 및 경보 서비스 구축 |
| **6주차** | [`지능형 IoT 네트워크(6주차 - OPC UA 개요).pdf`](./지능형%20IoT%20네트워크(6주차%20-%20OPC%20UA%20개요).pdf) | [`6주_과제/`](./6주_과제/) | • 산업 자동화 표준 프로토콜 OPC UA (Open Platform Communications Unified Architecture)<br>• 주소 공간(Address Space), 정보 모델(Information Model), 보안 아키텍처<br>• **[실습 과제]** OPC UA 클라이언트/서버 노드 탐색 및 데이터 교환 실습 |

---

## 🔬 3주차 핵심 연구 과제: 트래픽 분류 모델 성능 향상 (`3주_과제/`)

### 1. 연구 배경 및 문제 정의
* **데이터셋**: ISCXVPN2016 벤치마크 데이터셋 (총 2,773개 통신 플로우 샘플)
* **분류 대상 (5개 멀티클래스)**: `Audio`, `Chat`, `Email`, `File Transfer`, `Video`
* **기존 실습 베이스라인의 한계**:
  * 강의 실습 기본 5개 피처(`packet_count`, `total_bytes`, `avg_pkt_size`, `std_pkt_size`, `duration`) 기반 Baseline MLP는 **정확도 58.53%**, **Macro F1 0.4677**에 그쳐, 머신러닝 기준 모델인 Random Forest(**정확도 76.44%**, **Macro F1 0.6970**) 대비 성능 열세가 심각했음.
  * 특히 소수 클래스인 Video 클래스에서 **F1-Score 0.00(검출 실패)**을 기록하여 심각한 클래스 불균형 매몰 현상이 발생함.
* **연구 목표**: 머신러닝 기준 모델(Random Forest, 76.44%)을 통계적으로 유의미하게 상회하는 전주기 딥러닝 파이프라인(TDF-Net) 구축 및 검증.

---

### 2. 핵심 연구 방법론: TDF-Net (Tree-Deep Fusion Network)

```
[입력 데이터: ISCXVPN2016 2,773 플로우]
       │
       ├── 1. 네트워크 물리 도메인 피처 공학 (5종 파생: Throughput, Packet Rate, Bytes/Pkt, CV, Duration/Byte)
       ├── 2. 멱법칙 비선형 왜도 완화 (Log1p 10종 + Sqrt 10종) ───> [총 30개 도메인 연속형 피처]
       │                                                                  │
       └── 3. 계층적 트리 로짓 융합 (5-Fold Stratified OOF RF+ExtraTrees) ─> [10차원 불연속 결정 로짓]
                                                                          │
                                  ┌───────────────────────────────────────┘
                                  ▼
                     [40차원 결합 입력 공간 (X_tdf)]
                                  │
                                  ▼
                   ┌───────────────────────────────┐
                   │ Linear(40->256) + BN + Mish   │
                   └──────────────┬────────────────┘
                                  ▼
                   ┌───────────────────────────────┐
                   │  Residual Block 1 (Dim=256)   │  (Linear + BN + Mish + Dropout)
                   └──────────────┬────────────────┘
                                  ▼
                   ┌───────────────────────────────┐
                   │  Residual Block 2 (Dim=256)   │  (Linear + BN + Mish + Dropout)
                   └──────────────┬────────────────┘
                                  ▼
                   ┌───────────────────────────────┐
                   │ Classifier Head (128 -> 5)    │
                   └──────────────┬────────────────┘
                                  ▼
                  [CrossEntropy(Class Weights + Smooth)]
                                  │
                                  ▼
                   5-Seed 앙상블 Soft-Voting (Seeds: 42, 100, 2024, 777, 999)
                                  │
                                  ▼
                     ★ 최종 Test Accuracy: 78.61%
                     ★ 최종 Macro F1-Score: 0.7402 (RF 완벽 상회 달성)
```

---

### 3. 정량적 실험 및 성능 비교 검증

| 모델 구분 | 입력 피처 차원 | 파라미터 수 | Test Accuracy | Macro F1 | 비고 |
| :--- | :---: | :---: | :---: | :---: | :--- |
| **1. Baseline MLP** | 5 | 약 1.0만 | 58.53% | 0.4677 | 강의 실습 베이스라인 (Video F1: 0.00) |
| **2. Random Forest** | 5 | 100 Trees | 76.44% | 0.6970 | **과제 기준 벤치마크 모델** |
| **3. Tabular ResNet** | 30 | 약 35만 | 69.71% | 0.6057 | 도메인 피처 엔지니어링 + 잔차 구조 도입 |
| **4. TDF-Net 단일 모델 (시드 777)** | 40 | 약 28만 | 79.09% | 0.7420 | 단일 신경망으로 RF 전 지표 상회 달성 |
| **5. Final TDF-Net 앙상블** | **40** | **5x 앙상블** | **78.61%** | **0.7402** | **최종 제안 모델 (RF 대비 Acc +2.16%p, F1 +0.0432)** |

<p align="center">
  <img src="./3주_과제/tdf_net_confusion_matrices.png" width="95%" alt="Confusion Matrices Comparison"/>
  <br>
  <em>[그림] Baseline MLP(58.5%), Random Forest(76.4%), 제안 모델 TDF-Net Ensemble(78.6%)의 혼동 행렬(Confusion Matrix) 비교</em>
</p>

---

### 4. 과제 주요 산출물 파일 가이드 (`3주_과제/`)

* **결과보고서**:
  * [`결과보고서.pptx`](./3주_과제/결과보고서.pptx): 모던 UI 규격의 7장 핵심 요약 발표 자료.
* **실행 코드**:
  * [`iscx_vpn_multiclass.ipynb`](./3주_과제/iscx_vpn_multiclass.ipynb): 전체 파이프라인의 코드 및 주피터 커널 실행 결과 셀(Output)이 완비된 메인 노트북.
  * [`iscx_vpn_multiclass.py`](./3주_과제/iscx_vpn_multiclass.py): 독립 구동 무결성 검증 완료 CLI 파이프라인 스크립트.
  * [`code/output_multiple.csv`](./3주_과제/code/output_multiple.csv): ISCXVPN2016 2,773개 플로우 통계 데이터셋.
* **최종 제출용 패키징**:
  * [`트래픽 분류 모델 성능 향상_학번_이름.zip`](./3주_과제/트래픽%20분류%20모델%20성능%20향상_학번_이름.zip): eCampus 과제 제출 규격을 완벽 준수한 최종 압축 아카이브.

---

## 📡 5주차 과제 상세 안내: MQTT 기반 실시간 설비 이상 탐지 (`5주_과제/`)

스마트 공장 내 회전기계(베어링, 모터) 센서 데이터를 실시간 스트리밍하고, 이상 발생 시 실시간 경보를 전파하는 전주기 IoT 메시징 파이프라인 실습 및 과제입니다.

### 1. 주요 구현 모듈 (`mqtt_alarm_assignment/`)
* [`sensor_simulator.py`](./5주_과제/mqtt_alarm_assignment/sensor_simulator.py): 공장 내 다중 센서(진동, 온도, 압력 등) 정상/이상 시계열 데이터 시뮬레이터 및 MQTT 토픽 발행 (`factory/machine/sensor`)
* [`alarm_service.py`](./5주_과제/mqtt_alarm_assignment/alarm_service.py): 센서 토픽 실시간 구독, 이상치 탐지 알고리즘 적용 및 임계치 초과 시 경보 이벤트 토픽(`factory/alerts/#`) 발행 서비스
* [`anomaly_model.py`](./5주_과제/mqtt_alarm_assignment/anomaly_model.py): Z-Score 및 이동평균(Rolling Window) 기반 이상 탐지 모델
* [`watch_alarms.py`](./5주_과제/mqtt_alarm_assignment/watch_alarms.py): 운영자 관제용 실시간 알람 수신 및 콘솔 모니터링 툴
* [`check_alarms.py`](./5주_과제/mqtt_alarm_assignment/check_alarms.py): Ground Truth 대비 실시간 경보 검출 성능(정밀도, 재현율, 지연시간) 자동 채점 스크립트

### 2. MQTT 기초 실습 예제 (`실습자료/mqtt_lab/`)
* [`pub_step1_basic.py`](./5주_과제/실습자료/mqtt_lab/pub_step1_basic.py): 기본 메시지 발행 (Single Topic)
* [`pub_step2_wildcard.py`](./5주_과제/실습자료/mqtt_lab/pub_step2_wildcard.py): 와일드카드(`+`, `#`) 토픽 계층 구조 발행
* [`pub_step3_retained.py`](./5주_과제/실습자료/mqtt_lab/pub_step3_retained.py): Retained 플래그를 활용한 최종 상태 보존
* [`pub_step4_lwt.py`](./5주_과제/실습자료/mqtt_lab/pub_step4_lwt.py): LWT(Last Will and Testament) 비정상 연결 종료 유언 메시지
* [`sub_console.py`](./5주_과제/실습자료/mqtt_lab/sub_console.py): 다중 토픽 동시 수신 콘솔

### 3. 과제 보고서
* [`과제_결과보고서_2026254019_진찬언.pptx`](./5주_과제/과제_결과보고서_2026254019_진찬언.pptx) / [`.html`](./5주_과제/과제_결과보고서_2026254019_진찬언.html): 시스템 아키텍처 및 검증 결과 보고서
* [`mqtt_alarm_assignment_2026254019_진찬언.zip`](./5주_과제/mqtt_alarm_assignment_2026254019_진찬언.zip): 최종 제출 패키지

---

## 🏭 6주차 과제 안내: OPC UA 개요 및 정보 모델 실습 (`6주_과제/`)
* **강의 자료**: [`지능형 IoT 네트워크(6주차 - OPC UA 개요).pdf`](./지능형%20IoT%20네트워크(6주차%20-%20OPC%20UA%20개요).pdf)
* **실습 패키지**: [`6주_과제/6주차 opc-ua 실습.zip`](./6주_과제/6주차%20opc-ua%20실습.zip)
* **핵심 내용**: 산업용 상호운용성 표준 OPC UA 서버/클라이언트 환경 구축, NodeId 및 Reference 기반 객체 지향 정보 모델 브라우징, 센서 태그 읽기/쓰기 실습

---

*최종 업데이트: 2026-10-14*
