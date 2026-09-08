# ==========================================
# 충북대학교 산업인공지능학과 중간 프로젝트
# 주제: 시계열 데이터를 활용한 자전거 수요 예측 및 회귀 모델 비교
# ==========================================

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.datasets import fetch_openml
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.linear_model import LinearRegression, Ridge, Lasso
from sklearn.metrics import mean_squared_error, r2_score

# 한글 폰트 설정 (Windows: Malgun Gothic, Mac: AppleGothic)
plt.rcParams['font.family'] = 'Malgun Gothic'
plt.rcParams['axes.unicode_minus'] = False

# ==========================================
# 1. 데이터 수집 및 이해 (Data Loading)
# ==========================================
print("데이터를 불러오는 중입니다... (OpenML Bike Sharing Dataset)")
# OpenML에서 자전거 대여 데이터셋 로드 (정확한 ID: 42712 사용)
bike_data = fetch_openml(data_id=42712, as_frame=True, parser='auto')
df = bike_data.frame

# 분석에 사용할 주요 컬럼 선택 및 이름 변경 (OpenML 42712 구조에 맞춤)
df = df[['season', 'month', 'hour', 'holiday', 'weekday', 'workingday', 'weather', 'temp', 'humidity', 'windspeed',
         'count']]
df.rename(columns={'count': 'total_rentals'}, inplace=True)

# ==========================================
# 2. 데이터 전처리 (Data Preprocessing)
# ==========================================
print("데이터 전처리를 시작합니다...")

# (1) 결측치 확인 및 제거
df.dropna(inplace=True)

# (2) 범주형 데이터 원-핫 인코딩 (One-Hot Encoding)
# 'season' 등 문자열이 섞여 있을 수 있는 범주형 컬럼을 0과 1의 더미 변수로 변환
categorical_cols = ['season', 'month', 'hour', 'holiday', 'weekday', 'workingday', 'weather']
# drop_first=True: 다중공선성(Multi-collinearity) 방지를 위해 첫 번째 카테고리는 제외
df = pd.get_dummies(df, columns=categorical_cols, drop_first=True)

# (3) 피처와 타겟 분리
X = df.drop('total_rentals', axis=1)  # 독립변수 (피처)
y = df['total_rentals']  # 종속변수 (예측 타겟)

# (4) 학습용/테스트용 데이터 분할 (8:2 비율)
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# (5) 데이터 스케일링 (Standardization)
# 연속형 변수(온도, 습도, 풍속 등)를 포함한 모든 피처의 스케일을 동일하게 맞춤
scaler = StandardScaler()
X_train_scaled = scaler.fit_transform(X_train)
X_test_scaled = scaler.transform(X_test)

# ==========================================
# 3. 모델 훈련 및 비교 (Model Training)
# ==========================================
print("모델 학습 및 평가를 진행합니다...")

# 3가지 모델 선언 (일반 선형회귀, L2 리지, L1 라쏘)
models = {
    "Linear Regression (OLS)": LinearRegression(),
    "Ridge (L2 정규화)": Ridge(alpha=10.0),
    "Lasso (L1 정규화)": Lasso(alpha=10.0)
}

results = {}
coefficients = {}

for name, model in models.items():
    # 모델 학습
    model.fit(X_train_scaled, y_train)
    # 예측
    y_pred = model.predict(X_test_scaled)

    # 성능 평가 (MSE, RMSE, R2 Score)
    mse = mean_squared_error(y_test, y_pred)
    rmse = np.sqrt(mse)
    r2 = r2_score(y_test, y_pred)

    results[name] = {'MSE': mse, 'RMSE': rmse, 'R2': r2}
    coefficients[name] = model.coef_

# 결과 출력
print("\n=== 모델 성능 평가 결과 ===")
results_df = pd.DataFrame(results).T
print(results_df)

# ==========================================
# 4. 성능 평가 시각화 및 해석 (Visualization)
# ==========================================
plt.figure(figsize=(15, 10))

# [그래프 1] 실제값 vs 예측값 산점도 (Linear Regression 기준)
plt.subplot(2, 1, 1)
y_pred_ols = models["Linear Regression (OLS)"].predict(X_test_scaled)
plt.scatter(y_test, y_pred_ols, alpha=0.5, color='orange')
plt.plot([y_test.min(), y_test.max()], [y_test.min(), y_test.max()], 'r--', lw=2)
plt.title('실제 대여량 vs OLS 예측 대여량', fontsize=15)
plt.xlabel('실제 자전거 대여량')
plt.ylabel('예측 자전거 대여량')
plt.grid(True, alpha=0.3)

# [그래프 2] 모델별 가중치(Coefficient) 비교 (Lasso vs Ridge)
plt.subplot(2, 1, 2)
feature_names = X.columns
# 피처가 너무 많으면 그래프가 복잡해지므로 상위 15개 피처만 시각화
top_n = 15
ols_coef = np.abs(coefficients["Linear Regression (OLS)"])
top_idx = np.argsort(ols_coef)[::-1][:top_n]

x_idx = np.arange(top_n)
width = 0.3

# 선형회귀, 릿지, 라쏘 가중치 시각화 (상위 15개)
plt.bar(x_idx - width, coefficients["Linear Regression (OLS)"][top_idx], width, label='OLS', color='lightgray')
plt.bar(x_idx, coefficients["Ridge (L2 정규화)"][top_idx], width, label='Ridge (L2)', color='royalblue')
plt.bar(x_idx + width, coefficients["Lasso (L1 정규화)"][top_idx], width, label='Lasso (L1)', color='tomato')

plt.xticks(x_idx, feature_names[top_idx], rotation=45, ha='right')
plt.title(f'회귀 모델별 피처 가중치(Coefficient) 비교 (상위 {top_n}개 영향력 피처)', fontsize=15)
plt.xlabel('Features')
plt.ylabel('Coefficient Value')
plt.legend()
plt.grid(True, alpha=0.3)

plt.tight_layout()
plt.show()
