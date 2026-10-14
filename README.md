# 🎓 충북대학교 일반대학원 산업인공지능학과
## Industrial AI Graduate Curriculum & Research Archive

<p align="center">
  <img src="https://img.shields.io/badge/Graduate%20School-CBNU-blue?style=for-the-badge&logo=academia" alt="Graduate School"/>
  <img src="https://img.shields.io/badge/Department-Industrial%20AI-orange?style=for-the-badge" alt="Industrial AI"/>
  <img src="https://img.shields.io/badge/Degree-Master's%20Course-purple?style=for-the-badge" alt="Master's Course"/>
  <img src="https://img.shields.io/badge/Semester-1st%20%26%202nd%20Semester-green?style=for-the-badge" alt="Semesters"/>
  <img src="https://img.shields.io/badge/Status-Active%20Research-red?style=for-the-badge&logo=git" alt="Status"/>
</p>

본 저장소는 **충북대학교 일반대학원 산업인공지능학과**(석사과정)의 전공 교과목 강의 자료, 매주 진행된 실습 코드, 연구 과제 리포트, 기말 텀프로젝트 산출물 및 산학 프로젝트 자료를 체계적으로 정리하고 아카이빙하는 통합 공간입니다.

스마트 제조 현장의 도메인 데이터(진동, 시계열, 이미지, 음향) 분석과 결함 진단/예지보전(PHM/CBM), 자율주행 모빌리티 SW 공학, 최적화 이론, 지능형 IoT 네트워크 인프라 기술을 융합하여 산업 현장의 실질적인 문제를 해결하는 연구 역량을 축적해 나가고 있습니다.

---

## 📂 전체 디렉터리 아키텍처

저장소는 학년 및 학기별 단위 폴더로 구조화되어 있으며, 각 과목 및 프로젝트별 하위 디렉터리 내에 개별 `README.md`와 실행 코드, 강의 자료가 보관되어 있습니다.

