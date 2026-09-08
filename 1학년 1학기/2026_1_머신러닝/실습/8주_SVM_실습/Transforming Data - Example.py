import numpy as np
import matplotlib.pyplot as plt
from sklearn.datasets import make_circles

# 1. 2차원 도넛 모양 데이터 생성
X, y = make_circles(n_samples=200, factor=0.3, noise=0.05, random_state=42)
x1 = X[:, 0]
x2 = X[:, 1]

# 2. [핵심] 차원 확장 (Kernel Mapping)
# 여기서는 중심에서 멀어질수록 값이 커지는 x1^2 + x2^2 (다항식 커널 형태)를 사용합니다.
z = x1**2 + x2**2

# 3. 2D vs 3D 비교 시각화 세팅
fig = plt.figure(figsize=(16, 7))

# --- [왼쪽 그래프] 원래의 2차원 데이터 ---
ax1 = fig.add_subplot(1, 2, 1)
ax1.scatter(x1, x2, c=y, cmap='coolwarm', s=50, edgecolors='k')
ax1.set_title("Original 2D Space\n(Linearly Inseparable)", size=16)
ax1.set_xlabel("x1")
ax1.set_ylabel("x2")

# --- [오른쪽 그래프] 확장된 3차원 공간 ---
# projection='3d'를 사용하여 3차원 그래프로 설정합니다.
ax2 = fig.add_subplot(1, 2, 2, projection='3d')
ax2.scatter(x1, x2, z, c=y, cmap='coolwarm', s=50, edgecolors='k')

# 3차원 공간에서 데이터를 가르는 '평면(Hyperplane)' 그리기
# z값이 대략 0.4 정도인 높이에 투명한 평면을 끼워 넣습니다.
xx, yy = np.meshgrid(np.linspace(-1.2, 1.2, 10), np.linspace(-1.2, 1.2, 10))
zz = np.full(xx.shape, 0.4) # z=0.4 높이의 평면
ax2.plot_surface(xx, yy, zz, alpha=0.3, color='gray')

ax2.set_title("Projected 3D Space (z = x1^2 + x2^2)\n(Linearly Separable by a Plane)", size=16)
ax2.set_xlabel("x1")
ax2.set_ylabel("x2")
ax2.set_zlabel("z (New Dimension)")

# 3D 그래프를 보기 좋은 각도로 돌려줍니다.
ax2.view_init(elev=20, azim=45)

plt.tight_layout()
plt.show()