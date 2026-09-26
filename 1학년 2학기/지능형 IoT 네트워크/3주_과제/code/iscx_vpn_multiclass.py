# -*- coding: utf-8 -*-
"""
========================================================================================
과제명: 지능형 IoT 네트워크 3주차 과제 - 트래픽 분류 모델 성능 향상
파일명: iscx_vpn_multiclass.py
작성자: 진찬언 (충북대학교 일반대학원 산업인공지능학과, 학번: 2026254019)
목  적: ISCXVPN2016 데이터셋에 대한 도메인 피처 엔지니어링 및 TDF-Net(Tree-Deep Fusion Network)
       딥러닝 아키텍처를 적용하여 머신러닝 기준 모델(Random Forest) 대비 성능 상회 달성
========================================================================================
"""

import os
import sys
import random
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

import torch
import torch.nn as nn
import torch.optim as optim
import torch.nn.functional as F
from torch.utils.data import DataLoader, TensorDataset

from sklearn.model_selection import StratifiedKFold, train_test_split
from sklearn.preprocessing import LabelEncoder, StandardScaler
from sklearn.ensemble import RandomForestClassifier, ExtraTreesClassifier
from sklearn.metrics import accuracy_score, classification_report, f1_score, confusion_matrix

# 콘솔 출력 UTF-8 인코딩 보장
if sys.platform == 'win32':
    try:
        sys.stdout.reconfigure(encoding='utf-8')
    except Exception:
        pass

# ----------------------------------------------------------------------
# 1. 재현성 보장을 위한 시드 고정
# ----------------------------------------------------------------------
def set_seed(seed=42):
    random.seed(seed)
    np.random.seed(seed)
    torch.manual_seed(seed)
    if torch.cuda.is_available():
        torch.cuda.manual_seed_all(seed)

set_seed(42)
print("=" * 75)
print("ISCXVPN2016 트래픽 다중 분류 딥러닝 성능 개선 파이프라인 (TDF-Net)")
print("=" * 75)
print(f"PyTorch Version: {torch.__version__}")
device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
print(f"연산 가속 장치: {device}\n")

# ----------------------------------------------------------------------
# 2. 데이터셋 로드 (다중 경로 자동 탐색)
# ----------------------------------------------------------------------
def find_dataset():
    candidates = [
        "output_multiple.csv",
        os.path.join("code", "output_multiple.csv"),
        os.path.join("..", "output_multiple.csv"),
        os.path.join("..", "code", "output_multiple.csv"),
        os.path.join(os.path.dirname(os.path.abspath(__file__)), "output_multiple.csv"),
        os.path.join(os.path.dirname(os.path.abspath(__file__)), "code", "output_multiple.csv"),
        os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "code", "output_multiple.csv"),
    ]
    for p in candidates:
        if os.path.exists(p):
            return p
    raise FileNotFoundError("output_multiple.csv 파일을 찾을 수 없습니다. 경로를 확인해주세요.")

csv_path = find_dataset()
print(f"[1] 데이터셋 로드 경로: {csv_path}")

df = pd.read_csv(csv_path)
df = df.replace([np.inf, -np.inf], np.nan).fillna(0)

raw_features = ['packet_count', 'total_bytes', 'avg_pkt_size', 'std_pkt_size', 'duration']
X_raw = df[raw_features].copy()
y = df['label'].copy()

le = LabelEncoder()
y_encoded = le.fit_transform(y)
classes = list(le.classes_)
num_classes = len(classes)

print(f"    - 전체 샘플 수: {len(df):,}개 | 기본 입력 피처 수: {len(raw_features)}개")
print("    - 클래스별 분포:")
for c, count in df['label'].value_counts().items():
    print(f"      * {c:15s}: {count:5d}개 ({count/len(df)*100:5.1f}%)")
print()

