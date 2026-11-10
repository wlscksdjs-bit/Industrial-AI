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

# =========================================================================
# Architecture 1: Memory-Augmented AutoEncoder (MemAE)
# (ICCV 2019 Gong et al. - Solves deep AE over-generalization on anomalies)
# =========================================================================
class MemoryModule(nn.Module):
    def __init__(self, mem_dim=100, fea_dim=32, shrink_thres=0.0025):
        super(MemoryModule, self).__init__()
        self.mem_dim = mem_dim
        self.fea_dim = fea_dim
        self.shrink_thres = shrink_thres
        self.weight = nn.Parameter(torch.Tensor(mem_dim, fea_dim))
        self.reset_parameters()

    def reset_parameters(self):
        stdv = 1. / np.sqrt(self.weight.size(1))
        self.weight.data.uniform_(-stdv, stdv)

    def forward(self, z):
        # z: (Batch, fea_dim)
        # Cosine similarity or dot product
        att_weight = F.linear(z, self.weight)  # (Batch, mem_dim)
        att_weight = F.softmax(att_weight, dim=1)
        
        # Hard thresholding / shrinkage to promote sparsity
        if self.shrink_thres > 0:
            att_weight = F.relu(att_weight - self.shrink_thres)
            att_weight = att_weight / (torch.sum(att_weight, dim=1, keepdim=True) + 1e-8)
            
        mem_z = F.linear(att_weight, self.weight.t())  # (Batch, fea_dim)
        return mem_z, att_weight

class MemAE(nn.Module):
    def __init__(self, input_dim=8, hidden_dim=64, latent_dim=32, mem_dim=50):
        super(MemAE, self).__init__()
        self.encoder = nn.LSTM(input_dim, hidden_dim, num_layers=2, batch_first=True, dropout=0.1)
        self.enc_fc = nn.Linear(hidden_dim, latent_dim)
        self.mem = MemoryModule(mem_dim=mem_dim, fea_dim=latent_dim, shrink_thres=0.002)
        self.dec_fc = nn.Linear(latent_dim, hidden_dim)
        self.decoder = nn.LSTM(hidden_dim, hidden_dim, num_layers=2, batch_first=True, dropout=0.1)
        self.out_fc = nn.Linear(hidden_dim, input_dim)

    def forward(self, x):
        B, L, _ = x.size()
        out, _ = self.encoder(x)
        z = self.enc_fc(out[:, -1, :])
        mem_z, att = self.mem(z)
        
        dec_in = self.dec_fc(mem_z).unsqueeze(1).repeat(1, L, 1)
        dec_out, _ = self.decoder(dec_in)
        recon = self.out_fc(dec_out)
        return recon, att

# =========================================================================
# Architecture 2: Graph Deviation Network + Temporal AutoEncoder (GDN-AE)
# (KDD 2021 Deng & Hooi - Multi-sensor relationship learning)
# =========================================================================
class GraphCorrelationLayer(nn.Module):
    def __init__(self, num_nodes=8, embedding_dim=16):
        super(GraphCorrelationLayer, self).__init__()
        self.embedding = nn.Embedding(num_nodes, embedding_dim)
        self.lin_proj = nn.Linear(embedding_dim, embedding_dim)

    def forward(self):
        # Learn directed dynamic graph adjacency
        nodes = torch.arange(8)
        emb = self.embedding(nodes)
        A = torch.mm(emb, self.lin_proj(emb).t())
        A = F.softmax(F.relu(A), dim=-1)
        return A

class GraphTemporalAE(nn.Module):
    def __init__(self, input_dim=8, hidden_dim=64, latent_dim=32):
        super(GraphTemporalAE, self).__init__()
        self.graph = GraphCorrelationLayer(num_nodes=input_dim, embedding_dim=16)
        self.temporal_enc = nn.LSTM(input_dim, hidden_dim, num_layers=2, batch_first=True, dropout=0.1)
        self.enc_fc = nn.Linear(hidden_dim, latent_dim)
        
        self.dec_fc = nn.Linear(latent_dim, hidden_dim)
        self.decoder = nn.LSTM(hidden_dim, hidden_dim, num_layers=2, batch_first=True, dropout=0.1)
        self.out_fc = nn.Linear(hidden_dim, input_dim)

    def forward(self, x):
        # x: (B, L, D)
        B, L, D = x.size()
        A = self.graph() # (D, D)
        
        # Spatial Graph convolution on each time step
        # x_spatial: (B, L, D) * (D, D) -> (B, L, D)
        x_g = torch.matmul(x, A)
        x_comb = x + x_g
        
        enc_out, _ = self.temporal_enc(x_comb)
        z = torch.relu(self.enc_fc(enc_out[:, -1, :]))
        
        dec_in = self.dec_fc(z).unsqueeze(1).repeat(1, L, 1)
        dec_out, _ = self.decoder(dec_in)
        recon = self.out_fc(dec_out)
        return recon, A

