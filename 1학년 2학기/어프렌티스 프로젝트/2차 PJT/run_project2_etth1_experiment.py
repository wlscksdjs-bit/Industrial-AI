#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
충북대학교 대학원 산업인공지능학과 어프렌티스 프로젝트 5주차 과제
ETT 데이터셋(ETTh1) 기반 RNN, LSTM, GRU 시계열 예측 비교 및 Ablation Test
GPU 가속 환경: NVIDIA GeForce RTX 5070 Laptop GPU (CUDA)
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

# 디바이스 설정 (CUDA RTX 5070)
DEVICE = torch.device('cuda' if torch.cuda.is_available() else 'cpu')
print(f"[*] Active Device: {DEVICE}")
if torch.cuda.is_available():
    print(f"[*] GPU Name: {torch.cuda.get_device_name(0)}")
    print(f"[*] CUDA Version: {torch.version.cuda}")

# 시드 고정
def set_seed(seed=42):
    np.random.seed(seed)
    torch.manual_seed(seed)
    if torch.cuda.is_available():
        torch.cuda.manual_seed_all(seed)

set_seed(42)

# 1. 데이터 로드 및 전처리
DATA_FILE = 'ETTh1.csv'
if not os.path.exists(DATA_FILE):
    raise FileNotFoundError(f"{DATA_FILE} not found!")

df = pd.read_csv(DATA_FILE)
feature_cols = ['HUFL', 'HULL', 'MUFL', 'MULL', 'LUFL', 'LULL', 'OT']
target_col = 'OT'
target_idx = feature_cols.index(target_col)

data_values = df[feature_cols].values

# Train / Val / Test 분할 (표준 ETT 70% / 15% / 15%)
n_total = len(data_values)
n_train = int(n_total * 0.70)
n_val = int(n_total * 0.15)
n_test = n_total - n_train - n_val

train_data = data_values[:n_train]
val_data = data_values[n_train:n_train + n_val]
test_data = data_values[n_train + n_val:]

scaler = StandardScaler()
train_scaled = scaler.fit_transform(train_data)
val_scaled = scaler.transform(val_data)
test_scaled = scaler.transform(test_data)

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
        return x, y.unsqueeze(-1)

# 2. 모델 아키텍처 정의 (RNN, LSTM, GRU)
class SeqModel(nn.Module):
    def __init__(self, model_type='lstm', input_size=7, hidden_size=64, num_layers=2, dropout=0.1):
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
        
        self.fc = nn.Linear(hidden_size, 1)

    def forward(self, x):
        out, _ = self.rnn(x)
        last_hidden = out[:, -1, :]
        pred = self.fc(last_hidden)
        return pred

