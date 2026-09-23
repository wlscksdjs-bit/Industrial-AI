# 🏭 제조 AI 실제 (Manufacturing AI in Practice)

본 저장소는 충북대학교 일반대학원 산업인공지능학과 **제조 AI 실제** 강의의 강의 자료(PDF), 주차별 실습 코드(Jupyter Notebook) 및 과제 산출물을 체계적으로 관리하는 공간입니다.

---

## 📌 교과 개요 및 목표
* **교과목명**: 제조 AI 실제 (Manufacturing AI in Practice)
* **주요 내용**: 스마트 제조 현장에서 수집되는 다양한 센서 및 신호 데이터(진동, 음향, 온도, 압력 등)를 바탕으로 산업 인공지능 기법(신호처리, 특징 공학, 패턴인식, 신경망 모델링, 결함 진단 및 예지보전)을 적용하는 실무 역량을 함양합니다.
* **주요 도메인 데이터**: CWRU (Case Western Reserve University) 모터 베어링 진동 데이터셋, MNIST 손글씨 데이터셋, 비선형 합성 신호 데이터셋 등

---

## 📂 주차별 강의 자료 및 실습 과제 일람

| 주차 / 주제 | 강의 자료 | 실습 및 과제 폴더 | 주요 학습 내용 및 키워드 |
| :--- | :--- | :--- | :--- |
| **1주차** | [`제조AI실제(1주차).pdf`](./제조AI실제(1주차).pdf) | - | • 제조 인공지능 개요 및 스마트팩토리 적용 사례<br>• 산업 데이터 특성 및 강의 오리엔테이션 |
| **2주차** | [`제조AI실제(2주차).pdf`](./제조AI실제(2주차).pdf) | [`2주_과제/`](./2주_과제/) | • 패턴인식(Pattern Recognition)과 특징(Feature)의 정의<br>• 좋은 특징(Good Feature)과 클래스 분리성(Separability)<br>• 일반화(Generalization)와 제약 조건(Constraints) |
| **3주차** | [`제조AI실제(3주차).pdf`](./제조AI실제(3주차).pdf) | [`3주_과제/`](./3주_과제/) | • 인공신경망(ANN) 기초 및 발전사<br>• 선형회귀(Linear Regression)와 MSE 손실 함수 경사하강법(SGD) 최적화<br>• 로지스틱 회귀(Logistic Regression)와 이진 크로스엔트로피(Log Loss)<br>• 다층 퍼셉트론(MLP) 기반 MNIST 손글씨 분류 및 과적합(Overfitting) 징후 분석 |
| **4주차** | [`제조AI실제(4주차).pdf`](./제조AI실제(4주차).pdf) | [`4주_과제/`](./4주_과제/) | • 활성화 함수(Activation Function): Sigmoid, ReLU, Tanh, Leaky ReLU 비교<br>• 손실 함수(Loss Function): MSE, MAE, Binary/Categorical Cross-Entropy<br>• 기울기 소실(Vanishing Gradient) 문제 및 ReLU를 통한 해결<br>• 과적합(Overfitting) / 과소적합(Underfitting) 진단<br>• 클래스 불균형(Class Imbalance) 문제와 평가 지표(F1, Recall)<br>• ResNet(Skip Connection), Regularization(L1/L2), Dropout, Class Weighting |

---

## 📖 1주차 강의 자료 안내
* **강의 자료**: [`제조AI실제(1주차).pdf`](./제조AI실제(1주차).pdf)
* **주요 내용**:
  * 제조 인공지능(Manufacturing AI)의 정의 및 스마트 제조/스마트팩토리 발전 단계
  * 제조 도메인 데이터 특성: 시계열 센서 데이터, 잡음(Noise), 데이터 불균형, 고차원 특성
  * 산업 AI 응용 분야: 예지보전(PdM, Predictive Maintenance), 불량 검출 및 품질 예측, 공정 최적화
  * 학기 강의 구성 및 실습 환경 안내

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

---

## 🔬 3주차 과제 상세 안내 (`3주_과제/`)

신경망의 기본 빌딩 블록(선형회귀, 로지스틱 회귀, 다층 퍼셉트론)의 수식적 원리를 이해하고 TensorFlow로 구현·실습한 3종의 주피터 노트북 과제입니다.

