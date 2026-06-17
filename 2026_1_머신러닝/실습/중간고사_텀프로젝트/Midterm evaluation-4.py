# ==========================================
# 충북대학교 산업인공지능학과 중간 프로젝트 (고도화 버전 2.0)
# 주제: OAC(외기) vs 내부 공정(BAY) 케미컬 필터 교체 예측 및 킬러 가스 도출
# 모델 평가 방식: Train 6 : Validation 2 : Test 2
# ==========================================

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
from sklearn.preprocessing import StandardScaler
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score, precision_score, recall_score

# 한글 폰트 및 마이너스 기호 깨짐 방지
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


print("1. 실측 데이터 로드 및 날짜(Date) 파싱 버그 수정 중...")
try:
    raw_df = safe_load_csv('Raw Data.csv')
    action_df = safe_load_csv('Action History.csv')

    # ★ 해결 1: '23/12/28'을 2028년으로 잘못 읽는 버그 수정 (%y/%m/%d 명시적 강제 적용)
    raw_df['START_TIME'] = pd.to_datetime(raw_df['START_TIME'].astype(str).str.strip(), format='%y/%m/%d %H:%M:%S',
                                          errors='coerce').fillna(
        pd.to_datetime(raw_df['START_TIME'].astype(str).str.strip(), format='mixed', errors='coerce')
    )

    action_df['TIMESTAMP'] = pd.to_datetime(action_df['TIMESTAMP'].astype(str).str.strip(), format='%Y/%m/%d %H:%M:%S',
                                            errors='coerce').fillna(
        pd.to_datetime(action_df['TIMESTAMP'].astype(str).str.strip(), format='mixed', errors='coerce')
    )
except FileNotFoundError:
    print("[에러] 'Raw Data.csv' 또는 'Action History.csv' 파일이 없습니다.")
    exit()

# ==========================================
# [Step 1] OAC(외기) vs BAY(내부 공정) 데이터 분리 및 파생 변수
# ==========================================
ion_cols = ['NO3', 'SO4', 'NH4', 'BR', 'CL', 'F', 'PO4', 'NO2', 'O3']

oac_df = raw_df[raw_df['AREA'] == 'OAC'].copy()
oac_daily = oac_df.set_index('START_TIME')[ion_cols].resample('1D').mean().interpolate(method='linear')

fab_df = raw_df[raw_df['AREA'] != 'OAC'].copy()

# ==========================================
# [Step 2] ★ 타겟팅 변경: 측정기 PM이 아닌 "케미컬 필터 교체" 명확화
# ==========================================
print("2. '케미컬 필터 교체' 이력 탐색 및 타겟(Y) 매핑 중...")
action_df['JOB'] = action_df['JOB'].fillna('')
action_df['COMMENT'] = action_df['COMMENT'].fillna('')

# 측정설비 PM을 제외하고 '교체', '필터', 'Filter', '케미컬' 관련 이력만 엄격하게 필터링
filter_keywords = '교체|필터|케미컬|filter|change'
filter_mask = action_df['JOB'].str.contains(filter_keywords, case=False) | action_df['COMMENT'].str.contains(
    filter_keywords, case=False)
filter_actions = action_df[filter_mask]

if len(filter_actions) > 0:
    target_bay = filter_actions['BAY'].mode()[0]
    print(f"-> 케미컬 필터 교체 이력이 가장 많은 공정(BAY) 선정: {target_bay}")
else:
    # 예외 처리: 데이터에 '교체' 단어가 전혀 없을 경우 시뮬레이션 모드 전환
    target_bay = fab_df['BAY'].mode()[0]
    print(f"-> [안내] 명시적인 '필터 교체' 단어가 없어, {target_bay} 구역의 고농도 누적 지점을 교체 시점으로 시뮬레이션 타겟팅합니다.")

bay_daily = fab_df[fab_df['BAY'] == target_bay].set_index('START_TIME')[ion_cols].resample('1D').mean().interpolate(
    method='linear')

# 데이터 병합 및 '설비 자체 발생(Internal Generation)' 피처 생성
combined_df = pd.DataFrame(index=bay_daily.index)
for col in ion_cols:
    combined_df[f'{col}_BAY'] = bay_daily[col]  # 내부 순환기 농도
    combined_df[f'{col}_OAC'] = oac_daily[col]  # 외기 농도
    # (내부 농도 - 외부 농도)를 계산하여 내부 설비 누출 가스 추정
    combined_df[f'{col}_Internal_Gen'] = (combined_df[f'{col}_BAY'] - combined_df[f'{col}_OAC']).clip(lower=0)

# 타겟(Y) 생성
if len(filter_actions) > 0:
    pm_dates = filter_actions['TIMESTAMP'].dt.floor('D').unique()
    combined_df['Filter_Replace'] = np.where(combined_df.index.isin(pm_dates), 1, 0)
else:
    # 시뮬레이션 타겟: 내부 누적 농도 상위 3% 날짜를 '가상의 필터 교체일'로 라벨링
    threshold = combined_df[[f'{c}_BAY' for c in ion_cols]].sum(axis=1).quantile(0.97)
    combined_df['Filter_Replace'] = np.where(combined_df[[f'{c}_BAY' for c in ion_cols]].sum(axis=1) >= threshold, 1, 0)