def train_and_eval(model_type, lookback=24, hidden_size=64, num_layers=2, lr=1e-3, epochs=12, batch_size=128):
    set_seed(42)
    train_ds = TimeSeriesDataset(train_scaled, lookback=lookback, horizon=1, target_idx=target_idx)
    val_ds = TimeSeriesDataset(val_scaled, lookback=lookback, horizon=1, target_idx=target_idx)
    test_ds = TimeSeriesDataset(test_scaled, lookback=lookback, horizon=1, target_idx=target_idx)

    train_loader = DataLoader(train_ds, batch_size=batch_size, shuffle=True)
    val_loader = DataLoader(val_ds, batch_size=batch_size, shuffle=False)
    test_loader = DataLoader(test_ds, batch_size=batch_size, shuffle=False)

    model = SeqModel(model_type=model_type, input_size=7, hidden_size=hidden_size, num_layers=num_layers).to(DEVICE)
    criterion = nn.MSELoss()
    optimizer = torch.optim.Adam(model.parameters(), lr=lr)

    if torch.cuda.is_available():
        torch.cuda.synchronize()
    start_t = time.time()
    best_val_loss = float('inf')
    best_state = None

    for epoch in range(epochs):
        model.train()
        train_loss = 0.0
        for bx, by in train_loader:
            bx, by = bx.to(DEVICE), by.to(DEVICE)
            optimizer.zero_grad()
            preds = model(bx)
            loss = criterion(preds, by)
            loss.backward()
            optimizer.step()
            train_loss += loss.item() * len(bx)
        train_loss /= len(train_ds)

        model.eval()
        val_loss = 0.0
        with torch.no_grad():
            for bx, by in val_loader:
                bx, by = bx.to(DEVICE), by.to(DEVICE)
                preds = model(bx)
                loss = criterion(preds, by)
                val_loss += loss.item() * len(bx)
        val_loss /= len(val_ds)

        if val_loss < best_val_loss:
            best_val_loss = val_loss
            best_state = {k: v.cpu().clone() for k, v in model.state_dict().items()}

    if torch.cuda.is_available():
        torch.cuda.synchronize()
    train_time = time.time() - start_t

    # Test 평가
    model.load_state_dict(best_state)
    model.eval()
    all_preds, all_trues = [], []
    with torch.no_grad():
        for bx, by in test_loader:
            bx = bx.to(DEVICE)
            preds = model(bx)
            all_preds.append(preds.cpu().numpy())
            all_trues.append(by.numpy())

    preds_arr = np.concatenate(all_preds, axis=0)
    trues_arr = np.concatenate(all_trues, axis=0)

    # 원래 스케일로 역변환
    target_mean = scaler.mean_[target_idx]
    target_scale = scaler.scale_[target_idx]

    preds_orig = preds_arr * target_scale + target_mean
    trues_orig = trues_arr * target_scale + target_mean

    mse = float(mean_squared_error(trues_orig, preds_orig))
    mae = float(mean_absolute_error(trues_orig, preds_orig))
    rmse = float(np.sqrt(mse))
    r2 = float(r2_score(trues_orig, preds_orig))

    return {
        'model_type': model_type,
        'lookback': lookback,
        'hidden_size': hidden_size,
        'num_layers': num_layers,
        'train_time_sec': round(train_time, 2),
        'MSE': round(mse, 4),
        'MAE': round(mae, 4),
        'RMSE': round(rmse, 4),
        'R2': round(r2, 4),
        'preds': preds_orig.flatten()[:500].tolist(),
        'trues': trues_orig.flatten()[:500].tolist()
    }

