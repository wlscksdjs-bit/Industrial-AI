import numpy as np
import matplotlib.pyplot as plt
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_squared_error, r2_score

np.random.seed(45)
x = 100 * np.random.rand(100, 1)
y = 5 * x + 10 + np.random.rand(100, 1) * 10

model = LinearRegression()
model.fit(x, y)

w1 = model.coef_[0][0]
w0 = model.intercept_[0]

print(f"=== Training Results ===")
print(f"Estimated Slope (w1): {w1: .2f}")
print(f"Estimated Intercept (w0): {w0: .2f}")
print(f"final Equation: y = {w1:.2f} * x + {w0:.2f}")

y_pred = model.predict(x)
mse = mean_squared_error(y, y_pred)
r2 = r2_score(y, y_pred)

print(f"\n=== Model Evaluation ===")
print(f"Mean Squared Error (MSE): {mse:.2f}")
print(f"R-Squared (R2 Score): {r2:.2f}")

plt.figure(figsize=(10, 6))
plt.scatter(x, y, color='blue', alpha=0.6, label='Actual Data')

plt.plot(x, y_pred, color='red', linewidth=2, label='Predicted Line')

plt.title("Linear Regression: Watcha Likes vs Audience", fontsize=14)
plt.xlabel("Watcha 'Like' Count", fontsize=12)
plt.ylabel("Total Audience Count", fontsize=12)
plt.legend()
plt.grid(True, linestyle='--', alpha=0.6)
plt.show()