# 시계열 누적 피처 생성 (과거 3일 이동평균)
for col in ion_cols:
    combined_df[f'{col}_Gen_MA3'] = combined_df[f'{col}_Internal_Gen'].rolling(window=3).mean()
    combined_df[f'{col}_OAC_MA3'] = combined_df[f'{col}_OAC'].rolling(window=3).mean()

combined_df.dropna(inplace=True)

# ==========================================
# [Step 3] 데이터 분할 (Train 6 : Validation 2 : Test 2)
# ==========================================
print("3. 모델 학습 (Train 60% / Val 20% / Test 20%) 및 킬러 가스 분석...")

drop_cols = ['Filter_Replace'] + [f'{col}_BAY' for col in ion_cols]  # 내부 원본 제거, 파생 변수(OAC/Gen)만 사용
X = combined_df.drop(columns=drop_cols)
y = combined_df['Filter_Replace']

# 시계열 순서 유지(shuffle=False) 분할
n_total = len(X)
train_end = int(n_total * 0.6)
val_end = int(n_total * 0.8)

X_train, y_train = X.iloc[:train_end], y.iloc[:train_end]
X_val, y_val = X.iloc[train_end:val_end], y.iloc[train_end:val_end]
X_test, y_test = X.iloc[val_end:], y.iloc[val_end:]

scaler = StandardScaler()
X_train_scaled = scaler.fit_transform(X_train)
X_val_scaled = scaler.transform(X_val)
X_test_scaled = scaler.transform(X_test)

# ★ 해결 2: 텅 빈 Lasso 그래프 방지 (C값 조정 및 balanced 클래스 가중치)
# C값이 클수록(예: 5.0) 규제가 약해져 유의미한 가스들이 0이 되지 않고 살아남습니다.
l1_model = LogisticRegression(penalty='l1', solver='liblinear', C=5.0, class_weight='balanced', random_state=42)

# 학습(Train) 및 검토(Validation)
l1_model.fit(X_train_scaled, y_train)
y_val_pred = l1_model.predict(X_val_scaled)
print(f"-> [검토(Validation)] 단계 교체 예측 정확도: {accuracy_score(y_val, y_val_pred):.3f}")

# 평가(Test)
y_test_pred = l1_model.predict(X_test_scaled)
print(f"-> [평가(Test)] 단계 최종 케미컬 필터 교체 예측 정확도: {accuracy_score(y_test, y_test_pred):.3f}")

# ==========================================
# [Step 4] 결과 시각화
# ==========================================
plt.figure(figsize=(16, 7))

# --- [그래프 1] 외기(OAC) vs 내부(BAY) 농도 시계열 ---
# 가중치가 가장 높은 이온을 자동으로 선택하여 보여줌
top_feature_idx = np.argmax(np.abs(l1_model.coef_[0]))
best_gas = X.columns[top_feature_idx].split('_')[0]

ax1 = plt.subplot(1, 2, 1)
ax1.plot(combined_df.index, combined_df[f'{best_gas}_OAC'], label=f'OAC (외기 유입 {best_gas})', color='mediumseagreen',
         linestyle='--')
ax1.plot(combined_df.index, combined_df[f'{best_gas}_BAY'], label=f'BAY (순환기 {best_gas})', color='royalblue')

ax1.fill_between(combined_df.index, combined_df[f'{best_gas}_OAC'], combined_df[f'{best_gas}_BAY'],
                 where=(combined_df[f'{best_gas}_BAY'] > combined_df[f'{best_gas}_OAC']),
                 color='tomato', alpha=0.3, label='설비 내부 누출(Internal Gen)')

# ★ 해결 1: 연도가 2032년으로 튀는 현상 완벽 방어 (Y-m 형식 강제)
ax1.xaxis.set_major_formatter(mdates.DateFormatter('%Y-%m'))
plt.xticks(rotation=45)

plt.title(f'외기 vs 공조기 농도 비교 ({best_gas} 가스 누출 탐지)', fontsize=14)
plt.ylabel('이온 농도 (ppb)')
plt.legend(loc='upper right')
plt.grid(True, alpha=0.3)

# --- [그래프 2] 필터 교체 유발 '킬러 가스' 가중치 (L1 모델) ---
ax2 = plt.subplot(1, 2, 2)
coef_abs = np.abs(l1_model.coef_[0])
top_n = 10
top_indices = np.argsort(coef_abs)[::-1][:top_n]
top_features = X.columns[top_indices]
top_coefs = l1_model.coef_[0][top_indices]

x_pos = np.arange(len(top_features))
colors = ['tomato' if 'Gen' in feat else 'mediumseagreen' for feat in top_features]

ax2.bar(x_pos, top_coefs, color=colors)
plt.xticks(x_pos, top_features, rotation=45, ha='right')
plt.axhline(0, color='black', linewidth=1)

# 범례 추가 (색상 의미)
import matplotlib.patches as mpatches

red_patch = mpatches.Patch(color='tomato', label='내부 설비 누출 가스 (Internal)')
green_patch = mpatches.Patch(color='mediumseagreen', label='외부 유입 가스 (OAC)')
plt.legend(handles=[red_patch, green_patch])

plt.title("케미컬 필터 교체를 유발하는 '킬러 가스' 영향력 (L1 정규화)", fontsize=14)
plt.ylabel("가중치 (Coefficient)")
plt.grid(True, alpha=0.3)

plt.tight_layout()
plt.show()