import numpy as np
import matplotlib.pyplot as plt
from sklearn.tree import DecisionTreeRegressor, plot_tree

# [Part 3: Regression Tree Example]

np.random.seed(42)
X = np.sort(5 * np.random.rand(80, 1), axis=0)
y = np.sin(X).ravel()
y[::5] += 3 * (0.5 - np.random.rand(16)) # 5번째 데이터마다 노이즈 추가

# 2. 서로 다른 깊이(depth)를 가진 회귀 나무 모델 학습
regr_1 = DecisionTreeRegressor(max_depth=2)
regr_2 = DecisionTreeRegressor(max_depth=5)
regr_1.fit(X, y)
regr_2.fit(X, y)

# 3. 예측값 계산
X_test = np.arange(0.0, 5.0, 0.01)[:, np.newaxis]
y_1 = regr_1.predict(X_test)
y_2 = regr_2.predict(X_test)

# 4. 결과 시각화 (Step-function Prediction)
plt.figure(figsize=(10, 6))
plt.scatter(X, y, s=20, edgecolor="black", c="darkorange", label="data")
plt.plot(X_test, y_1, color="cornflowerblue", label="max_depth=2", linewidth=2)
plt.plot(X_test, y_2, color="yellowgreen", label="max_depth=5", linewidth=2)
plt.xlabel("data")
plt.ylabel("target")
plt.title("Decision Tree Regression (Step-function Prediction)")
plt.legend()
plt.show()

# 5. 트리 구조 시각화 (깊이 2 모델)
plt.figure(figsize=(12, 6))
plot_tree(regr_1, filled=True, feature_names=["X"])
plt.title("Regression Tree Structure (MSE Minimization)")
plt.show()
