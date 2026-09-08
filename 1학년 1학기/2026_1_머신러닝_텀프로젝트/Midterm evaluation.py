# ==========================================
# 충북대학교 산업인공지능학과 중간 프로젝트
# 주제: 반도체 Fab 환경 이온(AMC) 데이터 분석 및 PM(예방정비) 예측
# 핵심: 다변량 이온 데이터 병합, Lasso 특징 선택, 시계열 피처 엔지니어링
# ==========================================

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.linear_model import LogisticRegression, Lasso
from sklearn.metrics import accuracy_score, classification_report

# 한글 폰트 및 마이너스 기호 깨짐 방지
plt.rcParams['font.family'] = 'Malgun Gothic'
plt.rcParams['axes.unicode_minus'] = False

print("1. 데이터를 불러오고 병합(Merge)하는 중입니다...")


# [멘토의 팁] 여러 인코딩 방식을 자동으로 테스트하여 에러 없이 데이터를 로드하는 무적 함수
def safe_load_csv(filepath):
    encodings = ['utf-8', 'cp949', 'utf-8-sig', 'euc-kr']
    for enc in encodings:
        try:
            return pd.read_csv(filepath, encoding=enc)
        except UnicodeDecodeError:
            continue
    # 모든 인코딩이 실패할 경우, 에러를 무시하고 강제 로드
    return pd.read_csv(filepath, encoding='utf-8', encoding_errors='ignore')


try:
    # 데이터 로드 (자동 인코딩 감지 함수 적용 및 혼합 날짜 포맷 자동 인식)
    raw_df = safe_load_csv('Raw Data.csv')
    raw_df['START_TIME'] = pd.to_datetime(raw_df['START_TIME'], format='mixed')

    action_df = safe_load_csv('Action History.csv')
    action_df['TIMESTAMP'] = pd.to_datetime(action_df['TIMESTAMP'], format='mixed')
except FileNotFoundError:
    print("[에러] 'Raw Data.csv' 또는 'Action History.csv' 파일이 없습니다. 코드가 있는 폴더에 넣어주세요.")
    exit()

# --- [전처리 1] 데이터 클렌징 및 일(Day) 단위 병합 ---
# 분석의 단순화를 위해 특정 층(예: F4 2F)과 구역(예: ThinFilm)의 특정 베이(BAY)를 하나 지정하여 샘플 분석 수행
# 실제 논문/프로젝트에서는 전체 데이터로 확장 가능
target_bay = raw_df['BAY'].mode()[0]  # 가장 데이터가 많은 BAY 자동 선택
print(f"분석 대상 위치(BAY): {target_bay}")

# 타겟 구역의 농도 데이터만 필터링 및 일(Day) 단위 평균 계산
raw_sub = raw_df[raw_df['BAY'] == target_bay].copy()
raw_sub.set_index('START_TIME', inplace=True)
# 이온 농도 데이터 (NO3, SO4, NH4, BR, CL, F, PO4, NO2, O3)
ion_cols = ['NO3', 'SO4', 'NH4', 'BR', 'CL', 'F', 'PO4', 'NO2', 'O3']
# 일 단위로 다운샘플링(평균) 및 결측치 선형 보간 처리
daily_ions = raw_sub[ion_cols].resample('1D').mean().interpolate(method='linear')

# 타겟 구역의 액션(PM) 데이터 필터링
action_sub = action_df[action_df['BAY'] == target_bay].copy()
action_sub['Date'] = action_sub['TIMESTAMP'].dt.floor('D')
# 해당 날짜에 PM이 수행되었는지 여부 (1: 수행, 0: 미수행)
pm_dates = action_sub['Date'].unique()

# 데이터 융합: 이온 농도 데이터프레임에 타겟 변수(PM_Action) 추가
daily_ions['PM_Action'] = 0
daily_ions.loc[daily_ions.index.isin(pm_dates), 'PM_Action'] = 1

# 결측치 최종 정리
daily_ions.dropna(inplace=True)
print(f"병합 완료: 총 {len(daily_ions)}일(Days) 치 데이터 준비 완료")

