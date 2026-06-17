import numpy as np
import matplotlib.pyplot as plt
from sklearn.svm import SVC
from sklearn.datasets import make_blobs

X, y = make_blobs(n_samples=50, centers=2, random_state=6, cluster_std=1.5)
# 라벨을 SVM 수식처럼 -1과 1로 변경
y[y == 0] = -1

# 소프트 마진 (C=0.1) 모델 학습
svm_soft = SVC(kernel='linear', C=0.1)
svm_soft.fit(X, y)

# 하드 마진 스타일 (C=1000) 모델 학습
svm_hard = SVC(kernel='linear', C=1000.0)
svm_hard.fit(X, y)


# 결과 확인: 알파(dual_coef_)의 절대값 출력 (텍스트)
def print_alpha_info(model, name):
    alphas = np.abs(model.dual_coef_)[0]
    print(f"[{name} 결과]")
    print(f"설정된 C 값: {model.C}")
    print(f"실제 알파(alpha)들의 최대값: {np.max(alphas):.4f}")
    print(f"C 값에 도달한 서포트 벡터 개수: {np.sum(np.isclose(alphas, model.C))}개")
    print("-" * 30)


# 결정 경계 방정식 출력 (텍스트)
def print_equation(model, name):
    # 1. w 값 추출 (coef_ 배열에 저장되어 있음)
    w = model.coef_[0]

    # 2. b 값 추출 (intercept_ 에 저장되어 있음)
    b = model.intercept_[0]

    print(f"[{name} 결정 경계 방정식]")
    print(f"w (가중치 벡터): [{w[0]:.4f}, {w[1]:.4f}]")
    print(f"b (편향/절편): {b:.4f}")
    # 2차원 데이터이므로 w1*x1 + w2*x2 + b = 0 형태가 됩니다.
    print(f"방정식: {w[0]:.4f}*x1 + {w[1]:.4f}*x2 + {b:.4f} = 0")
    print("-" * 40)


# 텍스트 출력 함수 실행
print_alpha_info(svm_soft, "Soft Margin")
print_alpha_info(svm_hard, "Hard Margin (High C)")

print_equation(svm_soft, "Soft Margin (C=0.1)")
print_equation(svm_hard, "Hard Margin (C=1000.0)")

# 시각화 설정 및 그리기
fig, axes = plt.subplots(1, 2, figsize=(14, 6))
models = [svm_soft, svm_hard]
titles = ["Soft Margin (C=0.1)", "Hard Margin (C=1000.0)"]

for i, (model, title) in enumerate(zip(models, titles)):
    ax = axes[i]

    # 데이터 산점도 그리기
    ax.scatter(X[:, 0], X[:, 1], c=y, cmap='coolwarm', s=50, edgecolors='k')

    # 마진 선을 그리기 위한 가상의 그물망(그리드) 생성
    xlim, ylim = ax.get_xlim(), ax.get_ylim()
    xx, yy = np.meshgrid(np.linspace(xlim[0], xlim[1], 50), np.linspace(ylim[0], ylim[1], 50))
    Z = model.decision_function(np.c_[xx.ravel(), yy.ravel()]).reshape(xx.shape)

    # 결정 경계(0) 및 마진 선(-1, 1) 시각화
    ax.contour(xx, yy, Z, colors='k', levels=[-1, 0, 1], alpha=0.5, linestyles=['--', '-', '--'])

    # 서포트 벡터에 큰 동그라미 그려서 강조
    ax.scatter(model.support_vectors_[:, 0], model.support_vectors_[:, 1],
               s=200, linewidth=2, facecolors='none', edgecolors='k')

    ax.set_title(f'Decision Boundary: {title}', size=16)

plt.tight_layout()
plt.show()