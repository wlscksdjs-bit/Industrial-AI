import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from sklearn.linear_model import LinearRegression
from sklearn.metrics import r2_score

# 1. 데이터 불러오기
file_path = r"C:\Users\JIN\PycharmProjects\PythonProject1\datasets\Salary_Data.csv"
data = pd.read_csv(file_path)

# 2. 데이터 분리(x: 경력, y: 연봉)
x = data[['YearsExperience']]
y = data['Salary']

# 3. 모델 생성 및 학습
model = LinearRegression()
model.fit(x, y)

# 4. 학습 결과 확인
w1 = model.coef_[0]     # 기울기(1년당 인상액)
w0 = model.intercept_   # 절편(초봉)

print(f"=== AI 분석 결과 ===")
print(f"공식: Salary = {w1:.2f} * Experience + {w0:.2f}")
print(f"1) 연봉 인상액: ${w1:.2f}")
print(f"2) 예상 초봉: ${w0:.2f}")

# 5. 모델 평가 및 미래 예측
y_pred = model.predict(x)
print(f"3) 정확도(R2): {r2_score(y, y_pred):.4f}")

# 6. 경력 15년차 예측
x_new = pd.DataFrame([[15]], columns=['YearsExperience'])
pred_15 = model.predict(x_new)
print(f"4) 15년차 예상 연봉: ${pred_15[0]:,.2f}")
plt.figure(figsize=(10, 6))
plt.scatter(x, y, color='blue', label='Actual Data')
plt.plot(x, y_pred, color='red', linewidth=2, label='Regression Line')

# 7. 시각화
plt.title("Salary vs Experience Analysis", fontsize=15)
plt.xlabel("Years of Experience")
plt.ylabel("Salary ($)")
plt.legend()
plt.grid(True, alpha=0.3)
plt.show()
