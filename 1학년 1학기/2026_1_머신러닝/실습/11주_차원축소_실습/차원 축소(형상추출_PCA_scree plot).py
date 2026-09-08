import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from sklearn.preprocessing import StandardScaler
from sklearn.decomposition import PCA

# 1. 데이터 준비 및 전처리
file_path = r"C:\Users\JIN\PycharmProjects\PythonProject1\11_data.csv"
df = pd.read_csv(file_path)
df = df.drop(labels=['id', 'Unnamed: 32'], axis=1, errors='ignore')
df['target'] = df['diagnosis'].map({'B': 0, 'M': 1})
X = df.drop(labels=['diagnosis', 'target'], axis=1, errors='ignore')
y = df['target']

# 2. 스케일링 및 전체 30차원 PCA 가동
X_scaled = StandardScaler().fit_transform(X)
pca = PCA()
pca.fit(X_scaled)

# 개별 보존율 및 누적 보존율 계산
variance_ratio = pca.explained_variance_ratio_
cumulative_variance = np.cumsum(variance_ratio)

# 3. 스크리 플롯 (Scree Plot) 시각화
plt.figure(figsize=(10, 6))
x_components = range(1, len(variance_ratio) + 1)

# 개별 분산(막대) & 누적 분산(꺾은선) 그래프
plt.bar(x_components, variance_ratio, alpha=0.5, color='steelblue', label='Individual Variance')
plt.plot(x_components, cumulative_variance, marker='o', color='indianred', linewidth=2, label='Cumulative Variance')

plt.title("Scree Plot: Find the 'Elbow' Point!")
plt.xlabel("Number of Principal Components (PC)")
plt.ylabel("Explained Variance Ratio (0.0 to 1.0)")
plt.xticks(range(1, 32, 2))
plt.legend(loc='center right')
plt.grid(axis='y', linestyle='--', alpha=0.5)

plt.tight_layout()
plt.show()

# 4. 콘솔 결과 요약 출력
print("\n[주요 PC 개수별 누적 정보 보존율]")
print("-" * 50)
print(f"PC 2개 사용 시 : {cumulative_variance[1]:.1%} 보존")
print(f"PC 5개 사용 시 : {cumulative_variance[4]:.1%} 보존")
print(f"PC 10개 사용 시: {cumulative_variance[9]:.1%} 보존")
print("-" * 50)
print("결론: 주성분 개수를 늘릴수록 정보 보존율은 높아지지만, 효율적인 차원 축소 지점을 찾는 것이 중요합니다.")
