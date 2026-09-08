import os
import glob
import torch
import torch.nn as nn
import numpy as np
import librosa
from sklearn.metrics import precision_recall_curve
from torch.utils.data import Dataset, DataLoader

device = torch.device('cuda' if torch.cuda.is_available() else 'mps' if torch.backends.mps.is_available() else 'cpu')

class MIMIIDenoisingDataset(Dataset):
    def __init__(self, file_paths):
        self.data = []
        for path in file_paths:
            y, _ = librosa.load(path, sr=16000)
            
            # Use MFCC + Delta
            mfcc = librosa.feature.mfcc(y=y, sr=16000, n_mfcc=40, n_mels=128, hop_length=512)
            mfcc_delta = librosa.feature.delta(mfcc)
            
            # Concat along features
            feat = np.concatenate([mfcc, mfcc_delta], axis=0) # Shape: 80 x frames
            
            feat = (feat - np.mean(feat)) / (np.std(feat) + 1e-6)
            
            context = 7 # Larger context window
            for i in range(feat.shape[1] - context + 1):
                chunk = feat[:, i:i+context].flatten()
                self.data.append(chunk)
        self.data = np.array(self.data, dtype=np.float32)

    def __len__(self):
        return len(self.data)

    def __getitem__(self, idx):
        return self.data[idx]

normal_files = sorted(glob.glob('0_dB_valve/valve/id_02/normal/*.wav'))
train_files = normal_files[:500]
test_normal = normal_files[500:]
test_abnormal = sorted(glob.glob('0_dB_valve/valve/id_02/abnormal/*.wav'))

train_dataset = MIMIIDenoisingDataset(train_files)
train_loader = DataLoader(train_dataset, batch_size=256, shuffle=True)

class DAE(nn.Module):
    def __init__(self):
        super().__init__()
        # Input size: 80 feat * 7 context = 560
        self.encoder = nn.Sequential(
            nn.Linear(560, 256), nn.BatchNorm1d(256), nn.ReLU(),
            nn.Linear(256, 128), nn.BatchNorm1d(128), nn.ReLU(),
            nn.Linear(128, 32), nn.BatchNorm1d(32), nn.ReLU()
        )
        self.decoder = nn.Sequential(
            nn.Linear(32, 128), nn.BatchNorm1d(128), nn.ReLU(),
            nn.Linear(128, 256), nn.BatchNorm1d(256), nn.ReLU(),
            nn.Linear(256, 560)
        )
    def forward(self, x):
        return self.decoder(self.encoder(x))

model = DAE().to(device)
optimizer = torch.optim.Adam(model.parameters(), lr=1e-3)
criterion = nn.L1Loss() # MAE Loss instead of MSE! Might be more robust to outliers.

for epoch in range(15):
    model.train()
    for batch in train_loader:
        batch = batch.to(device)
        # Denoising Autoencoder: Add noise to inputs
        noise = torch.randn_like(batch) * 0.1 
        noisy_batch = batch + noise
        
        pred = model(noisy_batch)
        loss = criterion(pred, batch) # reconstruct clean batch
        optimizer.zero_grad()
        loss.backward()
        optimizer.step()

model.eval()

def smooth(x, window_len=21):
    if len(x) < window_len: return x
    s = np.r_[x[window_len-1:0:-1], x, x[-2:-window_len-1:-1]]
    w = np.ones(window_len,'d')
    y = np.convolve(w/w.sum(), s, mode='valid')
    return y[(window_len//2-1):-(window_len//2)]

def get_errors(file_paths):
    errors_smoothed = []
    criterion_eval = nn.L1Loss(reduction='none')
    for path in file_paths:
        y, _ = librosa.load(path, sr=16000)
        mfcc = librosa.feature.mfcc(y=y, sr=16000, n_mfcc=40, n_mels=128, hop_length=512)
        mfcc_delta = librosa.feature.delta(mfcc)
        feat = np.concatenate([mfcc, mfcc_delta], axis=0)
        feat = (feat - np.mean(feat)) / (np.std(feat) + 1e-6)
        
        context = 7
        chunks = []
        if feat.shape[1] >= context:
            for i in range(feat.shape[1] - context + 1):
                chunks.append(feat[:, i:i+context].flatten())
            chunks = torch.tensor(np.array(chunks), dtype=torch.float32).to(device)
            with torch.no_grad():
                preds = model(chunks)
                loss = torch.mean(torch.abs(preds - chunks), dim=1).cpu().numpy()
                errors_smoothed.append(np.max(smooth(loss, 21)))
        else:
            errors_smoothed.append(0)
    return errors_smoothed

n_smax = get_errors(test_normal)
a_smax = get_errors(test_abnormal)

y_true = np.concatenate([np.zeros(len(n_smax)), np.ones(len(a_smax))])
y_scores = np.concatenate([n_smax, a_smax])

p, r, t = precision_recall_curve(y_true, y_scores)
f1 = 2 * (p * r) / (p + r + 1e-8)
print(f"Extreme Denoising AE (MFCC+Delta, context=7, L1 Loss, noise=0.1, smooth=21) F1: {np.max(f1):.4f}")
