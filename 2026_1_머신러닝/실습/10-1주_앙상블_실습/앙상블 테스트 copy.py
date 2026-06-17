import numpy as np
import matplotlib.pyplot as plt
from sklearn.datasets import make_moons
from sklearn.model_selection import train_test_split
from sklearn.tree import DecisionTreeClassifier
from sklearn.ensemble import (RandomForestClassifier, GradientBoostingClassifier,
                              VotingClassifier, StackingClassifier)
from sklearn.linear_model import LogisticRegression
from sklearn.svm import SVC
from sklearn.neighbors import KNeighborsClassifier
from sklearn.metrics import accuracy_score

# 1. 극한 노이즈 데이터 생성
X, y = make_moons(n_samples=500, noise=0.3, random_state=42)
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.3, random_state=42)

# 2. 모델 세팅 (인라인 선언으로 변수 최소화)
dt = DecisionTreeClassifier(random_state=42)
rf = RandomForestClassifier(n_estimators=500, random_state=42)
gb = GradientBoostingClassifier(n_estimators=100, max_depth=30, random_state=42)

models = {
    'Single Tree': dt,
    'Voting': VotingClassifier([('lr', LogisticRegression()), ('dt', dt),
                                 ('svc', SVC(probability=True, random_state=42))], voting='soft'),
    'Bagging (RF)': rf,
    'Boosting (GBM)': gb,
    'Stacking': StackingClassifier([('rf', rf), ('gb', gb), ('knn', KNeighborsClassifier())],
                                    final_estimator=LogisticRegression())
}

# 3. 모델 학습, 평가 및 시각화 (반복문 통합)
print("\n [극한 노이즈 환경] 앙상블 모델 성능 리포트\n")
fig, axes = plt.subplots(1, 5, figsize=(25, 4))
xx, yy = np.meshgrid(np.linspace(X[:, 0].min() - 0.5, X[:, 0].max() + 0.5, 100),
                     np.linspace(X[:, 1].min() - 0.5, X[:, 1].max() + 0.5, 100))

for ax, (name, model) in zip(axes, models.items()):
    model.fit(X_train, y_train)
    acc = accuracy_score(y_test, model.predict(X_test))

    # 텍스트 결과 출력 (간결하게 한 줄로)
    print(f"▶ {name:15s} 정확도: {acc * 100:.2f}%")

    # 그래프 시각화
    Z = model.predict(np.c_[xx.ravel(), yy.ravel()]).reshape(xx.shape)
    ax.contourf(xx, yy, Z, alpha=0.3, cmap='coolwarm')
    ax.scatter(X_train[:, 0], X_train[:, 1], c=y_train, cmap='coolwarm', edgecolors='k', s=20)

    ax.set_title(f"{name}\nAcc: {acc:.3f}", fontsize=14, fontweight='bold', color='darkred')
    ax.axis('off')

plt.tight_layout()
plt.show()
