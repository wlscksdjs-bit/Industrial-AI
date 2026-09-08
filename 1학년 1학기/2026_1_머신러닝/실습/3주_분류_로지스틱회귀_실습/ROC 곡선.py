import numpy as np
from sklearn.metrics import roc_curve
import matplotlib.pyplot as plt

y_true = np.array([0, 0, 1, 1])
y_scores = np.array([0.1, 0.4, 0.35, 0.8])

fpr, tpr, thresholds = roc_curve(y_true, y_scores)

print("=== ROC 곡선 계산 결과 ===")
print(f"기준점(Thresholds) : {thresholds}")
print(f"X축 - FPR (오경보 비율) : {fpr}")
print(f"Y축 - TPR (민감도) : {tpr}")
print()

plt.figure(figsize=(6, 6))

plt.plot(fpr, tpr, marker='o', color='blue', linewidth=2, label='Our AI Model')

plt.plot([0, 1], [0, 1], color='gray', linestyle='--', label='Random (50%)')

plt.title('ROC Curve Analysis')
plt.xlabel('False Positive Rate (FPR)')
plt.ylabel('True Positive Rate (TPR)')
plt.grid(True)
plt.legend()

plt.show()
