#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
충북대학교 일반대학원 산업인공지능학과 어프렌티스 프로젝트 5주차 과제
ETTh1 시계열 예측 모델 비교 및 구조적 성능 개선 (모델 x -> 모델 y)
실행 환경: NVIDIA GeForce RTX 5070 Laptop GPU (CUDA 가속)
"""
import os
import sys
os.environ['KMP_DUPLICATE_LIB_OK'] = 'TRUE'

import json
import time
import numpy as np
import pandas as pd
import torch
import torch.nn as nn
from torch.utils.data import Dataset, DataLoader
from sklearn.preprocessing import StandardScaler
from sklearn.metrics import mean_squared_error, mean_absolute_error, r2_score
import matplotlib.pyplot as plt

# 1. GPU 디바이스 설정
DEVICE = torch.device('cuda' if torch.cuda.is_available() else 'cpu')
print(f"[*] Active Device: {DEVICE}")
if torch.cuda.is_available():
    print(f"[*] GPU Name: {torch.cuda.get_device_name(0)}")
    print(f"[*] CUDA Version: {torch.version.cuda}")

def set_seed(seed=42):
    np.random.seed(seed)
    torch.manual_seed(seed)
    if torch.cuda.is_available():
        torch.cuda.manual_seed_all(seed)

set_seed(42)

# 2. 데이터셋 로드 및 분할
data_path = os.path.join(os.path.dirname(__file__), 'ETTh1.csv')
if not os.path.exists(data_path):
    data_path = 'ETTh1.csv'
if not os.path.exists(data_path):
    data_path = os.path.join('2차 PJT', 'ETTh1.csv')

df = pd.read_csv(data_path)
feature_cols = ['HUFL', 'HULL', 'MUFL', 'MULL', 'LUFL', 'LULL', 'OT']
target_col = 'OT'
target_idx = feature_cols.index(target_col)

data_values = df[feature_cols].values
n_total = len(data_values)

# 60% Train / 20% Val (3개 모델 비교 및 베이스라인 x 선정용) / 20% Test (최종 x vs y 비교용)
n_train = int(n_total * 0.60)
n_val = int(n_total * 0.20)
n_test = n_total - n_train - n_val

print(f"[*] Total rows: {n_total:,} | Train: {n_train:,} (60%) | Val: {n_val:,} (20%) | Test: {n_test:,} (20%)")

train_raw = data_values[:n_train]
val_raw = data_values[n_train:n_train + n_val]
test_raw = data_values[n_train + n_val:]

scaler = StandardScaler()
train_scaled = scaler.fit_transform(train_raw)
val_scaled = scaler.transform(val_raw)
test_scaled = scaler.transform(test_raw)

# 시계열 슬라이딩 윈도우 데이터셋
class TimeSeriesDataset(Dataset):
    def __init__(self, data, lookback=24, horizon=1, target_idx=6):
        self.data = torch.tensor(data, dtype=torch.float32)
        self.lookback = lookback
        self.horizon = horizon
        self.target_idx = target_idx

    def __len__(self):
        return len(self.data) - self.lookback - self.horizon + 1

    def __getitem__(self, idx):
        x = self.data[idx : idx + self.lookback]
        y = self.data[idx + self.lookback + self.horizon - 1, self.target_idx]
        last_target = self.data[idx + self.lookback - 1, self.target_idx]
        return x, y.unsqueeze(-1), last_target.unsqueeze(-1)

# 3. 모델 아키텍처 정의

# (1) 기본 모델 x (RNN, LSTM, GRU) - 단순 선형 Head, 직접 예측
class BaseSeqModel(nn.Module):
    def __init__(self, model_type='gru', input_size=7, hidden_size=64, num_layers=2, dropout=0.1):
        super().__init__()
        self.model_type = model_type.lower()
        if self.model_type == 'rnn':
            self.rnn = nn.RNN(input_size, hidden_size, num_layers=num_layers, batch_first=True, dropout=dropout if num_layers>1 else 0.0)
        elif self.model_type == 'lstm':
            self.rnn = nn.LSTM(input_size, hidden_size, num_layers=num_layers, batch_first=True, dropout=dropout if num_layers>1 else 0.0)
        elif self.model_type == 'gru':
            self.rnn = nn.GRU(input_size, hidden_size, num_layers=num_layers, batch_first=True, dropout=dropout if num_layers>1 else 0.0)
        else:
            raise ValueError(f"Unknown model_type: {model_type}")
        
        self.head = nn.Linear(hidden_size, 1)

    def forward(self, x, last_target=None):
        out, _ = self.rnn(x)
        last_hidden = out[:, -1, :]
        pred = self.head(last_hidden)
        return pred

# (2) 개선 모델 y (Upgraded Model)
# 개선 1: 은닉 차원 확대 (64 -> 128) + LayerNorm
# 개선 2: 비선형 예측 Head (Linear -> LayerNorm -> GELU -> Dropout -> Linear)
# 개선 3: Residual Delta Prediction (이전 OT + 변화량 예측: y_pred = last_ot + delta)
class UpgradedSeqModel(nn.Module):
    def __init__(self, model_type='gru', input_size=7, hidden_size=128, num_layers=2, dropout=0.15, 
                 use_residual_delta=True, use_nonlinear_head=True):
        super().__init__()
        self.model_type = model_type.lower()
        self.use_residual_delta = use_residual_delta
        self.use_nonlinear_head = use_nonlinear_head

        if self.model_type == 'gru':
            self.rnn = nn.GRU(input_size, hidden_size, num_layers=num_layers, batch_first=True, dropout=dropout if num_layers>1 else 0.0)
        elif self.model_type == 'lstm':
            self.rnn = nn.LSTM(input_size, hidden_size, num_layers=num_layers, batch_first=True, dropout=dropout if num_layers>1 else 0.0)
        else:
            self.rnn = nn.RNN(input_size, hidden_size, num_layers=num_layers, batch_first=True, dropout=dropout if num_layers>1 else 0.0)

        self.ln = nn.LayerNorm(hidden_size)

        if use_nonlinear_head:
            self.head = nn.Sequential(
                nn.Linear(hidden_size, 64),
                nn.LayerNorm(64),
                nn.GELU(),
                nn.Dropout(dropout),
                nn.Linear(64, 1)
            )
        else:
            self.head = nn.Linear(hidden_size, 1)

    def forward(self, x, last_target=None):
        out, _ = self.rnn(x)
        last_hidden = self.ln(out[:, -1, :])
        delta_or_pred = self.head(last_hidden)

        if self.use_residual_delta and last_target is not None:
            return last_target + delta_or_pred
        return delta_or_pred

# 4. 훈련 및 평가 함수
def train_and_evaluate(model, lookback=24, epochs=12, batch_size=64, lr=1e-3):
    set_seed(42)
    train_ds = TimeSeriesDataset(train_scaled, lookback=lookback, horizon=1, target_idx=target_idx)
    val_ds = TimeSeriesDataset(val_scaled, lookback=lookback, horizon=1, target_idx=target_idx)
    test_ds = TimeSeriesDataset(test_scaled, lookback=lookback, horizon=1, target_idx=target_idx)

    train_loader = DataLoader(train_ds, batch_size=batch_size, shuffle=True)
    val_loader = DataLoader(val_ds, batch_size=batch_size, shuffle=False)
    test_loader = DataLoader(test_ds, batch_size=batch_size, shuffle=False)

    model = model.to(DEVICE)
    criterion = nn.MSELoss()
    optimizer = torch.optim.AdamW(model.parameters(), lr=lr, weight_decay=1e-4)

    best_val_loss = float('inf')
    best_state = None

    if torch.cuda.is_available():
        torch.cuda.synchronize()
    start_time = time.time()

    for epoch in range(epochs):
        model.train()
        train_loss = 0.0
        for bx, by, blast in train_loader:
            bx, by, blast = bx.to(DEVICE), by.to(DEVICE), blast.to(DEVICE)
            optimizer.zero_grad()
            preds = model(bx, blast)
            loss = criterion(preds, by)
            loss.backward()
            optimizer.step()
            train_loss += loss.item() * len(bx)
        train_loss /= len(train_ds)

        model.eval()
        val_loss = 0.0
        with torch.no_grad():
            for bx, by, blast in val_loader:
                bx, by, blast = bx.to(DEVICE), by.to(DEVICE), blast.to(DEVICE)
                preds = model(bx, blast)
                loss = criterion(preds, by)
                val_loss += loss.item() * len(bx)
        val_loss /= len(val_ds)

        if val_loss < best_val_loss:
            best_val_loss = val_loss
            best_state = {k: v.cpu().clone() for k, v in model.state_dict().items()}

    if torch.cuda.is_available():
        torch.cuda.synchronize()
    train_time = time.time() - start_time

    # 최적 가중치 로드
    model.load_state_dict(best_state)
    model.eval()

    # Val 평가 (원래 스케일)
    val_preds, val_trues = [], []
    with torch.no_grad():
        for bx, by, blast in val_loader:
            bx, blast = bx.to(DEVICE), blast.to(DEVICE)
            preds = model(bx, blast)
            val_preds.append(preds.cpu().numpy())
            val_trues.append(by.numpy())
    v_preds_arr = np.concatenate(val_preds, axis=0)
    v_trues_arr = np.concatenate(val_trues, axis=0)

    # Test 평가 (원래 스케일)
    test_preds, test_trues = [], []
    with torch.no_grad():
        for bx, by, blast in test_loader:
            bx, blast = bx.to(DEVICE), blast.to(DEVICE)
            preds = model(bx, blast)
            test_preds.append(preds.cpu().numpy())
            test_trues.append(by.numpy())
    t_preds_arr = np.concatenate(test_preds, axis=0)
    t_trues_arr = np.concatenate(test_trues, axis=0)

    # 역정규화
    t_mean = scaler.mean_[target_idx]
    t_scale = scaler.scale_[target_idx]

    v_preds_orig = v_preds_arr * t_scale + t_mean
    v_trues_orig = v_trues_arr * t_scale + t_mean

    t_preds_orig = t_preds_arr * t_scale + t_mean
    t_trues_orig = t_trues_arr * t_scale + t_mean

    val_mse = float(mean_squared_error(v_trues_orig, v_preds_orig))
    val_mae = float(mean_absolute_error(v_trues_orig, v_preds_orig))

    test_mse = float(mean_squared_error(t_trues_orig, t_preds_orig))
    test_mae = float(mean_absolute_error(t_trues_orig, t_preds_orig))
    test_rmse = float(np.sqrt(test_mse))
    test_r2 = float(r2_score(t_trues_orig, t_preds_orig))

    return {
        'train_time_sec': round(train_time, 2),
        'val_mse': round(val_mse, 4),
        'val_mae': round(val_mae, 4),
        'test_mse': round(test_mse, 4),
        'test_mae': round(test_mae, 4),
        'test_rmse': round(test_rmse, 4),
        'test_r2': round(test_r2, 4),
        'test_preds_sample': t_preds_orig.flatten()[:300].tolist(),
        'test_trues_sample': t_trues_orig.flatten()[:300].tolist()
    }

def main():
    print("\n=======================================================")
    print(" [Step 1] 동일 조건의 3개 기본 모델 비교 (RNN vs LSTM vs GRU)")
    print("=======================================================")
    base_models = ['rnn', 'lstm', 'gru']
    step1_results = {}
    for m in base_models:
        print(f"--> Training Base {m.upper()} on RTX 5070...")
        net = BaseSeqModel(model_type=m, input_size=7, hidden_size=64, num_layers=2)
        res = train_and_evaluate(net, lookback=24, epochs=10, batch_size=64, lr=1e-3)
        step1_results[m] = res
        print(f"    [{m.upper()}] Val MSE: {res['val_mse']} | Val MAE: {res['val_mae']} | Train Time: {res['train_time_sec']}s")

    # 최적 모델 x 선정
    best_base_name = min(step1_results, key=lambda k: step1_results[k]['val_mse'])
    print(f"\n[*] 3개 모델 Val MSE 기준 최적 기본 모델 x: {best_base_name.upper()} (Val MSE: {step1_results[best_base_name]['val_mse']})")

    print("\n=======================================================")
    print(f" [Step 2 & 3] 모델 x ({best_base_name.upper()}) 개선 및 Ablation Test")
    print("=======================================================")

    # 1. 모델 x (기본 베이스라인)
    model_x_results = step1_results[best_base_name]

    # 2. 개선 모델 y (Full Upgrade: Hidden 128 + Nonlinear GELU Head + Residual Delta)
    print("--> Training Model y (Full Upgrade: Hidden 128 + GELU Head + Residual Delta)...")
    model_y = UpgradedSeqModel(model_type=best_base_name, input_size=7, hidden_size=128, num_layers=2, 
                               use_residual_delta=True, use_nonlinear_head=True)
    model_y_results = train_and_evaluate(model_y, lookback=24, epochs=12, batch_size=64, lr=1e-3)
    print(f"    [Model y] Test MSE: {model_y_results['test_mse']} | MAE: {model_y_results['test_mae']} | RMSE: {model_y_results['test_rmse']} | R2: {model_y_results['test_r2']}")

    # 3. Ablation 1: w/o Residual Delta (Hidden 128 + GELU Head, 직접 예측)
    print("--> Training Ablation 1 (w/o Residual Delta: 직접 예측)...")
    abl1 = UpgradedSeqModel(model_type=best_base_name, input_size=7, hidden_size=128, num_layers=2, 
                            use_residual_delta=False, use_nonlinear_head=True)
    abl1_results = train_and_evaluate(abl1, lookback=24, epochs=12, batch_size=64, lr=1e-3)
    print(f"    [w/o Residual Delta] Test MSE: {abl1_results['test_mse']} | MAE: {abl1_results['test_mae']}")

    # 4. Ablation 2: w/o Nonlinear Head (Hidden 128 + 단일 Linear Head + Residual Delta)
    print("--> Training Ablation 2 (w/o Nonlinear Head: 단일 Linear Head)...")
    abl2 = UpgradedSeqModel(model_type=best_base_name, input_size=7, hidden_size=128, num_layers=2, 
                            use_residual_delta=True, use_nonlinear_head=False)
    abl2_results = train_and_evaluate(abl2, lookback=24, epochs=12, batch_size=64, lr=1e-3)
    print(f"    [w/o Nonlinear Head] Test MSE: {abl2_results['test_mse']} | MAE: {abl2_results['test_mae']}")

    # 성능 개선율 계산
    mse_impr = (model_x_results['test_mse'] - model_y_results['test_mse']) / model_x_results['test_mse'] * 100
    mae_impr = (model_x_results['test_mae'] - model_y_results['test_mae']) / model_x_results['test_mae'] * 100
    rmse_impr = (model_x_results['test_rmse'] - model_y_results['test_rmse']) / model_x_results['test_rmse'] * 100
    r2_impr = (model_y_results['test_r2'] - model_x_results['test_r2']) / (1.0 - model_x_results['test_r2'] + 1e-8) * 100

    print("\n=======================================================")
    print(" [Step 4] 최종 모델 x vs 모델 y 성능 비교 (Test Set)")
    print("=======================================================")
    print(f"MAE:  모델 x {model_x_results['test_mae']} -> 모델 y {model_y_results['test_mae']} (개선율: {mae_impr:.1f}% 감소)")
    print(f"MSE:  모델 x {model_x_results['test_mse']} -> 모델 y {model_y_results['test_mse']} (개선율: {mse_impr:.1f}% 감소)")
    print(f"RMSE: 모델 x {model_x_results['test_rmse']} -> 모델 y {model_y_results['test_rmse']} (개선율: {rmse_impr:.1f}% 감소)")
    print(f"R2:   모델 x {model_x_results['test_r2']} -> 모델 y {model_y_results['test_r2']} (향상)")

    # JSON 저장
    full_output = {
        'hardware': {
            'device': str(DEVICE),
            'gpu_name': torch.cuda.get_device_name(0) if torch.cuda.is_available() else 'CPU',
            'cuda_version': torch.version.cuda if torch.cuda.is_available() else None
        },
        'dataset': {
            'name': 'ETTh1',
            'total_rows': n_total,
            'split': {'train': n_train, 'val': n_val, 'test': n_test},
            'lookback': 24,
            'target': 'OT'
        },
        'step1_base_comparison': step1_results,
        'best_base_model': best_base_name,
        'model_x': model_x_results,
        'model_y': model_y_results,
        'ablation': {
            'model_y_full': model_y_results,
            'wo_residual_delta': abl1_results,
            'wo_nonlinear_head': abl2_results,
            'model_x_baseline': model_x_results
        },
        'improvements': {
            'mae_pct': round(mae_impr, 1),
            'mse_pct': round(mse_impr, 1),
            'rmse_pct': round(rmse_impr, 1),
            'r2_diff': round(model_y_results['test_r2'] - model_x_results['test_r2'], 4)
        }
    }

    with open('experiment_results_v2.json', 'w', encoding='utf-8') as f:
        json.dump(full_output, f, ensure_ascii=False, indent=2)
    print("\n[V] Saved experiment_results_v2.json")

    # 5. 고해상도 시각화 차트 생성 (다크모피즘 디자인)
    plt.style.use('dark_background')
    
    # Chart 1: 3개 기본 모델 Val 성능 비교
    fig, ax = plt.subplots(figsize=(6.2, 4.0), facecolor='#15171b')
    ax.set_facecolor('#1c1f24')
    m_names = ['Vanilla RNN', 'LSTM', 'GRU']
    val_mses = [step1_results['rnn']['val_mse'], step1_results['lstm']['val_mse'], step1_results['gru']['val_mse']]
    colors = ['#f87171', '#38bdf8', '#4ade80']
    bars = ax.bar(m_names, val_mses, color=colors, width=0.48, edgecolor='#2d3748', linewidth=1.2)
    for b, v in zip(bars, val_mses):
        ax.text(b.get_x() + b.get_width()/2, v + 0.015, f"{v:.4f}", ha='center', va='bottom', color='#ffffff', fontsize=11, fontweight='bold')
    ax.set_title("Validation MSE Comparison (3 Base Models)", color='#5eead4', fontsize=12, fontweight='bold', pad=12)
    ax.set_ylabel("Validation MSE (Lower is Better)", color='#cbd5e1', fontsize=10)
    ax.tick_params(colors='#cbd5e1', labelsize=10)
    ax.grid(True, color='#2b2f37', linestyle=':', alpha=0.7)
    plt.tight_layout()
    plt.savefig('chart_base_val.png', dpi=220, facecolor='#15171b')
    plt.close()

    # Chart 2: Ablation Study 차트 (컴포넌트별 MSE)
    fig, ax = plt.subplots(figsize=(7.5, 4.0), facecolor='#15171b')
    ax.set_facecolor('#1c1f24')
    abl_labels = [
        f"Model x\n(Base {best_base_name.upper()})",
        "w/o Delta Pred\n(Direct)",
        "w/o GELU Head\n(Linear)",
        f"Model y\n(Full Upgrade)"
    ]
    abl_mses = [
        model_x_results['test_mse'],
        abl1_results['test_mse'],
        abl2_results['test_mse'],
        model_y_results['test_mse']
    ]
    abl_colors = ['#94a3b8', '#fb923c', '#f43f5e', '#38bdf8']
    bars = ax.bar(abl_labels, abl_mses, color=abl_colors, width=0.52, edgecolor='#2d3748', linewidth=1.2)
    for b, v in zip(bars, abl_mses):
        ax.text(b.get_x() + b.get_width()/2, v + 0.01, f"{v:.4f}", ha='center', va='bottom', color='#ffffff', fontsize=10.5, fontweight='bold')
    ax.set_title("Ablation Study: Test MSE by Architectural Component", color='#5eead4', fontsize=12, fontweight='bold', pad=12)
    ax.set_ylabel("Test MSE (Lower is Better)", color='#cbd5e1', fontsize=10)
    ax.tick_params(colors='#cbd5e1', labelsize=9.5)
    ax.grid(True, color='#2b2f37', linestyle=':', alpha=0.7)
    plt.tight_layout()
    plt.savefig('chart_ablation_upgrades.png', dpi=220, facecolor='#15171b')
    plt.close()

    # Chart 3: 250개 시점 예측 궤적 비교 (Ground Truth vs Model x vs Model y)
    fig, ax = plt.subplots(figsize=(13.5, 4.5), facecolor='#15171b')
    ax.set_facecolor('#1c1f24')
    pts = 250
    gt = model_y_results['test_trues_sample'][:pts]
    px = model_x_results['test_preds_sample'][:pts]
    py = model_y_results['test_preds_sample'][:pts]

    ax.plot(gt, label='Ground Truth (Actual OT)', color='#f8fafc', linewidth=2.0, alpha=0.95)
    ax.plot(px, label=f"Model x (Base {best_base_name.upper()}, MSE: {model_x_results['test_mse']})", color='#f87171', linestyle='--', linewidth=1.6, alpha=0.85)
    ax.plot(py, label=f"Model y (Upgraded {best_base_name.upper()}, MSE: {model_y_results['test_mse']})", color='#38bdf8', linestyle='-', linewidth=2.0, alpha=0.95)

    ax.set_title("Test Set Oil Temperature Prediction Trajectory (First 250 Hours)", color='#5eead4', fontsize=13, fontweight='bold', pad=12)
    ax.set_xlabel("Time Step (Hour)", color='#cbd5e1', fontsize=11)
    ax.set_ylabel("Oil Temperature (°C)", color='#cbd5e1', fontsize=11)
    ax.tick_params(colors='#cbd5e1', labelsize=10)
    ax.legend(loc='upper left', framealpha=0.85, facecolor='#15171b', edgecolor='#4fd1c5', fontsize=10)
    ax.grid(True, color='#2b2f37', linestyle=':', alpha=0.7)
    # y축 마진 확보
    ax.set_ylim(min(gt) - 2.0, max(gt) + 4.0)
    plt.tight_layout()
    plt.savefig('chart_predictions_xy.png', dpi=220, facecolor='#15171b')
    plt.close()

    # Chart 4: 주요 성능 지표 비교 (오차 지표 및 R2)
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(11.5, 4.2), facecolor='#15171b', gridspec_kw={'width_ratios': [2.2, 1]})
    ax1.set_facecolor('#1c1f24')
    ax2.set_facecolor('#1c1f24')

    metrics = ['MAE', 'MSE', 'RMSE']
    vals_x = [model_x_results['test_mae'], model_x_results['test_mse'], model_x_results['test_rmse']]
    vals_y = [model_y_results['test_mae'], model_y_results['test_mse'], model_y_results['test_rmse']]

    x_idx = np.arange(len(metrics))
    w = 0.35
    b1 = ax1.bar(x_idx - w/2, vals_x, w, label=f"Model x ({best_base_name.upper()})", color='#f87171', alpha=0.85, edgecolor='#2d3748')
    b2 = ax1.bar(x_idx + w/2, vals_y, w, label=f"Model y (Upgraded)", color='#38bdf8', alpha=0.9, edgecolor='#2d3748')

    for b, vx, vy in zip(b2, vals_x, vals_y):
        pct = (vx - vy) / vx * 100
        ax1.text(b.get_x() + b.get_width()/2, vy + 0.02, f"-{pct:.1f}%", ha='center', va='bottom', color='#4ade80', fontsize=10.5, fontweight='bold')

    ax1.set_xticks(x_idx)
    ax1.set_xticklabels(metrics, color='#cbd5e1', fontsize=11, fontweight='bold')
    ax1.set_title("Test Error Metrics Comparison (Lower is Better)", color='#5eead4', fontsize=12, fontweight='bold', pad=12)
    ax1.set_ylabel("Error Metric Value", color='#cbd5e1', fontsize=10)
    ax1.tick_params(colors='#cbd5e1', labelsize=10)
    ax1.legend(loc='upper right', framealpha=0.85, facecolor='#15171b', edgecolor='#4fd1c5', fontsize=9.5)
    ax1.grid(True, color='#2b2f37', linestyle=':', alpha=0.7)

    # R2 bar
    r2_x = model_x_results['test_r2']
    r2_y = model_y_results['test_r2']
    b_r2 = ax2.bar([f"Model x", f"Model y"], [r2_x, r2_y], color=['#f87171', '#38bdf8'], width=0.48, edgecolor='#2d3748')
    for b, val in zip(b_r2, [r2_x, r2_y]):
        ax2.text(b.get_x() + b.get_width()/2, val - 0.03, f"{val:.4f}", ha='center', va='top', color='#ffffff', fontsize=10.5, fontweight='bold')
    ax2.set_title("R² Score (Higher is Better)", color='#5eead4', fontsize=12, fontweight='bold', pad=12)
    ax2.set_ylim(0.85, 1.0)
    ax2.tick_params(colors='#cbd5e1', labelsize=10)
    ax2.grid(True, color='#2b2f37', linestyle=':', alpha=0.7)

    plt.tight_layout()
    plt.savefig('chart_final_metrics.png', dpi=220, facecolor='#15171b')
    plt.close()

    print("[V] All 4 visual charts generated successfully!")

if __name__ == '__main__':
    main()
