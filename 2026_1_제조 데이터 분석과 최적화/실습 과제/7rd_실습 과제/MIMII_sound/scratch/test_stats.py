import os
import glob
import torch
import torch.nn as nn
import numpy as np
import librosa
from sklearn.metrics import precision_recall_curve

device = torch.device('cuda' if torch.cuda.is_available() else 'mps' if torch.backends.mps.is_available() else 'cpu')

class AudioAutoencoder(nn.Module):
    def __init__(self):
        super(AudioAutoencoder, self).__init__()
        self.encoder = nn.Sequential(
            nn.Conv2d(1, 16, kernel_size=3, stride=2, padding=1),
            nn.ReLU(),
            nn.BatchNorm2d(16),
            nn.Conv2d(16, 32, kernel_size=3, stride=2, padding=1),
            nn.ReLU(),
            nn.BatchNorm2d(32),
            nn.Conv2d(32, 64, kernel_size=3, stride=2, padding=1),
            nn.ReLU(),
            nn.BatchNorm2d(64),
            nn.Conv2d(64, 128, kernel_size=3, stride=2, padding=1),
            nn.ReLU(),
            nn.BatchNorm2d(128),
            nn.Conv2d(128, 256, kernel_size=3, stride=2, padding=1),
            nn.ReLU(),
            nn.Flatten(),
            nn.Linear(256 * 4 * 4, 64)
        )
        self.decoder_fc = nn.Sequential(
            nn.Linear(64, 256 * 4 * 4),
            nn.ReLU()
        )
        self.decoder_conv = nn.Sequential(
            nn.ConvTranspose2d(256, 128, kernel_size=3, stride=2, padding=1, output_padding=1),
            nn.ReLU(),
            nn.BatchNorm2d(128),
            nn.ConvTranspose2d(128, 64, kernel_size=3, stride=2, padding=1, output_padding=1),
            nn.ReLU(),
            nn.BatchNorm2d(64),
            nn.ConvTranspose2d(64, 32, kernel_size=3, stride=2, padding=1, output_padding=1),
            nn.ReLU(),
            nn.BatchNorm2d(32),
            nn.ConvTranspose2d(32, 16, kernel_size=3, stride=2, padding=1, output_padding=1),
            nn.ReLU(),
            nn.BatchNorm2d(16),
            nn.ConvTranspose2d(16, 1, kernel_size=3, stride=2, padding=1, output_padding=1),
            nn.Sigmoid()
        )

    def forward(self, x):
        encoded = self.encoder(x)
        decoded = self.decoder_fc(encoded)
        decoded = decoded.view(-1, 256, 4, 4)
        return self.decoder_conv(decoded)

model = AudioAutoencoder().to(device)
model.load_state_dict(torch.load('audio_models/audio_autoencoder_real.pth', map_location=device, weights_only=True))
model.eval()

normal_test_files = sorted(glob.glob('0_dB_valve/valve/id_02/normal/*.wav'))[500:]
abnormal_test_files = sorted(glob.glob('0_dB_valve/valve/id_02/abnormal/*.wav'))

def get_window_errors(file_list):
    all_window_errors = []
    criterion = nn.MSELoss()
    with torch.no_grad():
        for path in file_list:
            y, _ = librosa.load(path, sr=16000)
            mel = librosa.feature.melspectrogram(y=y, sr=16000, n_mels=128)
            mel_db = (librosa.power_to_db(mel, ref=np.max) + 80.0) / 80.0
            
            w_errs = []
            if mel_db.shape[1] >= 128:
                stride = 64
                for start in range(0, mel_db.shape[1] - 128 + 1, stride):
                    mel_input = mel_db[:, start : start + 128]
                    tensor = torch.tensor(mel_input, dtype=torch.float32).unsqueeze(0).unsqueeze(0).to(device)
                    loss = criterion(model(tensor), tensor).item()
                    w_errs.append(loss)
            else:
                mel_input = np.pad(mel_db, ((0,0),(0, 128-mel_db.shape[1])))
                tensor = torch.tensor(mel_input, dtype=torch.float32).unsqueeze(0).unsqueeze(0).to(device)
                w_errs.append(criterion(model(tensor), tensor).item())
            all_window_errors.append(w_errs)
    return all_window_errors

norm_we = get_window_errors(normal_test_files)
abn_we = get_window_errors(abnormal_test_files)

y_true = np.concatenate([np.zeros(len(norm_we)), np.ones(len(abn_we))])

for agg_name, agg_func in [("Max", np.max), ("Mean", np.mean), ("Median", np.median), ("90th P", lambda x: np.percentile(x, 90)), ("95th P", lambda x: np.percentile(x, 95))]:
    norm_scores = [agg_func(e) for e in norm_we]
    abn_scores = [agg_func(e) for e in abn_we]
    y_scores = np.concatenate([norm_scores, abn_scores])
    precision, recall, _ = precision_recall_curve(y_true, y_scores)
    f1_scores = 2 * (precision * recall) / (precision + recall + 1e-8)
    print(f"Aggregation: {agg_name: <10} | Best F1: {np.max(f1_scores):.4f}")
