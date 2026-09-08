import numpy as np
import matplotlib.pyplot as plt


def softmax(values):
    array_values = np.exp(values)
    return array_values / np.sum(array_values)


values = [-2, -1, -5, 0.5]
y = softmax(values)


labels = [f'Class {i} ({v})' for i, v in enumerate(values)]
colors = ['#4f46e5', '#818cf8', '#c7d2fe', '#f43f5e']

fig, ax = plt.subplots(figsize=(12, 4))

left_pos = 0
for i in range(len(y)):
    ax.barh('Softmax Total (1.0)', y[i], left=left_pos, color=colors[i], label=labels[i], edgecolor='white', height=0.6)


    if y[i] > 0.03:
        ax.text(left_pos + y[i] / 2, 0, f'{y[i] * 100:.1f}%',
                va='center', ha='center', color='white' if i != 2 else 'black',
                fontweight='bold', fontsize=11)

    left_pos += y[i]


ax.set_title('Softmax Output: 100% Stacked Visualization', fontsize=16, pad=20)
ax.set_xlim(0, 1)
ax.set_xticks([0, 0.25, 0.5, 0.75, 1.0])
ax.set_xticklabels(['0', '0.25', '0.5', '0.75', '1.0 (Total)'])
ax.legend(loc='upper center', bbox_to_anchor=(0.5, -0.15), ncol=4, frameon=False)

ax.spines['top'].set_visible(False)
ax.spines['right'].set_visible(False)
ax.spines['left'].set_visible(False)

plt.tight_layout()
plt.show()

print("각 클래스 확률:", [f"{prob:.4f}" for prob in y])
print("확률 총합:", np.sum(y))