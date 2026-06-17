import numpy as np
import matplotlib.pyplot as plt
from sklearn.datasets import make_circles
from sklearn.cluster import DBSCAN
from sklearn.preprocessing import StandardScaler
import warnings
warnings.filterwarnings('ignore')

# 1. 시뮬레이션 센서 데이터 생성 (정상: 동심원, 이상치: 무작위 노이즈)
X_circles, _ = make_circles(n_samples=500, factor=0.5, noise=0.05, random_state=42)
np.random.seed(42)
X_noise = np.random.uniform(low=-1.5, high=1.5, size=(30, 2))
X = np.vstack([X_circles, X_noise])

# 2. 데이터 정규화
X_scaled = StandardScaler().fit_transform(X)

# 3. DBSCAN 모델 학습 (eps=0.3으로 설정)
dbscan = DBSCAN(eps=0.3, min_samples=5)
dbscan_labels = dbscan.fit_predict(X_scaled)

# 4. 결과 출력
n_clusters = len(set(dbscan_labels)) - (1 if -1 in dbscan_labels else 0)
n_noise = list(dbscan_labels).count(-1)

print("-" * 40)
print(f"▶ 탐지된 정상 궤적(군집) 수: {n_clusters}개")
print(f"▶ 탐지된 고장(노이즈) 신호 수: {n_noise}개")
print("-" * 40)

# 5. 초간단 시각화 (색상 자동 할당)
plt.figure(figsize=(7, 5))
plt.scatter(X_scaled[:, 0], X_scaled[:, 1], c=dbscan_labels, cmap='viridis', edgecolor='k')
plt.title('DBSCAN Simplified Result (eps=0.3)', fontsize=14)
plt.show()