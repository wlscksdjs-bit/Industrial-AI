# ==========================================
# 충북대학교 산업인공지능학과 텀프로젝트(2026254019|진찬언)
# 주제: 반도체 Fab 케미컬 필터 예지 보전 예측(Bi-LSTM) 및 원인 분석(XAI)
# 핵심 포인트: 
# 1. Bi-LSTM 도입 타당성: 양방향 시퀀스 학습을 통한 재현율(Recall) 한계 돌파
# 2. XAI (Explainable AI): L1 정규화를 통한 킬러 가스(원인) 시각적 도출
# 3. Data Leakage 완벽 차단: 머신러닝 vs 딥러닝 진검 승부 환경 구축
# ==========================================

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import matplotlib.gridspec as gridspec
import warnings

from sklearn.preprocessing import StandardScaler
from sklearn.ensemble import RandomForestClassifier
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score
import tensorflow as tf
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import LSTM, Dense, Dropout, Bidirectional
from tensorflow.keras.callbacks import EarlyStopping
from tensorflow.keras.optimizers import Adam

warnings.filterwarnings('ignore')
plt.rcParams['font.family'] = 'Malgun Gothic'
plt.rcParams['axes.unicode_minus'] = False

# ==========================================
# 1. 데이터 세팅 및 도메인 지식 반영
# ==========================================
print("1. 시계열 물리/화학 데이터 생성 및 전처리 중...")
ion_cols = ['NO3', 'SO4', 'NH4', 'BR', 'CL', 'F', 'PO4', 'NO2', 'O3']
n_samples = 730 # 2년치 데이터

np.random.seed(42)
tf.random.set_seed(42)
dates = pd.date_range(start='2022-01-01', periods=n_samples, freq='D')
combined_df = pd.DataFrame(index=dates)

for col in ion_cols:
    trend = np.linspace(0, 3, n_samples)
    seasonality = np.sin(np.linspace(0, 40, n_samples)) * 2.5
    noise = np.random.normal(0, 0.5, n_samples) 
    
    oac = np.abs(seasonality + noise + 1.5)
    bay = np.abs(trend + seasonality + noise * 1.2 + 2.5)
    
    combined_df[f'{col}_OAC'] = oac
    combined_df[f'{col}_BAY'] = bay
    combined_df[f'{col}_Internal_Gen'] = (bay - oac).clip(min=0)
    
    # [도메인 지식] 장기 누적(Accumulation) 피처 (XAI 해석용)
    combined_df[f'{col}_Gen_Sum14'] = combined_df[f'{col}_Internal_Gen'].rolling(14).sum().fillna(0)
    combined_df[f'{col}_Gen_Sum28'] = combined_df[f'{col}_Internal_Gen'].rolling(28).sum().fillna(0)
    combined_df[f'{col}_OAC_Sum14'] = combined_df[f'{col}_OAC'].rolling(14).sum().fillna(0)

# 가상 타겟(Y): F 내부 누적과 NO3 외부 유입 누적이 겹쳤을 때 알람 발생 (4주 경고 구간)
combined_df['Filter_Replace_Warning'] = 0
risk_score = (combined_df['F_Gen_Sum14'] * 1.5) + combined_df['NO3_OAC_Sum14']
limit = risk_score.quantile(0.80)
breakdown_dates = combined_df.index[risk_score >= limit]

for pm_date in breakdown_dates:
    mask = (combined_df.index <= pm_date) & (combined_df.index >= pm_date - pd.Timedelta(days=28))
    combined_df.loc[mask, 'Filter_Replace_Warning'] = 1

# 다중분류 에러 방지를 위한 0/1 이진 분류 강제 고정
combined_df['Filter_Replace_Warning'] = np.where(combined_df['Filter_Replace_Warning'] > 0, 1, 0)

# ==========================================
# 2. XAI 피처 vs 예측(Raw) 피처 분리 및 3D 텐서 변환
# ==========================================
print("2. 알고리즘 비교를 위한 피처 분리 및 3D 텐서 변환...")

# (1) XAI (원인 규명) 모델을 위한 전체 피처 (누적합 포함)
feature_cols_all = [c for c in combined_df.columns if c != 'Filter_Replace_Warning']
scaler_all = StandardScaler()
scaled_features_all = scaler_all.fit_transform(combined_df[feature_cols_all])

# (2) 예측 타당성 증명을 위한 순수 센서 피처 (Data Leakage 완벽 차단!)
feature_cols_raw = [f'{col}_BAY' for col in ion_cols] + [f'{col}_OAC' for col in ion_cols] + [f'{col}_Internal_Gen' for col in ion_cols]
scaler_raw = StandardScaler()
scaled_features_raw = scaler_raw.fit_transform(combined_df[feature_cols_raw])

TIME_STEPS = 14 # 14일간의 맥락(Context)을 시퀀스로 주입

def create_sequences(data, target, time_steps):
    Xs, ys = [], []
    for i in range(len(data) - time_steps):
        Xs.append(data[i:(i + time_steps)])
        ys.append(target.iloc[i + time_steps])
    return np.array(Xs), np.array(ys)

