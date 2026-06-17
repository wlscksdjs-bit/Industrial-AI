import os
import glob
import torch
import torch.nn as nn
import numpy as np
import librosa
from sklearn.metrics import precision_recall_curve
from torch.utils.data import Dataset, DataLoader

device = torch.device('cuda' if torch.cuda.is_available() else 'mps' if torch.backends.mps.is_available() else 'cpu')

class MIMIIDenseDataset(Dataset):
    def __init__(self, file_paths):
        self.data = []
        for path in file_paths:
            y, _ = librosa.load(path, sr=16000)
            mel = librosa.feature.melspectrogram(y=y, sr=16000, n_mels=128, hop_length=512)
            mel_db = librosa.power_to_db(mel, ref=np.max)
            mel_db = (mel_db + 80.0) / 80.0
            
            # Extract 5 consecutive frames (context window)
            context = 5
            for i in range(mel_db.shape[1] - context + 1):
                chunk = mel_db[:, i:i+context].flatten()
                self.data.append(chunk)
        self.data = np.array(self.data, dtype=np.float32)

    def __len__(self):
        return len(self.data)

    def __getitem__(self, idx):
        return self.data[idx]

normal_files = glob.glob('0_dB_valve/valve/id_02/normal/*.wav')
# Use fewer files for faster testing
train_files = sorted(normal_files)[:200]
test_normal = sorted(normal_files)[500:600]
test_abnormal = glob.glob('0_dB_valve/valve/id_02/abnormal/*.wav')[:100]

print("Loading dataset...")
train_dataset = MIMIIDenseDataset(train_files)
train_loader = DataLoader(train_dataset, batch_size=256, shuffle=True)

class DenseAE(nn.Module):
    def __init__(self):
        super().__init__()
        self.encoder = nn.Sequential(
            nn.Linear(128 * 5, 128), nn.BatchNorm1d(128), nn.ReLU(),
            nn.Linear(128, 128), nn.BatchNorm1d(128), nn.ReLU(),
            nn.Linear(128, 8), nn.BatchNorm1d(8), nn.ReLU()
        )
        self.decoder = nn.Sequential(
            nn.Linear(8, 128), nn.BatchNorm1d(128), nn.ReLU(),
            nn.Linear(128, 128), nn.BatchNorm1d(128), nn.ReLU(),
            nn.Linear(128, 128 * 5), nn.Sigmoid()
        )
    def forward(self, x):
        return self.decoder(self.encoder(x))

model = DenseAE().to(device)
optimizer = torch.optim.Adam(model.parameters(), lr=1e-3)
criterion = nn.MSELoss()

print("Training...")
for epoch in range(10): # quick train
    model.train()
    for batch in train_loader:
        batch = batch.to(device)
        pred = model(batch)
        loss = criterion(pred, batch)
        optimizer.zero_grad()
        loss.backward()
        optimizer.step()

model.eval()
print("Evaluating...")
def get_errors(file_paths):
    errors = []
    for path in file_paths:
        y, _ = librosa.load(path, sr=16000)
        mel = librosa.feature.melspectrogram(y=y, sr=16000, n_mels=128, hop_length=512)
        mel_db = (librosa.power_to_db(mel, ref=np.max) + 80.0) / 80.0
        
        context = 5
        chunks = []
        if mel_db.shape[1] >= context:
            for i in range(mel_db.shape[1] - context + 1):
                chunks.append(mel_db[:, i:i+context].flatten())
            chunks = torch.tensor(np.array(chunks), dtype=torch.float32).to(device)
            with torch.no_grad():
                preds = model(chunks)
                loss = torch.mean((preds - chunks)**2, dim=1)
                errors.append(loss.mean().item()) # mean error over chunks
        else:
            errors.append(0)
    return errors

norm_e = get_errors(test_normal)
abn_e = get_errors(test_abnormal)
y_true = np.concatenate([np.zeros(len(norm_e)), np.ones(len(abn_e))])
y_scores = np.concatenate([norm_e, abn_e])

p, r, t = precision_recall_curve(y_true, y_scores)
f1 = 2 * (p * r) / (p + r + 1e-8)
print(f"Dense AE Mean F1: {np.max(f1):.4f}")
