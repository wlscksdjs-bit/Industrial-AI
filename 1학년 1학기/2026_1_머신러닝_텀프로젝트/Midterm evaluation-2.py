# ==========================================
# 충북대학교 산업인공지능학과 중간 프로젝트 (고도화 버전)
# 주제: OAC(외기)와 BAY(순환기) 데이터 분리를 통한 내부 오염 누출 탐지 및
#       케미컬 필터 수명 예측(CBM) 결합 모델
# ==========================================

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.linear_model import LogisticRegression, Lasso
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

# 1-2. 실제 공정(BAY) 데이터 추출 (데이터가 가장 많은 타겟 공정 1개 선정)
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

    # ★ 핵심 도메인 지식: 내부 농도가 외부 농도보다 높다면, 이는 설비 내부 배관 누출/발생을 의미함
    # (내부 농도 - 외부 농도)를 계산하되, 음수(외부 유입이 더 큰 경우)는 0으로 클리핑
    combined_df[f'{col}_Internal_Gen'] = (combined_df[f'{col}_BAY'] - combined_df[f'{col}_OAC']).clip(lower=0)

# ==========================================
# [Step 2] Use Case 1: 케미컬 필터 교체(CBM) 타겟팅 및 피처링
# ==========================================
print("2. 필터 교체 이력을 추출하고 시계열 누적 피처를 생성합니다...")

# 2-1. 측정기 PM이 아닌 '케미컬 필터 교체' 이력만 필터링
# (현업 기록 특성상 '교체', '필터', 'Filter' 등의 키워드를 포함하는 ROW 추출)
filter_actions = action_df[
    (action_df['BAY'] == target_bay) &
    (action_df['JOB'].str.contains('교체|필터|Filter|change', na=False, case=False))
    ]

# 만약 필터 교체 명시 이력이 부족할 경우, 전체 정비 이력으로 대체 (코드 안정성 확보)
if len(filter_actions) < 5:
    print("   [안내] 명시적인 '필터 교체' 키워드 이력이 부족하여 해당 구역 전체 PM 이력을 타겟으로 사용합니다.")
    filter_actions = action_df[action_df['BAY'] == target_bay]

pm_dates = filter_actions['TIMESTAMP'].dt.floor('D').unique()
combined_df['Filter_Replace'] = np.where(combined_df.index.isin(pm_dates), 1, 0)

# 2-2. 화학 물질 '누적(Accumulation)'을 모사하는 시계열 피처 추가
for col in ion_cols:
    # 설비 자체 발생량의 최근 3일 이동평균 (지속적 누출 감지)
    combined_df[f'{col}_Gen_MA3'] = combined_df[f'{col}_Internal_Gen'].rolling(window=3).mean()
    # 전체 내부 농도의 전날 누적량
    combined_df[f'{col}_BAY_Lag1'] = combined_df[f'{col}_BAY'].shift(1)

# 결측치 최종 제거
combined_df.dropna(inplace=True)

# ==========================================
# [Step 3] AI 모델링 (Lasso 특징 선택 및 로지스틱 예측)
# ==========================================
print("3. AI 모델 학습 및 킬러 이온 분석 중...")

# 예측에 불필요한 OAC 원본 데이터는 독립변수에서 제외 (내부 농도와 자체 발생량만으로 필터 수명 예측)
drop_cols = ['Filter_Replace'] + [f'{col}_OAC' for col in ion_cols]
X = combined_df.drop(columns=drop_cols)
y = combined_df['Filter_Replace']

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, shuffle=False)

scaler = StandardScaler()
X_train_scaled = scaler.fit_transform(X_train)
X_test_scaled = scaler.transform(X_test)

# Lasso (L1) 모델: 필터 교체를 유발하는 '진짜' 킬러 이온 색출
lasso = Lasso(alpha=0.05, random_state=42)
lasso.fit(X_train_scaled, y_train)

# 분류 성능 확인
clf = LogisticRegression(class_weight='balanced', random_state=42)
clf.fit(X_train_scaled, y_train)
y_pred = clf.predict(X_test_scaled)
print(f"-> 케미컬 필터 교체(PM) 예측 정확도: {accuracy_score(y_test, y_pred):.3f}")

# ==========================================
# [Step 4] 결과 시각화 (발표 핵심 자료)
# ==========================================
plt.figure(figsize=(16, 7))

# --- [그래프 1] Use Case 3: 외기(OAC) vs 내부(BAY) 농도 비교 (설비 자체 누출 탐지) ---
# 가장 평균 농도가 높은 이온 하나를 선택하여 시각화 (예: F 또는 NH4)
sample_ion = 'F' if 'F' in ion_cols else ion_cols[0]

plt.subplot(1, 2, 1)
plt.plot(combined_df.index, combined_df[f'{sample_ion}_OAC'], label='OAC (외기 유입 농도)', color='mediumseagreen',
         linestyle='--')
plt.plot(combined_df.index, combined_df[f'{sample_ion}_BAY'], label='BAY (내부 순환 농도)', color='royalblue')

# 내부 농도가 외부보다 비정상적으로 높은 '자체 누출(Internal Gen)' 영역을 빨간색으로 채움
plt.fill_between(combined_df.index, combined_df[f'{sample_ion}_OAC'], combined_df[f'{sample_ion}_BAY'],
                 where=(combined_df[f'{sample_ion}_BAY'] > combined_df[f'{sample_ion}_OAC']),
                 color='tomato', alpha=0.3, label='설비 자체 발생(누출) 의심 구간')

plt.title(f'외기 vs 내부 농도 비교를 통한 설비 자체 누출 탐지 ({sample_ion})', fontsize=14)
plt.ylabel('이온 농도')
plt.legend()
plt.grid(True, alpha=0.3)

# --- [그래프 2] Use Case 1: Lasso 기반 필터 교체 유발 '킬러 이온' 분석 ---
plt.subplot(1, 2, 2)
coef_abs = np.abs(lasso.coef_)
top_n = 10
top_indices = np.argsort(coef_abs)[::-1][:top_n]
top_features = X.columns[top_indices]
top_coefs = lasso.coef_[top_indices]

x_pos = np.arange(len(top_features))
colors = ['tomato' if c > 0 else 'royalblue' for c in top_coefs]

plt.bar(x_pos, top_coefs, color=colors)
plt.xticks(x_pos, top_features, rotation=45, ha='right')
plt.axhline(0, color='black', linewidth=1)
plt.title("케미컬 필터 수명 단축 킬러 이온 가중치 (Lasso Feature Selection)", fontsize=14)
plt.ylabel("영향력 (Lasso Coefficient)")
plt.grid(True, alpha=0.3)

plt.tight_layout()
plt.show()