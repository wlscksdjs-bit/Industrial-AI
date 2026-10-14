# 🏭 제조 AI 실제 (Manufacturing AI in Practice)

본 저장소는 충북대학교 일반대학원 산업인공지능학과 **제조 AI 실제** 강의의 강의 자료(PDF), 주차별 실습 코드(Jupyter Notebook) 및 과제 산출물을 체계적으로 관리하는 공간입니다.

---

## 📌 교과 개요 및 목표
* **교과목명**: 제조 AI 실제 (Manufacturing AI in Practice)
* **담당 교수**: 조경록 교수님
* **소속**: 충북대학교 일반대학원 산업인공지능학과 (석사과정)
* **연구자**: 진찬언 (학번: 2026254019)
* **주요 내용**: 스마트 제조 현장에서 수집되는 다양한 센서 및 신호 데이터(진동, 음향, 온도, 압력 등)를 바탕으로 산업 인공지능 기법(신호처리, 특징 공학, 패턴인식, 신경망 모델링, 결함 진단, 예지보전, 생성형 AI 기반 비지도 이상치 탐지/데이터 증강 및 합성곱 신경망 CNN/전이학습)을 적용하는 실무 역량을 함양합니다.
* **주요 도메인 데이터**: CWRU (Case Western Reserve University) 모터 베어링 진동 데이터셋, MNIST 손글씨 데이터셋, CIFAR-10 객체 데이터셋, 비선형 합성 신호 데이터셋 등

---

## 📂 주차별 강의 자료 및 실습 과제 일람

| 주차 / 주제 | 강의 자료 | 실습 및 과제 폴더 | 주요 학습 내용 및 키워드 |
| :--- | :--- | :--- | :--- |
| **1주차** | [`제조AI실제(1주차).pdf`](./제조AI실제(1주차).pdf) | - | • 제조 인공지능 개요 및 스마트팩토리 적용 사례<br>• 산업 데이터 특성 및 강의 오리엔테이션 |
| **2주차** | [`제조AI실제(2주차).pdf`](./제조AI실제(2주차).pdf) | [`2주_과제/`](./2주_과제/) | • 패턴인식(Pattern Recognition)과 특징(Feature)의 정의<br>• 좋은 특징(Good Feature)과 클래스 분리성(Separability)<br>• 일반화(Generalization)와 제약 조건(Constraints) |
| **3주차** | [`제조AI실제(3주차).pdf`](./제조AI실제(3주차).pdf) | [`3주_과제/`](./3주_과제/) | • 인공신경망(ANN) 기초 및 발전사<br>• 선형회귀(Linear Regression)와 MSE 손실 함수 경사하강법(SGD) 최적화<br>• 로지스틱 회귀(Logistic Regression)와 이진 크로스엔트로피(Log Loss)<br>• 다층 퍼셉트론(MLP) 기반 MNIST 손글씨 분류 및 과적합(Overfitting) 징후 분석 |
| **4주차** | [`제조AI실제(4주차).pdf`](./제조AI실제(4주차).pdf) | [`4주_과제/`](./4주_과제/) | • 활성화 함수(Activation Function): Sigmoid, ReLU, Tanh, Leaky ReLU 비교<br>• 손실 함수(Loss Function): MSE, MAE, Binary/Categorical Cross-Entropy<br>• 기울기 소실(Vanishing Gradient) 문제 및 ReLU를 통한 해결<br>• 과적합(Overfitting) / 과소적합(Underfitting) 진단<br>• 클래스 불균형(Class Imbalance) 문제와 평가 지표(F1, Recall)<br>• ResNet(Skip Connection), Regularization(L1/L2), Dropout, Class Weighting |
| **5주차** | [`제조AI실제(5주차).pdf`](./제조AI실제(5주차).pdf) | [`5주_과제/`](./5주_과제/) | • 생성 모델(Generative Models)의 원리와 산업 도메인 적용<br>• 오토인코더(Autoencoder) 구조 및 재구성 오차 기반 비지도 이상치 탐지<br>• 변이형 오토인코더(VAE)와 잠재 공간(Latent Space) 매니폴드 형성<br>• 적대적 생성 신경망(GAN) 기반 이미지 합성 및 Minimax 목적함수<br>• 확산 모델(Diffusion Model, DDPM)의 Forward/Reverse Denoising 과정 |
| **6주차** | [`제조AI실제_6주차_글로벌제조트렌드.pdf`](./제조AI실제_6주차_글로벌제조트렌드.pdf) | - | • 글로벌 제조 패러다임 변화 및 디지털 트윈, 자율 제조 트렌드<br>• 지속가능 제조(ESG) 및 공급망 복원력을 위한 인공지능 전략 |
| **7주차** | [`제조AI실제(7주차).pdf`](./제조AI실제(7주차).pdf) | [`7주_과제/`](./7주_과제/) | • 합성곱 신경망(CNN) 동작 원리(Convolution, Stride, Padding, Pooling)<br>• 고전 CNN 모델 아키텍처: LeNet-5, VGG16<br>• 고급 CNN 및 전이학습: GoogLeNet(InceptionV3), ResNet50, Fine-tuning |

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