# =========================================================================
# Architecture 3: Multi-Scale Trend-Residual Decoupled AutoEncoder (TRD-AE)
# (Separating low-frequency physical trend from high-frequency shock vibration)
# =========================================================================
class TrendResidualAE(nn.Module):
    def __init__(self, input_dim=8, hidden_dim=64, latent_dim=32):
        super(TrendResidualAE, self).__init__()
        # Trend branch (moving average pool filter)
        self.pool = nn.AvgPool1d(kernel_size=5, stride=1, padding=2)
        self.trend_lstm = nn.LSTM(input_dim, hidden_dim, num_layers=1, batch_first=True)
        self.trend_fc = nn.Linear(hidden_dim, latent_dim // 2)
        
        # Residual branch (high-pass vibration detail)
        self.res_lstm = nn.LSTM(input_dim, hidden_dim, num_layers=1, batch_first=True)
        self.res_fc = nn.Linear(hidden_dim, latent_dim // 2)
        
        # Joint Decoder
        self.dec_fc = nn.Linear(latent_dim, hidden_dim)
        self.decoder = nn.LSTM(hidden_dim, hidden_dim, num_layers=2, batch_first=True, dropout=0.1)
        self.out_fc = nn.Linear(hidden_dim, input_dim)

    def forward(self, x):
        B, L, D = x.size()
        # x permuted for conv/pool: (B, D, L)
        trend = self.pool(x.permute(0, 2, 1)).permute(0, 2, 1)
        resid = x - trend
        
        t_out, _ = self.trend_lstm(trend)
        z_t = self.trend_fc(t_out[:, -1, :])
        
        r_out, _ = self.res_lstm(resid)
        z_r = self.res_fc(r_out[:, -1, :])
        
        z = torch.cat([z_t, z_r], dim=-1)
        dec_in = self.dec_fc(z).unsqueeze(1).repeat(1, L, 1)
        dec_out, _ = self.decoder(dec_in)
        recon = self.out_fc(dec_out)
        return recon

# =========================================================================
# Architecture 4: Novel Proposed SOTA: 
# Physics-Informed Memory-Graph Spatio-Temporal Network (PIMG-Net)
# Combining:
# 1. Unsupervised Sensor Precision/Uncertainty Learning (Homoscedastic Loss)
# 2. Graph Adjacency Relational Modeling
# 3. Memory Matrix Sparsity Bottleneck (Zero Over-generalization)
# 4. Multi-Scale Temporal Diffusion/Smoothing
# =========================================================================
class PIMGNet(nn.Module):
    def __init__(self, input_dim=8, hidden_dim=64, latent_dim=32, mem_dim=40):
        super(PIMGNet, self).__init__()
        # 1. Graph correlation
        self.graph = GraphCorrelationLayer(num_nodes=input_dim, embedding_dim=16)
        
        # 2. Bidirectional Temporal Encoder
        self.bilstm = nn.LSTM(input_dim, hidden_dim, num_layers=1, batch_first=True, bidirectional=True)
        self.enc_fc = nn.Linear(hidden_dim * 2, latent_dim)
        
        # 3. Memory bank module
        self.mem = MemoryModule(mem_dim=mem_dim, fea_dim=latent_dim, shrink_thres=0.003)
        
        # 4. Decoder
        self.dec_fc = nn.Linear(latent_dim, hidden_dim)
        self.decoder = nn.LSTM(hidden_dim, hidden_dim, num_layers=2, batch_first=True, dropout=0.1)
        self.out_fc = nn.Linear(hidden_dim, input_dim)
        
        # 5. Learnable Sensor Uncertainty log(sigma^2) strictly on normal data
        self.log_vars = nn.Parameter(torch.zeros(input_dim))

    def forward(self, x):
        B, L, D = x.size()
        A = self.graph()
        x_g = torch.matmul(x, A)
        x_comb = x + 0.5 * x_g
        
        out, _ = self.bilstm(x_comb)
        z = self.enc_fc(out[:, -1, :])
        mem_z, att = self.mem(z)
        
        dec_in = self.dec_fc(mem_z).unsqueeze(1).repeat(1, L, 1)
        dec_out, _ = self.decoder(dec_in)
        recon = self.out_fc(dec_out)
        return recon, att, A

def main():
    device = torch.device('cpu')
    print("=== Exploring Novel SOTA Architectures for Industrial Anomaly Detection ===", flush=True)

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

    def train_and_eval(model_name, model, loss_type='mse', epochs=15):
        print(f"\n[Training {model_name}]...", flush=True)
        t0 = time.time()
        optimizer = torch.optim.AdamW(model.parameters(), lr=1e-3, weight_decay=1e-4)
        
        for ep in range(epochs):
            model.train()
            for batch in tr_loader:
                bx = batch[0].to(device)
                optimizer.zero_grad()
                
                if model_name == 'MemAE':
                    recon, att = model(bx)
                    # MSE + Entropy sparsity loss on memory addressing
                    entropy_loss = -torch.mean(torch.sum(att * torch.log(att + 1e-12), dim=1))
                    loss = F.mse_loss(recon, bx) + 0.0002 * entropy_loss
                elif model_name == 'GraphTemporalAE':
                    recon, A = model(bx)
                    # Graph smoothness regularization
                    loss = F.mse_loss(recon, bx) + 0.001 * torch.norm(A, p=1)
                elif model_name == 'TrendResidualAE':
                    recon = model(bx)
                    loss = F.mse_loss(recon, bx)
                elif model_name == 'PIMGNet':
                    recon, att, A = model(bx)
                    # Homoscedastic uncertainty loss
                    precisions = torch.exp(-model.log_vars)
                    diff = (bx - recon) ** 2
                    uncertainty_loss = torch.mean(torch.sum(precisions * diff + model.log_vars, dim=-1))
                    entropy_loss = -torch.mean(torch.sum(att * torch.log(att + 1e-12), dim=1))
                    loss = uncertainty_loss + 0.0002 * entropy_loss + 0.001 * torch.norm(A, p=1)
                else:
                    recon = model(bx)
                    loss = F.mse_loss(recon, bx)
                    
                loss.backward()
                optimizer.step()
                
        train_time = time.time() - t0
        print(f" -> Trained in {train_time:.2f}s", flush=True)

        # Evaluate
        model.eval()
        def get_model_errs(X_data):
            ds = TensorDataset(torch.tensor(X_data, dtype=torch.float32))
            ld = DataLoader(ds, batch_size=128, shuffle=False)
            all_errs = []
            with torch.no_grad():
                for b in ld:
                    bx = b[0].to(device)
                    if model_name == 'MemAE':
                        recon, _ = model(bx)
                    elif model_name == 'GraphTemporalAE':
                        recon, _ = model(bx)
                    elif model_name == 'PIMGNet':
                        recon, _, _ = model(bx)
                    else:
                        recon = model(bx)
                    err = ((bx[:, -1, :] - recon[:, -1, :]) ** 2).cpu().numpy()
                    all_errs.append(err)
            return np.vstack(all_errs)

        v_errs = get_model_errs(X_v_w)
        te_errs = get_model_errs(X_te_w)

        # 1. Raw unweighted score
        v_raw = np.mean(v_errs, axis=1)
        te_raw = np.mean(te_errs, axis=1)
        th_raw = find_best_threshold(y_v_w, v_raw)
        res_raw = evaluate_predictions(y_te_w, te_raw, th_raw)
        print(f"   [{model_name} Raw]: F1={res_raw['f1_raw']} | Prec={res_raw['prec_raw']} | Rec={res_raw['rec_raw']} | AUPRC={res_raw['auprc']} | F1(PA)={res_raw['f1_pa']}", flush=True)

        # 2. Physics-weighted + Temporal Filter k=5
        key_weights = np.array([2.0, 2.0, 1.0, 0.5, 1.5, 0.5, 0.2, 3.0])
        v_w = np.dot(v_errs, key_weights)
        te_w = np.dot(te_errs, key_weights)
        
        for k in [3, 5, 7]:
            v_s = pd.Series(v_w).rolling(k, min_periods=1).mean().values
            te_s = pd.Series(te_w).rolling(k, min_periods=1).mean().values
            th_s = find_best_threshold(y_v_w, v_s)
            res_s = evaluate_predictions(y_te_w, te_s, th_s)
            print(f"   [{model_name} + Weight + Rolling(k={k})]: F1={res_s['f1_raw']} | Prec={res_s['prec_raw']} | Rec={res_s['rec_raw']} | AUPRC={res_s['auprc']} | F1(PA)={res_s['f1_pa']}", flush=True)

        if model_name == 'PIMGNet':
            # Also test purely learned uncertainty weighting without manual weights!
            learn_prec = torch.exp(-model.log_vars).detach().cpu().numpy()
            print(f"   Learned Sensor Precisions: {learn_prec}", flush=True)
            v_auto = np.dot(v_errs, learn_prec)
            te_auto = np.dot(te_errs, learn_prec)
            for k in [3, 5]:
                v_as = pd.Series(v_auto).rolling(k, min_periods=1).mean().values
                te_as = pd.Series(te_auto).rolling(k, min_periods=1).mean().values
                th_as = find_best_threshold(y_v_w, v_as)
                res_as = evaluate_predictions(y_te_w, te_as, th_as)
                print(f"   [{model_name} Fully-Unsupervised (Learned Weights) Rolling(k={k})]: F1={res_as['f1_raw']} | Prec={res_as['prec_raw']} | Rec={res_as['rec_raw']} | AUPRC={res_as['auprc']} | F1(PA)={res_as['f1_pa']}", flush=True)

        return res_raw

    # Run experiments
    memae = MemAE(input_dim=8, hidden_dim=64, latent_dim=32, mem_dim=50)
    train_and_eval('MemAE', memae, epochs=15)

    gta = GraphTemporalAE(input_dim=8, hidden_dim=64, latent_dim=32)
    train_and_eval('GraphTemporalAE', gta, epochs=15)

    trd = TrendResidualAE(input_dim=8, hidden_dim=64, latent_dim=32)
    train_and_eval('TrendResidualAE', trd, epochs=15)

    pimg = PIMGNet(input_dim=8, hidden_dim=64, latent_dim=32, mem_dim=40)
    train_and_eval('PIMGNet', pimg, epochs=15)

if __name__ == '__main__':
    main()
