import pandas as pd
import matplotlib.pyplot as plt
from sklearn.linear_model import LinearRegression, SGDRegressor
from sklearn.preprocessing import StandardScaler

df = pd.read_csv(r'C:\Users\JIN\PycharmProjects\PythonProject1\datasets\Salary_Data.csv')
X, y = df[["YearsExperience"]], df["Salary"]

ols = LinearRegression().fit(X, y)

scaler = StandardScaler()
X_s = scaler.fit_transform(X)

sgd_short = SGDRegressor(max_iter=1, tol=None, eta0=0.01, random_state=42).fit(X_s, y)

sgd_long = SGDRegressor(max_iter=1000, tol=1e-3, eta0=0.01, random_state=42).fit(X_s, y)

plt.figure(figsize=(18, 6))

plt.subplot(1, 3, 1)
plt.scatter(X, y, color='orange', alpha=0.5)
plt.plot(X, ols.predict(X), color='blue', linewidth=3)
title_ols = f"OLS: Exact Solution\nw: {ols.coef_[0]:.2f}, b: {ols.intercept_:.2f}"
plt.title(title_ols, fontsize=12, fontweight='bold')

plt.subplot(1, 3, 2)
plt.scatter(X, y, color='orange', alpha=0.5)
plt.plot(X_s, sgd_short.predict(X_s), color='red', linestyle='--', label='1 Iteration')
title_short = f"SGD: 1 Iteration\nw: {sgd_short.coef_[0]:.2f}, b: {sgd_short.intercept_[0]:.2f}"
plt.title(title_short, fontsize=12, color='red')
plt.legend()

plt.subplot(1, 3, 3)
plt.scatter(X_s, y, color='orange', alpha=0.5)
plt.plot(X_s, sgd_long.predict(X_s), color='green', linewidth=3, label='1000 Iterations')
tittle_long = f"SGD: Final Convergence\nw: {sgd_long.coef_[0]:.2f}, b: {sgd_long.intercept_[0]:.2f}"
plt.title(tittle_long, fontsize=12, fontweight='bold', color='green')
plt.legend()
plt.tight_layout()
plt.show()