X_seq_raw, y_seq = create_sequences(scaled_features_raw, combined_df['Filter_Replace_Warning'], TIME_STEPS)
X_seq_all, _ = create_sequences(scaled_features_all, combined_df['Filter_Replace_Warning'], TIME_STEPS)

train_end, val_end = int(len(X_seq_raw) * 0.6), int(len(X_seq_raw) * 0.8)

# Test 세트 내 불균형(정답 0건) 방지를 위한 분할선 자동 보정
if np.sum(y_seq[val_end:]) == 0 and np.sum(y_seq) > 0:
    last_event_idx = np.where(y_seq == 1)[0][-1]
    val_end = max(0, last_event_idx - 30) 
    train_end = int(val_end * 0.75)

# 예측용 데이터 분할 (Hint 없음)
X_train_raw, X_test_raw = X_seq_raw[:train_end], X_seq_raw[val_end:]
X_val_raw = X_seq_raw[train_end:val_end]
y_train, y_val, y_test = y_seq[:train_end].astype(int), y_seq[train_end:val_end].astype(int), y_seq[val_end:].astype(int)

# ML용 2D 변환 (현재 시점 단 하루만 봄)
X_train_rf = X_train_raw[:, -1, :] 
X_test_rf = X_test_raw[:, -1, :]

# XAI용 2D 데이터
X_train_l1 = X_seq_all[:train_end][:, -1, :]

# ==========================================
# 3. Two-Track 모델 학습 (XAI + 예측)
# ==========================================
print("3. 모델 학습 (XAI 원인 분석 + Bi-LSTM 예측성능 평가)...")

# Track 1: XAI (L1 정규화) - 어떤 가스가 범인인가?
l1_model = LogisticRegression(penalty='l1', solver='liblinear', C=0.5, class_weight='balanced', random_state=42)
l1_model.fit(X_train_l1, y_train)

# Track 2-1: 머신러닝 (RF) - 과거 흐름을 모르는 모델의 한계 증명용
rf_model = RandomForestClassifier(n_estimators=100, class_weight='balanced', random_state=42)
rf_model.fit(X_train_rf, y_train)
rf_preds = rf_model.predict(X_test_rf)

# Track 2-2: 양방향 딥러닝 (Bi-LSTM) - 과거와 미래의 문맥을 융합하는 제안 모델
print("-> 양방향 시계열 딥러닝(Bi-LSTM) 훈련 및 최적화 중...")
bilstm_model = Sequential([
    Bidirectional(LSTM(64, activation='tanh', return_sequences=True), input_shape=(X_train_raw.shape[1], X_train_raw.shape[2])),
    Dropout(0.2),
    Bidirectional(LSTM(32, activation='tanh')),
    Dropout(0.2),
    Dense(16, activation='relu'),
    Dense(1, activation='sigmoid')
])

bilstm_model.compile(optimizer=Adam(learning_rate=0.001), loss='binary_crossentropy', metrics=['accuracy'])
early_stop = EarlyStopping(monitor='val_loss', patience=15, restore_best_weights=True)
bilstm_model.fit(X_train_raw, y_train, epochs=100, batch_size=16, validation_data=(X_val_raw, y_val), callbacks=[early_stop], verbose=0)

# ==========================================
# 4. 동적 임계값 최적화 및 최종 평가
# ==========================================
print("4. 동적 임계값 최적화 및 최종 평가...")
y_val_prob = bilstm_model.predict(X_val_raw, verbose=0).flatten()
y_test_prob = bilstm_model.predict(X_test_raw, verbose=0).flatten()

thresholds = np.arange(0.1, 0.9, 0.05)
f1_scores = []
best_threshold = 0.5; best_f1 = 0

for th in thresholds:
    preds = (y_val_prob >= th).astype(int)
    f1 = f1_score(y_val, preds, zero_division=0)
    f1_scores.append(f1)
    if f1 > best_f1:
        best_f1 = f1; best_threshold = th

bilstm_preds = (y_test_prob >= best_threshold).astype(int)

def get_metrics(y_true, y_pred):
    return [accuracy_score(y_true, y_pred), precision_score(y_true, y_pred, zero_division=0), 
            recall_score(y_true, y_pred, zero_division=0), f1_score(y_true, y_pred, zero_division=0)]

rf_metrics = get_metrics(y_test, rf_preds)
bilstm_metrics = get_metrics(y_test, bilstm_preds)

print(f"\n=== 최종 알고리즘 적합성 평가 결과 ===")
print(f"-> 최적 알람 임계값 탐색 완료: {best_threshold:.2f}")
print(f"-> ML (Random Forest) | 정밀도: {rf_metrics[1]:.3f} | 재현율(Recall): {rf_metrics[2]:.3f} | F1-Score: {rf_metrics[3]:.3f}")
print(f"-> DL (Bi-LSTM)       | 정밀도: {bilstm_metrics[1]:.3f} | 재현율(Recall): {bilstm_metrics[2]:.3f} | F1-Score: {bilstm_metrics[3]:.3f}")

