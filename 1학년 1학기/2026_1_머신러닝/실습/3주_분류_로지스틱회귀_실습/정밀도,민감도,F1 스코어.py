import numpy as np
from sklearn.metrics import accuracy_score, recall_score, f1_score, precision_score

y_pred = np.array([0, 1, 1, 0, 1, 1, 1, 0])
y_true = np.array([0, 1, 0, 0, 0, 0, 1, 1])

precision = precision_score(y_true, y_pred)
print("1. 정밀도(Precision):")
print(f"결과: {precision}")
print()

recall = recall_score(y_true, y_pred)
print("2. 민감도(Recall):")
print(f"결과: {recall}")
print()

f1 = f1_score(y_true, y_pred)
print("3. F1 스코어(F1-Score:")
print(f"결과: {f1}")
