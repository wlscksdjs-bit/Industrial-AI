import pandas as pd
import matplotlib.pyplot as plt
from sklearn.preprocessing import StandardScaler
from sklearn.decomposition import PCA
# 3D 시각화를 위해 필요한 도구
from mpl_toolkits.mplot3d import Axes3D

# 1. 데이터 준비 및 전처리
file_path = r"C:\Users\JIN\PycharmProjects\PythonProject1\11_data.csv"
df = pd.read_csv(file_path)
df = df.drop(labels=['id', 'Unnamed: 32'], axis=1, errors='ignore')
df['target'] = df['diagnosis'].map({'B': 0, 'M': 1})
X = df.drop(labels=['diagnosis', 'target'], axis=1, errors='ignore')
y = df['target']

# 2. 형상 추출 (30차원 -> 3차원 압축!)
X_scaled = StandardScaler().fit_transform(X)
pca = PCA(n_components=3)   # 도착지를 3차원으로 변경!
X_pca = pca.fit_transform(X_scaled)

# 3. 3차원 데이터 시각화 준비
pca_df = pd.DataFrame(X_pca, columns=['PC1', 'PC2', 'PC3']) # PC3 기둥 추가!
pca_df['target'] = y.values

# 보존율 계산
pc1_ratio, pc2_ratio, pc3_ratio = pca.explained_variance_ratio_

# 3D 도화지 펴기
fig = plt.figure(figsize=(10, 8))
ax = fig.add_subplot(111, projection='3d') # 3D 옵션 켜기

# 정답(target)별로 데이터를 분리해서 3D 공간에 점 찍기
df_0 = pca_df[pca_df['target'] == 0] # 양성
df_1 = pca_df[pca_df['target'] == 1] # 악성

ax.scatter(df_0['PC1'], df_0['PC2'], df_0['PC3'], color='steelblue', label='Benign (0)', alpha=0.7)
ax.scatter(df_1['PC1'], df_1['PC2'], df_1['PC3'], color='indianred', label='Malignant (1)', alpha=0.7)

# 축 이름과 제목 설정 (한글 폰트 에러 방지를 위해 영어 사용)
ax.set_title("PCA Projection: 30D to 3D")
ax.set_xlabel(f"PC1 ({pc1_ratio:.1%})")
ax.set_ylabel(f"PC2 ({pc2_ratio:.1%})")
ax.set_zlabel(f"PC3 ({pc3_ratio:.1%})") # Z축(깊이) 추가!
ax.legend()

plt.show()

# 4. 결과 요약 출력
print(f"PC1: 원본 정보의 {pc1_ratio:.1%} 보존")
print(f"PC2: 원본 정보의 {pc2_ratio:.1%} 보존")
print(f"PC3: 원본 정보의 {pc3_ratio:.1%} 보존")
total_ratio = pc1_ratio + pc2_ratio + pc3_ratio
print(f"결론: 3개의 차원으로 원본 30차원 정보의 총 {total_ratio:.1%} 보존 완료!")
