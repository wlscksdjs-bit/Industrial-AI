import os
import sys
import numpy as np
import pandas as pd
from sklearn.preprocessing import RobustScaler
from sklearn.metrics import precision_score, recall_score, f1_score, precision_recall_curve, auc, roc_auc_score
import torch
import torch.nn as nn
import torch.nn.functional as F
from torch.utils.data import DataLoader, TensorDataset
import time

os.environ['KMP_DUPLICATE_LIB_OK'] = 'TRUE'
sys.stdout.reconfigure(encoding='utf-8')

torch.manual_seed(42)
np.random.seed(42)

BASE_DIR = r"g:\내 드라이브\03_충북대_대학원_산업인공지능학과\2학기\어프렌티스 프로젝트\3차 PJT"
SKAB_DATA_DIR = os.path.join(BASE_DIR, "SKAB", "data")
NORMAL_PATH = os.path.join(SKAB_DATA_DIR, "anomaly-free", "anomaly-free.csv")
VALVE1_DIR = os.path.join(SKAB_DATA_DIR, "valve1")
VALVE2_DIR = os.path.join(SKAB_DATA_DIR, "valve2")
OTHER_DIR = os.path.join(SKAB_DATA_DIR, "other")

BASE_SENSOR_COLS = [
    'Accelerometer1RMS',
    'Accelerometer2RMS',
    'Current',
    'Pressure',
    'Temperature',
    'Thermocouple',
    'Voltage',
    'Volume Flow RateRMS'
]

def create_sliding_windows(data, window_size=30):
    X = []
    for i in range(len(data) - window_size + 1):
        X.append(data[i:i + window_size])
    return np.array(X)

def apply_point_adjustment(y_true, y_pred):
    adjusted_pred = y_pred.copy()
    n = len(y_true)
    i = 0
    while i < n:
        if y_true[i] == 1:
            start = i
            while i < n and y_true[i] == 1:
                i += 1
            end = i
            if np.sum(adjusted_pred[start:end]) > 0:
                adjusted_pred[start:end] = 1
        else:
            i += 1
    return adjusted_pred

def evaluate_predictions(y_true, scores, threshold):
    y_pred = (scores >= threshold).astype(int)
    prec_raw = float(precision_score(y_true, y_pred, zero_division=0))
    rec_raw = float(recall_score(y_true, y_pred, zero_division=0))
    f1_raw = float(f1_score(y_true, y_pred, zero_division=0))
    
    prec_curve, rec_curve, _ = precision_recall_curve(y_true, scores)
    auprc = float(auc(rec_curve, prec_curve))
    
    try:
        auroc = float(roc_auc_score(y_true, scores))
    except Exception:
        auroc = 0.5
        
    y_pred_pa = apply_point_adjustment(y_true, y_pred)
    prec_pa = float(precision_score(y_true, y_pred_pa, zero_division=0))
    rec_pa = float(recall_score(y_true, y_pred_pa, zero_division=0))
    f1_pa = float(f1_score(y_true, y_pred_pa, zero_division=0))
    
    return {
        'threshold': float(threshold),
        'f1_raw': round(f1_raw, 4),
        'prec_raw': round(prec_raw, 4),
        'rec_raw': round(rec_raw, 4),
        'auprc': round(auprc, 4),
        'auroc': round(auroc, 4),
        'f1_pa': round(f1_pa, 4),
        'prec_pa': round(prec_pa, 4),
        'rec_pa': round(rec_pa, 4)
    }

def find_best_threshold(y_true, scores):
    prec, rec, thresholds = precision_recall_curve(y_true, scores)
    f1_scores = 2 * (prec * rec) / (prec + rec + 1e-8)
    best_idx = np.argmax(f1_scores)
    best_th = thresholds[min(best_idx, len(thresholds)-1)]
    return best_th

# Backbone Model: Advanced Temporal BiLSTM-AE
class TemporalBiLSTMAE(nn.Module):
    def __init__(self, input_dim=8, hidden_dim=64, latent_dim=32):
        super(TemporalBiLSTMAE, self).__init__()
        self.encoder = nn.LSTM(input_dim, hidden_dim, num_layers=2, batch_first=True, bidirectional=True, dropout=0.1)
        self.enc_fc = nn.Linear(hidden_dim * 2, latent_dim)
        self.ln = nn.LayerNorm(latent_dim)
        
        self.dec_fc = nn.Linear(latent_dim, hidden_dim)
        self.decoder = nn.LSTM(hidden_dim, hidden_dim, num_layers=2, batch_first=True, dropout=0.1)
        self.out_fc = nn.Linear(hidden_dim, input_dim)

    def forward(self, x):
        B, L, _ = x.size()
        enc_out, _ = self.encoder(x)
        z = F.gelu(self.ln(self.enc_fc(enc_out[:, -1, :])))
        dec_in = self.dec_fc(z).unsqueeze(1).repeat(1, L, 1)
        dec_out, _ = self.decoder(dec_in)
        return self.out_fc(dec_out)