```
📁 Industrial-AI (Root)
│
├── 📁 1학년 1학기                                      # 2026학년도 1학기 아카이브
│   ├── 📁 2026_1_머신러닝                             # 머신러닝 알고리즘 수식 이론 및 구현 실습
│   ├── 📁 2026_1_머신러닝_텀프로젝트                    # 스마트팩토리/제철소 품질·전력 예측 텀프로젝트
│   ├── 📁 2026_1_자율주행이동체 실제                     # 차량 임베디드 SW, AUTOSAR, ISO 26262, V2X
│   ├── 📁 2026_1_제조 데이터 분석과 최적화                # 스마트제조 모달리티 AI 및 공정 최적화 스케줄링
│   ├── 📁 2026_1_제조 데이터 분석과 최적화_텀프로젝트         # BiLSTM + XAI 기반 설비 예지보전(CBM) 논문·보고서
│   ├── 📄 학생상담양식 (신입생).hwp                     # 신입생 학사 상담 기록 양식
│   └── 📄 README.md                                  # 1학기 안내 및 인덱스
│
├── 📁 1학년 2학기                                      # 2026학년도 2학기 아카이브
│   ├── 📁 제조 AI 실제                                # CWRU 베어링 진동 신호처리, 특징공학, 생성형 AI, CNN/전이학습
│   │   ├── 📁 2주_과제                               # 2주차: CWRU 베어링 좋은 특징 정의 & Fisher Separability
│   │   ├── 📁 3주_과제                               # 3주차: 선형회귀(SGD), 로지스틱 회귀, MNIST MLP 과적합 분석
│   │   ├── 📁 4주_과제                               # 4주차: 활성화/손실함수 및 4대 도전과제 극복(ResNet/규제/Dropout)
│   │   ├── 📁 5주_과제                               # 5주차: 생성 모델 4종(AE/VAE/GAN/DDPM) 심층 실습
│   │   ├── 📁 7주_과제                               # 7주차: CNN & 전이학습(LeNet-5/VGG16/Inception/ResNet)
│   │   │   ├── 📄 Lab7_1.cnn_mnist_convolution_pooling.ipynb
│   │   │   ├── 📄 Lab7_2.classic_cnn.ipynb           # LeNet-5(98.17%), VGG16 가중치 추론
│   │   │   └── 📄 Lab7_3.inception_resnet_finetuning_transfer.ipynb # Inception Fine-tuning, ResNet CIFAR-10 전이학습
│   │   ├── 📕 제조AI실제(1~5주차).pdf                 # 1~5주차 강의 자료 PDF
│   │   ├── 📕 제조AI실제_6주차_글로벌제조트렌드.pdf      # 6주차 강의 자료: 글로벌 제조 트렌드 & DX
│   │   ├── 📕 제조AI실제(7주차).pdf                   # 7주차 강의 자료: 합성곱 신경망 및 전이학습
│   │   └── 📄 README.md                              # 제조 AI 실제 교과 안내
│   │
│   ├── 📁 지능형 IoT 네트워크                           # 산업용 IoT 프로토콜, 무선 센서망, 엣지 컴퓨팅
│   │   ├── 📁 3주_과제                               # [연구 과제] ISCXVPN2016 트래픽 다중 분류 TDF-Net
│   │   │   ├── 📊 결과보고서.pptx                     # 모던 UI 규격의 7장 핵심 연구 결과보고서
│   │   │   ├── 💻 iscx_vpn_multiclass.ipynb          # 실행 셀 완비 메인 딥러닝(TDF-Net) 분석 노트북
│   │   │   └── 🐍 iscx_vpn_multiclass.py             # 독립 실행 검증 완료 CLI 파이프라인
│   │   ├── 📁 5주_과제                               # [실무 과제] MQTT 기반 실시간 설비 이상 탐지 시스템
│   │   │   ├── 📁 mqtt_alarm_assignment/             # 센서 시뮬레이터, 이상치 탐지 서비스, 관제 모니터
│   │   │   ├── 📁 실습자료/mqtt_lab/                  # MQTT 기초 예제 4단계 및 수신 콘솔
│   │   │   └── 📊 과제_결과보고서_2026254019_진찬언.pptx # 5주차 결과보고서
│   │   ├── 📁 6주_과제                               # [실습 과제] OPC UA 정보 모델 실습
│   │   ├── 📕 1~6주차 강의 PDF                        # 1~6주차 강의 자료 완비
│   │   └── 📄 README.md                              # 지능형 IoT 네트워크 교과 안내
│   │
│   ├── 📁 어프렌티스 프로젝트                           # 산학 협력 및 현장 실무 기반 캡스톤 프로젝트
│   │   ├── 📕 2주차, 5주차 강의 자료 PDF               # ML 5단계 절차, 스케일링, 시계열(RNN/LSTM/GRU)
│   │   ├── 📁 1차 프로젝트: 설비 고장 예측 머신러닝 5단계 실증 # AI4I 2020 1만 건 기반 고장 재현율 86.8%, AUC 0.986
│   │   │   ├── 📊 발표자료 PPTX, 구두대본 DOCX/PDF, 기획서 MD, 실험 스크립트 py
│   │   └── 📁 2차 PJT: ETTh1 전력 변압기 유온 시계열 예측   # 1시간 후 유온 예측 다변량 딥러닝 프로젝트
│   │       ├── 🌐 프로젝트2_진찬언_ETTh1_v3.html      # 16:9 인터랙티브 프레젠테이션 슬라이드 덱
│   │       ├── 📑 어프렌티스_5주차_과제_발표대본_진찬언.docx # 5분 발표 구두 대본
│   │       ├── 💻 run_project2_upgrade_experiment.py # 전과정 재현 파이썬 스크립트
│   │       ├── 📊 experiment_results_v2.json         # 정량 평가 지표 및 차트 일체
│   │       └── 📊 ETTh1.csv                          # 전력 변압기 센서 원천 데이터셋
│   │
│   └── 📄 README.md                                  # 2학기 종합 안내 및 인덱스
│
├── ⚙️ .gitignore                                      # 대용량 바이너리 및 불필요 파일 제외 설정
└── 📄 README.md                                        # 통합 메인 인덱스
```

---

## 📘 1학년 1학기 (2026-1) 전공 심화 내역

> 상세 내역은 [**1학년 1학기 폴더**](./1학년%201학기/) 및 각 하위 폴더의 README에서 확인하실 수 있습니다.

* **머신러닝 (Machine Learning)**: 지도/비지도 머신러닝 수학적 원리, 최적화 이론 및 스마트팩토리 품질 예측 텀프로젝트.
* **자율주행이동체 실제 (Autonomous Mobile Systems)**: ISO 26262 기능안전성, AUTOSAR Adaptive 플랫폼 및 V2X 차량 통신.
* **제조 데이터 분석과 최적화 (Manufacturing Data Analytics & Optimization)**: 다변량 센서 신호처리, 메타휴리스틱 공정 스케줄링 및 BiLSTM+XAI CBM 텀프로젝트.

---

## 📗 1학년 2학기 (2026-2) 전공 심화 내역

> 상세 내역은 [**1학년 2학기 폴더**](./1학년%202학기/) 및 각 하위 폴더의 README에서 확인하실 수 있습니다.

