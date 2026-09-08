import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from sklearn.linear_model import SGDRegressor
from sklearn.preprocessing import StandardScaler
from sklearn.metrics import mean_squared_error

# 1. 데이터 로드 및 전처리
df = pd.read_csv(r'C:\Users\JIN\PycharmProjects\PythonProject1\datasets\Salary_Data.csv')
X, y = df[["YearsExperience"]].values, df["Salary"].values

scaler = StandardScaler()
X_s = scaler.fit_transform(X)

# 2. 하이퍼파라미터 세팅
epochs = 50  # 전체 데이터를 50번 반복 학습
eta0 = 0.05  # 변동성을 확실히 보기 위해 학습률(보폭)을 약간 높임 (0.01 -> 0.05)
batch_size_mini = 5  # 미니 배치 크기 설정

sgd_stochastic = SGDRegressor(learning_rate='constant', eta0=eta0, random_state=42)
sgd_minibatch = SGDRegressor(learning_rate='constant', eta0=eta0, random_state=42)

# 에포크마다 오차(MSE)를 기록할 리스트
loss_stochastic = []
loss_minibatch = []

n_samples = len(X_s)

# 3. 학습 진행 (For loop)
for epoch in range(epochs):
    # 매 에포크마다 데이터를 섞어줌 (확률적 특성을 살리기 위함)
    indices = np.random.permutation(n_samples)
    X_shuffled = X_s[indices]
    y_shuffled = y[indices]

    # --- [Stochastic GD: 데이터 1개씩 학습] ---
    for i in range(n_samples):
        X_batch = X_shuffled[i:i + 1]
        y_batch = y_shuffled[i:i + 1]
        sgd_stochastic.partial_fit(X_batch, y_batch)
    # 1 에포크 종료 후 현재 모델의 전체 오차 기록
    loss_stochastic.append(mean_squared_error(y, sgd_stochastic.predict(X_s)))

    # --- [Mini-batch GD: 데이터 5개씩 묶어서 학습] ---
    for i in range(0, n_samples, batch_size_mini):
        X_batch = X_shuffled[i:i + batch_size_mini]
        y_batch = y_shuffled[i:i + batch_size_mini]
        sgd_minibatch.partial_fit(X_batch, y_batch)
    # 1 에포크 종료 후 현재 모델의 전체 오차 기록
    loss_minibatch.append(mean_squared_error(y, sgd_minibatch.predict(X_s)))

# 4. 결과 시각화
plt.figure(figsize=(12, 6))

# 선 그래프 그리기
plt.plot(range(1, epochs + 1), loss_stochastic, color='red', alpha=0.7, label='Stochastic (Size=1)')
plt.plot(range(1, epochs + 1), loss_minibatch, color='blue', linewidth=2.5, label='Mini-batch (Size=5)')

plt.title("SGD vs Mini-batch GD Loss Curve\n(Stochastic의 요동치는 모습과 Mini-batch의 안정성 비교)", fontsize=15, fontweight='bold')
plt.xlabel("Epochs (반복 횟수)", fontsize=12)
plt.ylabel("Mean Squared Error (오차)", fontsize=12)
plt.legend(fontsize=12)
plt.grid(True, linestyle='--', alpha=0.6)

plt.tight_layout()
plt.show()