### 1. [`linear_regression.ipynb`](./3주_과제/linear_regression.ipynb)
* **주제**: TensorFlow를 활용한 선형회귀 및 경사하강법(SGD) 최적화
* **주요 내용**:
  * $y = 3x + 2 + \text{noise}$ 합성 데이터 생성 및 산점도 시각화
  * 단일 노드 Dense Layer 정의, MSE 손실 함수 및 SGD(lr=0.01) 컴파일
  * 200 Epoch 학습 진행 및 손실 곡선(Loss Curve) 수렴 확인
  * 학습된 가중치(기울기 $W$, 절편 $b$) 확인 및 원본 데이터 대비 회귀선 시각화
  * **생각해보기 분석**: 학습 샘플 수 축소에 따른 높은 분산(High Variance)/과적합 위험 및 노이즈 증가 시 대수의 법칙(Law of Large Numbers)에 따른 필요 데이터양 고찰

### 2. [`logistic_regression.ipynb`](./3주_과제/logistic_regression.ipynb)
* **주제**: Iris 데이터셋 기반 로지스틱 회귀 이진 분류 및 결정 경계 시각화
* **주요 내용**:
  * Iris 붓꽃 꽃받침 길이·너비(2개 특성) 추출 및 표준화(StandardScaler)
  * Setosa($y=1$) vs Others($y=0$) 이진 레이블링 및 8:2 Train/Test 분리
  * Dense(1, activation='sigmoid') 모델 정의 및 Binary Crossentropy 손실 함수 설정
  * 100 Epoch 학습 진행, Train/Val 손실 곡선 및 정확도 곡선 도출, 테스트셋 정확도 100% 달성
  * 2D 메쉬그리드 상의 로지스틱 결정 경계(Decision Boundary) 컨투어 플롯 시각화
  * **생각해보기 분석**: 선형회귀와 로지스틱 회귀의 목적·출력·손실 곡면(Convexity) 차이 및 학습률(Learning Rate) 크기에 따른 오버슈팅/발산과 언더피팅 영향 분석

### 3. [`mnist_nn_classification.ipynb`](./3주_과제/mnist_nn_classification.ipynb)
* **주제**: MNIST 손글씨 데이터셋 다층 퍼셉트론(MLP) 분류 및 과적합(Overfitting) 징후 분석
* **주요 내용**:
  * MNIST 손글씨 데이터(60,000장) 로드, [0, 1] 정규화 및 784차원 1D 벡터 변환
  * 다중 클래스(0~9) 분류를 위한 One-hot 인코딩
  * Sequential MLP 모델 설계: Dense(256, ReLU) -> Dense(128, ReLU) -> Dense(10, Softmax)
  * Adam(lr=0.001) 옵티마이저 및 Categorical Crossentropy 컴파일, 10 Epoch 배치 학습 진행
  * 테스트셋 평가(정확도 ~97.9%) 및 정상 분류/오분류(Failed) 이미지 서브플롯 시각화
  * **생각해보기 분석**: Train/Val 손실 및 정확도 곡선의 일반화 격차(Generalization Gap) 관찰, 4~5 에폭 이후의 과적합(Overfitting) 징후 분석 및 Early Stopping/Dropout 등 규제 해결책 도출

---

## 🔬 4주차 과제 상세 안내 (`4주_과제/`)

신경망 학습의 핵심 구성 요소인 활성화 함수와 손실 함수의 특성을 비교하고, 실제 딥러닝 학습 시 마주하는 4대 도전과제(기울기 소실, 과적합, 데이터 부족, 클래스 불균형) 및 이를 해결하기 위한 현대적 딥러닝 테크닉을 실습한 4종의 주피터 노트북 과제입니다.

### 1. [`lab4_1_regression_activation_and_loss.ipynb`](./4주_과제/lab4_1_regression_activation_and_loss.ipynb)
* **주제**: 회귀(Regression) 문제에서의 활성화 함수 및 손실 함수 비교
* **주요 내용**:
  * 비선형 사인 함수 데이터셋($y = \sin(x) + \text{noise}$) 생성
  * 활성화 함수 비교: `Linear` vs `Sigmoid` vs `ReLU`에 따른 비선형 회귀 표현력 분석
  * 손실 함수 비교: `MSE` vs `MAE`의 이상치(Outlier) 민감도 및 견고성(Robustness) 비교
  * 학습 곡선(Loss Curve)을 통한 수렴 속도 및 최종 피팅 성능 평가

