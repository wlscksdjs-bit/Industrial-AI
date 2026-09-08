import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_squared_error, r2_score

file_path = r"C:\Users\JIN\PycharmProjects\PythonProject1\datasets\Salary_Data.csv"
dataset = pd.read_csv(file_path)

print("데이터셋 정보")
print(dataset.info())
print("\n- 데이터 상위 5행 -")
print(dataset.head())

X = dataset.iloc[:, :-1].values
y = dataset.iloc[:, -1].values

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size = 0.2, random_state = 0)

model = LinearRegression()
model.fit(X_train, y_train)

y_pred = model.predict(X_test)

rmse = np.sqrt(mean_squared_error(y_test, y_pred))
r2 = r2_score(y_test, y_pred)

print(f"\n--- [실습 결과] ---")
print(f"기울기(Weight, w): {model.coef_[0]:.2f}")
print(f"절편(Bias, b): {model.intercept_:.2f}")
print(f"RMSE: {rmse:.2f}")
print(f"R-squared: {r2:.4f}")

plt.figure(figsize=(10, 6))
plt.scatter(X, y, color='darkorange', label='Actual Data')
plt.plot(X, model.predict(X), color='royalblue', linewidth=2, label='OLS Line')
plt.title('Salary vs Experience (OLS Regression)')
plt.xlabel('Years of Experience')
plt.ylabel('Salary')
plt.legend()
plt.grid(True, linestyle='--', alpha=0.6)
plt.show()
