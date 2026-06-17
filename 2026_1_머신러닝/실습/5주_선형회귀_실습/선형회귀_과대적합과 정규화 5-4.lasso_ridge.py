import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from sklearn.linear_model import Ridge, Lasso
from sklearn.datasets import make_regression

# 1. 데이터 생성 (변수 100개 중 진짜 중요한 건 10개뿐인 상황)
X, y = make_regression(n_samples=50, n_features=100, n_informative=10, noise=1, random_state=42)

# 2. L1(Lasso)과 L2(Ridge) 학습
lasso = Lasso(alpha=0.1).fit(X, y)
ridge = Ridge(alpha=1.0).fit(X, y)

# [파트 1] 결과 수치 출력 (콘솔)
print("="*60)
print("=== [가중치 값 비교 (상위 10개)] ===")
print("="*60)
df_comp = pd.DataFrame({
    'L2 (Ridge) 가중치': ridge.coef_,
    'L1 (Lasso) 가중치': lasso.coef_
})
print(df_comp.head(10)) # 상위 10개만 출력
print("\n" + "="*60)
# 결정적 차이: 가중치가 '정확히 0'인 변수의 개수 세기
print(f"L2 (Ridge)가 0으로 만든 변수 개수: {np.sum(ridge.coef_ == 0)}개 / 100개")
print(f"L1 (Lasso)가 0으로 만든 변수 개수: {np.sum(lasso.coef_ == 0)}개 / 100개")
print("="*60)

# [파트 2] 결과 시각화 (그래프)
plt.figure(figsize=(15, 6))

# 왼쪽: Ridge (가중치가 빼곡함)
plt.subplot(1, 2, 1)
# 가중치 분포를 막대 그래프(Stem plot)로 표현
plt.stem(ridge.coef_, markerfmt=' ', basefmt="k-")
plt.title("L2 (Ridge) Coefficients\n(Many small non-zero values)", fontsize=14)
plt.xlabel("Feature Index (0~99)")
plt.ylabel("Coefficient Value")
plt.ylim(-100, 100) # 스케일 통일
plt.grid(True, alpha=0.3)

# 오른쪽: Lasso (대부분이 0이라 텅 비어 있음)
plt.subplot(1, 2, 2)
plt.stem(lasso.coef_, markerfmt=' ', basefmt="k-")
plt.title("L1 (Lasso) Coefficients\n(Sparse: Most are exactly 0)", fontsize=14)
plt.xlabel("Feature Index (0~99)")
plt.ylabel("Coefficient Value")
plt.ylim(-100, 100) # 스케일 통일
plt.grid(True, alpha=0.3)

plt.tight_layout()
plt.show()