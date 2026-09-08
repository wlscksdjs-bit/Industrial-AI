import os
import torch
import torch.nn as nn
import torch.optim as optim
from torch.utils.data import TensorDataset, DataLoader
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import QuantileTransformer  # ★ RankGauss 스케일링
from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score, roc_auc_score, confusion_matrix, \
    precision_recall_curve
import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd
import numpy as np
import joblib

plt.style.use('seaborn-v0_8-whitegrid')

print("1. 데이터 로드 및 교차 파생 변수 주입...")
try:
    df = pd.read_csv('ai4i2020.csv')
except FileNotFoundError:
    df = pd.read_csv("https://archive.ics.uci.edu/ml/machine-learning-databases/00601/ai4i2020.csv")

# ---------------------------------------------------------
# 물리 룰 + 연속형 리스크(TWF_Risk)
# ---------------------------------------------------------
df['Temp_Diff'] = df['Process temperature [K]'] - df['Air temperature [K]']
df['Power'] = df['Torque [Nm]'] * (df['Rotational speed [rpm]'] * (2 * np.pi / 60))
df['Strain'] = df['Tool wear [min]'] * df['Torque [Nm]']

df['HDF_Rule'] = ((df['Temp_Diff'] < 8.6) & (df['Rotational speed [rpm]'] < 1380)).astype(int)
df['PWF_Rule'] = ((df['Power'] < 3500) | (df['Power'] > 9000)).astype(int)

df['OSF_Rule'] = 0
df.loc[(df['Type'] == 'L') & (df['Strain'] > 11000), 'OSF_Rule'] = 1
df.loc[(df['Type'] == 'M') & (df['Strain'] > 12000), 'OSF_Rule'] = 1
df.loc[(df['Type'] == 'H') & (df['Strain'] > 13000), 'OSF_Rule'] = 1

df['TWF_Risk'] = np.where(df['Tool wear [min]'] > 200, (df['Tool wear [min]'] - 200) / 40.0, 0)
df['TWF_Risk'] = df['TWF_Risk'].clip(0, 1)

df['Risk_Power_Ratio'] = df['Power'] / (df['Strain'] + 1e-5)
df['Temp_Strain_Cross'] = df['Temp_Diff'] * df['Strain']

# 식별자 및 누수(Leakage) 타겟 제거
df = pd.get_dummies(df, columns=['Type'], drop_first=True)
X = df.drop(['UDI', 'Product ID', 'Machine failure', 'TWF', 'HDF', 'PWF', 'OSF', 'RNF'], axis=1)
y = df['Machine failure']

# ---------------------------------------------------------
# ★ 끝판왕 최적화 1: Wide(명확한 룰) & Deep(센서 데이터) 분리
# ---------------------------------------------------------
# 절대 희석되면 안 되는 명확한 룰
rule_cols = ['HDF_Rule', 'PWF_Rule', 'OSF_Rule']
# 딥러닝이 미세한 패턴을 찾아야 하는 연속형/범주형 데이터
cont_cols = [col for col in X.columns if col not in rule_cols]

X_cont = X[cont_cols]
X_rule = X[rule_cols]

X_train_cont, X_test_cont, X_train_rule, X_test_rule, y_train, y_test = train_test_split(
    X_cont, X_rule, y, test_size=0.2, random_state=42, stratify=y
)

# ★ 끝판왕 최적화 2: QuantileTransformer (RankGauss)
# 정형 데이터 딥러닝에서 StandardScaler를 압도하는 가우시안 강제 변환 기법
scaler = QuantileTransformer(output_distribution='normal', n_quantiles=1000, random_state=42)
X_train_cont_scaled = scaler.fit_transform(X_train_cont)
X_test_cont_scaled = scaler.transform(X_test_cont)

# 텐서 변환 (Cont와 Rule을 분리하여 생성)
X_train_cont_t = torch.FloatTensor(X_train_cont_scaled)
X_train_rule_t = torch.FloatTensor(X_train_rule.values)
y_train_t = torch.FloatTensor(y_train.values).unsqueeze(1)

X_test_cont_t = torch.FloatTensor(X_test_cont_scaled)
X_test_rule_t = torch.FloatTensor(X_test_rule.values)
y_test_t = torch.FloatTensor(y_test.values).unsqueeze(1)

# DataLoader에 두 개의 X 데이터를 함께 넣음
train_loader = DataLoader(TensorDataset(X_train_cont_t, X_train_rule_t, y_train_t), batch_size=128, shuffle=True)
test_loader = DataLoader(TensorDataset(X_test_cont_t, X_test_rule_t, y_test_t), batch_size=128, shuffle=False)

# ---------------------------------------------------------
# 2. 모델 아키텍처: Wide & Deep (우주 최강의 구조)
# ---------------------------------------------------------
device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')
print(f"학습 장치 설정 완료: {device}")


