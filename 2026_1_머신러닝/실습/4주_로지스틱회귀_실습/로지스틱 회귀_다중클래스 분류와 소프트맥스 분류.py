import numpy as np
def softmax(values):
    array_values = np.exp(values)
    return array_values / np.sum(array_values)
values = [-2, -1, -5, 0.5]
y = softmax(values)
print("1. 입력값 (values):", values)
print("2. 소프트맥스 결과 (y):")
for i, prob in enumerate(y):
    print(f"  - 클래스 {i}의 확률: {prob:.8f} ({prob * 100:.2f}%)")

total_sum = y.sum()
print("\n3. 결과값의 총합 (y.sum()):", total_sum)
max_index = np.argmax(y)
print(f"\n 가장 높은 확률을 가진 인덱스는 {max_index}번이며, 값은{values[max_index]}입니다.")