### 1. 🏭 [제조 AI 실제 (Manufacturing AI in Practice)](./1학년%202학기/제조%20AI%20실제/)
* **강의 요약**: 제조 현장의 기계 설비 상태 모니터링, 신호 분석(Signal Processing), 특징 공학(Feature Engineering), 결함 탐지 및 기계학습/딥러닝 모델 적용 실무와 비지도 이상치 탐지/데이터 증강을 위한 생성 모델(Generative Models), 합성곱 신경망(CNN) 및 전이학습(Transfer Learning)을 체계적으로 다룹니다.
* **주요 강의 자료**: 1~7주차 강의 자료 PDF (개요, 패턴인식, 신경망 기초, 도전과제 극복, 생성 모델, 글로벌 트렌드, CNN/전이학습)
* **실습 과제**:
  * **2주_과제**: CWRU 모터 베어링 진동 좋은 특징(RMS, Kurtosis 등) 추출 및 Fisher Separability 비교, 일반화 제약 조건 실습
  * **3주_과제**: 선형회귀(SGD), 로지스틱 회귀(결정 경계 시각화), MNIST 다층 퍼셉트론(MLP) 과적합 징후 분석
  * **4주_과제**: 회귀/분류 활성화 및 손실함수 비교, 기울기 소실 및 클래스 불균형 극복(ResNet Skip Connection, L1/L2, Dropout)
  * **5주_과제**: Autoencoder 비지도 결함 진단, VAE 잠재 공간 매니폴드 생성, GAN 적대적 숫자 합성, Diffusion Model(DDPM) Denoising 실습
  * **7주_과제**: Convolution & Pooling 연산 시각화, LeNet-5 직접 구현 및 학습(**정확도 98.17%**), VGG16 사전학습 가중치 추론, InceptionV3 Fine-tuning 및 ResNet50 기반 CIFAR-10 전이학습

### 2. 🌐 [지능형 IoT 네트워크 (Intelligent IoT Network)](./1학년%202학기/지능형%20IoT%20네트워크/)
* **강의 요약**: 산업용 사물인터넷(IIoT), 산업 통신 프로토콜, 무선 센서 네트워크, OSI 7계층 분석, 산업용 메시징 프로토콜(MQTT, OPC UA) 및 암호화 트래픽 다중 분류 딥러닝 모델링.
* **주요 강의 자료**: 1~6주차 강의 자료 PDF (오리엔테이션, 지능형 IoT 개요, OSI 7계층, 무선 통신 기술, MQTT 데이터 수집, OPC UA 개요)
* **연구 과제 ([3주_과제](./1학년%202학기/지능형%20IoT%20네트워크/3주_과제/))**:
  * **ISCXVPN2016 암호화 트래픽 분류 TDF-Net 아키텍처 구현**:
    * 30개 네트워크 물리 도메인 피처 공학 + 10차원 계층적 트리 로짓 결합(40차원) + ResBlock + 5-Seed 앙상블.
    * 머신러닝 기준 모델(Random Forest 76.44%)을 뛰어넘는 **정확도 78.61% (+2.16%p 상회)** 및 **Macro F1 0.7402 (+0.0432 상회)** 달성.
* **실무 과제 ([5주_과제](./1학년%202학기/지능형%20IoT%20네트워크/5주_과제/))**:
  * **MQTT 기반 실시간 설비 센서 이상 탐지 및 경보 서비스**:
    * 센서 시뮬레이터(`sensor_simulator.py`), 실시간 이상치 탐지 서비스(`alarm_service.py`), 관제 모니터(`watch_alarms.py`), 성능 검증기(`check_alarms.py`).
* **실습 과제 ([6주_과제](./1학년%202학기/지능형%20IoT%20네트워크/6주_과제/))**:
  * **OPC UA 정보 모델 실습**: 산업용 상호운용성 표준 OPC UA 서버/클라이언트 연동 및 Address Space 노드 탐색.

### 3. 🚀 [어프렌티스 프로젝트 (Apprentice Project)](./1학년%202학기/어프렌티스%20프로젝트/)
* **강의 요약**: 산학 협력 및 현장 실무 데이터셋을 기반으로 머신러닝 전주기 5대 핵심 절차 실증 및 시계열(Time-Series) 딥러닝(RNN, LSTM, GRU) 기반 예측 프로젝트.
* **주요 강의 자료**: 2주차, 5주차 강의 자료 PDF (데이터 분할, 스케일링, 논문의 종류, 시계열 딥러닝)
* **실증 프로젝트 1 ([프로젝트 1](./1학년%202학기/어프렌티스%20프로젝트/))**:
  * **AI4I 2020 공작기계 가공 설비 고장 예측 머신러닝 5단계 실증**:
    * 10,000건 센서 로그에서 고장률 3.4% 극단적 불균형을 극복하기 위해 3단계 층화 분할(6:2:2) 및 RobustScaler 데이터 누수 원천 차단.
    * Random Forest 깊이 규제(10) 및 결정 임계값(0.35) 튜닝으로 **고장 재현율(Recall) 86.8% (+36.8%p 향상)**, **F1 0.868**, **ROC-AUC 0.986** 달성.