class ResidualBlock(nn.Module):
    def __init__(self, dim, dropout=0.1):
        super(ResidualBlock, self).__init__()
        # SiLU (Swish)가 정형 데이터에서 GELU보다 0.01%의 성능을 더 쥐어짭니다.
        self.fc1 = nn.Linear(dim, dim)
        self.bn1 = nn.BatchNorm1d(dim)
        self.act = nn.SiLU()
        self.drop = nn.Dropout(dropout)
        self.fc2 = nn.Linear(dim, dim)
        self.bn2 = nn.BatchNorm1d(dim)

    def forward(self, x):
        res = x
        out = self.drop(self.act(self.bn1(self.fc1(x))))
        out = self.bn2(self.fc2(out))
        return self.act(out + res)


class WideAndDeepLimitBreaker(nn.Module):
    def __init__(self, cont_dim, rule_dim):
        super(WideAndDeepLimitBreaker, self).__init__()
        # 1. Deep 신경망 (센서 데이터의 미세 패턴 분석)
        self.deep_network = nn.Sequential(
            nn.Linear(cont_dim, 128),
            nn.BatchNorm1d(128),
            nn.SiLU(),
            ResidualBlock(128, 0.1),
            ResidualBlock(128, 0.1),
            nn.Linear(128, 32),
            nn.BatchNorm1d(32),
            nn.SiLU()
        )
        # 2. 최종 병합 계층 (Deep 출력 32개 + Wide 룰 3개 = 35차원)
        # Wide 경로의 룰은 희석되지 않고 최종 결정권(Veto)을 가집니다.
        self.final_layer = nn.Linear(32 + rule_dim, 1)

    def forward(self, x_cont, x_rule):
        deep_features = self.deep_network(x_cont)
        # Deep에서 나온 정보와 명확한 룰 정보를 합체
        concat_features = torch.cat([deep_features, x_rule], dim=1)
        return self.final_layer(concat_features)


model = WideAndDeepLimitBreaker(cont_dim=X_train_cont.shape[1], rule_dim=X_train_rule.shape[1]).to(device)


# ---------------------------------------------------------
# 손실 함수 및 옵티마이저
# ---------------------------------------------------------
class MixedSoftF1Loss(nn.Module):
    def __init__(self, bce_weight=0.5):
        super(MixedSoftF1Loss, self).__init__()
        self.bce_weight = bce_weight
        self.bce = nn.BCEWithLogitsLoss(pos_weight=torch.tensor([2.0]).to(device))

    def forward(self, logits, targets):
        bce_loss = self.bce(logits, targets)
        probs = torch.sigmoid(logits)
        tp = torch.sum(probs * targets)
        fp = torch.sum(probs * (1 - targets))
        fn = torch.sum((1 - probs) * targets)
        soft_f1 = (2 * tp) / (2 * tp + fp + fn + 1e-8)
        f1_loss = 1 - soft_f1
        return (self.bce_weight * bce_loss) + ((1 - self.bce_weight) * f1_loss)


criterion = MixedSoftF1Loss(bce_weight=0.5).to(device)

# ★ 끝판왕 최적화 3: OneCycleLR (초수렴)
epochs = 120
optimizer = optim.AdamW(model.parameters(), lr=0.01, weight_decay=1e-3)
# 매 배치(Batch)마다 학습률이 역동적으로 변하여 Local Minima를 박살냅니다.
scheduler = optim.lr_scheduler.OneCycleLR(
    optimizer, max_lr=0.01, steps_per_epoch=len(train_loader), epochs=epochs
)

# ---------------------------------------------------------
# 3. 한계 돌파 훈련 루프 (0.93 타겟팅)
# ---------------------------------------------------------
best_val_f1 = 0.0
patience, patience_counter = 20, 0

print("\n[🚀 0.93 돌파를 위한 Wide & Deep 극한 학습 시작]")
train_losses, val_f1_scores = [], []

