import os
import sys
import numpy as np
import pandas as pd
from sklearn.preprocessing import RobustScaler
from sklearn.metrics import precision_score, recall_score, f1_score, precision_recall_curve, auc, roc_auc_score
import torch
import torch.nn as nn
from torch.utils.data import DataLoader, TensorDataset

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

# Model Architectures
# 1. Base LSTM-AE
class BaseLSTMAE(nn.Module):
    def __init__(self, input_dim=8, hidden_dim=64, latent_dim=32, num_layers=2):
        super(BaseLSTMAE, self).__init__()
        self.encoder = nn.LSTM(input_dim, hidden_dim, num_layers=num_layers, batch_first=True, dropout=0.15)
        self.enc_linear = nn.Linear(hidden_dim, latent_dim)
        self.ln = nn.LayerNorm(latent_dim)
        self.act = nn.GELU()
        
        self.dec_linear = nn.Linear(latent_dim, hidden_dim)
        self.decoder = nn.LSTM(hidden_dim, hidden_dim, num_layers=num_layers, batch_first=True, dropout=0.15)
        self.out_linear = nn.Linear(hidden_dim, input_dim)

    def forward(self, x):
        batch_size, seq_len, _ = x.size()
        enc_out, _ = self.encoder(x)
        last_hidden = enc_out[:, -1, :]
        latent = self.act(self.ln(self.enc_linear(last_hidden)))
        
        dec_in = self.dec_linear(latent).unsqueeze(1).repeat(1, seq_len, 1)
        dec_out, _ = self.decoder(dec_in)
        return self.out_linear(dec_out)

# 2. Conv-BiLSTM AutoEncoder (Extracts multiscale spatial patterns + bidirectional temporal flow)
class ConvBiLSTMAE(nn.Module):
    def __init__(self, input_dim=8, hidden_dim=64, latent_dim=32):
        super(ConvBiLSTMAE, self).__init__()
        # 1D Convolution to extract local features
        self.conv1 = nn.Conv1d(input_dim, 32, kernel_size=3, padding=1)
        self.conv2 = nn.Conv1d(32, 64, kernel_size=3, padding=1)
        self.relu = nn.GELU()
        
        # BiLSTM Encoder
        self.encoder = nn.LSTM(64, hidden_dim, num_layers=1, batch_first=True, bidirectional=True)
        self.enc_linear = nn.Linear(hidden_dim * 2, latent_dim)
        self.ln = nn.LayerNorm(latent_dim)
        
        # Decoder
        self.dec_linear = nn.Linear(latent_dim, hidden_dim)
        self.decoder = nn.LSTM(hidden_dim, hidden_dim, num_layers=2, batch_first=True, dropout=0.1)
        self.out_linear = nn.Linear(hidden_dim, input_dim)

    def forward(self, x):
        # x: (Batch, Seq_Len, Input_Dim)
        batch_size, seq_len, _ = x.size()
        
        # Conv expects (Batch, Input_Dim, Seq_Len)
        c = x.permute(0, 2, 1)
        c = self.relu(self.conv1(c))
        c = self.relu(self.conv2(c))
        c = c.permute(0, 2, 1) # (Batch, Seq_Len, 64)
        
        enc_out, _ = self.encoder(c)
        last_hidden = enc_out[:, -1, :] # (Batch, Hidden_Dim*2)
        latent = self.relu(self.ln(self.enc_linear(last_hidden)))
        
        dec_in = self.dec_linear(latent).unsqueeze(1).repeat(1, seq_len, 1)
        dec_out, _ = self.decoder(dec_in)
        return self.out_linear(dec_out)

def train_model(model, train_loader, epochs=15, lr=1e-3, device='cpu'):
    model.to(device)
    optimizer = torch.optim.AdamW(model.parameters(), lr=lr, weight_decay=1e-4)
    criterion = nn.MSELoss()
    model.train()
    for ep in range(epochs):
        for batch_x in train_loader:
            bx = batch_x[0].to(device)
            optimizer.zero_grad()
            recon = model(bx)
            loss = criterion(recon, bx)
            loss.backward()
            optimizer.step()

def get_residuals_and_scores(model, X_windows, device='cpu'):
    model.to(device)
    model.eval()
    all_errs = []
    
    ds = TensorDataset(torch.tensor(X_windows, dtype=torch.float32))
    loader = DataLoader(ds, batch_size=128, shuffle=False)
    
    with torch.no_grad():
        for batch_x in loader:
            bx = batch_x[0].to(device)
            recon = model(bx)
            last_real = bx[:, -1, :]
            last_recon = recon[:, -1, :]
            err_per_dim = ((last_real - last_recon) ** 2).cpu().numpy()
            all_errs.append(err_per_dim)
            
    errs = np.vstack(all_errs)
    raw_score = np.mean(errs, axis=1)
    return raw_score, errs