* **실증 프로젝트 2 ([2차 PJT](./1학년%202학기/어프렌티스%20프로젝트/2차%20PJT/))**:
  * **ETTh1 다변량 시계열 기반 전력 변압기 유온 1시간 후 예측**:
    * 17,420개 시간별 변압기 센서 데이터 기반 1시간 후 오일 온도(OT) 정밀 예측 시계열 회귀 모델링.
    * 시계열 분할, Lag/Rolling 특징 공학, 다중 아키텍처(Linear, Ridge, MLP, GRU, LSTM) 비교 평가.
    * 16:9 인터랙티브 슬라이드 덱(HTML v3), 5분 발표 구두 대본(DOCX/MD), 전과정 재현 파이썬 스크립트 완비.

---

#### 🏆 2학기 주요 실습 및 과제 산출물 일람

| 과목명 | 주차 / 주제 | 핵심 산출물 및 소스코드 | 주요 학습 내용 및 해결 기법 |
| :--- | :--- | :--- | :--- |
| **제조 AI 실제** | **1주차: 스마트 제조 AI 개요** | 📕 [제조AI실제(1주차).pdf](./1학년%202학기/제조%20AI%20실제/제조AI실제(1주차).pdf) | 스마트 제조 AI 개요, 산업 도메인 센서 데이터 특성 분석 |
| | **2주차: CWRU 베어링 신호 분석** | 💻 [2주_과제/](./1학년%202학기/제조%20AI%20실제/2주_과제/) ([lab2_1.ipynb](./1학년%202학기/제조%20AI%20실제/2주_과제/manufacturing_ai_lab2_1.ipynb), [lab2_2.ipynb](./1학년%202학기/제조%20AI%20실제/2주_과제/manufacturing_ai_lab2_2.ipynb)) | 시간영역 통계 특징(RMS, Kurtosis 등), Fisher Separability 계산, 모델/데이터 제약과 일반화 |
| | **3주차: 인공신경망 기초 및 최적화** | 💻 [3주_과제/](./1학년%202학기/제조%20AI%20실제/3주_과제/) ([선형회귀](./1학년%202학기/제조%20AI%20실제/3주_과제/linear_regression.ipynb), [로지스틱 회귀](./1학년%202학기/제조%20AI%20실제/3주_과제/logistic_regression.ipynb), [MNIST MLP](./1학년%202학기/제조%20AI%20실제/3주_과제/mnist_nn_classification.ipynb)) | 단일 노드 Dense Layer, SGD 최적화, 2D 결정 경계 컨투어 플롯, 과적합 분석 |
| | **4주차: 활성화/손실함수 및 4대 도전과제** | 💻 [4주_과제/](./1학년%202학기/제조%20AI%20실제/4주_과제/) ([lab4_1~lab4_4](./1학년%202학기/제조%20AI%20실제/4주_과제/)) | Sigmoid/ReLU/Tanh 비교, MSE vs MAE/BCE, 기울기 소실 체감, ResNet Skip Connection, L1/L2, Dropout |
| | **5주차: 생성 모델(AE/VAE/GAN/DDPM)** | 💻 [5주_과제/](./1학년%202학기/제조%20AI%20실제/5주_과제/) ([lab5_1~lab5_4](./1학년%202학기/제조%20AI%20실제/5주_과제/)) | 재구성 오차 기반 비지도 결함 진단, 잠재 공간 매니폴드 형성, Minimax 게임, Denoising 과정 |
| | **6주차: 글로벌 제조 트렌드** | 📕 [제조AI실제_6주차_글로벌제조트렌드.pdf](./1학년%202학기/제조%20AI%20실제/제조AI실제_6주차_글로벌제조트렌드.pdf) | 스마트 제조 DX 트렌드, 자율 제조 및 탄소 중립 최적화 방향 |
| | **7주차: CNN 및 전이학습** | 💻 [7주_과제/](./1학년%202학기/제조%20AI%20실제/7주_과제/) ([Lab7_1](./1학년%202학기/제조%20AI%20실제/7주_과제/Lab7_1.cnn_mnist_convolution_pooling.ipynb), [Lab7_2](./1학년%202학기/제조%20AI%20실제/7주_과제/Lab7_2.classic_cnn.ipynb), [Lab7_3](./1학년%202학기/제조%20AI%20실제/7주_과제/Lab7_3.inception_resnet_finetuning_transfer.ipynb)) | Convolution/Pooling 시각화, LeNet-5 직접 구현(정확도 98.17%), VGG16 추론, Inception Fine-tuning, ResNet CIFAR-10 전이학습 |
| **지능형 IoT 네트워크** | **1~6주차 강의자료 완비** | 📕 [1~6주차 강의 PDF](./1학년%202학기/지능형%20IoT%20네트워크/) | 오리엔테이션, 지능형 IoT 개요, OSI 7계층, WSN/LPWAN 무선 통신, MQTT 수집, OPC UA 개요 |
| | **3주차: ISCXVPN 트래픽 분류 TDF-Net** | 📊 [3주_과제/](./1학년%202학기/지능형%20IoT%20네트워크/3주_과제/) | 30개 피처 공학 + 10차원 트리 로짓 결합 + ResBlock + 앙상블 딥러닝 TDF-Net (정확도 78.61%, Macro F1 0.7402로 RF 상회) |
| | **5주차: MQTT 기반 설비 이상 탐지** | 📡 [5주_과제/](./1학년%202학기/지능형%20IoT%20네트워크/5주_과제/) | MQTT 기반 실시간 센서 데이터 스트리밍, 이상치 탐지 서비스 및 경보 발행 전주기 파이프라인 구현 |
| | **6주차: OPC UA 정보 모델 실습** | 🏭 [6주_과제/](./1학년%202학기/지능형%20IoT%20네트워크/6주_과제/) | 산업용 표준 OPC UA 서버/클라이언트 연동 및 Address Space 노드 탐색 |
| **어프렌티스 프로젝트** | **2주차, 5주차 강의자료 완비** | 📕 [2주차, 5주차 강의자료](./1학년%202학기/어프렌티스%20프로젝트/) | 머신러닝 5단계 절차, 데이터 누수 차단, 학술 논문 종류, 순환 신경망(RNN, LSTM, GRU) |
| | **프로젝트 1: 제조 설비 고장 예측** | 📊 [프로젝트 1 산출물](./1학년%202학기/어프렌티스%20프로젝트/) | AI4I 2020 1만건 센서 로그 기반 5단계 실증, 3단계 층화 분할, RobustScaler 누수 방지, RF 튜닝으로 고장 재현율 86.8%, AUC 0.986 달성 |
| | **프로젝트 2: ETTh1 변압기 유온 시계열 예측** | ⚡ [2차 PJT 산출물](./1학년%202학기/어프렌티스%20프로젝트/2차%20PJT/) | ETTh1 다변량 시계열 1시간 후 유온 예측, Lag/Rolling 특징 공학, 다중 딥러닝 모델링 및 16:9 인터랙티브 슬라이드 덱 |

