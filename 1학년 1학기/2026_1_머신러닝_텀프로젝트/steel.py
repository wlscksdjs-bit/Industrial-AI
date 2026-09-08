# ==========================================
# 충북대학교 산업인공지능학과 중간 프로젝트
# 주제: 대한민국 광양 제철소 실제 전력 소비 데이터 시계열 예측
# ==========================================

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.linear_model import LinearRegression, Ridge, Lasso
from sklearn.metrics import mean_squared_error, r2_score

# 한글 폰트 설정
plt.rcParams['font.family'] = 'Malgun Gothic'
plt.rcParams['axes.unicode_minus'] = False

# ==========================================
# 1. 실제 산업 데이터 로드 (Real-world Data)
# ==========================================
print("광양 제철소 실측 전력 데이터를 불러옵니다...")
try:
    # UCI 머신러닝 저장소에서 다운로드한 실제 CSV 파일 로드
    df = pd.read_csv('Steel_industry_data.csv')
except FileNotFoundError:
    print("\n[에러] 'Steel_industry_data.csv' 파일이 없습니다.")
    print("UCI 저장소에서 다운로드하여 스크립트와 같은 폴더에 넣어주세요.")
    exit()

# 불필요한 날짜 문자열 컬럼 임시 제외 (분석의 편의성을 위함)
# 실제 전력량: 'Usage_kWh' / 주요 센서: 'Lagging_Current_Reactive.Power_kVarh', 'CO2(tCO2)' 등
df.rename(columns={'Usage_kWh': 'Power_Usage', 'CO2(tCO2)': 'CO2_Emission'}, inplace=True)

# ==========================================
# 2. ★ 시계열 피처 엔지니어링 (Time-Series Feature Engineering) ★
# ==========================================
print("시계열 피처(Lag, 이동평균)를 추출합니다...")

# (1) 과거 데이터 피처링 (Shift & Rolling) -> 15분 단위 데이터
df['Power_Lag_1'] = df['Power_Usage'].shift(1)  # 15분 전 전력 사용량
df['Power_Lag_4'] = df['Power_Usage'].shift(4)  # 1시간 전 전력 사용량
df['Power_Lag_96'] = df['Power_Usage'].shift(96)  # 하루(24h) 전 동시간 전력 사용량
df['Moving_Avg_2h'] = df['Power_Usage'].rolling(window=8).mean()  # 최근 2시간 평균 추세

# (2) 범주형 데이터 원-핫 인코딩 (주중/주말 상태, 요일, 부하 유형)
df = pd.get_dummies(df, columns=['WeekStatus', 'Day_of_week', 'Load_Type'], drop_first=True)

# shift와 rolling으로 인해 발생한 초기 96행(하루치) 결측치 제거
df.dropna(inplace=True)

# 날짜 컬럼(date) 제외 및 X, y 분리
X = df.drop(['date', 'Power_Usage'], axis=1)
y = df['Power_Usage']

# ==========================================
# 3. 데이터 분할 및 스케일링
# ==========================================
# 시계열 데이터이므로 과거로 미래를 예측하기 위해 shuffle=False 필수!
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, shuffle=False)

# 수많은 센서의 단위(kWh, kVarh, tCO2 등)를 일치시킴
scaler = StandardScaler()
X_train_scaled = scaler.fit_transform(X_train)
X_test_scaled = scaler.transform(X_test)

# ==========================================
# 4. 모델 훈련 및 비교
# ==========================================
print("회귀 모델 학습 및 평가 중...")

models = {
    "Linear Regression": LinearRegression(),
    "Ridge (L2)": Ridge(alpha=10.0),
    "Lasso (L1)": Lasso(alpha=2.0)
}

results = {}
coefficients = {}
predictions = {}

for name, model in models.items():
    model.fit(X_train_scaled, y_train)
    y_pred = model.predict(X_test_scaled)
    predictions[name] = y_pred

    mse = mean_squared_error(y_test, y_pred)
    results[name] = {'RMSE': np.sqrt(mse), 'R2 Score': r2_score(y_test, y_pred)}
    coefficients[name] = model.coef_

print("\n=== 모델 성능 평가 결과 ===")
print(pd.DataFrame(results).T.round(4))

# ==========================================
# 5. 시각화 (시계열 흐름 & 가중치 비교)
# ==========================================
plt.figure(figsize=(16, 7))

# [그래프 1] 시계열 흐름 예측 결과 (테스트 데이터 최근 이틀치: 192 스텝)
plt.subplot(1, 2, 1)
plot_steps = 192
plt.plot(y_test.values[-plot_steps:], label='Actual Power Usage', color='black', linewidth=2)
plt.plot(predictions["Lasso (L1)"][-plot_steps:], label='Lasso Prediction', color='tomato', linestyle='--', linewidth=2)
plt.title('광양 제철소 실측 전력 수요 예측 (최근 이틀)', fontsize=15)
plt.xlabel('시간 스텝 (15분 단위)')
plt.ylabel('전력 사용량 (kWh)')
plt.legend()
plt.grid(True, alpha=0.3)

# [그래프 2] 상위 10개 핵심 가중치 비교
plt.subplot(1, 2, 2)
feature_names = X.columns
lasso_coef = np.abs(coefficients["Lasso (L1)"])
top_idx = np.argsort(lasso_coef)[::-1][:10]

x_idx = np.arange(len(top_idx))
width = 0.3

plt.bar(x_idx - width / 2, coefficients["Ridge (L2)"][top_idx], width, label='Ridge', color='royalblue')
plt.bar(x_idx + width / 2, coefficients["Lasso (L1)"][top_idx], width, label='Lasso', color='tomato')

plt.xticks(x_idx, feature_names[top_idx], rotation=45, ha='right')
plt.title('제철소 실측 데이터 핵심 피처 가중치 비교', fontsize=15)
plt.axhline(0, color='black', linewidth=1)
plt.legend()
plt.grid(True, alpha=0.3)

plt.tight_layout()
plt.show()