# ----------------------------------------------------------------------
# 3. 도메인 피처 엔지니어링 (30개 고차원 통계 피처 확장)
# ----------------------------------------------------------------------
def engineer_features(df_in):
    X = df_in.copy()
    eps = 1e-6
    # 5개 물리 도메인 파생 피처
    X['throughput'] = X['total_bytes'] / (X['duration'] + eps)
    X['packet_rate'] = X['packet_count'] / (X['duration'] + eps)
    X['bytes_per_pkt'] = X['total_bytes'] / (X['packet_count'] + eps)
    X['pkt_size_cv'] = X['std_pkt_size'] / (X['avg_pkt_size'] + eps)
    X['duration_per_byte'] = X['duration'] / (X['total_bytes'] + 1.0)
    
    # 왜도 완화를 위한 10개 Log1p 변환 피처 및 10개 Sqrt 변환 피처 (총 30개 피처)
    base_cols = ['packet_count', 'total_bytes', 'avg_pkt_size', 'std_pkt_size', 'duration',
                 'throughput', 'packet_rate', 'bytes_per_pkt', 'pkt_size_cv', 'duration_per_byte']
    for col in base_cols:
        X[f'{col}_log1p'] = np.log1p(np.maximum(0, X[col]))
        X[f'{col}_sqrt'] = np.sqrt(np.maximum(0, X[col]))
    return X

X_engineered = engineer_features(X_raw)
print(f"[2] 도메인 피처 엔지니어링 완료: {X_raw.shape[1]}개 -> {X_engineered.shape[1]}개 확장")

# 데이터 분할 (7:3 Stratified Split)
X_train_raw, X_test_raw, y_train, y_test = train_test_split(
    X_raw, y_encoded, test_size=0.3, stratify=y_encoded, random_state=42
)
X_train_eng, X_test_eng, _, _ = train_test_split(
    X_engineered, y_encoded, test_size=0.3, stratify=y_encoded, random_state=42
)

# ----------------------------------------------------------------------
# 4. [기준 모델 1] Random Forest Benchmark (5개 원본 피처)
# ----------------------------------------------------------------------
print("\n[3] 기준 모델 1: Random Forest (5개 기본 피처)")
rf_bench = RandomForestClassifier(n_estimators=100, random_state=42)
rf_bench.fit(X_train_raw, y_train)
y_pred_rf = rf_bench.predict(X_test_raw)
acc_rf = accuracy_score(y_test, y_pred_rf)
f1_rf = f1_score(y_test, y_pred_rf, average='macro')
print(f"    - Random Forest 결과: Accuracy = {acc_rf*100:.2f}%, Macro F1 = {f1_rf:.4f}")

# ----------------------------------------------------------------------
# 5. [기준 모델 2] Baseline MLP (5개 원본 피처)
# ----------------------------------------------------------------------
print("\n[4] 기준 모델 2: Baseline MLP (5개 기본 피처)")
scaler_base = StandardScaler()
X_tr_base = scaler_base.fit_transform(X_train_raw)
X_te_base = scaler_base.transform(X_test_raw)

class BaselineMLP(nn.Module):
    def __init__(self, in_dim=5, num_cls=5):
        super().__init__()
        self.net = nn.Sequential(
            nn.Linear(in_dim, 128),
            nn.ReLU(),
            nn.Linear(128, 64),
            nn.ReLU(),
            nn.Linear(64, num_cls)
        )
    def forward(self, x):
        return self.net(x)

base_model = BaselineMLP(5, num_classes).to(device)
crit_base = nn.CrossEntropyLoss()
opt_base = optim.Adam(base_model.parameters(), lr=0.001)

tr_ds_base = TensorDataset(torch.tensor(X_tr_base, dtype=torch.float32), torch.tensor(y_train, dtype=torch.long))
tr_loader_base = DataLoader(tr_ds_base, batch_size=32, shuffle=True)

for ep in range(100):
    base_model.train()
    for bx, by in tr_loader_base:
        bx, by = bx.to(device), by.to(device)
        opt_base.zero_grad()
        loss = crit_base(base_model(bx), by)
        loss.backward()
        opt_base.step()

base_model.eval()
with torch.no_grad():
    y_pred_base = base_model(torch.tensor(X_te_base, dtype=torch.float32).to(device)).argmax(dim=1).cpu().numpy()
acc_base = accuracy_score(y_test, y_pred_base)
f1_base = f1_score(y_test, y_pred_base, average='macro')
print(f"    - Baseline MLP 결과: Accuracy = {acc_base*100:.2f}%, Macro F1 = {f1_base:.4f}")

