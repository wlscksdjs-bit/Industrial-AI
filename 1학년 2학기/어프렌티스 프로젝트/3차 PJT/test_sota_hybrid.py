import os
import sys
import numpy as np
import pandas as pd
from sklearn.preprocessing import RobustScaler
from sklearn.metrics import precision_score, recall_score, f1_score, precision_recall_curve, auc, roc_auc_score
import torch
import torch.nn as nn
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
    
    y_pred_pa = apply_point_adjustment(y_true, y_pred)
    prec_pa = float(precision_score(y_true, y_pred_pa, zero_division=0))
    rec_pa = float(recall_score(y_true, y_pred_pa, zero_division=0))
    f1_pa = float(f1_score(y_true, y_pred_pa, zero_division=0))
    
    return {
        'f1_raw': round(f1_raw, 4),
        'prec_raw': round(prec_raw, 4),
        'rec_raw': round(rec_raw, 4),
        'auprc': round(auprc, 4),
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

# SOTA Architecture: Physics-Informed Attention-Augmented AutoEncoder (PA-AE)
# Incorporating Self-Attention (Vaswani et al. / Xu et al. ICLR 2022) + BiLSTM + Domain Weighting
class AttentionBiLSTMAE(nn.Module):
    def __init__(self, input_dim=8, hidden_dim=64, num_heads=4, latent_dim=32):
        super(AttentionBiLSTMAE, self).__init__()
        # 1. Temporal BiLSTM
        self.bilstm = nn.LSTM(input_dim, hidden_dim, num_layers=1, batch_first=True, bidirectional=True)
        # 2. Multi-Head Self-Attention across temporal steps
        self.mha = nn.MultiheadAttention(embed_dim=hidden_dim*2, num_heads=num_heads, batch_first=True)
        self.ln = nn.LayerNorm(hidden_dim*2)
        
        # Latent bottleneck
        self.enc_fc = nn.Linear(hidden_dim*2, latent_dim)
        
        # Decoder
        self.dec_fc = nn.Linear(latent_dim, hidden_dim)
        self.decoder = nn.LSTM(hidden_dim, hidden_dim, num_layers=2, batch_first=True, dropout=0.1)
        self.out_fc = nn.Linear(hidden_dim, input_dim)

    def forward(self, x):
        B, L, _ = x.size()
        lstm_out, _ = self.bilstm(x) # (B, L, hidden*2)
        attn_out, _ = self.mha(lstm_out, lstm_out, lstm_out)
        h = self.ln(lstm_out + attn_out) # (B, L, hidden*2)
        
        latent = torch.relu(self.enc_fc(h[:, -1, :])) # (B, latent_dim)
        
        dec_in = self.dec_fc(latent).unsqueeze(1).repeat(1, L, 1)
        dec_out, _ = self.decoder(dec_in)
        recon = self.out_fc(dec_out)
        return recon

def main():
    device = torch.device('cpu')
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

    print("Training Attention-BiLSTM AutoEncoder (SOTA Hybrid)...", flush=True)
    model = AttentionBiLSTMAE(input_dim=8, hidden_dim=64, num_heads=4, latent_dim=32).to(device)
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

    v_errs = get_errs(model, X_v_w)
    te_errs = get_errs(model, X_te_w)

    key_weights = np.array([2.0, 2.0, 1.0, 0.5, 1.5, 0.5, 0.2, 3.0])
    
    # 1. Unweighted Raw
    v_raw = np.mean(v_errs, axis=1)
    te_raw = np.mean(te_errs, axis=1)
    th1 = find_best_threshold(y_v_w, v_raw)
    print("1. Attn-BiLSTM (Unweighted Raw):", evaluate_predictions(y_te_w, te_raw, th1), flush=True)

    # 2. Attn-BiLSTM + Rolling (k=5)
    v_raw_s = pd.Series(v_raw).rolling(5, min_periods=1).mean().values
    te_raw_s = pd.Series(te_raw).rolling(5, min_periods=1).mean().values
    th2 = find_best_threshold(y_v_w, v_raw_s)
    print("2. Attn-BiLSTM + Rolling(5):", evaluate_predictions(y_te_w, te_raw_s, th2), flush=True)

    # 3. Attn-BiLSTM + Domain Weighting
    v_w = np.dot(v_errs, key_weights)
    te_w = np.dot(te_errs, key_weights)
    th3 = find_best_threshold(y_v_w, v_w)
    print("3. Attn-BiLSTM + Domain Weighting:", evaluate_predictions(y_te_w, te_w, th3), flush=True)

    # 4. Attn-BiLSTM + Domain Weighting + Rolling (k=5)
    v_w_s = pd.Series(v_w).rolling(5, min_periods=1).mean().values
    te_w_s = pd.Series(te_w).rolling(5, min_periods=1).mean().values
    th4 = find_best_threshold(y_v_w, v_w_s)
    print("4. Attn-BiLSTM + Domain Weighting + Rolling(5):", evaluate_predictions(y_te_w, te_w_s, th4), flush=True)

    # 5. Test different k: 3, 5, 7, 9
    for k in [3, 7, 9]:
        v_k = pd.Series(v_w).rolling(k, min_periods=1).mean().values
        te_k = pd.Series(te_w).rolling(k, min_periods=1).mean().values
        th_k = find_best_threshold(y_v_w, v_k)
        print(f"   k={k}:", evaluate_predictions(y_te_w, te_k, th_k), flush=True)

if __name__ == '__main__':
    main()
