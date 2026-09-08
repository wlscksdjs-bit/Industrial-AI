# 🏭 제조 AI 실제 (Manufacturing AI in Practice)

본 폴더는 충북대학교 일반대학원 산업인공지능학과 1학년 2학기 **제조 AI 실제** 강의의 강의 자료, 실습 코드 및 과제 산출물을 체계적으로 관리하는 공간입니다.

---

## 📌 교과 개요 및 목표
* **교과목명**: 제조 AI 실제 (Manufacturing AI in Practice)
* **주요 내용**: 스마트 제조 현장에서 수집되는 다양한 센서 및 신호 데이터(진동, 음향, 온도, 압력 등)를 바탕으로 산업 인공지능 기법(신호처리, 특징 공학, 패턴인식, 결함 진단 및 예지보전)을 적용하는 실무 역량을 함양합니다.
* **주요 도메인 데이터**: CWRU (Case Western Reserve University) 모터 베어링 진동 데이터셋 등

---

## 📂 주차별 강의 자료 및 실습 과제 일람

| 주차 / 주제 | 강의 자료 | 실습 및 과제 파일 | 주요 학습 내용 및 키워드 |
| :--- | :--- | :--- | :--- |
| **1주차** | [`제조AI실제(1주차).pdf`](./제조AI실제(1주차).pdf) | - | • 제조 인공지능 개요 및 스마트팩토리 적용 사례<br>• 산업 데이터 특성 및 강의 오리엔테이션 |
| **2주차** | [`제조AI실제(2주차).pdf`](./제조AI실제(2주차).pdf) | [`2주_과제/`](./2주_과제/) | • 패턴인식(Pattern Recognition)과 특징(Feature)의 정의<br>• 좋은 특징(Good Feature)과 클래스 분리성(Separability)<br>• 일반화(Generalization)와 제약 조건(Constraints) |

---

## 🔬 2주차 과제 상세 안내 (`2주_과제/`)

CWRU 모터 베어링 진동 실데이터(`Normal` 정상 vs `Inner Race Fault` 내륜 결함)를 활용한 2종의 주피터 노트북 실습 및 분석 과제입니다.

### 1. [`manufacturing_ai_lab2_1.ipynb`](./2주_과제/manufacturing_ai_lab2_1.ipynb)
* **주제**: 좋은 특징(Good Feature)의 정의와 클래스 분리성(Separability) 체감
* **핵심 내용**:
  * CWRU 베어링 진동 가속도 신호 로드 및 시간 영역 시각화
  * **나쁜 특징(Bad Feature)** 추출 시의 문제점: 단순 평균값 등 클래스 간 중첩 현상 관찰
  * **좋은 특징(Good Feature)** 추출: 실효값(RMS), 첨도(Kurtosis), 피크값(Peak), 파고율(Crest Factor) 등을 활용한 클래스 간 분리도 극대화
  * **Fisher Separability** 지표 정량 계산 및 로지스틱 회귀(Logistic Regression) 분류 모델 성능 비교

### 2. [`manufacturing_ai_lab2_2.ipynb`](./2주_과제/manufacturing_ai_lab2_2.ipynb)
* **주제**: 제약 조건(Constraints)에 따른 일반화(Generalization)와 문제 난이도 비교
* **핵심 내용**:
  * **데이터/환경 제약**: 노이즈 제거 및 데이터 정형화 전후의 특징 분리도 비교
  * **모델 제약**: 고차 다항식 과적합(Overfitting) 모델 vs 정규화(L2 Penalty) 단순화 모델 비교
  * **작업(Task) 제약**: 복잡한 연속치 회귀(Regression) 문제 vs 이진 분류(Classification) 문제의 난이도 및 일반화 성능 비교

### 3. 데이터셋 (`.mat`)
* [`cwru_normal.mat`](./2주_과제/cwru_normal.mat): 정상 상태 모터 베어링 구동 진동 신호
* [`cwru_fault.mat`](./2주_과제/cwru_fault.mat): 내륜 결함(Inner Race Fault) 상태 모터 베어링 구동 진동 신호
