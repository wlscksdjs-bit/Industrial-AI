import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from sklearn.cluster import KMeans
from sklearn.metrics import silhouette_score
from sklearn.preprocessing import StandardScaler
from sklearn.decomposition import PCA
import warnings
warnings.filterwarnings('ignore')

# 데이터 로드
file_path = r"C:\Users\JIN\PycharmProjects\PythonProject1\11_data.csv"
df = pd.read_csv(file_path)

# 수치형 데이터만 추출
X = df.select_dtypes(include=[np.number])

# 전처리 (ID 제거, 결측치 처리)
if 'id' in X.columns:
    X = X.drop(columns=['id'])
X = X.dropna(axis=1, how='all')
X = X.fillna(X.mean())

# 데이터 정규화 (스케일링)
scaler = StandardScaler()
X_scaled = scaler.fit_transform(X)

# K-Means 모델 학습 (K=3)
k_value = 3
kmeans = KMeans(n_clusters=k_value, random_state=42)
kmeans_labels = kmeans.fit_predict(X_scaled)

# 성능 평가 지표 계산
sil_score = silhouette_score(X_scaled, kmeans_labels)
sse = kmeans.inertia_

# 결과 출력
print("-" * 40)
print(f"🎯 K-Means 군집화 결과 (K={k_value})")
print("-" * 40)
print(f"▶ 실루엣 점수 (Silhouette Score): {sil_score:.4f}")
print(f"▶ SSE (오차제곱합, Inertia): {sse:.4f}")
print("-" * 40)

# PCA를 통한 2차원 축소 및 시각화
pca = PCA(n_components=2, random_state=42)
X_pca = pca.fit_transform(X_scaled)

plt.figure(figsize=(8, 6))
plt.scatter(X_pca[:, 0], X_pca[:, 1], c=kmeans_labels, cmap='viridis', s=30, edgecolor='k')

plt.title(f'K-Means Clustering Result (K={k_value})', fontsize=14, fontweight='bold')
plt.xlabel('Principal Component 1 (PC1)')
plt.ylabel('Principal Component 2 (PC2)')
plt.grid(True, linestyle='--', alpha=0.6)
plt.tight_layout()
plt.show()