# --- [전처리 2] 시계열 피처 엔지니어링 (Time-Series Features) ---
print("2. 시계열 피처(Lag, 이동평균)를 생성합니다...")
# 과거의 이온 축적량이 PM 결정에 영향을 미치므로 파생 변수 생성
for col in ion_cols:
    daily_ions[f'{col}_Lag_1d'] = daily_ions[col].shift(1)  # 전날 농도
    daily_ions[f'{col}_MA_3d'] = daily_ions[col].rolling(window=3).mean()  # 최근 3일 이동 평균

daily_ions.dropna(inplace=True)

# 독립 변수(X)와 종속 변수(y: PM 수행 여부) 분리
X = daily_ions.drop('PM_Action', axis=1)
y = daily_ions['PM_Action']

# --- [전처리 3] 데이터 분할 및 스케일링 ---
# 시계열 데이터이므로 과거로 미래를 예측 (shuffle=False)
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, shuffle=False)

scaler = StandardScaler()
X_train_scaled = scaler.fit_transform(X_train)
X_test_scaled = scaler.transform(X_test)

print("3. 모델 학습 및 핵심 이온(Lasso) 선별 중...")

# --- [모델링 1] Lasso를 이용한 수율 저하 핵심 이온(Feature Selection) 찾기 ---
# PM 액션(분류 문제)이지만, 어떤 이온이 가장 큰 영향을 주는지 회귀 계수(가중치)로 파악하기 위해 Lasso 적용
lasso_model = Lasso(alpha=0.05, random_state=42)  # alpha 값으로 피처 압축 강도 조절
lasso_model.fit(X_train_scaled, y_train)

# --- [모델링 2] PM 시점 예측을 위한 로지스틱 회귀 (분류) ---
# Y값이 0과 1이므로 회귀 대신 분류 알고리즘 적용
log_model = LogisticRegression(class_weight='balanced', random_state=42)
log_model.fit(X_train_scaled, y_train)
y_pred = log_model.predict(X_test_scaled)

print("\n=== PM 예측 모델 (로지스틱 회귀) 성능 ===")
print(f"정확도(Accuracy): {accuracy_score(y_test, y_pred):.3f}")
# print(classification_report(y_test, y_pred)) # 상세 지표가 필요할 경우 주석 해제

# --- [시각화] 결과 해석 ---
plt.figure(figsize=(16, 7))

# [그래프 1] Lasso 가중치 비교 (어떤 이온이 PM을 유발하는가?)
plt.subplot(1, 2, 1)
feature_names = X.columns
lasso_coef = np.abs(lasso_model.coef_)
# 영향력이 큰 상위 10개 피처만 추출
top_idx = np.argsort(lasso_coef)[::-1][:10]

x_idx = np.arange(len(top_idx))
plt.bar(x_idx, lasso_model.coef_[top_idx], color='tomato', label='Lasso 가중치')
plt.xticks(x_idx, feature_names[top_idx], rotation=45, ha='right')
plt.title(f'Fab 이온 종류별 PM(예방정비) 유발 영향력 (Lasso)', fontsize=15)
plt.axhline(0, color='black', linewidth=1)
plt.ylabel('가중치 (Coefficient)')
plt.legend()
plt.grid(True, alpha=0.3)

# [그래프 2] 핵심 이온 농도 흐름과 실제 PM 시점 매칭
plt.subplot(1, 2, 2)
# Lasso에서 가장 가중치가 높았던 핵심 이온(1위) 찾기
top_feature = feature_names[top_idx[0]]
# 원본 이온 이름 추출 (예: 'NH4_MA_3d' -> 'NH4')
core_ion = top_feature.split('_')[0]

plt.plot(daily_ions.index, daily_ions[core_ion], color='royalblue', label=f'{core_ion} 농도 흐름')
# 실제 PM이 발생한 날짜에 빨간 점 찍기
pm_points = daily_ions[daily_ions['PM_Action'] == 1]
plt.scatter(pm_points.index, pm_points[core_ion], color='red', s=100, zorder=5, label='실제 PM 수행 (필터 교체)')

plt.title(f'핵심 이온({core_ion}) 농도 시계열 흐름 및 PM 발생 시점', fontsize=15)
plt.xlabel('측정 일자 (Date)')
plt.ylabel('이온 농도 (단위)')
plt.legend()
plt.grid(True, alpha=0.3)

plt.tight_layout()
plt.show()