---

## ⚙️ 저장소 정책 및 파일 관리 규칙 (Git Policies)

안정적이고 효율적인 깃허브 저장소 운영을 위해 다음 규칙을 적용하고 있습니다.
* **불필요/임시 파일 차단**: `.vscode/`, `.idea/`, `.bkit/`, `.castra/`, `.ipynb_checkpoints/`, 임시 파일(`~$*`), Python 바이트코드(`*.pyc`, `__pycache__/`) 자동 제외.
* **대용량 미디어/데이터셋 관리**: 무손실 압축 파일(`*.zip`, `*.egg`, `*.tar.gz`), 대용량 오디오 샘플(`*.wav`, `*.mp3`), 대용량 네트워크 패킷 캡처(`*.pcap`, `*.pcapng`)는 깃 추적에서 제외하여 최적 용량을 유지합니다.
* **100MB 단일 파일 제한 준수**: GitHub의 100MB 파일 용량 제한을 초과하는 대형 슬라이드나 원본 패킷 파일은 `.gitignore`를 통해 로컬에서만 안전하게 보관됩니다.
* **상세 규칙**: [`.gitignore`](./.gitignore) 파일 참조.

---

### 🎓 Graduate Contact
* **소속**: 충북대학교 일반대학원 산업인공지능학과 (Chungbuk National University)
* **연구원**: **진찬언** (석사과정 / Chan-Eon Jin / 학번: 2026254019)
* **이메일**: [wlscksdjs@gmail.com](mailto:wlscksdjs@gmail.com)
* **GitHub**: [@wlscksdjs-bit](https://github.com/wlscksdjs-bit)
