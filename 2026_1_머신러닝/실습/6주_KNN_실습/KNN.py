import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.neighbors import KNeighborsClassifier
from sklearn.metrics import classification_report, confusion_matrix, accuracy_score

file_path = r"C:\Users\JIN\PycharmProjects\PythonProject1\iris.csv"
df = pd.read_csv(file_path)
X = df.drop(columns=['variety'])
y = df['variety']

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

scaler = StandardScaler()
X_train_scaled = scaler.fit_transform(X_train)
X_test_scaled = scaler.transform(X_test)

knn = KNeighborsClassifier(n_neighbors=26)
knn.fit(X_train_scaled, y_train)
y_pred = knn.predict(X_test_scaled)

print("\n" + "="*50)
print(f" 최종 모델 정확도: {accuracy_score(y_test, y_pred) * 100:.2f}%")
print("="*50 + "\n")

report_dict = classification_report(y_test, y_pred, output_dict=True)
report_df = pd.DataFrame(report_dict).transpose()

print("[표 1: 품종별 상세 분류 성능 지표]")
print(report_df.round(3))
print("-" * 50 + "\n")

cm = confusion_matrix(y_test, y_pred)
labels = knn.classes_
cm_df = pd.DataFrame(cm, index=[f"실제_{l}" for l in labels],
                        columns=[f"예측_{l}" for l in labels])

print("[표2: 혼동 행렬 (Confusion Matrix Table)]")
print(cm_df)
print("=" * 50)