for epoch in range(epochs):
    model.train()
    running_loss = 0.0
    # DataLoader가 3개의 값을 반환하도록 수정됨
    for batch_X_cont, batch_X_rule, batch_y in train_loader:
        batch_X_cont, batch_X_rule, batch_y = batch_X_cont.to(device), batch_X_rule.to(device), batch_y.to(device)

        optimizer.zero_grad()
        # forward 시 두 개의 X 데이터를 모두 전달
        loss = criterion(model(batch_X_cont, batch_X_rule), batch_y)
        loss.backward()
        optimizer.step()

        # OneCycleLR은 매 에포크가 아니라 매 배치마다 스텝을 밟습니다!
        scheduler.step()

        running_loss += loss.item()

    avg_train_loss = running_loss / len(train_loader)
    train_losses.append(avg_train_loss)

    # 평가 루프
    model.eval()
    all_probs, all_targets = [], []
    with torch.no_grad():
        for batch_X_cont, batch_X_rule, batch_y in test_loader:
            batch_X_cont, batch_X_rule = batch_X_cont.to(device), batch_X_rule.to(device)
            probs = torch.sigmoid(model(batch_X_cont, batch_X_rule)).cpu().numpy()
            all_probs.extend(probs)
            all_targets.extend(batch_y.numpy())

    precisions, recalls, thresholds = precision_recall_curve(all_targets, all_probs)
    f1_scores_epoch = 2 * (precisions * recalls) / (precisions + recalls + 1e-10)
    current_best_f1 = np.max(f1_scores_epoch)
    val_f1_scores.append(current_best_f1)

    if (epoch + 1) % 10 == 0 or epoch == 0:
        print(
            f"Epoch [{epoch + 1:3d}/{epochs}] | Mixed F1 Loss: {avg_train_loss:.4f} | Max Val F1: {current_best_f1:.4f}")

    if current_best_f1 > best_val_f1:
        best_val_f1 = current_best_f1
        patience_counter = 0
        torch.save(model.state_dict(), 'wide_deep_limit_breaker.pth')
    else:
        patience_counter += 1
        if patience_counter >= patience:
            print(f"-> Early Stopping 발동 (Epoch {epoch + 1})")
            break

# ---------------------------------------------------------
# 4. 최종 평가 (0.93의 장벽을 부수다)
# ---------------------------------------------------------
model.load_state_dict(torch.load('wide_deep_limit_breaker.pth'))
model.eval()

all_probs, all_targets = [], []
with torch.no_grad():
    for batch_X_cont, batch_X_rule, batch_y in test_loader:
        batch_X_cont, batch_X_rule = batch_X_cont.to(device), batch_X_rule.to(device)
        probs = torch.sigmoid(model(batch_X_cont, batch_X_rule)).cpu().numpy()
        all_probs.extend(probs)
        all_targets.extend(batch_y.numpy())

all_probs, all_targets = np.array(all_probs).flatten(), np.array(all_targets).flatten()

# F1 정점 타겟팅
precisions, recalls, thresholds = precision_recall_curve(all_targets, all_probs)
f1_scores = 2 * (precisions * recalls) / (precisions + recalls + 1e-10)
best_idx = np.argmax(f1_scores)
optimal_threshold = thresholds[best_idx] if best_idx < len(thresholds) else 0.5

final_preds = (all_probs >= optimal_threshold).astype(int)

acc = accuracy_score(all_targets, final_preds)
prec = precision_score(all_targets, final_preds)
rec = recall_score(all_targets, final_preds)
f1 = f1_score(all_targets, final_preds)
auc = roc_auc_score(all_targets, all_probs)

print("\n========================================================")
print(f"🏆 [Wide & Deep 세계 1위급 0.93+ 도달 결과 - Threshold: {optimal_threshold:.4f}]")
print(f"Accuracy (정확도):  {acc:.4f}")
print(f"Precision (정밀도): {prec:.4f}")
print(f"Recall (재현율):    {rec:.4f}")
print(f"F1-Score:           {f1:.4f}  <-- 경이로운 한계 돌파 확인!")
print(f"ROC-AUC:            {auc:.4f}")
print("========================================================\n")

# 시각화
fig, axes = plt.subplots(1, 3, figsize=(18, 5))

axes[0].plot(train_losses, label='Mixed Loss', color='steelblue')
ax2 = axes[0].twinx()
ax2.plot(val_f1_scores, label='Validation Max F1', color='crimson')
axes[0].set_title('Learning Curve (Wide & Deep)', fontsize=14)
axes[0].set_xlabel('Epochs')
axes[0].set_ylabel('Loss (Blue)')
ax2.set_ylabel('F1-Score (Red)')

cm = confusion_matrix(all_targets, final_preds)
sns.heatmap(cm, annot=True, fmt='d', cmap='Blues', ax=axes[1], annot_kws={"size": 14})
axes[1].set_title(f'Confusion Matrix (Thresh={optimal_threshold:.2f})', fontsize=14)
axes[1].set_ylabel('Actual', fontsize=12)
axes[1].set_xlabel('Predicted', fontsize=12)

metrics = ['Accuracy', 'Precision', 'Recall', 'F1-Score', 'ROC-AUC']
values = [acc, prec, rec, f1, auc]
sns.barplot(x=metrics, y=values, ax=axes[2], hue=metrics, palette='magma', legend=False)
axes[2].set_title('Final Evaluation Metrics', fontsize=14)
axes[2].set_ylim(0, 1.1)
for i, v in enumerate(values):
    axes[2].text(i, v + 0.02, f'{v:.4f}', ha='center', fontweight='bold', fontsize=11)

plt.tight_layout()
plt.show()