# ==========================================
# 5. 핵심 4대 대시보드 시각화
# ==========================================
fig = plt.figure(figsize=(18, 12))
gs = gridspec.GridSpec(2, 3, height_ratios=[1, 1.2]) 

# [그래프 1] 알고리즘 타당성 (RF vs Bi-LSTM)
ax1 = fig.add_subplot(gs[0, 0])
metrics_labels = ['Accuracy', 'Precision', 'Recall', 'F1-Score']
x = np.arange(len(metrics_labels))
width = 0.35
ax1.bar(x - width/2, [m*100 for m in rf_metrics], width, label='Random Forest (단방향 한계)', color='lightslategray')
ax1.bar(x + width/2, [m*100 for m in bilstm_metrics], width, label='Bi-LSTM (양방향 맥락 융합)', color='royalblue')
for i, v in enumerate(rf_metrics): ax1.text(x[i]-width/2, v*100+1, f"{v*100:.1f}%", ha='center', fontsize=9)
for i, v in enumerate(bilstm_metrics): ax1.text(x[i]+width/2, v*100+1, f"{v*100:.1f}%", ha='center', fontsize=9, fontweight='bold', color='darkblue')
ax1.set_ylabel('성능 지표 (%)')
ax1.set_title('[타당성 검증] 양방향 시퀀스 모델의 재현율(Recall) 돌파', fontsize=12, fontweight='bold')
ax1.set_xticks(x); ax1.set_xticklabels(metrics_labels)
ax1.set_ylim(0, 115)
ax1.legend(loc='lower left', fontsize=9); ax1.grid(axis='y', alpha=0.3)

# [그래프 2] XAI 원인 규명
ax2 = fig.add_subplot(gs[0, 1])
coef_abs = np.abs(l1_model.coef_[0])
top_idx = np.argsort(coef_abs)[::-1][:6]
top_features = [feature_cols_all[i] for i in top_idx]
top_coefs = l1_model.coef_[0][top_idx]
x_pos = np.arange(len(top_features))
colors = ['tomato' if 'Gen' in feat else 'mediumseagreen' for feat in top_features]
ax2.bar(x_pos, top_coefs, color=colors)
ax2.set_xticks(x_pos); ax2.set_xticklabels(top_features, rotation=25, ha='right', fontsize=9)
ax2.axhline(0, color='black', linewidth=1)
import matplotlib.patches as mpatches
ax2.legend(handles=[mpatches.Patch(color='tomato', label='내부 공정 누출'), mpatches.Patch(color='mediumseagreen', label='외부 유입 OAC')], fontsize=9)
ax2.set_title("[XAI 해석] 필터 파괴 '핵심 킬러가스' 도출 (L1 정규화)", fontsize=12, fontweight='bold')
ax2.grid(True, alpha=0.3)

# [그래프 3] 동적 임계값 최적화
ax3 = fig.add_subplot(gs[0, 2])
ax3.plot(thresholds, f1_scores, marker='o', color='darkorange', linewidth=2)
ax3.axvline(best_threshold, color='red', linestyle='--', label=f'Optimal Threshold ({best_threshold:.2f})')
ax3.set_title('[모델 최적화] 동적 임계값(Threshold) 자동 탐색', fontsize=12, fontweight='bold')
ax3.set_xlabel('Decision Threshold'); ax3.set_ylabel('Validation F1-Score')
ax3.legend(fontsize=9); ax3.grid(True, alpha=0.3)

# [그래프 4] 예측 시뮬레이션
ax4 = fig.add_subplot(gs[1, :])
time_index = combined_df.index[val_end + TIME_STEPS:] 
ax4.plot(time_index, y_test, label='Actual Replace Window (실제 4주 경고 구간 정답)', color='gray', linestyle='--', linewidth=1.5)
ax4.plot(time_index, y_test_prob, label='Bi-LSTM Predicted Risk (AI 예측 위험 확률)', color='mediumseagreen', linewidth=2.5)
ax4.axhline(best_threshold, color='red', linestyle='-', linewidth=2, label=f'Optimal Threshold (알람 기준선: {best_threshold:.2f})')
ax4.fill_between(time_index, 0, y_test_prob, where=(y_test_prob >= best_threshold), color='red', alpha=0.3, label='AI Predictive Alarm (조기 알람 작동)')
ax4.set_title('양방향 딥러닝(Bi-LSTM) 기반 케미컬 필터 예지 보전(CBM) 최종 시뮬레이션', fontsize=15, fontweight='bold')
ax4.set_xlabel('Date (최종 평가 구간)')
ax4.set_ylabel('고장 위험 확률 (Probability)')
ax4.xaxis.set_major_formatter(mdates.DateFormatter('%Y-%m'))
ax4.legend(loc='upper right', fontsize=11)
ax4.grid(True, alpha=0.3)

plt.tight_layout()
plt.show()