from sklearn.metrics import confusion_matrix

y_true = [1, 0, 1, 1, 0, 1]
y_pred = [0, 0, 1, 1, 0, 1]

cm = confusion_matrix(y_true, y_pred)

print("1. 혼동 행렬 전체 모습")
print(cm)
print()

tn, fp, fn, tp = confusion_matrix(y_true, y_pred).ravel()

print("2. 세부 지표 값 확인")
print(f"TN (True Negatives) : {tn}")
print(f"FP (False Positives) : {fp}")
print(f"FN (False Negatives) : {fn}")
print(f"TP (True Positives) : {tp}")

