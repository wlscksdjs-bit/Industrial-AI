# 🎓 충북대학교 일반대학원 산업인공지능학과 (2026-1)
## Industrial AI Graduate Curriculum Archive

<p align="center">
  <img src="https://img.shields.io/badge/Graduate%20School-CBNU-blue?style=for-the-badge&logo=academia" alt="Graduate School"/>
  <img src="https://img.shields.io/badge/Department-Industrial%20AI-orange?style=for-the-badge" alt="Industrial AI"/>
  <img src="https://img.shields.io/badge/Semester-2026--1%20(1st%20Year)-green?style=for-the-badge" alt="2026-1"/>
  <img src="https://img.shields.io/badge/Workspace-Archived-red?style=for-the-badge&logo=git" alt="Workspace"/>
</p>

본 저장소는 **충북대학교 일반대학원 산업인공지능학과** 1학년 1학기(2026학년도 1학기) 전공 교과정의 강의자료, 매주 진행된 실습 코드, 과제 리포트 및 기말 텀프로젝트 산출물을 체계적으로 정리하고 아카이빙하는 공간입니다. 

제조 공정 지능화, 자율주행이동체 SW 엔지니어링, 그리고 인공지능 기반 분석론을 결합하여 산업 현장의 실무 도메인 문제를 해결하기 위한 연구 역량 축적을 목적으로 합니다.

---

## 📚 교과목 구성 및 로드맵

저장소는 학기별 총 3개의 핵심 전공심화 과목 및 이에 따른 전용 텀프로젝트 폴더로 분할하여 관리되고 있습니다. 각 폴더별 상세 내역은 폴더 내 개별 `README.md` 문서에서 확인하실 수 있습니다.

```
📁 d:/Industrial-AI (Root)
├── 📁 2026_1_머신러닝                      # 머신러닝 이론 및 알고리즘 구현 실습
├── 📁 2026_1_머신러닝_텀프로젝트             # 머신러닝 실무 텀프로젝트 및 응용 보고서/코드 (NEW)
├── 📁 2026_1_자율주행이동체 실제              # 미래 자동차 SW 설계, 전장 네트워크 및 EV 제어
├── 📁 2026_1_제조 데이터 분석과 최적화         # 스마트 제조 모달리티 AI 및 공정 최적화 스케줄링
├── 📁 2026_1_제조 데이터 분석과 최적화_텀프로젝트  # BiLSTM + XAI 상태 기반 예지보전 텀프로젝트 (NEW)
└── 📄 학생상담양식 (신입생).hwp              # 일반 대학원 신입생 학사 상담 기록 양식
```

### 1. 🤖 [머신러닝 (Machine Learning)](./2026_1_머신러닝/)
* **강의 요약**: 전통적인 선형 모델부터 앙상블 기법, 차원 축소 및 비지도 학습 알고리즘의 수학적 원리를 이해하고 실제 산업 도메인 데이터셋에 적용하여 분류 및 예측 모델을 구축합니다.
* **주요 학습 키워드**: `Logistic Regression`, `Lasso/Ridge regularization`, `KNN`, `SVM`, `Decision Tree`, `Ensemble`, `Random Forest`, `PCA`, `Clustering`, `Anomaly Detection`.
* **학습 성과**: 스마트팩토리 품질 예측, 광양제철소 전력 사용량 예측, 반도체 AMC 예지보전 텀프로젝트 진행 및 알고리즘별 성능 평가 분석. ([머신러닝 텀프로젝트 폴더](./2026_1_머신러닝_텀프로젝트/))

### 2. 🚗 [자율주행이동체 실제 (Autonomous Vehicle in Practice)](./2026_1_자율주행이동체%20실제/)
* **강의 요약**: 기석철 교수님 지도 하에 차량용 임베디드 소프트웨어를 개발할 때 필요한 표준 아키텍처(AUTOSAR)와 기능 안전(Functional Safety), ADAS 시스템 및 V2X 통신 기반 커넥티드 카 구조를 체계적으로 학습합니다.
* **주요 학습 키워드**: `Chassis Systems`, `ADAS`, `Vehicle Development Process`, `Functional Safety (ISO 26262)`, `AUTOSAR`, `AIVD`, `In-Vehicle Networks`, `Connected Vehicle (V2X/V2N)`, `EV Powertrain (BMS/Regenerative Braking)`.
* **학습 성과**: 자율주행 엣지케이스 대응을 위한 원격운영 및 V2N 시장 동향 분석 레포트 작성.

