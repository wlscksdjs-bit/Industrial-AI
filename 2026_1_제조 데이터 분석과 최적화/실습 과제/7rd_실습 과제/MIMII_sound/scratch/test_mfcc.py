import os
import glob
import torch
import torch.nn as nn
import numpy as np
import librosa
from sklearn.metrics import precision_recall_curve
from torch.utils.data import Dataset, DataLoader

device = torch.device('cuda' if torch.cuda.is_available() else 'mps' if torch.backends.mps.is_available() else 'cpu')

class MIMIIDF(Dataset):
    def __init__(self, file_paths):
        self.data = []
        for path in file_paths:
            y, _ = librosa.load(path, sr=16000)
            # Use MFCC for noise robustness
            mfcc = librosa.feature.mfcc(y=y, sr=16000, n_mfcc=40, n_mels=128, hop_length=512)
            # Normalize MFCC per file (standardization)
            mfcc = (mfcc - np.mean(mfcc)) / (np.std(mfcc) + 1e-6)
            
            context = 5
            for i in range(mfcc.shape[1] - context + 1):
                chunk = mfcc[:, i:i+context].flatten()
                self.data.append(chunk)
        self.data = np.array(self.data, dtype=np.float32)

    def __len__(self):
        return len(self.data)

    def __getitem__(self, idx):
        return self.data[idx]

normal_files = sorted(glob.glob('0_dB_valve/valve/id_02/normal/*.wav'))
train_files = normal_files[:500]
test_normal = normal_files[500:]
test_abnormal = glob.glob('0_dB_valve/valve/id_02/abnormal/*.wav')

train_dataset = MIMIIDF(train_files)
train_loader = DataLoader(train_dataset, batch_size=256, shuffle=True)

class DenseAE(nn.Module):
    def __init__(self):
        super().__init__()
        self.encoder = nn.Sequential(
            nn.Linear(200, 128), nn.BatchNorm1d(128), nn.ReLU(),
            nn.Linear(128, 64), nn.BatchNorm1d(64), nn.ReLU(),
            nn.Linear(64, 16), nn.BatchNorm1d(16), nn.ReLU()
        )
        self.decoder = nn.Sequential(
            nn.Linear(16, 64), nn.BatchNorm1d(64), nn.ReLU(),
            nn.Linear(64, 128), nn.BatchNorm1d(128), nn.ReLU(),
            nn.Linear(128, 200)
        )
    def forward(self, x):
        return self.decoder(self.encoder(x))

model = DenseAE().to(device)
optimizer = torch.optim.Adam(model.parameters(), lr=1e-3)
criterion = nn.MSELoss()

for epoch in range(10): # Quick train
    model.train()
    for batch in train_loader:
        batch = batch.to(device)
        pred = model(batch)
        loss = criterion(pred, batch)
        optimizer.zero_grad()
        loss.backward()
        optimizer.step()

model.eval()

def smooth(x, window_len=10):
    if len(x) < window_len: return x
    s = np.r_[x[window_len-1:0:-1], x, x[-2:-window_len-1:-1]]
    w = np.ones(window_len,'d')
    y = np.convolve(w/w.sum(), s, mode='valid')
    return y[(window_len//2-1):-(window_len//2)]

def get_errors(file_paths):
    errors_max = []
    errors_mean = []
    errors_smoothed_max = []
    for path in file_paths:
        y, _ = librosa.load(path, sr=16000)
        mfcc = librosa.feature.mfcc(y=y, sr=16000, n_mfcc=40, n_mels=128, hop_length=512)
        mfcc = (mfcc - np.mean(mfcc)) / (np.std(mfcc) + 1e-6)
        
        context = 5
        chunks = []
        if mfcc.shape[1] >= context:
            for i in range(mfcc.shape[1] - context + 1):
                chunks.append(mfcc[:, i:i+context].flatten())
            chunks = torch.tensor(np.array(chunks), dtype=torch.float32).to(device)
            with torch.no_grad():
                preds = model(chunks)
                loss = torch.mean((preds - chunks)**2, dim=1).cpu().numpy()
                errors_max.append(np.max(loss))
                errors_mean.append(np.mean(loss))
                errors_smoothed_max.append(np.max(smooth(loss, 15)))
        else:
            errors_max.append(0)
            errors_mean.append(0)
            errors_smoothed_max.append(0)
    return errors_max, errors_mean, errors_smoothed_max

n_max, n_mean, n_smax = get_errors(test_normal)
a_max, a_mean, a_smax = get_errors(test_abnormal)

y_true = np.concatenate([np.zeros(len(n_max)), np.ones(len(a_max))])

for name, n_s, a_s in [('Max', n_max, a_max), ('Mean', n_mean, a_mean), ('Smoothed Max', n_smax, a_smax)]:
    y_scores = np.concatenate([n_s, a_s])
    p, r, t = precision_recall_curve(y_true, y_scores)
    f1 = 2 * (p * r) / (p + r + 1e-8)
    print(f"MFCC Dense {name: <15} F1: {np.max(f1):.4f}")
