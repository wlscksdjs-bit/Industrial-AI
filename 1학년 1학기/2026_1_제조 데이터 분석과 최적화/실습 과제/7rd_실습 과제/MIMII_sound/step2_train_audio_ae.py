# %% [1] 라이브러리 임포트 및 장치 설정
import os
import glob
import torch
import torch.nn as nn
import torch.optim as optim
from torch.utils.data import Dataset, DataLoader
import numpy as np
import librosa

device = torch.device('cuda' if torch.cuda.is_available() else 'mps' if torch.backends.mps.is_available() else 'cpu')
print(f"학습 장치(Device) 설정 완료: {device}")

# %% [2] 실제 MIMII 데이터셋 경로 설정 및 커스텀 Dataset 구축
normal_dir = '0_dB_valve/valve/id_02/normal'
normal_files = sorted(glob.glob(os.path.join(normal_dir, '*.wav')))
# F1-Score의 명확한 측정을 위해 엄격하게 Train/Test 분리 (첫 500개만 사용, 나머지는 완전 독립 평가용)
train_files = normal_files[:500] 

if not train_files:
    print(f"에러: '{normal_dir}' 경로에서 학습용 .wav 파일을 찾을 수 없습니다.")
    exit()

print(f"로드된 정상 학습 오디오 파일 개수: {len(train_files)}개")

class MIMII_MFCC_Dataset(Dataset):
    """
    CNN 멜스펙트로그램의 한계를 깨고 F1-Score를 1.0에 가깝게 올리기 위해
    노이즈 스펙트럼에서 지배적인 주파수를 더 잘 뽑아내는 MFCC로 전처리를 리팩토링합니다.
    단일 프레임이 아닌 '5개 연속 프레임(Context Window)'을 엮어 모델에 시간적 흐름을 학습시킵니다.
    """
    def __init__(self, file_paths, sr=16000, n_mfcc=40, context=5):
        self.data = []
        for path in file_paths:
            y, _ = librosa.load(path, sr=sr)
            # 1. MFCC 특징 추출 (Mel-Spectrogram 대비 노이즈에 훨씬 강력함)
            mfcc = librosa.feature.mfcc(y=y, sr=sr, n_mfcc=n_mfcc, n_mels=128, hop_length=512)
            
            # 2. 파일 단위 정규화(Standardization) - 볼륨 차이 등에 의한 오차 상쇄
            mfcc = (mfcc - np.mean(mfcc)) / (np.std(mfcc) + 1e-6)
            
            # 3. 맥락 윈도우(Context Window) 분할 - 5개의 연속된 프레임을 하나의 벡터로 이어붙임
            for i in range(mfcc.shape[1] - context + 1):
                chunk = mfcc[:, i:i+context].flatten()
                self.data.append(chunk)

        self.data = np.array(self.data, dtype=np.float32)

    def __len__(self):
        return len(self.data)

    def __getitem__(self, idx):
        return self.data[idx]

print("데이터 전처리 중... (MFCC 추출 및 윈도우 분할 - 시간이 약간 소요될 수 있습니다)")
train_dataset = MIMII_MFCC_Dataset(train_files)
# 학습 데이터가 아주 많아졌으므로 배치사이즈를 256으로 상향
train_loader = DataLoader(train_dataset, batch_size=256, shuffle=True)
print("학습용 DataLoader 구축 완료 (MFCC 기반 시계열 윈도우 전처리 적용)")

# %% [3] 고성능 Dense 오토인코더(Autoencoder) 아키텍처 재설계
class DenseAudioAutoencoder(nn.Module):
    def __init__(self):
        super(DenseAudioAutoencoder, self).__init__()
        
        # 입력 차원: 40(MFCC) * 5(Context) = 200 차원
        # 극강의 재현력을 위해 병목(Bottleneck) 차원을 16 -> 32로 상향하여
        # 정상 밸브 소음을 완벽히 복원하도록 과적합(Overfitting)시킵니다.
        self.encoder = nn.Sequential(
            nn.Linear(200, 128),
            nn.BatchNorm1d(128),
            nn.ReLU(),
            nn.Linear(128, 64),
            nn.BatchNorm1d(64),
            nn.ReLU(),
            nn.Linear(64, 32),
            nn.BatchNorm1d(32),
            nn.ReLU()
        )
        
        self.decoder = nn.Sequential(
            nn.Linear(32, 64),
            nn.BatchNorm1d(64),
            nn.ReLU(),
            nn.Linear(64, 128),
            nn.BatchNorm1d(128),
            nn.ReLU(),
            nn.Linear(128, 200) 
        )

    def forward(self, x):
        encoded = self.encoder(x)
        decoded = self.decoder(encoded)
        return decoded

model = DenseAudioAutoencoder().to(device)
print("\n[리팩토링된 고성능 Dense 오토인코더 모델 준비 완료]")

# %% [4] 손실 함수 및 최적화 설정
# 스케일 변환이 없으므로 MSELoss 단독 적용에 최적화됨
criterion = nn.MSELoss()
optimizer = optim.Adam(model.parameters(), lr=0.001)

# %% [5] 오토인코더 학습 루프 (Training Loop)
epochs = 80 # 더 높은 F1-Score 도달을 위해 학습량을 30 -> 80으로 대폭 확대
print(f"\n[모델 학습 시작 - 최고 F1-Score 타겟팅 (Epoch: {epochs})]")
model.train()

for epoch in range(epochs):
    epoch_loss = 0.0
    for batch_x in train_loader:
        batch_x = batch_x.to(device)
        
        # Forward, Loss, Backward, Step
        outputs = model(batch_x)
        loss = criterion(outputs, batch_x) # 자기 자신을 복원
        
        optimizer.zero_grad()
        loss.backward()
        optimizer.step()
        
        epoch_loss += loss.item()
        
    avg_loss = epoch_loss / len(train_loader)
    
    if (epoch + 1) % 5 == 0 or epoch == 0:
        print(f"Epoch [{epoch+1:2d}/{epochs}] | Reconstruction Loss (MSE): {avg_loss:.4f}")

print("학습 완료!")

# %% [6] 모델 가중치 저장
os.makedirs('audio_models', exist_ok=True)
model_path = 'audio_models/audio_autoencoder_real.pth'
torch.save(model.state_dict(), model_path)
print(f"\n[저장 완료] 새로운 구조의 밸브 정상음 학습 모델이 '{model_path}'에 저장되었습니다.")