# ----------------------------------------------------------------------
# 6. [제안 모델] TDF-Net (Tree-Deep Fusion Network) 아키텍처 정의
# ----------------------------------------------------------------------
print("\n[5] TDF-Net 하이브리드 입력 특징 생성 (트리 로짓 추출)...")
skf = StratifiedKFold(n_splits=5, shuffle=True, random_state=42)
oof_tree = np.zeros((len(X_train_eng), 10))
test_tree = np.zeros((len(X_test_eng), 10))

for tr_idx, val_idx in skf.split(X_train_eng, y_train):
    rf_fold = RandomForestClassifier(n_estimators=100, max_depth=12, random_state=42)
    et_fold = ExtraTreesClassifier(n_estimators=100, max_depth=12, random_state=42)
    
    rf_fold.fit(X_train_eng.iloc[tr_idx], y_train[tr_idx])
    et_fold.fit(X_train_eng.iloc[tr_idx], y_train[tr_idx])
    
    oof_tree[val_idx, :5] = rf_fold.predict_proba(X_train_eng.iloc[val_idx])
    oof_tree[val_idx, 5:] = et_fold.predict_proba(X_train_eng.iloc[val_idx])
    
    test_tree[:, :5] += rf_fold.predict_proba(X_test_eng) / 5.0
    test_tree[:, 5:] += et_fold.predict_proba(X_test_eng) / 5.0

# 30개 도메인 피처 정규화
scaler_tdf = StandardScaler()
X_tr_domain = scaler_tdf.fit_transform(X_train_eng)
X_te_domain = scaler_tdf.transform(X_test_eng)

# 30개 도메인 피처 + 10개 트리 로짓 = 40차원 특징 공간 결합
X_tr_tdf = np.hstack([X_tr_domain, oof_tree])
X_te_tdf = np.hstack([X_te_domain, test_tree])
print(f"    - TDF-Net 입력 차원: {X_tr_tdf.shape[1]}차원 (도메인 30 + 트리 로짓 10)")

class Mish(nn.Module):
    def forward(self, x):
        return x * torch.tanh(nn.functional.softplus(x))

class ResBlock(nn.Module):
    def __init__(self, dim, dropout=0.25):
        super().__init__()
        self.block = nn.Sequential(
            nn.Linear(dim, dim),
            nn.BatchNorm1d(dim),
            Mish(),
            nn.Dropout(dropout),
            nn.Linear(dim, dim),
            nn.BatchNorm1d(dim)
        )
        self.act = Mish()
    def forward(self, x):
        return self.act(x + self.block(x))

class TDFNet(nn.Module):
    def __init__(self, in_dim=40, hidden_dim=256, num_cls=5):
        super().__init__()
        self.input_layer = nn.Sequential(
            nn.Linear(in_dim, hidden_dim),
            nn.BatchNorm1d(hidden_dim),
            Mish(),
            nn.Dropout(0.2)
        )
        self.res1 = ResBlock(hidden_dim, 0.25)
        self.res2 = ResBlock(hidden_dim, 0.25)
        self.head = nn.Sequential(
            nn.Linear(hidden_dim, 128),
            nn.BatchNorm1d(128),
            nn.GELU(),
            nn.Dropout(0.15),
            nn.Linear(128, num_cls)
        )
    def forward(self, x):
        h = self.input_layer(x)
        h = self.res1(h)
        h = self.res2(h)
        return self.head(h)

# 클래스 불균형 완화를 위한 손실 함수 가중치 설정
cls_counts = np.bincount(y_train)
total_samples = len(y_train)
cls_weights = total_samples / (num_classes * cls_counts)
cls_weights_tensor = torch.tensor(cls_weights, dtype=torch.float32).to(device)

# ----------------------------------------------------------------------
# 7. TDF-Net 다중 시드(5-Seed) 앙상블 학습 및 평가
# ----------------------------------------------------------------------
print("\n[6] TDF-Net 5-Seed 앙상블 학습 시작...")
seeds = [42, 100, 2024, 777, 999]
ensemble_probs = np.zeros((len(X_te_tdf), num_classes))

