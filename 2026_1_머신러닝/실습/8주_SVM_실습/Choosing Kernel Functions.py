import numpy as np
import matplotlib.pyplot as plt
from sklearn.svm import SVC
from sklearn.datasets import make_circles
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score

# 데이터 생성
X, y = make_circles(n_samples=300, factor=0.3, noise=0.15, random_state=42)

# 훈련/테스트 데이터 분리
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.3, random_state=42)

# 3가지 모델 정의
models = {
    "1. Linear Kernel ": SVC(kernel='linear', C=1.0),
    "2. RBF Kernel ": SVC(kernel='rbf', C=1.0, gamma=0.5),
    "3. RBF Kernel ": SVC(kernel='rbf', C=1.0, gamma=50.0)
}

ESTIMATED_BAYES_ERROR = 0.05
print("=" * 50)
print(f"🎯 [이론적 한계] Bayes Error (Irreducible Error): 약 {ESTIMATED_BAYES_ERROR * 100:.1f}%\n"
      f"   (데이터 생성 시 부여된 15%의 노이즈로 인해 발생하는 본질적 겹침)")
print("=" * 50)

# 모델 학습 및 Error 계산과 시각화 준비
fig, axes = plt.subplots(1, 3, figsize=(18, 5))

for i, (title, model) in enumerate(models.items()):
    # 학습
    model.fit(X_train, y_train)

    # 예측
    y_train_pred = model.predict(X_train)
    y_test_pred = model.predict(X_test)

    # Error Rate 계산 (1 - 정확도)
    train_error = 1.0 - accuracy_score(y_train, y_train_pred)
    test_error = 1.0 - accuracy_score(y_test, y_test_pred)

    # 결과 출력
    print(f"[{title}]")
    print(f" - Train Error: {train_error * 100:.1f}%")
    print(f" - Test Error : {test_error * 100:.1f}%")
    print("-" * 50)

    # === 시각화 (결정 경계 및 Test 데이터 산점도) ===
    ax = axes[i]
    # 훈련 데이터는 연하게, 테스트 데이터는 진하게 표시
    ax.scatter(X_train[:, 0], X_train[:, 1], c=y_train, cmap='coolwarm', s=20, alpha=0.3)
    ax.scatter(X_test[:, 0], X_test[:, 1], c=y_test, cmap='coolwarm', s=60, edgecolors='k', marker='^')

    xlim, ylim = ax.get_xlim(), ax.get_ylim()
    xx, yy = np.meshgrid(np.linspace(xlim[0], xlim[1], 100), np.linspace(ylim[0], ylim[1], 100))
    Z = model.decision_function(np.c_[xx.ravel(), yy.ravel()]).reshape(xx.shape)

    ax.contour(xx, yy, Z, colors='k', levels=[0], alpha=0.8, linestyles=['-'])
    ax.set_title(f"{title}\nTest Err: {test_error * 100:.1f}%", size=13)

# ----------------- 두 번째 이미지 코드 추가 -----------------
# 딕셔너리의 모델(Value)들만 싹 모아서 리스트로 바꾼 뒤, 첫 번째[0] 모델을 가져옵니다.
linear_model = list(models.values())[0]

print("\n[수학적 증명: 선형 SVM의 항복 선언]")
print("선형 SVM의 가중치(w):", linear_model.coef_)
print("선형 SVM의 편향(b):", linear_model.intercept_)
# -----------------------------------------------------------

plt.tight_layout()
plt.show()