인공신경망의 수학적 기초인 선형회귀, 로지스틱 회귀 및 다층 퍼셉트론(MLP)을 직접 구현하고 학습 과정을 분석하는 3종의 주피터 노트북 실습 과제입니다.

### 1. [`linear_regression.ipynb`](./3주_과제/linear_regression.ipynb)
* **주제**: 선형회귀(Linear Regression)와 경사하강법(Gradient Descent)
* **핵심 내용**:
  * 합성 선형 데이터셋 생성 및 정규화
  * MSE(Mean Squared Error) 손실 함수 정의 및 확률적 경사하강법(SGD) 가중치/편향 업데이트 구현
  * 학습률(Learning Rate)에 따른 수렴 속도 및 손실 감소 곡선 시각화

### 2. [`logistic_regression.ipynb`](./3주_과제/logistic_regression.ipynb)
* **주제**: 로지스틱 회귀(Logistic Regression)와 이진 분류 결정 경계
* **핵심 내용**:
  * Iris 붓꽃 데이터셋 이진 분류 태스크 구성
  * 시그모이드(Sigmoid) 함수 및 Binary Cross-Entropy (Log Loss) 구현
  * 2차원 특징 공간에서의 선형 결정 경계(Decision Boundary) 시각화

### 3. [`mnist_nn_classification.ipynb`](./3주_과제/mnist_nn_classification.ipynb)
* **주제**: 다층 퍼셉트론(MLP) 기반 MNIST 손글씨 숫자 분류 및 과적합 분석
* **핵심 내용**:
  * 28x28 이미지 평탄화(Flatten) 및 다층 밀집층(Dense Layer) 모델 구축
  * Categorical Cross-Entropy 손실 함수 및 Adam 옵티마이저 학습
  * 훈련 손실 vs 검증 손실 곡선을 통한 과적합(Overfitting) 징후 분석 및 혼동 행렬(Confusion Matrix) 도출

---

## 🔬 4주차 과제 상세 안내 (`4주_과제/`)

신경망 학습 과정에서 마주하는 4대 기술적 난제(기울기 소실, 과적합/과소적합, 클래스 불균형, 비선형 한계)를 진단하고 극복하는 4종 주피터 노트북 실습 과제입니다.

### 1. [`lab4_1_regression_activation_and_loss.ipynb`](./4주_과제/lab4_1_regression_activation_and_loss.ipynb)
* **주제**: 회귀(Regression) 모델에서의 활성화 함수와 손실 함수 최적 조합 실습
* **핵심 내용**:
  * 비선형 사인파/다항식 데이터셋 생성
  * 활성화 함수(Linear, ReLU, Tanh)에 따른 비선형 함수 근사 능력 비교
  * 손실 함수(MSE, MAE, Huber Loss)의 이상치(Outlier) 민감도 비교

### 2. [`lab4_2_classification_activation_and_loss.ipynb`](./4주_과제/lab4_2_classification_activation_and_loss.ipynb)
* **주제**: 분류(Classification) 모델에서의 출력층 활성화 함수 및 크로스엔트로피 손실 함수
* **핵심 내용**:
  * 이진 분류: Sigmoid + Binary Cross-Entropy
  * 다중 분류: Softmax + Categorical Cross-Entropy의 확률 분포 출력 해석
  * 잘못된 손실 함수 조합 시 학습 정체 및 발산 현상 실증

### 3. [`lab4_3_challenging_problems.ipynb`](./4주_과제/lab4_3_challenging_problems.ipynb)
* **주제**: 심층 신경망의 4대 도전과제 직접 체감 및 문제점 가시화
* **핵심 내용**:
  * 깊은 신경망(10층 이상)에서 Sigmoid 활성화 함수 사용 시 초기 레이어로 전달되는 그래디언트 소실(Vanishing Gradient) 현상 시각화
  * 소수 샘플 대비 과도한 파라미터로 인한 극단적 과적합(Overfitting) 재현
  * 불균형 데이터셋(99:1) 학습 시 정확도 착시(Accuracy Paradox) 현상 입증