def main():
    print("=== [1] 기본 3개 모델 비교 실험 (Lookback=24, Hidden=64, Layer=2, Epochs=12) ===")
    models = ['rnn', 'lstm', 'gru']
    base_results = {}
    for m in models:
        print(f"Training {m.upper()} on {DEVICE}...")
        res = train_and_eval(m, lookback=24, hidden_size=64, num_layers=2, epochs=12)
        base_results[m] = res
        print(f"[{m.upper()}] Time: {res['train_time_sec']}s | MSE: {res['MSE']} | MAE: {res['MAE']} | RMSE: {res['RMSE']} | R2: {res['R2']}")

    print("\n=== [2] Ablation Test: 입력 윈도우 길이 (Lookback Window: 12h vs 24h vs 48h) ===")
    ablation_results = {}
    lookbacks = [12, 24, 48]
    for lb in lookbacks:
        ablation_results[lb] = {}
        for m in ['rnn', 'lstm', 'gru']:
            if lb == 24:
                ablation_results[lb][m] = base_results[m]
            else:
                print(f"Training {m.upper()} (Lookback={lb})...")
                res = train_and_eval(m, lookback=lb, hidden_size=64, num_layers=2, epochs=12)
                ablation_results[lb][m] = res
                print(f"[{m.upper()} L={lb}] MSE: {res['MSE']} | MAE: {res['MAE']} | RMSE: {res['RMSE']} | R2: {res['R2']}")

    # 결과 JSON 저장
    output_data = {
        'device_info': {
            'device': str(DEVICE),
            'gpu_name': torch.cuda.get_device_name(0) if torch.cuda.is_available() else 'CPU',
            'cuda_version': torch.version.cuda if torch.cuda.is_available() else None
        },
        'dataset': 'ETTh1 (Electricity Transformer Temperature - 1 hour resolution)',
        'target': 'OT (Oil Temperature)',
        'features': feature_cols,
        'train_val_test_split': [n_train, n_val, n_test],
        'base_comparison': base_results,
        'ablation_lookback': ablation_results
    }

    with open('experiment_results.json', 'w', encoding='utf-8') as f:
        json.dump(output_data, f, ensure_ascii=False, indent=2)

    print("\n[V] Experiment complete! Saved to experiment_results.json")

    # 시각화 그래프 저장 (다크모피즘 톤 스타일)
    plt.style.use('dark_background')
    fig, axes = plt.subplots(1, 2, figsize=(14, 5.2), facecolor='#22252b')

    # 1. 시계열 예측 비교 (첫 150 스텝)
    ax1 = axes[0]
    ax1.set_facecolor('#22252b')
    trues_plot = base_results['lstm']['trues'][:150]
    rnn_plot = base_results['rnn']['preds'][:150]
    lstm_plot = base_results['lstm']['preds'][:150]
    gru_plot = base_results['gru']['preds'][:150]

    ax1.plot(trues_plot, label='Ground Truth (Actual OT)', color='#ffffff', linewidth=2.2, alpha=0.95)
    ax1.plot(rnn_plot, label=f"Vanilla RNN (MSE: {base_results['rnn']['MSE']})", color='#f87171', linestyle='--', linewidth=1.4)
    ax1.plot(lstm_plot, label=f"LSTM (MSE: {base_results['lstm']['MSE']})", color='#38bdf8', linestyle='-', linewidth=1.8)
    ax1.plot(gru_plot, label=f"GRU (MSE: {base_results['gru']['MSE']})", color='#4fd1c5', linestyle='-.', linewidth=1.8)
    ax1.set_title("Test Set Oil Temp (OT) Prediction (150 Hours)", color='#5eead4', fontsize=13, fontweight='bold', pad=12)
    ax1.set_xlabel("Time Step (Hour)", color='#c8cdd6', fontsize=11)
    ax1.set_ylabel("Oil Temperature (°C)", color='#c8cdd6', fontsize=11)
    ax1.legend(loc='upper right', framealpha=0.4, facecolor='#15171b', edgecolor='#4fd1c5', fontsize=9.5)
    ax1.grid(True, color='#2b2f37', linestyle=':', alpha=0.7)

    # 2. Ablation Test: Lookback 길이에 따른 MAE 비교
    ax2 = axes[1]
    ax2.set_facecolor('#22252b')
    x_indices = np.arange(len(lookbacks))
    width = 0.25

    rnn_maes = [ablation_results[lb]['rnn']['MAE'] for lb in lookbacks]
    lstm_maes = [ablation_results[lb]['lstm']['MAE'] for lb in lookbacks]
    gru_maes = [ablation_results[lb]['gru']['MAE'] for lb in lookbacks]

    ax2.bar(x_indices - width, rnn_maes, width, label='Vanilla RNN', color='#f87171', alpha=0.85)
    ax2.bar(x_indices, lstm_maes, width, label='LSTM', color='#38bdf8', alpha=0.85)
    ax2.bar(x_indices + width, gru_maes, width, label='GRU', color='#4fd1c5', alpha=0.85)

    ax2.set_xticks(x_indices)
    ax2.set_xticklabels([f"L={lb}h" for lb in lookbacks], color='#c8cdd6', fontsize=11)
    ax2.set_title("Ablation Study: Lookback Window vs MAE", color='#5eead4', fontsize=13, fontweight='bold', pad=12)
    ax2.set_xlabel("Lookback Window Length (Hours)", color='#c8cdd6', fontsize=11)
    ax2.set_ylabel("Test MAE (Lower is better)", color='#c8cdd6', fontsize=11)
    ax2.legend(loc='upper left', framealpha=0.4, facecolor='#15171b', edgecolor='#4fd1c5', fontsize=9.5)
    ax2.grid(True, color='#2b2f37', linestyle=':', alpha=0.7)

    plt.tight_layout()
    plt.savefig('experiment_chart.png', dpi=200, facecolor='#22252b')
    print("[V] Saved experiment_chart.png successfully!")

if __name__ == '__main__':
    main()
