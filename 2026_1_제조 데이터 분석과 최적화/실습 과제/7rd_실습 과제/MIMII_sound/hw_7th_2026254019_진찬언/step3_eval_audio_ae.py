# %% [1] 라이브러리 임포트 및 모델 로드
import os
import glob
import torch
import torch.nn as nn
import numpy as np
import librosa
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.metrics import roc_curve, auc

device = torch.device('cuda' if torch.cuda.is_available() else 'mps' if torch.backends.mps.is_available() else 'cpu')

# 새로 정의된 고성능 Dense 오토인코더
class DenseAudioAutoencoder(nn.Module):
    def __init__(self):
        super(DenseAudioAutoencoder, self).__init__()
        self.encoder = nn.Sequential(
            nn.Linear(200, 128), nn.BatchNorm1d(128), nn.ReLU(),
            nn.Linear(128, 64), nn.BatchNorm1d(64), nn.ReLU(),
            nn.Linear(64, 32), nn.BatchNorm1d(32), nn.ReLU()
        )
        self.decoder = nn.Sequential(
            nn.Linear(32, 64), nn.BatchNorm1d(64), nn.ReLU(),
            nn.Linear(64, 128), nn.BatchNorm1d(128), nn.ReLU(),
            nn.Linear(128, 200)
        )
    def forward(self, x):
        return self.decoder(self.encoder(x))

model = DenseAudioAutoencoder().to(device)
model.load_state_dict(torch.load('audio_models/audio_autoencoder_real.pth', map_location=device, weights_only=True))
model.eval()
print("새로운 Dense 학습 모델 로드 완료 (0_dB_valve 타겟)")

# %% [2] 독립적인 평가용 데이터 경로 설정 (정상/비정상)
normal_test_dir = '0_dB_valve/valve/id_02/normal'
abnormal_test_dir = '0_dB_valve/valve/id_02/abnormal'

# Train 단에서 500개까지만 사용했으므로 500 이후의 데이터는 전혀 본 적 없는 Clean Test-set 입니다.
normal_test_files = sorted(glob.glob(os.path.join(normal_test_dir, '*.wav')))[500:] 
abnormal_test_files = sorted(glob.glob(os.path.join(abnormal_test_dir, '*.wav')))

# %% [3] 파일별 복원 오차 계산 함수 (Smoothing 기법 도입)
def smooth(x, window_len=25):
    """결정적 불량판정을 위해 노이즈 스파이크를 강력하게 줄여주는 이동평균 함수입니다."""
    if len(x) < window_len: return x
    s = np.r_[x[window_len-1:0:-1], x, x[-2:-window_len-1:-1]]
    w = np.ones(window_len, 'd')
    y = np.convolve(w/w.sum(), s, mode='valid')
    return y[(window_len//2-1):-(window_len//2)]

def compute_errors(file_list, sr=16000, n_mfcc=40, context=5):
    errors = []
    
    with torch.no_grad():
        for path in file_list:
            y, _ = librosa.load(path, sr=sr)
            # 학습과 동일하게 MFCC 추출 및 정규화
            mfcc = librosa.feature.mfcc(y=y, sr=sr, n_mfcc=n_mfcc, n_mels=128, hop_length=512)
            mfcc = (mfcc - np.mean(mfcc)) / (np.std(mfcc) + 1e-6)
            
            chunks = []
            if mfcc.shape[1] >= context:
                # 파일 내 모든 5-프레임 윈도우 조각 모음
                for i in range(mfcc.shape[1] - context + 1):
                    chunks.append(mfcc[:, i:i+context].flatten())
                chunks_tensor = torch.tensor(np.array(chunks), dtype=torch.float32).to(device)
                
                # 병렬 배치 추론
                preds = model(chunks_tensor)
                # 각 조각별 복원 오차 계산 (Mean Squared Error)
                frame_errors = torch.mean((preds - chunks_tensor)**2, dim=1).cpu().numpy()
                
                # [핵심] F1-Score 극대화를 위한 후처리 기법 (Moving Average Smoothing)
                # 단기간 치솟는 0 dB 백색소음에 의한 오진(False Positive)을 막기 위해 
                # 주변 프레임의 오차를 좀 더 강력하게 뭉갠(Window=25) 뒤 가장 큰 이상치(Max)를 산출합니다.
                smoothed_errors = smooth(frame_errors, window_len=25)
                errors.append(np.max(smoothed_errors))
            else:
                errors.append(0)
    return np.array(errors)

print("정상 및 비정상 데이터의 복원 오차 계산 중 (Smoothing 적용)...")
normal_errors = compute_errors(normal_test_files)
abnormal_errors = compute_errors(abnormal_test_files)

# %% [4] 오차 분포 시각화
plt.figure(figsize=(10, 6))
sns.histplot(normal_errors, kde=True, color='blue', label='Normal (Valve)')
sns.histplot(abnormal_errors, kde=True, color='red', label='Abnormal (Valve)')
plt.title('Reconstruction Error Distribution with Smoothing (MIMII Valve ID02)')
plt.xlabel('Smoothed Mean Squared Error (MSE)')
plt.legend()
plt.show()

# %% [5] ROC-AUC 및 F1-Score 도출
y_true = np.concatenate([np.zeros(len(normal_errors)), np.ones(len(abnormal_errors))])
y_scores = np.concatenate([normal_errors, abnormal_errors])

from sklearn.metrics import precision_recall_curve, f1_score, confusion_matrix, ConfusionMatrixDisplay

# Precision-Recall Curve 계산을 통해 최적의 임계값 찾기
precision, recall, thresholds = precision_recall_curve(y_true, y_scores)

# F1-Score가 최대가 되는 임계값 찾기
f1_scores = 2 * (precision * recall) / (precision + recall + 1e-8)
optimal_idx = np.argmax(f1_scores)
optimal_threshold = thresholds[optimal_idx]
optimal_f1 = f1_scores[optimal_idx]

print(f"\n최적의 이상치 탐지 임계값(Threshold): {optimal_threshold:.4f}")
print(f"⭐️ 해당 임계값에서의 평가지표 - 최고 F1-Score: {optimal_f1:.4f} ⭐️")

# 최적 임계값을 기준으로 예측(Prediction) 정오표 시각화
y_pred = (y_scores >= optimal_threshold).astype(int)

cm = confusion_matrix(y_true, y_pred)
plt.figure(figsize=(6, 5))
disp = ConfusionMatrixDisplay(confusion_matrix=cm, display_labels=['Normal', 'Abnormal'])
disp.plot(cmap='Blues', values_format='d', ax=plt.gca())
plt.title(f'Confusion Matrix (Optimal Threshold: {optimal_threshold:.4f})')
plt.show()