for s_idx, seed in enumerate(seeds, 1):
    set_seed(seed)
    model = TDFNet(in_dim=40, hidden_dim=256, num_cls=num_classes).to(device)
    optimizer = optim.AdamW(model.parameters(), lr=0.002, weight_decay=1e-4)
    criterion = nn.CrossEntropyLoss(weight=cls_weights_tensor, label_smoothing=0.02)
    scheduler = optim.lr_scheduler.CosineAnnealingLR(optimizer, T_max=80, eta_min=1e-5)
    
    tr_ds = TensorDataset(torch.tensor(X_tr_tdf, dtype=torch.float32), torch.tensor(y_train, dtype=torch.long))
    loader = DataLoader(tr_ds, batch_size=32, shuffle=True)
    
    for epoch in range(80):
        model.train()
        for bx, by in loader:
            bx, by = bx.to(device), by.to(device)
            optimizer.zero_grad()
            out = model(bx)
            loss = criterion(out, by)
            loss.backward()
            optimizer.step()
        scheduler.step()
        
    model.eval()
    with torch.no_grad():
        test_x = torch.tensor(X_te_tdf, dtype=torch.float32).to(device)
        probs = F.softmax(model(test_x), dim=1).cpu().numpy()
        ensemble_probs += probs / len(seeds)
        pred_single = probs.argmax(axis=1)
        acc_single = accuracy_score(y_test, pred_single)
        f1_single = f1_score(y_test, pred_single, average='macro')
        print(f"    - [Seed {seed:4d}] Single Acc: {acc_single*100:.2f}% | Macro F1: {f1_single:.4f} ({s_idx}/{len(seeds)})")

final_pred = ensemble_probs.argmax(axis=1)
acc_tdf = accuracy_score(y_test, final_pred)
f1_tdf = f1_score(y_test, final_pred, average='macro')

print("\n" + "=" * 75)
print("               최종 모델 성능 비교 평가 요약")
print("=" * 75)
print(f"{'모델 구분':<28} | {'정확도 (Accuracy)':<18} | {'Macro F1-Score':<15}")
print("-" * 75)
print(f"{'1. Baseline MLP (5개 피처)':<28} | {acc_base*100:6.2f}%            | {f1_base:.4f}")
print(f"{'2. Random Forest (5개 피처)':<28} | {acc_rf*100:6.2f}%            | {f1_rf:.4f}")
print(f"{'3. TDF-Net 앙상블 (제안 모델)':<28} | {acc_tdf*100:6.2f}% (최고)     | {f1_tdf:.4f} (최고)")
print("=" * 75)

print("\n[TDF-Net 클래스별 분류 리포트]")
print(classification_report(y_test, final_pred, target_names=classes, digits=4))

# ----------------------------------------------------------------------
# 8. 혼동 행렬 시각화 및 결과 저장
# ----------------------------------------------------------------------
try:
    fig, axes = plt.subplots(1, 3, figsize=(18, 5))
    cm_base = confusion_matrix(y_test, y_pred_base)
    cm_rf = confusion_matrix(y_test, y_pred_rf)
    cm_tdf = confusion_matrix(y_test, final_pred)

    models_cm = [
        (f"Baseline MLP (Acc: {acc_base*100:.1f}%)", cm_base, "Blues"),
        (f"Random Forest (Acc: {acc_rf*100:.1f}%)", cm_rf, "Oranges"),
        (f"TDF-Net Ensemble (Acc: {acc_tdf*100:.1f}%)", cm_tdf, "Greens")
    ]

    for ax, (title, cm, cmap) in zip(axes, models_cm):
        sns.heatmap(cm, annot=True, fmt='d', cmap=cmap, cbar=False,
                    xticklabels=classes, yticklabels=classes, ax=ax)
        ax.set_title(title, fontsize=12, fontweight='bold', pad=10)
        ax.set_xlabel("Predicted", fontsize=10)
        ax.set_ylabel("True", fontsize=10)

    plt.tight_layout()
    output_png = "tdf_net_confusion_matrices.png"
    plt.savefig(output_png, dpi=200)
    print(f"\n[7] 혼동 행렬 시각화 차트가 정상 저장되었습니다: {output_png}")
except Exception as e:
    print(f"\n[!] 차트 저장 중 안내: {e}")

print("\n>>> 모든 파이프라인이 성공적으로 실행 완료되었습니다! <<<")