### 4. [`lab4_4_techniques_for_challenging_problems.ipynb`](./4주_과제/lab4_4_techniques_for_challenging_problems.ipynb)
* **주제**: 도전과제 극복을 위한 현대 딥러닝 핵심 기법 적용 실습
* **핵심 내용**:
  * **기울기 소실 극복**: ReLU/Leaky ReLU 도입 및 He/Xavier 가중치 초기화, 배치 정규화(Batch Normalization), ResNet Skip Connection
  * **과적합 방지**: L1/L2 가중치 규제(Weight Decay), 드롭아웃(Dropout 0.3~0.5), 조기 종료(Early Stopping)
  * **클래스 불균형 완화**: Class Weighting, Focal Loss, 층화 샘플링 및 F1-Score/PR-AUC 중심 평가 체계 전환

---

## 🔬 5주차 과제 상세 안내 (`5주_과제/`)

생성형 AI(Generative AI)의 4대 핵심 아키텍처(AE, VAE, GAN, DDPM)의 수학적 원리를 이해하고 구현하는 4종 주피터 노트북 실습 과제입니다.

### 1. [`lab5_1_autoencoder.ipynb`](./5주_과제/lab5_1_autoencoder.ipynb)
* **주제**: 기본 Autoencoder 구조 및 재구성 오차 기반 비지도 결함 진단
* **핵심 내용**:
  * **인코더-디코더 구조**: 차원 축소(Bottleneck)를 통한 핵심 잠재 표현(Latent Representation) 압축
  * **비지도 이상치 탐지(Anomaly Detection)**: 정상 데이터로만 학습 후, 결함 신호 입력 시 발생하는 높은 재구성 오차(MSE)를 임계값 기준으로 탐지
  * **노이즈 제거 오토인코더(Denoising Autoencoder)**: 가우시안 노이즈가 주입된 센서 신호의 원본 복원 성능 검증

### 2. [`lab5_2_vae.ipynb`](./5주_과제/lab5_2_vae.ipynb)
* **주제**: 변이형 오토인코더(Variational Autoencoder)와 잠재 공간 매니폴드 형성
* **핵심 내용**:
  * **확률적 잠재 변수 모델링**: 잠재 벡터를 단일 점이 아닌 평균($\mu$)과 분산($\sigma^2$)의 정규분포로 추정
  * **Reparameterization Trick**: 역전파(Backpropagation)가 가능하도록 확률적 샘플링 과정을 분리 ($z = \mu + \sigma \odot \epsilon$)
  * **ELBO (Evidence Lower Bound) 손실 함수**: 재구성 손실(Reconstruction Loss) + KL 발산(KL Divergence) 정규화
  * 잠재 공간 2차원 매니폴드 시각화 및 부드러운 보간(Interpolation)을 통한 신규 샘플 생성

### 3. [`lab5_3_gan.ipynb`](./5주_과제/lab5_3_gan.ipynb)
* **주제**: 적대적 생성 신경망(Generative Adversarial Network) 기반 이미지 합성
* **핵심 내용**:
  * **생성자(Generator) vs 판별자(Discriminator)**: Minimax 게임 이론 기반 제로섬 경쟁 학습 체계 구축
  * **이진 크로스엔트로피 기반 적대적 손실**: $\min_G \max_D V(D, G)$ 최적화
  * MNIST 손글씨 데이터셋 대상 숫자 이미지 생성 실습
  * **모드 붕괴(Mode Collapse)** 및 학습 불안정성 문제와 안정화 테크닉 고찰

### 4. [`lab5_4_diffusion_model.ipynb`](./5주_과제/lab5_4_diffusion_model.ipynb)
* **주제**: Denoising Diffusion Probabilistic Model (DDPM) 기초 실습
* **핵심 내용**:
  * **순방향 확산 과정(Forward Process)**: 원본 데이터에 $T$스텝에 걸쳐 점진적으로 가우시안 노이즈를 주입하여 완전한 가우시안 노이즈로 변환
  * **역방향 디노이징 과정(Reverse Process)**: 신경망(U-Net / MLP)을 통해 각 스텝에 주입된 노이즈를 예측하고 제거하여 원본 데이터 복원
  * **노이즈 스케줄러(Beta Schedule)**: Linear / Cosine 스케줄러에 따른 확산 강도 제어
  * **현대 생성형 AI 기술 체계화**: GAN 대비 안정적인 학습과 VAE 대비 고품질 합성 샘플 생성의 원리 비교

---

## 📖 6주차 강의 자료 안내
* **강의 자료**: [`제조AI실제_6주차_글로벌제조트렌드.pdf`](./제조AI실제_6주차_글로벌제조트렌드.pdf)
* **주요 내용**:
  * 글로벌 제조업의 스마트화·디지털 전환(DX) 동향 및 미래 제조 트렌드
  * 인공지능 기반 자율 공정 제어 및 예측 유지보수 실증 사례
  * 탄소 중립 및 제조 지속가능성을 위한 AI 최적화 방향

