# ==========================================
# 충북대학교 산업인공지능학과 중간 프로젝트
# 주제: 스마트 팩토리 CNC 가공 장비 센서 데이터를 활용한 품질 점수 예측 및 모델 최적화
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
# 1. 산업 데이터 생성 (Data Generation)
# - 실제 CNC 장비 센서 데이터를 모사하여 생성
# ==========================================
print("스마트 팩토리 센서 데이터를 생성합니다...")
np.random.seed(42)
n_samples = 2000  # 2000개의 가공 데이터

# (1) 유의미한 핵심 센서 데이터 (품질에 직접적 영향을 미침)
temp = np.random.normal(80, 10, n_samples)  # 장비 온도 (높을수록 품질 하락)
vibration = np.random.normal(5, 2, n_samples)  # 장비 진동 (높을수록 품질 크게 하락)
rpm = np.random.normal(3000, 300, n_samples)  # 스핀들 회전속도 (적절히 높을수록 품질 상승)
pressure = np.random.normal(120, 15, n_samples)  # 냉각수 압력 (높을수록 품질 상승)

# (2) 무의미한 노이즈 센서 데이터 (품질과 무관함)
room_humidity = np.random.normal(50, 10, n_samples)  # 공장 실내 습도
ambient_light = np.random.normal(300, 50, n_samples)  # 공장 실내 조도

# (3) 종속 변수(Target): 제품 품질 점수 (100점 만점 기준)
# 수학적 관계식: 기본 80점 - 온도영향 - 진동영향 + 속도영향 + 압력영향 + 약간의 랜덤 노이즈
quality_score = (
        80
        - 0.5 * (temp - 80)
        - 3.0 * (vibration - 5)
        + 0.02 * (rpm - 3000)
        + 0.3 * (pressure - 120)
        + np.random.normal(0, 2, n_samples)  # 알 수 없는 미세한 노이즈
)

# 데이터프레임 구축
df = pd.DataFrame({
    'Temperature_C': temp,
    'Vibration_mm_s': vibration,
    'Spindle_RPM': rpm,
    'Coolant_Pressure_bar': pressure,
    'Room_Humidity_%': room_humidity,
    'Ambient_Light_lux': ambient_light,
    'Quality_Score': quality_score
})

print("데이터 형태:", df.shape)

# ==========================================
# 2. 데이터 전처리 (Data Preprocessing)
# ==========================================
print("데이터 스케일링을 진행합니다...")

X = df.drop('Quality_Score', axis=1)
y = df['Quality_Score']

# 학습/테스트 분할 (8:2)
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# StandardScaler를 이용한 표준화 (단위가 모두 다르므로 필수)
scaler = StandardScaler()
X_train_scaled = scaler.fit_transform(X_train)
X_test_scaled = scaler.transform(X_test)

# ==========================================
# 3. 모델 훈련 및 비교 (Model Training)
# ==========================================
print("회귀 모델 학습 및 평가 중...")

models = {
    "Linear Regression (OLS)": LinearRegression(),
    "Ridge (L2 정규화)": Ridge(alpha=10.0),
    "Lasso (L1 정규화)": Lasso(alpha=1.0)  # Feature Selection을 명확히 보기 위해 alpha=1.0 설정
}

results = {}
coefficients = {}

for name, model in models.items():
    model.fit(X_train_scaled, y_train)
    y_pred = model.predict(X_test_scaled)

    mse = mean_squared_error(y_test, y_pred)
    rmse = np.sqrt(mse)
    r2 = r2_score(y_test, y_pred)

    results[name] = {'MSE': mse, 'RMSE': rmse, 'R2': r2}
    coefficients[name] = model.coef_

# 성능 결과 출력
print("\n=== 모델 성능 평가 결과 ===")
results_df = pd.DataFrame(results).T
print(results_df.round(4))

# ==========================================
# 4. 시각화 (Visualization) - 발표 핵심 자료
# ==========================================
plt.figure(figsize=(16, 7))

# [그래프 1] 실제 품질 점수 vs 예측 품질 점수 (Ridge 기준)
plt.subplot(1, 2, 1)
y_pred_ridge = models["Ridge (L2 정규화)"].predict(X_test_scaled)
plt.scatter(y_test, y_pred_ridge, alpha=0.5, color='teal')
plt.plot([y_test.min(), y_test.max()], [y_test.min(), y_test.max()], 'r--', lw=2)
plt.title('실제 제품 품질 vs 예측 품질 (Ridge 모델)', fontsize=15)
plt.xlabel('실제 품질 점수')
plt.ylabel('예측 품질 점수')
plt.grid(True, alpha=0.3)

# [그래프 2] 모델별 가중치(Coefficient) 비교 - Feature Selection 증명
plt.subplot(1, 2, 2)
feature_names = X.columns
x_idx = np.arange(len(feature_names))
width = 0.25

plt.bar(x_idx - width, coefficients["Linear Regression (OLS)"], width, label='OLS', color='lightgray')
plt.bar(x_idx, coefficients["Ridge (L2 정규화)"], width, label='Ridge (L2)', color='royalblue')
plt.bar(x_idx + width, coefficients["Lasso (L1 정규화)"], width, label='Lasso (L1)', color='tomato')

plt.xticks(x_idx, feature_names, rotation=30, ha='right')
plt.title('센서 데이터별 품질 영향력(가중치) 비교', fontsize=15)
plt.xlabel('센서 종류 (Features)')
plt.ylabel('가중치 (Coefficient Value)')
plt.axhline(0, color='black', linewidth=1)
plt.legend()
plt.grid(True, alpha=0.3)

plt.tight_layout()
plt.show()