def main():
    device = torch.device('cpu')
    print("=== Testing Novel SOTA: Dynamic Top-K Standardized Residual Routing ===")

    df_normal = pd.read_csv(NORMAL_PATH, sep=';', parse_dates=['datetime'], index_col='datetime')
    scaler = RobustScaler().fit(df_normal[BASE_SENSOR_COLS])
    X_train_sc = scaler.transform(df_normal[BASE_SENSOR_COLS])

    val_files = [os.path.join(VALVE1_DIR, f"{i}.csv") for i in [0, 1, 2, 3]]
    test_files = []
    for i in range(4, 16): test_files.append(os.path.join(VALVE1_DIR, f"{i}.csv"))
    for f in sorted(os.listdir(VALVE2_DIR)):
        if f.endswith('.csv'): test_files.append(os.path.join(VALVE2_DIR, f))
    for f in sorted(os.listdir(OTHER_DIR)):
        if f.endswith('.csv'): test_files.append(os.path.join(OTHER_DIR, f))

    def load_dfs(files):
        dfs = [pd.read_csv(fp, sep=';') for fp in files]
        df_all = pd.concat(dfs, axis=0, ignore_index=True)
        return scaler.transform(df_all[BASE_SENSOR_COLS]), df_all['anomaly'].values.astype(int)

    X_val_sc, y_val = load_dfs(val_files)
    X_test_sc, y_test = load_dfs(test_files)

    W = 30
    X_tr_w = create_sliding_windows(X_train_sc, W)
    X_v_w = create_sliding_windows(X_val_sc, W)
    y_v_w = y_val[W - 1:]
    X_te_w = create_sliding_windows(X_test_sc, W)
    y_te_w = y_test[W - 1:]

    tr_ds = TensorDataset(torch.tensor(X_tr_w, dtype=torch.float32))
    tr_loader = DataLoader(tr_ds, batch_size=128, shuffle=True)

    print("Training Temporal BiLSTM AutoEncoder...", flush=True)
    model = TemporalBiLSTMAE(input_dim=8, hidden_dim=64, latent_dim=32).to(device)
    optimizer = torch.optim.AdamW(model.parameters(), lr=1e-3, weight_decay=1e-4)
    criterion = nn.MSELoss()

    for ep in range(15):
        model.train()
        for bx in tr_loader:
            bx = bx[0].to(device)
            optimizer.zero_grad()
            recon = model(bx)
            loss = criterion(recon, bx)
            loss.backward()
            optimizer.step()

    model.eval()
    def get_errs(m, X):
        ds = TensorDataset(torch.tensor(X, dtype=torch.float32))
        ld = DataLoader(ds, batch_size=128, shuffle=False)
        all_errs = []
        with torch.no_grad():
            for bx in ld:
                bx = bx[0].to(device)
                recon = m(bx)
                err = ((bx[:, -1, :] - recon[:, -1, :]) ** 2).cpu().numpy()
                all_errs.append(err)
        return np.vstack(all_errs)

    # Normal residuals to compute baseline variance per channel
    tr_errs = get_errs(model, X_tr_w[-2000:])
    mean_tr = np.mean(tr_errs, axis=0)
    std_tr = np.std(tr_errs, axis=0) + 1e-6
    print(f"Normal Residual Baseline Mean: {mean_tr}")
    print(f"Normal Residual Baseline Std:  {std_tr}")

    v_errs = get_errs(model, X_v_w)
    te_errs = get_errs(model, X_te_w)

    # Standardize residuals using normal data statistics: Z = (err - mean) / std
    v_z = np.maximum(0, (v_errs - mean_tr) / std_tr)
    te_z = np.maximum(0, (te_errs - mean_tr) / std_tr)

    # Novel SOTA Strategy: Dynamic Top-K Residual Aggregation
    # For each sample, take the mean of the top K largest standardized deviations
    for K in [1, 2, 3, 4, 8]:
        v_topk = np.mean(np.sort(v_z, axis=1)[:, -K:], axis=1)
        te_topk = np.mean(np.sort(te_z, axis=1)[:, -K:], axis=1)

        th = find_best_threshold(y_v_w, v_topk)
        res = evaluate_predictions(y_te_w, te_topk, th)
        print(f"\n--- Dynamic Top-{K} Standardized (Raw): ---")
        print(f"F1={res['f1_raw']} | Prec={res['prec_raw']} | Rec={res['rec_raw']} | AUPRC={res['auprc']} | F1(PA)={res['f1_pa']}")

        # With temporal smoothing
        for win in [3, 5, 7]:
            v_sm = pd.Series(v_topk).rolling(win, min_periods=1).mean().values
            te_sm = pd.Series(te_topk).rolling(win, min_periods=1).mean().values
            th_sm = find_best_threshold(y_v_w, v_sm)
            res_sm = evaluate_predictions(y_te_w, te_sm, th_sm)
            print(f"  + Rolling({win}): F1={res_sm['f1_raw']} | Prec={res_sm['prec_raw']} | Rec={res_sm['rec_raw']} | AUPRC={res_sm['auprc']} | F1(PA)={res_sm['f1_pa']}")

    # Strategy B: Multi-Scale Temporal Discrepancy (Short EMA vs Long EMA)
    print("\n--- Strategy B: Dual-Scale Temporal Discrepancy Filter ---")
    v_base = np.mean(np.sort(v_z, axis=1)[:, -3:], axis=1)
    te_base = np.mean(np.sort(te_z, axis=1)[:, -3:], axis=1)

    for fast_span, slow_span in [(3, 15), (5, 20), (5, 30)]:
        v_fast = pd.Series(v_base).ewm(span=fast_span).mean().values
        v_slow = pd.Series(v_base).ewm(span=slow_span).mean().values
        v_diff = np.maximum(0, v_fast - 0.5 * v_slow)

        te_fast = pd.Series(te_base).ewm(span=fast_span).mean().values
        te_slow = pd.Series(te_base).ewm(span=slow_span).mean().values
        te_diff = np.maximum(0, te_fast - 0.5 * te_slow)

        th_d = find_best_threshold(y_v_w, v_diff)
        res_d = evaluate_predictions(y_te_w, te_diff, th_d)
        print(f"Dual EMA (fast={fast_span}, slow={slow_span}): F1={res_d['f1_raw']} | Prec={res_d['prec_raw']} | Rec={res_d['rec_raw']} | AUPRC={res_d['auprc']} | F1(PA)={res_d['f1_pa']}")

if __name__ == '__main__':
    main()
