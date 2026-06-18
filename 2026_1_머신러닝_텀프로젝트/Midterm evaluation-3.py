# ==========================================
# 충북대학교 산업인공지능학과 중간 프로젝트 (고도화 버전)
# 주제: OAC(외기)와 BAY(순환기) 데이터 분리를 통한 내부 오염 누출 탐지 및
#       케미컬 필터 수명 예측(CBM) 결합 모델
# ==========================================

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.dates as mdates  # 날짜 표기 수정용 라이브러리 추가
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score

# 한글 폰트 및 마이너스 기호 깨짐 방지 (Windows 기준)
plt.rcParams['font.family'] = 'Malgun Gothic'
plt.rcParams['axes.unicode_minus'] = False


def safe_load_csv(filepath):
    """이종 시스템의 다양한 인코딩을 안전하게 로드하는 함수"""
    encodings = ['utf-8', 'cp949', 'euc-kr', 'utf-8-sig']
    for enc in encodings:
        try:
            return pd.read_csv(filepath, encoding=enc)
        except UnicodeDecodeError:
            continue
    return pd.read_csv(filepath, encoding='utf-8', encoding_errors='ignore')


print("1. 실측 데이터를 불러오고 도메인 기반으로 분류합니다...")
try:
    raw_df = safe_load_csv('Raw Data.csv')
    raw_df['START_TIME'] = pd.to_datetime(raw_df['START_TIME'], format='mixed')

    action_df = safe_load_csv('Action History.csv')
    action_df['TIMESTAMP'] = pd.to_datetime(action_df['TIMESTAMP'], format='mixed')
except FileNotFoundError:
    print("[에러] 'Raw Data.csv' 또는 'Action History.csv' 파일이 없습니다.")
    exit()

# ==========================================
# [Step 1] Use Case 3: OAC(외기) vs BAY(내부 공정) 데이터 분리
# ==========================================
ion_cols = ['NO3', 'SO4', 'NH4', 'BR', 'CL', 'F', 'PO4', 'NO2', 'O3']

# 1-1. OAC(외기) 데이터 일 단위 평균 추출
oac_df = raw_df[raw_df['AREA'] == 'OAC'].copy()
oac_daily = oac_df.set_index('START_TIME')[ion_cols].resample('1D').mean().interpolate(method='linear')

# 1-2. 실제 공정(BAY) 데이터 추출
fab_df = raw_df[raw_df['AREA'] != 'OAC'].copy()
target_bay = fab_df['BAY'].mode()[0]
print(f"-> 분석 대상 공정(BAY): {target_bay}")

bay_daily = fab_df[fab_df['BAY'] == target_bay].set_index('START_TIME')[ion_cols].resample('1D').mean().interpolate(
    method='linear')

# 1-3. 데이터 병합 및 '설비 자체 발생(Internal Generation)' 피처 창조
combined_df = pd.DataFrame(index=bay_daily.index)

for col in ion_cols:
    combined_df[f'{col}_BAY'] = bay_daily[col]  # 내부 순환기 농도
    combined_df[f'{col}_OAC'] = oac_daily[col]  # 외기 농도
    # (내부 농도 - 외부 농도)를 계산 (음수는 외부 유입이므로 0 처리)
    combined_df[f'{col}_Internal_Gen'] = (combined_df[f'{col}_BAY'] - combined_df[f'{col}_OAC']).clip(lower=0)

# ==========================================
# [Step 2] Use Case 1: PM/필터 교체 타겟팅 및 피처링
# ==========================================
print("2. PM 이력을 추출하고 시계열 누적 피처를 생성합니다...")

filter_actions = action_df[
    (action_df['BAY'] == target_bay) &
    (action_df['JOB'].str.contains('교체|필터|Filter|change', na=False, case=False))
    ]

if len(filter_actions) < 5:
    print("   [안내] 명시적인 '필터 교체' 키워드 이력이 부족하여 해당 구역 전체 PM 이력을 타겟으로 사용합니다.")
    filter_actions = action_df[action_df['BAY'] == target_bay]

pm_dates = filter_actions['TIMESTAMP'].dt.floor('D').unique()
combined_df['Target_Action'] = np.where(combined_df.index.isin(pm_dates), 1, 0)

