import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# 0. 데이터 불러오기 및 실전 전처리
file_path = r"C:\Users\JIN\PycharmProjects\PythonProject1\11_data.csv"

df = pd.read_csv(file_path)
print(f"Data Loaded Successfully! (Shape: {df.shape})")

# 불필요한 ID 컬럼 및 빈 컬럼 제거
df = df.drop(labels=['id', 'Unnamed: 32'], axis=1, errors='ignore')

# 정답(diagnosis) 문자형 데이터를 숫자형(0과 1)으로 인코딩
df['target'] = df['diagnosis'].map({'B': 0, 'M': 1})
df = df.drop('diagnosis', axis=1)

# 피처(X)와 정답(y) 분리
X = df.drop('target', axis=1)
y = df['target']

print(f"Preprocessing Complete! (Features: {X.shape[1]})\n")

# Step 1: 형상 선택 (Feature Selection)
print("Starting Correlation Heatmap Visualization...")

# 시각화 사이즈 설정
plt.figure(figsize=(12, 10))

# 30개 피처가 너무 많으니, 앞의 10개 피처만 잘라서 상관계수 계산
top10_variance_features = X.var().sort_values(ascending=False).head(10).index

print("변동(분산)이 가장 큰 Top 10 피처:")
print(top10_variance_features.tolist())
corr_matrix = X[top10_variance_features].corr()

# Seaborn 라이브러리로 히트맵 그리기
sns.heatmap(corr_matrix,
            annot=True,         # 칸 안에 숫자(상관계수) 표시
            fmt=".2f",          # 소수점 둘째 자리까지 표시
            cmap='coolwarm',    # 색상 테마 (빨간색일수록 양의 상관관계가 높음)
            vmin=-1, vmax=1)    # 최소/최대값 설정

plt.title("Feature Correlation Heatmap (Top 10 Features)")
plt.show()

# ---------------------------------------------------------
# 1-2. 트리 모델의 피처 중요도 (정답 힌트 점수 매기기)
from sklearn.ensemble import RandomForestClassifier

print("\n[1-2] 랜덤 포레스트를 활용한 피처 중요도 분석을 시작합니다.")

# 랜덤 포레스트 모델 생성 및 전체 피처(X)를 넣어 학습
rf_model = RandomForestClassifier(random_state=42)
rf_model.fit(X, y)

# 피처 중요도(Feature Importances) 추출 및 보기 좋게 시리즈로 변환
importances = pd.Series(rf_model.feature_importances_, index=X.columns)
top10_importances = importances.sort_values(ascending=False).head(10)

# 중요도가 높은 상위 10개 시각화 (막대그래프)
plt.figure(figsize=(10, 6))
top10_importances.plot.barh(color='steelblue')
plt.title("1-2. Feature Importance from Random Forest (The 'Strainer')")
plt.xlabel("Importance Score (Loss Reduction)")
plt.gca().invert_yaxis() # 1등이 맨 위에 오도록 y축 뒤집기

plt.tight_layout() # 글씨 잘림 방지
plt.show()

# 막대그래프 창을 닫으면 콘솔에 결과 표 출력
print("\n[결과 요약] 상위 10개 핵심 피처 및 중요도 점수")
print("-" * 50)

# 보기 좋은 표 형태로 변환하여 출력
top10_df = top10_importances.reset_index()
top10_df.columns = ['Feature Name (피처명)', 'Importance Score (중요도)']
print(top10_df.to_string(index=False))

print("-" * 50)
print("위 변수들이 정답을 맞히는 데 가장 큰 기여를 함을 알 수 있습니다.")

# Step 2: 형상 추출 (Feature Extraction) - PCA
print("\n[Step 2] PCA(주성분 분석)를 통한 형상 추출을 시작합니다.")
from sklearn.decomposition import PCA
from sklearn.preprocessing import StandardScaler

# PCA 전에는 스케일링이 필수! (평균 0, 분산 1로 표준화)
scaler = StandardScaler()
X_scaled = scaler.fit_transform(X)

# 2개의 주성분(PC1, PC2)으로 압축
pca = PCA(n_components=2)
X_pca = pca.fit_transform(X_scaled)

# PCA 결과 데이터프레임 생성
pca_df = pd.DataFrame(data=X_pca, columns=['PC1', 'PC2'])
pca_df['target'] = y.values

# PCA 시각화 (2차원 평면에 30개 피처의 정보를 압축하여 표현)
plt.figure(figsize=(10, 7))
sns.scatterplot(x='PC1', y='PC2', hue='target', data=pca_df, palette='viridis', alpha=0.7)
plt.title('Step 2. PCA Result (Dimension Reduction 30 -> 2)')
plt.grid(True)
plt.show()

print("\n[완료] 차원 축소 완료: 30개의 피처를 정보 손실을 최소화하며 2개로 압축하였습니다.")