### 3. ⚙️ [제조 데이터 분석과 최적화 (Manufacturing Data Analysis & Optimization)](./2026_1_제조%20데이터%20분석과%20최적화/)
* **강의 요약**: 김한진 교수님 지도 하에 스마트제조 공정에서 수집되는 다중 모달리티 데이터(수치, 이미지, 소리)를 분석하기 위한 전처리 및 AI 아키텍처를 실습하고, 다양한 최적화 알고리즘(LP, IP, DP, 유전 알고리즘) 및 SimPy 시뮬레이션을 활용한 공정 스케줄링(JSSP) 최적화 대안을 설계합니다.
* **주요 학습 키워드**: `OPC-UA Standard`, `Convolutional Autoencoder`, `MIMII Sound Pipeline`, `Linear Programming (LP/IP)`, `Dynamic Programming (DP)`, `Genetic Algorithm (GA)`, `Discrete Event Simulation (SimPy)`, `Job Shop Scheduling (JSSP)`.
* **학습 성과**: 양방향 LSTM(BiLSTM) 및 설명 가능한 AI(XAI) 기술 기반의 반도체 공정 설비 상태 기반 정비(CBM) 기말 텀프로젝트 소스코드 및 논문초안/최종보고서 도출. ([제조 데이터 분석 텀프로젝트 폴더](./2026_1_제조%20데이터%20분석과%20최적화_텀프로젝트/))

---

## 🏆 주요 학기 프로젝트 및 산출물 (Key Outputs)

| 과목명 | 프로젝트 주제 | 핵심 산출물 및 소스코드 |
| :--- | :--- | :--- |
| **제조 데이터 분석과 최적화** | **CBM using BiLSTM & XAI** (설비 예지보전) | 💻 [CBM 분석 파이썬 소스코드](./2026_1_제조%20데이터%20분석과%20최적화_텀프로젝트/2026254019_진찬언/텀프로젝트.py)<br>📕 [최종 완성 보고서 (DOCX)](./2026_1_제조%20데이터%20분석과%20최적화_텀프로젝트/CBM_BiLSTM_XAI_최종완성본.docx)<br>📝 [학술 논문 초안 (DOCX)](./2026_1_제조%20데이터%20분석과%20최적화_텀프로젝트/CBM_BiLSTM_XAI_논문초안.docx)<br>📊 [최종 발표 자료 (PPTX)](./2026_1_제조%20데이터%20분석과%20최적화_텀프로젝트/2026254019_진찬언/CBM_BiLSTM_XAI_진찬언(2026254019).pptx) |
| **자율주행이동체 실제** | **자율주행 원격운영 및 V2N 시장 분석** | 📑 [원격운영 및 V2N 시장 분석 레포트 (DOCX)](./2026_1_자율주행이동체%20실제/과제/자율주행%20엣지케이스%20대응을%20위한%20원격운영%20및%20V2N%20시장%20분석_260512(2026254019%20진찬언).docx) |
| **머신러닝** | **공업 도메인 품질 및 전력 예측** | 💻 [충북대 산업인공지능학과 텀프로젝트 코드](./2026_1_머신러닝_텀프로젝트/충북대학교%20산업인공지능학과%20텀프로젝트.py) |

---

## ⚙️ 저장소 정책 및 무시 설정 (Git Policies)

GitHub 저장소의 원활한 운영 및 용량 최적화를 위해 다음과 같은 예외 규칙을 도입하여 관리하고 있습니다.
* **오디오/데이터셋 차단**: 대용량 오디오 샘플(`*.wav`, `*.mp3`) 및 압축 파일(`*.zip`, `*.egg`), 데이터셋 원본(`*.csv`) 파일은 깃허브 전송 영역에서 제외됩니다.
* **100MB 단일 파일 초과 차단**: GitHub 업로드 한도를 상회하는 446MB 용량의 대형 슬라이드 `9. Connected Vehicle.pptx` 파일은 명시적 차단 패턴이 설정되어 로컬에만 보관됩니다.
* **자세한 내역**: [`.gitignore`](./.gitignore) 파일 참조.

---

### 🎓 Graduate Contact
* **소속**: 충북대학교 일반대학원 산업인공지능학과
* **연구원**: **진찬언** (석사과정 / 학번: 2026254019)
