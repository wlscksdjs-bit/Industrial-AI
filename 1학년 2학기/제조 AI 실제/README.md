# 🏭 제조 AI 실제 (Manufacturing AI in Practice)

본 저장소는 충북대학교 일반대학원 산업인공지능학과 **제조 AI 실제** 강의의 강의 자료(PDF), 주차별 실습 코드(Jupyter Notebook) 및 과제 산출물을 체계적으로 관리하는 공간입니다.

---

## 📌 교과 개요 및 목표
* **교과목명**: 제조 AI 실제 (Manufacturing AI in Practice)
* **담당 교수**: 조경록 교수님
* **소속**: 충북대학교 일반대학원 산업인공지능학과 (석사과정)
* **연구자**: 진찬언 (학번: 2026254019)
* **주요 내용**: 스마트 제조 현장에서 수집되는 다양한 센서 및 신호 데이터(진동, 음향, 온도, 압력 등)를 바탕으로 산업 인공지능 기법(신호처리, 특징 공학, 패턴인식, 신경망 모델링, 결함 진단, 예지보전 및 생성형 AI 기반 비지도 이상치 탐지/데이터 증강)을 적용하는 실무 역량을 함양합니다.
* **주요 도메인 데이터**: CWRU (Case Western Reserve University) 모터 베어링 진동 데이터셋, MNIST 손글씨 데이터셋, 비선형 합성 신호 데이터셋 등

---

## 📂 주차별 강의 자료 및 실습 과제 일람

| 주차 / 주제 | 강의 자료 | 실습 및 과제 폴더 | 주요 학습 내용 및 키워드 |
| :--- | :--- | :--- | :--- |
| **1주차** | [`제조AI실제(1주차).pdf`](./제조AI실제(1주차).pdf) | - | • 제조 인공지능 개요 및 스마트팩토리 적용 사례<br>• 산업 데이터 특성 및 강의 오리엔테이션 |
| **2주차** | [`제조AI실제(2주차).pdf`](./제조AI실제(2주차).pdf) | [`2주_과제/`](./2주_과제/) | • 패턴인식(Pattern Recognition)과 특징(Feature)의 정의<br>• 좋은 특징(Good Feature)과 클래스 분리성(Separability)<br>• 일반화(Generalization)와 제약 조건(Constraints) |
| **3주차** | [`제조AI실제(3주차).pdf`](./제조AI실제(3주차).pdf) | [`3주_과제/`](./3주_과제/) | • 인공신경망(ANN) 기초 및 발전사<br>• 선형회귀(Linear Regression)와 MSE 손실 함수 경사하강법(SGD) 최적화<br>• 로지스틱 회귀(Logistic Regression)와 이진 크로스엔트로피(Log Loss)<br>• 다층 퍼셉트론(MLP) 기반 MNIST 손글씨 분류 및 과적합(Overfitting) 징후 분석 |
| **4주차** | [`제조AI실제(4주차).pdf`](./제조AI실제(4주차).pdf) | [`4주_과제/`](./4주_과제/) | • 활성화 함수(Activation Function): Sigmoid, ReLU, Tanh, Leaky ReLU 비교<br>• 손실 함수(Loss Function): MSE, MAE, Binary/Categorical Cross-Entropy<br>• 기울기 소실(Vanishing Gradient) 문제 및 ReLU를 통한 해결<br>• 과적합(Overfitting) / 과소적합(Underfitting) 진단<br>• 클래스 불균형(Class Imbalance) 문제와 평가 지표(F1, Recall)<br>• ResNet(Skip Connection), Regularization(L1/L2), Dropout, Class Weighting |
| **5주차** | [`제조AI실제(5주차).pdf`](./제조AI실제(5주차).pdf) | [`5주_과제/`](./5주_과제/) | • 생성 모델(Generative Models)의 원리와 산업 도메인 적용<br>• 오토인코더(Autoencoder) 구조 및 재구성 오차 기반 비지도 이상치 탐지<br>• 변이형 오토인코더(VAE)와 잠재 공간(Latent Space) 매니폴드 형성<br>• 적대적 생성 신경망(GAN) 기반 이미지 합성 및 Minimax 목적함수<br>• 확산 모델(Diffusion Model, DDPM)의 Forward/Reverse Denoising 과정 |

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

### 2. [`logistic_regression.ipynb`](./3주_과제/logistic_regression.ipynb)
* **주제**: Iris 데이터셋 기반 로지스틱 회귀 이진 분류 및 결정 경계 시각화
* **주요 내용**:
  * Iris 붓꽃 꽃받침 길이·너비(2개 특성) 추출 및 표준화(StandardScaler)
  * Setosa($y=1$) vs Others($y=0$) 이진 레이블링 및 8:2 Train/Test 분리
  * Dense(1, activation='sigmoid') 모델 정의 및 Binary Crossentropy 손실 함수 설정
  * 100 Epoch 학습 진행, Train/Val 손실 곡선 및 정확도 곡선 도출, 테스트셋 정확도 100% 달성
  * 2D 메쉬그리드 상의 로지스틱 결정 경계(Decision Boundary) 컨투어 플롯 시각화

