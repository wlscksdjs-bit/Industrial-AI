import numpy as np
import matplotlib.pyplot as plt

def softmax(values):
    array_values = np.exp(values)
    return array_values / np.sum(array_values)

values = [-2, -1, -5, 0.5]
labels = [f'Class {i}\n({v})' for i, v in enumerate(values)]

y= softmax(values)

plt.figure(figsize=(10, 6))

bars = plt.bar(labels, y, color=['#4f45e5', '#818cf8', '#c7d2fe', '#f43f5e'])

for bar in bars:
    height = bar.get_height()
    plt.text(bar.get_x() + bar.get_width() / 2, height + 0.01, f'{height*100:.1f}%', ha='center', va='bottom', fontweight='bold')

plt.title("Softmax Output: Probability Distribution", fontsize=15, pad=20)
plt.xlabel("Classes (Input Score)", fontsize=12)
plt.ylabel("Probability", fontsize=12)
plt.ylim(0, 1.1)
plt.grid(axis='y', linestyle='--', alpha=0.7)
plt.show()

print("입력 점수:", values)
print("확률 변환:", [f"{prob*100:.2f}%" for prob in y])