# 시계열 피처 추가 (3일 이동평균, 전날 누적량)
for col in ion_cols:
    combined_df[f'{col}_Gen_MA3'] = combined_df[f'{col}_Internal_Gen'].rolling(window=3).mean()
    combined_df[f'{col}_BAY_Lag1'] = combined_df[f'{col}_BAY'].shift(1)

combined_df.dropna(inplace=True)

# ==========================================
# [Step 3] AI 모델링 (L1 로지스틱 회귀를 통한 특징 선택)
# ==========================================
print("3. AI 모델 학습 및 킬러 이온 분석 중...")

drop_cols = ['Target_Action'] + [f'{col}_OAC' for col in ion_cols]
X = combined_df.drop(columns=drop_cols)
y = combined_df['Target_Action']

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, shuffle=False)

scaler = StandardScaler()
X_train_scaled = scaler.fit_transform(X_train)
X_test_scaled = scaler.transform(X_test)

# ★ 해결 포인트: 불균형 데이터를 위해 class_weight='balanced'가 들어간 L1 분류 모델 사용!
# 이를 통해 텅 빈 그래프 문제를 해결하고 정확한 킬러 이온 가중치를 도출합니다.
l1_model = LogisticRegression(penalty='l1', solver='liblinear', C=1.0, class_weight='balanced', random_state=42)
l1_model.fit(X_train_scaled, y_train)

y_pred = l1_model.predict(X_test_scaled)
print(f"-> 예방 정비(PM) 예측 정확도: {accuracy_score(y_test, y_pred):.3f}")

# ==========================================
# [Step 4] 결과 시각화 (발표 핵심 자료)
# ==========================================
plt.figure(figsize=(16, 7))

# --- [그래프 1] 외기(OAC) vs 내부(BAY) 농도 비교 ---
sample_ion = 'NH4' if 'NH4' in ion_cols else ion_cols[0]

ax1 = plt.subplot(1, 2, 1)
ax1.plot(combined_df.index, combined_df[f'{sample_ion}_OAC'], label='OAC (외기 유입 농도)', color='mediumseagreen',
         linestyle='--')
ax1.plot(combined_df.index, combined_df[f'{sample_ion}_BAY'], label='BAY (내부 순환 농도)', color='royalblue')

ax1.fill_between(combined_df.index, combined_df[f'{sample_ion}_OAC'], combined_df[f'{sample_ion}_BAY'],
                 where=(combined_df[f'{sample_ion}_BAY'] > combined_df[f'{sample_ion}_OAC']),
                 color='tomato', alpha=0.3, label='설비 자체 발생(누출) 의심 구간')

# ★ 해결 포인트: X축 날짜 표기 강제 수정 (YYYY-MM 형식)
ax1.xaxis.set_major_formatter(mdates.DateFormatter('%Y-%m'))
plt.xticks(rotation=45)

plt.title(f'외기 vs 내부 농도 비교를 통한 설비 자체 누출 탐지 ({sample_ion})', fontsize=14)
plt.ylabel('이온 농도')
plt.legend(loc='upper right')
plt.grid(True, alpha=0.3)

# --- [그래프 2] L1 정규화 기반 킬러 이온 가중치 분석 ---
ax2 = plt.subplot(1, 2, 2)

# 로지스틱 회귀의 계수 추출 (2차원 배열이므로 [0] 인덱스 사용)
coef_abs = np.abs(l1_model.coef_[0])
top_n = 10
top_indices = np.argsort(coef_abs)[::-1][:top_n]
top_features = X.columns[top_indices]
top_coefs = l1_model.coef_[0][top_indices]

x_pos = np.arange(len(top_features))
colors = ['tomato' if c > 0 else 'royalblue' for c in top_coefs]

ax2.bar(x_pos, top_coefs, color=colors)
plt.xticks(x_pos, top_features, rotation=45, ha='right')
plt.axhline(0, color='black', linewidth=1)
plt.title("장비 점검(PM) 유발 핵심 킬러 이온 가중치 (L1 정규화)", fontsize=14)
plt.ylabel("영향력 (Coefficient)")
plt.grid(True, alpha=0.3)

plt.tight_layout()
plt.show()