### 2. [`lab4_2_classification_activation_and_loss.ipynb`](./4주_과제/lab4_2_classification_activation_and_loss.ipynb)
* **주제**: 분류(Classification) 문제에서의 활성화 함수 및 손실 함수 비교
* **주요 내용**:
  * 비선형 나선형/달 모양(`make_moons`) 이진 분류 데이터셋 활용
  * 은닉층 활성화 함수 비교: `Sigmoid` vs `Tanh` vs `ReLU`의 학습 속도 및 수렴 특성 분석
  * 손실 함수 비교: 분류 문제에서 `Binary Crossentropy` vs `MSE`의 성능 및 그래디언트 차이 검증
  * 2D 결정 경계(Decision Boundary) 시각화를 통한 분류 평면 비교

### 3. [`lab4_3_challenging_problems.ipynb`](./4주_과제/lab4_3_challenging_problems.ipynb)
* **주제**: 지도학습의 4대 도전과제(Challenging Problems) 체감 실습
* **주요 내용**:
  * **기울기 소실(Vanishing Gradient)**: 20층 심층망에서 Sigmoid(기울기 소실로 학습 정체) vs ReLU(안정적 역전파로 정상 학습) 비교
  * **모델 복잡도와 과적합(Overfitting)**: 단순 모델(8유닛) vs 복잡 모델(128유닛 3층)의 Train/Val 곡선 비교 및 일반화 갭 분석
  * **데이터 크기와 과적합**: 작은 데이터셋(100개) vs 큰 데이터셋(2000개) 학습 비교를 통한 데이터 양의 중요성 체감
  * **클래스 불균형과 정확도의 착시**: 90:10 불균형 데이터에서 정확도(96%)의 함정과 50:50 균형 데이터 평가 시 정확도 폭락(38%) 및 재현율(Recall) 한계 분석

### 4. [`lab4_4_techniques_for_challenging_problems.ipynb`](./4주_과제/lab4_4_techniques_for_challenging_problems.ipynb)
* **주제**: 도전과제 극복을 위한 핵심 딥러닝 테크닉 실습
* **주요 내용**:
  * **ResNet Skip Connection**: Residual Block을 통해 20층 이상의 깊은 망에서도 기울기 소실 없이 빠른 손실 감소 및 안정적 수렴 달성
  * **가중치 규제 (L1/L2 Regularization)**: Lasso(L1, 가중치 희소화) 및 Ridge(L2, 가중치 감쇠)를 적용한 과적합 억제
  * **드롭아웃 (Dropout)**: 학습 시 무작위 뉴런 비활성화를 통한 앙상블 효과 및 과적합 방지
  * **불균형 데이터 해결 기법**: CIFAR-10 고양이(1,000장) vs 개(5,000장) 불균형 데이터셋에서 Baseline(고양이 재현율 5.8%) 대비 **Balanced Data Augmentation**(재현율 65.3%) 및 **Class Weighting**(재현율 73.0%) 적용을 통한 획기적 성능 개선

---

## 🗂️ 디렉토리 구조

```
제조 AI 실제/
├── .gitignore
├── README.md
├── 제조AI실제(1주차).pdf
├── 제조AI실제(2주차).pdf
├── 제조AI실제(3주차).pdf
├── 제조AI실제(4주차).pdf
├── 2주_과제/
│   ├── cwru_fault.mat
│   ├── cwru_normal.mat
│   ├── manufacturing_ai_lab2_1.ipynb
│   └── manufacturing_ai_lab2_2.ipynb
├── 3주_과제/
│   ├── linear_regression.ipynb
│   ├── logistic_regression.ipynb
│   └── mnist_nn_classification.ipynb
└── 4주_과제/
    ├── lab4_1_regression_activation_and_loss.ipynb
    ├── lab4_2_classification_activation_and_loss.ipynb
    ├── lab4_3_challenging_problems.ipynb
    └── lab4_4_techniques_for_challenging_problems.ipynb
```

---

## 🛠️ 실습 환경

| 항목 | 권장 버전 / 환경 |
| :--- | :--- |
| OS | Windows 10/11 / macOS / Linux |
| Python | 3.10+ |
| TensorFlow / Keras | 2.12+ |
| PyTorch | 2.0+ |
| scikit-learn | 1.2+ |
| NumPy | 1.24+ |
| SciPy | 1.10+ |
| Matplotlib / Seaborn | 3.7+ |

---

*최종 업데이트: 2026-09-23*