### 3. [`mnist_nn_classification.ipynb`](./3주_과제/mnist_nn_classification.ipynb)
* **주제**: MNIST 손글씨 데이터셋 다층 퍼셉트론(MLP) 분류 및 과적합(Overfitting) 징후 분석
* **주요 내용**:
  * MNIST 손글씨 데이터(60,000장) 로드, [0, 1] 정규화 및 784차원 1D 벡터 변환
  * Sequential MLP 모델 설계: Dense(256, ReLU) -> Dense(128, ReLU) -> Dense(10, Softmax)
  * 테스트셋 평가(정확도 ~97.9%) 및 정상 분류/오분류 이미지 시각화
  * Train/Val 손실 및 정확도 곡선의 일반화 격차(Generalization Gap) 관찰, 4~5 에폭 이후의 과적합 징후 분석

---

## 🔬 4주차 과제 상세 안내 (`4주_과제/`)

신경망 학습의 핵심 구성 요소인 활성화 함수와 손실 함수의 특성을 비교하고, 실제 딥러닝 학습 시 마주하는 4대 도전과제(기울기 소실, 과적합, 데이터 부족, 클래스 불균형) 및 이를 해결하기 위한 현대적 딥러닝 테크닉을 실습한 4종의 주피터 노트북 과제입니다.

### 1. [`lab4_1_regression_activation_and_loss.ipynb`](./4주_과제/lab4_1_regression_activation_and_loss.ipynb)
* **주제**: 회귀(Regression) 문제에서의 활성화 함수 및 손실 함수 비교
* **핵심 내용**: 비선형 출력 회귀에서 Linear vs ReLU 출력층 비교, 이상치 존재 시 MSE vs MAE 손실 함수의 강건성(Robustness) 비교

### 2. [`lab4_2_classification_activation_and_loss.ipynb`](./4주_과제/lab4_2_classification_activation_and_loss.ipynb)
* **주제**: 분류(Classification) 문제에서의 활성화 함수 및 손실 함수 비교
* **핵심 내용**: Sigmoid vs Tanh vs ReLU 은닉층 활성화 함수 비교, Binary Cross-Entropy vs MSE 손실 함수의 그래디언트 소실 방지 효과 체감

### 3. [`lab4_3_challenging_problems.ipynb`](./4주_과제/lab4_3_challenging_problems.ipynb)
* **주제**: 딥러닝 학습 시 직면하는 4대 도전과제 체감 실습
* **핵심 내용**:
  * **기울기 소실(Vanishing Gradient)**: 20층 깊은 신경망에서 Sigmoid vs ReLU 역전파 그래디언트 소멸 비교
  * **과적합(Overfitting)**: 데이터 대비 과도한 파라미터 용량으로 인한 일반화 성능 저하
  * **데이터 부족(Data Scarcity)**: 소량 샘플 학습 시 높은 분산과 예측 불안정성
  * **클래스 불균형(Class Imbalance)**: 다수 클래스 편향 학습 및 소수 클래스 F1/Recall 폭락 현상

### 4. [`lab4_4_techniques_for_challenging_problems.ipynb`](./4주_과제/lab4_4_techniques_for_challenging_problems.ipynb)
* **주제**: 4대 도전과제를 극복하기 위한 현대적 딥러닝 기법 실습
* **핵심 내용**:
  * **ResNet (Skip Connection)**: 잔차 연결을 통한 초심층 신경망 기울기 소실 해결
  * **정규화(Regularization) & Dropout**: L1/L2 Weight Decay 및 드롭아웃을 통한 과적합 억제
  * **데이터 증강(Data Augmentation)**: 회전, 이동 등 기하 변환을 통한 데이터 부족 극복
  * **클래스 가중치(Class Weighting)**: 손실 함수 역빈도 가중치를 통한 희소 클래스 검출력 회복

---

## 🔬 5주차 과제 상세 안내 (`5주_과제/`)

산업 인공지능 현장에서 결함 데이터가 절대적으로 부족한 문제를 해결하기 위해, 비지도 표현 학습 및 데이터 증강의 핵심 축을 담당하는 **생성 모델(Generative Models)** 4종을 단계별로 심층 실습한 과제입니다.

