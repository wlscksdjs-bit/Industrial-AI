import numpy as np
from sklearn.metrics import accuracy_score

y_pred = np.array([0, 1, 1, 0])
y_true = np.array([0, 1, 0, 0])

manual_accuracy = sum(y_pred == y_true) / len(y_true)
print(" 1. 직접 계산한 정확도 ")
print(f"맞춘 개수(3) / 전체 개수(4) = {manual_accuracy}")
print()
sklearn_accuracy = accuracy_score(y_true, y_pred)
print(" 2. 사이킷런 함수(accuracy_score)를 사용한 정확도 ")
print(f"결과: {sklearn_accuracy}")
