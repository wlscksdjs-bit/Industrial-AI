import numpy as np
import matplotlib.pyplot as plt
from sklearn import datasets
from sklearn.linear_model import LogisticRegression

digits = datasets.load_digits()
X, y = digits.data, digits.target
mask = np.isin(y, [0, 1, 2])
X_sub, y_sub = X[mask], y[mask]

y_binary = (y_sub == 0).astype(int)
model_sigmoid = LogisticRegression(max_iter=10000).fit(X_sub, y_binary)

prob_sigmoid = model_sigmoid.predict_proba(X_sub[:1])[0]

model_softmax = LogisticRegression(max_iter=10000).fit(X_sub, y_sub)
prob_softmax = model_softmax.predict_proba(X_sub[:1])[0]

print(f"=== 확률 결과 비교 ===")
print(f"Sigmoid Output (Is it 0?): {prob_sigmoid}")
print(f"Softmax Output (0, 1, or 2?): {prob_softmax}")

plt.figure(figsize=(12, 5))

plt.subplot(1, 2, 1)
plt.bar(['Not 0', 'Is 0'], prob_sigmoid, color=['lightgray', 'royalblue'], alpha=0.8)
plt.title("Sigmoid Output: Binary Classification", fontsize=14)
plt.ylabel("Probability")
plt.ylim(0, 1.1)
for i, v in enumerate(prob_sigmoid):
    plt.text(i, v + 0.02, f"{v:.2f}", ha='center')

plt.subplot(1, 2, 2)
plt.bar(['Digit 0', 'Digit 1', 'Digit 2'], prob_softmax, color=['tomato', 'mediumseagreen', 'orange'], alpha=0.8)
plt.title("Softmax (Multicass Classification)", fontsize=14)
plt.ylabel("Probability")
plt.ylim(0, 1.1)
for i, v in enumerate(prob_softmax):
    plt.text(i, v + 0.02, f"{v:.2f}", ha='center')

plt.tight_layout()
plt.show()
