import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.preprocessing import StandardScaler
from sklearn.decomposition import PCA

# 1. 데이터 준비 및 전처리
file_path = r"C:\Users\JIN\PycharmProjects\PythonProject1\11_data.csv"
df = pd.read_csv(file_path)
df = df.drop(labels=['id', 'Unnamed: 32'], axis=1, errors='ignore')
df['target'] = df['diagnosis'].map({'B': 0, 'M': 1})
X = df.drop(labels=['diagnosis', 'target'], axis=1, errors='ignore')
y = df['target']

# 2. 형상 추출 (30차원 -> 2차원 압축)
X_scaled = StandardScaler().fit_transform(X) # 스케일링
pca = PCA(n_components=2)
X_pca = pca.fit_transform(X_scaled)          # PCA 가동

# 3. 2차원 데이터 시각화 (그래프 내 한글 제거로 경고 완벽 해결)
pca_df = pd.DataFrame(X_pca, columns=['PC1', 'PC2'])
pca_df['target'] = y.values

# 보존율 계산
pc1_ratio, pc2_ratio = pca.explained_variance_ratio_

plt.figure(figsize=(8, 5))
sns.scatterplot(data=pca_df, x='PC1', y='PC2', hue='target', palette='Set1', alpha=0.7)
plt.title("PCA Projection: 30D to 2D")
plt.xlabel(f"PC1 (Variance: {pc1_ratio:.1%})")
plt.ylabel(f"PC2 (Variance: {pc2_ratio:.1%})")
plt.show()

# 4. 결과 요약 출력 (콘솔은 한글 지원이 되므로 유지)
print(f"PC1: 원본 정보의 {pc1_ratio:.1%} 보존")
print(f"PC2: 원본 정보의 {pc2_ratio:.1%} 보존")
print(f"결론: 2개의 차원으로 원본 30차원 정보의 총 {pc1_ratio + pc2_ratio:.1%} 보존 완료!")
