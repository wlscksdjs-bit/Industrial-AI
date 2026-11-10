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
    except:
        auroc = 0.5
        
    y_pred_pa = apply_point_adjustment(y_true, y_pred)
    prec_pa = float(precision_score(y_true, y_pred_pa, zero_division=0))
    rec_pa = float(recall_score(y_true, y_pred_pa, zero_division=0))
    f1_pa = float(f1_score(y_true, y_pred_pa, zero_division=0))
    
    return {
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

# ==========================================
# 1. Base LSTM AutoEncoder (Model B)
# ==========================================
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

# ==========================================
# 2. USAD (KDD 2020) Architecture
# Unsupervised Anomaly Detection with Dual Adversarial Decoders
# ==========================================
class USAD(nn.Module):
    def __init__(self, w_size=30*8, z_size=64):
        super(USAD, self).__init__()
        self.encoder = nn.Sequential(
            nn.Linear(w_size, 256),
            nn.ReLU(),
            nn.Linear(256, 128),
            nn.ReLU(),
            nn.Linear(128, z_size),
            nn.ReLU()
        )
        self.decoder1 = nn.Sequential(
            nn.Linear(z_size, 128),
            nn.ReLU(),
            nn.Linear(128, 256),
            nn.ReLU(),
            nn.Linear(256, w_size)
        )
        self.decoder2 = nn.Sequential(
            nn.Linear(z_size, 128),
            nn.ReLU(),
            nn.Linear(128, 256),
            nn.ReLU(),
            nn.Linear(256, w_size)
        )

    def forward(self, w):
        z = self.encoder(w)
        w1 = self.decoder1(z)
        w2 = self.decoder2(z)
        w3 = self.decoder2(self.encoder(w1))
        return w1, w2, w3

# ==========================================
# 3. Recurrent USAD (Temporal USAD with LSTM backbone)
# Combining Sequence Modeling + Dual Adversarial Decoders
# ==========================================
class RecurrentUSAD(nn.Module):
    def __init__(self, input_dim=8, hidden_dim=64, z_dim=32):
        super(RecurrentUSAD, self).__init__()
        self.encoder = nn.LSTM(input_dim, hidden_dim, num_layers=2, batch_first=True, dropout=0.1)
        self.enc_fc = nn.Linear(hidden_dim, z_dim)
        
        # Decoder 1
        self.dec1_fc = nn.Linear(z_dim, hidden_dim)
        self.decoder1 = nn.LSTM(hidden_dim, hidden_dim, num_layers=2, batch_first=True, dropout=0.1)
        self.out1 = nn.Linear(hidden_dim, input_dim)
        
        # Decoder 2 (Adversarial)
        self.dec2_fc = nn.Linear(z_dim, hidden_dim)
        self.decoder2 = nn.LSTM(hidden_dim, hidden_dim, num_layers=2, batch_first=True, dropout=0.1)
        self.out2 = nn.Linear(hidden_dim, input_dim)

    def encode(self, x):
        out, _ = self.encoder(x)
        return torch.relu(self.enc_fc(out[:, -1, :]))

    def decode1(self, z, seq_len):
        h = self.dec1_fc(z).unsqueeze(1).repeat(1, seq_len, 1)
        out, _ = self.decoder1(h)
        return self.out1(out)

    def decode2(self, z, seq_len):
        h = self.dec2_fc(z).unsqueeze(1).repeat(1, seq_len, 1)
        out, _ = self.decoder2(h)
        return self.out2(out)

    def forward(self, x):
        seq_len = x.size(1)
        z = self.encode(x)
        w1 = self.decode1(z, seq_len)
        w2 = self.decode2(z, seq_len)
        w3 = self.decode2(self.encode(w1), seq_len)
        return w1, w2, w3

# ==========================================
# 4. Anomaly Transformer-inspired Association Discrepancy AE
# (Xu et al., ICLR 2022)
# ==========================================
class AnomalyTransformerAE(nn.Module):
    def __init__(self, input_dim=8, d_model=64, n_heads=4, seq_len=30):
        super(AnomalyTransformerAE, self).__init__()
        self.seq_len = seq_len
        self.input_proj = nn.Linear(input_dim, d_model)
        self.pos_emb = nn.Parameter(torch.randn(1, seq_len, d_model) * 0.02)
        
        # Self-attention (Series association)
        self.mha = nn.MultiheadAttention(embed_dim=d_model, num_heads=n_heads, batch_first=True)
        self.ln1 = nn.LayerNorm(d_model)
        
        # Prior association parameter: learnable Gaussian scale sigma
        self.sigma = nn.Parameter(torch.ones(1, n_heads, seq_len, 1))
        
        # Feed-forward
        self.ffn = nn.Sequential(
            nn.Linear(d_model, d_model * 2),
            nn.GELU(),
            nn.Linear(d_model * 2, d_model)
        )
        self.ln2 = nn.LayerNorm(d_model)
        self.out_proj = nn.Linear(d_model, input_dim)

    def forward(self, x):
        B, L, D = x.size()
        h = self.input_proj(x) + self.pos_emb[:, :L, :]
        
        # Series attention
        attn_out, attn_weights = self.mha(h, h, h, average_attn_weights=False) # (B, heads, L, L)
        h = self.ln1(h + attn_out)
        
        # Feed forward
        h = self.ln2(h + self.ffn(h))
        recon = self.out_proj(h)
        
        # Prior association: Gaussian kernel based on temporal distance |i - j|
        distances = torch.abs(torch.arange(L).unsqueeze(0) - torch.arange(L).unsqueeze(1)).float().to(x.device)
        # distances: (L, L)
        sigma = torch.clamp(self.sigma, min=0.1) # (1, heads, L, 1)
        prior_attn = torch.exp(- (distances.unsqueeze(0).unsqueeze(0) ** 2) / (2 * (sigma ** 2)))
        prior_attn = prior_attn / (torch.sum(prior_attn, dim=-1, keepdim=True) + 1e-8)
        
        # Association Discrepancy (KL divergence between Prior and Series attention)
        # series attn: (B, heads, L, L)
        eps = 1e-8
        series_attn = torch.clamp(attn_weights, min=eps)
        prior_attn = torch.clamp(prior_attn, min=eps)
        
        kl_prior_series = torch.sum(prior_attn * (torch.log(prior_attn) - torch.log(series_attn)), dim=-1)
        kl_series_prior = torch.sum(series_attn * (torch.log(series_attn) - torch.log(prior_attn)), dim=-1)
        ass_dis = (kl_prior_series + kl_series_prior).mean(dim=1) # (B, L)
        
        return recon, ass_dis

def train_usad(model, dataloader, epochs=15, lr=1e-3, device='cpu', is_flat=True):
    model.to(device)
    opt1 = torch.optim.AdamW(list(model.encoder.parameters()) + list(model.decoder1.parameters()), lr=lr, weight_decay=1e-4)
    opt2 = torch.optim.AdamW(list(model.encoder.parameters()) + list(model.decoder2.parameters()), lr=lr, weight_decay=1e-4)
    
    for epoch in range(epochs):
        n = epoch + 1
        for batch in dataloader:
            bx = batch[0].to(device)
            if is_flat:
                bx_flat = bx.view(bx.size(0), -1)
                inp = bx_flat
            else:
                inp = bx
                
            # Phase 1: Train AE1
            w1, w2, w3 = model(inp)
            loss1 = (1.0 / n) * torch.mean((inp - w1)**2) + (1.0 - 1.0 / n) * torch.mean((inp - w3)**2)
            opt1.zero_grad()
            loss1.backward()
            opt1.step()
            
            # Phase 2: Train AE2
            w1, w2, w3 = model(inp)
            loss2 = (1.0 / n) * torch.mean((inp - w2)**2) - (1.0 - 1.0 / n) * torch.mean((inp - w3)**2)
            opt2.zero_grad()
            loss2.backward()
            opt2.step()

def evaluate_usad(model, X_windows, device='cpu', is_flat=True, alpha=0.5, beta=0.5):
    model.to(device)
    model.eval()
    ds = TensorDataset(torch.tensor(X_windows, dtype=torch.float32))
    loader = DataLoader(ds, batch_size=128, shuffle=False)
    scores = []
    
    with torch.no_grad():
        for batch in loader:
            bx = batch[0].to(device)
            if is_flat:
                bx_flat = bx.view(bx.size(0), -1)
                w1, w2, w3 = model(bx_flat)
                # Anomaly score per sample
                err1 = torch.mean((bx_flat - w1)**2, dim=1)
                err2 = torch.mean((bx_flat - w3)**2, dim=1)
            else:
                w1, w2, w3 = model(bx)
                err1 = torch.mean((bx[:, -1, :] - w1[:, -1, :])**2, dim=1)
                err2 = torch.mean((bx[:, -1, :] - w3[:, -1, :])**2, dim=1)
                
            score = alpha * err1 + beta * err2
            scores.extend(score.cpu().numpy())
            
    return np.array(scores)

def train_anomaly_transformer(model, dataloader, epochs=15, lr=1e-3, device='cpu'):
    model.to(device)
    optimizer = torch.optim.AdamW(model.parameters(), lr=lr, weight_decay=1e-4)
    criterion = nn.MSELoss()
    
    for epoch in range(epochs):
        for batch in dataloader:
            bx = batch[0].to(device)
            optimizer.zero_grad()
            recon, ass_dis = model(bx)
            
            recon_loss = criterion(recon, bx)
            # Minimax optimization on association discrepancy
            dis_loss = -torch.mean(ass_dis)
            loss = recon_loss + 0.01 * dis_loss
            loss.backward()
            optimizer.step()

def evaluate_anomaly_transformer(model, X_windows, device='cpu'):
    model.to(device)
    model.eval()
    ds = TensorDataset(torch.tensor(X_windows, dtype=torch.float32))
    loader = DataLoader(ds, batch_size=128, shuffle=False)
    scores = []
    
    with torch.no_grad():
        for batch in loader:
            bx = batch[0].to(device)
            recon, ass_dis = model(bx)
            recon_err = torch.mean((bx[:, -1, :] - recon[:, -1, :])**2, dim=1)
            dis_val = ass_dis[:, -1]
            # SOTA Anomaly score: Energy = ReconError * Softmax(-AssDis)
            score = recon_err * (1.0 + torch.relu(dis_val))
            scores.extend(score.cpu().numpy())
            
    return np.array(scores)

def main():
    device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')
    print('Evaluating SOTA Architectures on device:', device)

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

    print("\n--- Training Standard USAD (KDD 2020) ---")
    t0 = time.time()
    usad_flat = USAD(w_size=30*8, z_size=64)
    train_usad(usad_flat, tr_loader, epochs=15, lr=1e-3, device=device, is_flat=True)
    t_usad = time.time() - t0
    print(f"USAD trained in {t_usad:.2f}s")
    
    v_scores_usad = evaluate_usad(usad_flat, X_v_w, device=device, is_flat=True)
    te_scores_usad = evaluate_usad(usad_flat, X_te_w, device=device, is_flat=True)
    th_usad = find_best_threshold(y_v_w, v_scores_usad)
    res_usad = evaluate_predictions(y_te_w, te_scores_usad, th_usad)
    print("USAD (Raw):", res_usad)
    
    # USAD + Temporal Filter
    for k in [3, 5]:
        v_s = pd.Series(v_scores_usad).rolling(k, min_periods=1).mean().values
        te_s = pd.Series(te_scores_usad).rolling(k, min_periods=1).mean().values
        th = find_best_threshold(y_v_w, v_s)
        print(f"USAD + Temporal Filter (k={k}):", evaluate_predictions(y_te_w, te_s, th))

    print("\n--- Training Recurrent USAD (Temporal Dual Adversarial AE) ---")
    t0 = time.time()
    rec_usad = RecurrentUSAD(input_dim=8, hidden_dim=64, z_dim=32)
    train_usad(rec_usad, tr_loader, epochs=15, lr=1e-3, device=device, is_flat=False)
    t_rec = time.time() - t0
    print(f"Recurrent USAD trained in {t_rec:.2f}s")
    
    v_scores_rec = evaluate_usad(rec_usad, X_v_w, device=device, is_flat=False)
    te_scores_rec = evaluate_usad(rec_usad, X_te_w, device=device, is_flat=False)
    th_rec = find_best_threshold(y_v_w, v_scores_rec)
    res_rec = evaluate_predictions(y_te_w, te_scores_rec, th_rec)
    print("Recurrent USAD (Raw):", res_rec)
    
    for k in [3, 5]:
        v_s = pd.Series(v_scores_rec).rolling(k, min_periods=1).mean().values
        te_s = pd.Series(te_scores_rec).rolling(k, min_periods=1).mean().values
        th = find_best_threshold(y_v_w, v_s)
        print(f"Recurrent USAD + Temporal Filter (k={k}):", evaluate_predictions(y_te_w, te_s, th))

    print("\n--- Training Anomaly Transformer (ICLR 2022) ---")
    t0 = time.time()
    at_model = AnomalyTransformerAE(input_dim=8, d_model=64, n_heads=4, seq_len=30)
    train_anomaly_transformer(at_model, tr_loader, epochs=15, lr=1e-3, device=device)
    t_at = time.time() - t0
    print(f"Anomaly Transformer trained in {t_at:.2f}s")
    
    v_scores_at = evaluate_anomaly_transformer(at_model, X_v_w, device=device)
    te_scores_at = evaluate_anomaly_transformer(at_model, X_te_w, device=device)
    th_at = find_best_threshold(y_v_w, v_scores_at)
    res_at = evaluate_predictions(y_te_w, te_scores_at, th_at)
    print("Anomaly Transformer (Raw):", res_at)
    
    for k in [3, 5]:
        v_s = pd.Series(v_scores_at).rolling(k, min_periods=1).mean().values
        te_s = pd.Series(te_scores_at).rolling(k, min_periods=1).mean().values
        th = find_best_threshold(y_v_w, v_s)
        print(f"Anomaly Transformer + Temporal Filter (k={k}):", evaluate_predictions(y_te_w, te_s, th))

if __name__ == '__main__':
    main()