def main():
    device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')
    print('Testing on device:', device)

    # 1. Load data
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

    print('Training Base LSTM-AE...')
    base_model = BaseLSTMAE(input_dim=8)
    train_model(base_model, tr_loader, epochs=15, lr=1e-3, device=device)

    print('Training Conv-BiLSTM AE...')
    conv_bilstm = ConvBiLSTMAE(input_dim=8)
    train_model(conv_bilstm, tr_loader, epochs=15, lr=1e-3, device=device)

    # Compute residuals on normal validation data to find variance per sensor
    v_norm_scores, v_norm_errs = get_residuals_and_scores(base_model, X_tr_w[-1000:], device=device)
    var_per_dim_base = np.var(v_norm_errs, axis=0) + 1e-4

    # Predictions
    v_raw_base, v_errs_base = get_residuals_and_scores(base_model, X_v_w, device=device)
    te_raw_base, te_errs_base = get_residuals_and_scores(base_model, X_te_w, device=device)

    v_raw_conv, v_errs_conv = get_residuals_and_scores(conv_bilstm, X_v_w, device=device)
    te_raw_conv, te_errs_conv = get_residuals_and_scores(conv_bilstm, X_te_w, device=device)

    # Strategy 1: Standard Base LSTM-AE
    th1 = find_best_threshold(y_v_w, v_raw_base)
    res1 = evaluate_predictions(y_te_w, te_raw_base, th1)
    print('1. Baseline Model B (LSTM-AE):', res1)

    # Strategy 2: Conv-BiLSTM AE
    th2 = find_best_threshold(y_v_w, v_raw_conv)
    res2 = evaluate_predictions(y_te_w, te_raw_conv, th2)
    print('2. Conv-BiLSTM AE:', res2)

    # Strategy 3: Base LSTM-AE + Mahalanobis / Variance Normalization
    v_mahal_base = np.sum(v_errs_base / var_per_dim_base, axis=1)
    te_mahal_base = np.sum(te_errs_base / var_per_dim_base, axis=1)
    th3 = find_best_threshold(y_v_w, v_mahal_base)
    res3 = evaluate_predictions(y_te_w, te_mahal_base, th3)
    print('3. Base LSTM-AE + Variance Normalization:', res3)

    # Strategy 4: Base LSTM-AE + Temporal Smoothing (Rolling Mean / EMA filter k=3, 5, 7)
    for k in [3, 5, 7, 9]:
        v_smooth = pd.Series(v_raw_base).rolling(k, min_periods=1).mean().values
        te_smooth = pd.Series(te_raw_base).rolling(k, min_periods=1).mean().values
        th4 = find_best_threshold(y_v_w, v_smooth)
        res4 = evaluate_predictions(y_te_w, te_smooth, th4)
        print(f'4. Base LSTM-AE + Rolling Mean (k={k}):', res4)

    # Strategy 5: Conv-BiLSTM + Temporal Smoothing (k=3, 5, 7)
    for k in [3, 5, 7, 9]:
        v_smooth_c = pd.Series(v_raw_conv).rolling(k, min_periods=1).mean().values
        te_smooth_c = pd.Series(te_raw_conv).rolling(k, min_periods=1).mean().values
        th5 = find_best_threshold(y_v_w, v_smooth_c)
        res5 = evaluate_predictions(y_te_w, te_smooth_c, th5)
        print(f'5. Conv-BiLSTM + Rolling Mean (k={k}):', res5)

    # Strategy 6: Sensor-Focused / Selective Key Sensor Score
    # Remember from EDA: Volume Flow Rate (idx 7), Acc1 (idx 0), Acc2 (idx 1), Current (idx 2), Temp (idx 4)
    # Let's test weighted score:
    key_weights = np.array([2.0, 2.0, 1.0, 0.5, 1.5, 0.5, 0.2, 3.0])
    v_weighted = np.dot(v_errs_base, key_weights)
    te_weighted = np.dot(te_errs_base, key_weights)
    th6 = find_best_threshold(y_v_w, v_weighted)
    res6 = evaluate_predictions(y_te_w, te_weighted, th6)
    print('6. Key-Weighted Error Score:', res6)

    for k in [3, 5]:
        v_w_s = pd.Series(v_weighted).rolling(k, min_periods=1).mean().values
        te_w_s = pd.Series(te_weighted).rolling(k, min_periods=1).mean().values
        th6_s = find_best_threshold(y_v_w, v_w_s)
        res6_s = evaluate_predictions(y_te_w, te_w_s, th6_s)
        print(f'6. Key-Weighted + Rolling ({k}):', res6_s)

if __name__ == '__main__':
    main()