---

## 🔬 7주차 과제 상세 안내 (`7주_과제/`)

합성곱 신경망(CNN)의 핵심 메커니즘 체감, 고전 CNN 모델 구현, 사전학습 가중치를 활용한 전이학습(Transfer Learning) 및 미세조정(Fine-tuning)을 실습하는 3종 주피터 노트북입니다.

### 1. [`Lab7_1.cnn_mnist_convolution_pooling.ipynb`](./7주_과제/Lab7_1.cnn_mnist_convolution_pooling.ipynb)
* **주제**: Convolution & Pooling 동작 원리 실습 및 MNIST 기본 CNN 모델 구축
* **핵심 내용**:
  * **Convolution 파라미터 시각화**: 커널 크기(Kernel Size), Stride(보폭), Padding(`valid` vs `same`), Dilation, Filter 개수 및 Bias에 따른 특징맵(Feature Map) 변화 분석
  * **Pooling 연산 비교**: MaxPooling2D(주요 피처 보존) vs AveragePooling2D(평균 평활화)의 출력 특성 비교
  * **기본 CNN 모델 구축 및 학습**: MNIST 6만 장 데이터 대상 Conv2D + MaxPooling + Dense 구조 학습 (3 Epochs 무오류 검증 완료)

### 2. [`Lab7_2.classic_cnn.ipynb`](./7주_과제/Lab7_2.classic_cnn.ipynb)
* **주제**: 고전 CNN 대표 모델(LeNet-5, VGG16) 구조 실습 및 비교
* **핵심 내용**:
  * **LeNet-5 구현 및 학습**: Yann LeCun의 고전 구조(Conv-Pool-Conv-Pool-FC) 구현 및 MNIST 분류 5 에포크 학습 → **테스트 정확도 98.17%** 달성
  * **VGG16 ImageNet 사전학습 가중치 추론**: 1억 3,800만 파라미터의 깊은 3x3 Conv 적층 모델 로드 및 코끼리 이미지 추론 테스트
  * **모델 파라미터 비교**: LeNet-5 (61,706개) vs VGG16 (138,357,544개)의 크기 및 연산 복잡도 분석

### 3. [`Lab7_3.inception_resnet_finetuning_transfer.ipynb`](./7주_과제/Lab7_3.inception_resnet_finetuning_transfer.ipynb)
* **주제**: GoogLeNet(InceptionV3) & ResNet50 전이학습(Transfer Learning) 및 미세조정(Fine-tuning)
* **핵심 내용**:
  * **InceptionV3 & ResNet50 사전학습 모델 로드**: Top-3 추론 검증 (`African_elephant` 65.5%, `tusker` 24.4%, `Indian_elephant` 10.1%)
  * **InceptionV3 미세조정(Fine-tuning)**: Feature Extractor 고정 후 상위 30개 레이어 가중치 동결 해제(Unfreeze) 및 낮은 학습률(1e-5) 기반 미세조정 파이프라인 구성
  * **ResNet50 기반 CIFAR-10 전이학습(Transfer Learning)**: ResNet50 백본 고정 + GlobalAveragePooling2D + Dense 분류기 결합 후 CIFAR-10 대상 3 에포크 학습
  * **4종 모델 파라미터 종합 비교**: InceptionV3 (23.8M), ResNet50 (25.6M), Fine-tuned Inception (21.9M), Transfer ResNet50 (24.1M)

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
├── 제조AI실제_6주차_글로벌제조트렌드.pdf
├── 제조AI실제(7주차).pdf
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
├── 5주_과제/
│   ├── lab5_1_autoencoder.ipynb
│   ├── lab5_2_vae.ipynb
│   ├── lab5_3_gan.ipynb
│   └── lab5_4_diffusion_model.ipynb
└── 7주_과제/
    ├── Lab7_1.cnn_mnist_convolution_pooling.ipynb
    ├── Lab7_2.classic_cnn.ipynb
    └── Lab7_3.inception_resnet_finetuning_transfer.ipynb
```

---

## 🛠️ 실습 환경

| 항목 | 권장 버전 / 환경 |
| :--- | :--- |
| OS | Windows 10/11 / macOS / Linux |
| Python | 3.10+ |
| TensorFlow / Keras | 2.12+ (Keras 3.x 호환) |
| PyTorch | 2.0+ |
| scikit-learn | 1.2+ |
| NumPy | 1.24+ |
| SciPy | 1.10+ |
| Matplotlib / Seaborn | 3.7+ |

---

*최종 업데이트: 2026-10-14*