### 1. [`lab5_1_autoencoder.ipynb`](./5주_과제/lab5_1_autoencoder.ipynb)
* **주제**: Autoencoder 종합 실습 및 비지도 이상치 탐지
* **핵심 내용**:
  * **인코더(Encoder)-디코더(Decoder) 아키텍처**: 고차원 입력 신호를 저차원 병목 계층(Bottleneck Latent Space)으로 압축 후 원본 복원
  * **재구성 오차(Reconstruction Error)**: 정상 데이터로만 학습된 모델이 이상치(Anomaly) 입력 시 높은 재구성 오차를 발생시키는 원리를 활용한 비지도 결함 진단 실습
  * **노이즈 제거 오토인코더(Denoising Autoencoder)**: 가우시안 노이즈가 주입된 센서 신호의 노이즈 필터링 및 강건한 특징 추출

### 2. [`lab5_2_vae.ipynb`](./5주_과제/lab5_2_vae.ipynb)
* **주제**: Variational Autoencoder (VAE)를 활용한 잠재 공간 매니폴드 생성
* **핵심 내용**:
  * **확률론적 잠재 표현**: 고정된 점이 아닌 평균($\mu$)과 분산($\sigma^2$)의 가우시안 분포 매개변수를 출력
  * **재매개변수화 트릭(Reparameterization Trick)**: 확률적 샘플링 $z = \mu + \sigma \odot \epsilon$ ($\epsilon \sim \mathcal{N}(0, I)$)을 통해 역전파 그래디언트 전파 보장
  * **ELBO 손실 함수**: 재구성 손실(Reconstruction Loss) + 정규화 손실(KL Divergence)의 균형 제어
  * **2D 잠재 공간 매니폴드(Latent Manifold) 시각화**: 연속적인 잠재 공간 보간(Interpolation)을 통한 부드러운 합성 데이터 생성

### 3. [`lab5_3_gan.ipynb`](./5주_과제/lab5_3_gan.ipynb)
* **주제**: GAN (Generative Adversarial Network) 기반 데이터 생성 실습
* **핵심 내용**:
  * **적대적 학습(Adversarial Training)**: 잠재 벡터 $z$로부터 가짜 샘플을 만드는 생성자(Generator)와 진짜/가짜를 판별하는 판별자(Discriminator)의 Minimax Zero-Sum 게임
  * **손실 함수 최적화**: 판별자 손실($\mathcal{L}_D$)과 생성자 손실($\mathcal{L}_G$)의 교대 훈련
  * **생성 품질 모니터링**: 훈련 에폭 경과에 따른 노이즈에서 실제 데이터 분포로의 수렴 과정 시각화
  * **모드 붕괴(Mode Collapse)** 및 학습 불안정성 문제와 안정화 테크닉 고찰

### 4. [`lab5_4_diffusion_model.ipynb`](./5주_과제/lab5_4_diffusion_model.ipynb)
* **주제**: Denoising Diffusion Probabilistic Model (DDPM) 기초 실습
* **핵심 내용**:
  * **순방향 확산 과정(Forward Process)**: 원본 데이터에 $T$스텝에 걸쳐 점진적으로 가우시안 노이즈를 주입하여 완전한 가우시안 노이즈로 변환
  * **역방향 디노이징 과정(Reverse Process)**: 신경망(U-Net / MLP)을 통해 각 스텝에 주입된 노이즈를 예측하고 제거하여 원본 데이터 복원
  * **노이즈 스케줄러(Beta Schedule)**: Linear / Cosine 스케줄러에 따른 확산 강도 제어
  * **현대 생성형 AI 기술 체계화**: GAN 대비 안정적인 학습과 VAE 대비 고품질 합성 샘플 생성의 원리 비교

---

## 📂 디렉터리 구조

```
제조 AI 실제/
├── README.md
├── .gitignore
├── 제조AI실제(1주차).pdf
├── 제조AI실제(2주차).pdf
├── 제조AI실제(3주차).pdf
├── 제조AI실제(4주차).pdf
├── 제조AI실제(5주차).pdf
├── 2주_과제/
│   ├── cwru_fault.mat
│   ├── cwru_normal.mat
│   ├── manufacturing_ai_lab2_1.ipynb
│   └── manufacturing_ai_lab2_2.ipynb
├── 3주_과제/
│   ├── linear_regression.ipynb
│   ├── logistic_regression.ipynb
│   └── mnist_nn_classification.ipynb
├── 4주_과제/
│   ├── lab4_1_regression_activation_and_loss.ipynb
│   ├── lab4_2_classification_activation_and_loss.ipynb
│   ├── lab4_3_challenging_problems.ipynb
│   └── lab4_4_techniques_for_challenging_problems.ipynb
└── 5주_과제/
    ├── lab5_1_autoencoder.ipynb
    ├── lab5_2_vae.ipynb
    ├── lab5_3_gan.ipynb
    └── lab5_4_diffusion_model.ipynb
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

*최종 업데이트: 2026-09-29*
