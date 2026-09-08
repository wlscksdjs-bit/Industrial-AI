import numpy as np
import matplotlib.pyplot as plt

def sigmoid(z):
    return 1 / (1 + np.exp(-z))

print(" [PART 1] 시그모이드 함수 수치 테스트 ")

s_0 = sigmoid(0)
print(f"입력값 0  => 압축된 확률: {s_0:.5f} (50%)")

s_100 = sigmoid(100)
# 수정: '\입력값' 이라는 오타를 수정하고 숫자 100을 추가했습니다.
print(f"입력값 100 => 압축된 확률: {s_100:.5f} (약 100%)")

s_m100 = sigmoid(-100)
print(f"입력값 -100 => 압축된 확률: {s_m100:.5f} (약 0%)")

# 수정: stop: 10, num: 200 -> stop=10, num=200 으로 등호(=) 사용
z_values = np.linspace(-10, stop=10, num=200)

probabilities = sigmoid(z_values)

plt.figure(figsize=(10, 6))

# 수정: *args: z_values 라는 잘못된 문법 제거
plt.plot(z_values, probabilities, color='red', linewidth=3, label='Sigmoid Curve')

plt.axhline(y=1.0, color='gray', linestyle='--', alpha=0.5)
plt.axhline(y=0.0, color='gray', linestyle='--', alpha=0.5)
plt.axhline(y=0.5, color='black', linestyle=':', label='Threshold (0.5)')

# 수정: 수평선을 긋는 axhline에 x값을 넣으면 오류가 납니다. 수직선인 axvline으로 변경했습니다.
# 수정: linestyle='-- '에 들어간 불필요한 공백 제거
plt.axvline(x=0.0, color='gray', linestyle='--', alpha=0.5)

# 수정: x: 0, y: 0.5 -> x=0, y=0.5 로 등호(=) 사용
plt.scatter(x=0, y=0.5, color='blue', s=100, zorder=5, label='Sigmoid(0) = 0.5')

# 수정: 닫는 괄호만 있던 문자열 오타 수정
plt.title('Sigmoid Function (Compressor)')
plt.xlabel('Raw Score (z) - from AI model')
plt.ylabel('Probability (0.0 ~ 1.0) - output')

# 수정: visible:True -> visible=True 로 등호(=) 사용
plt.grid(visible=True, linestyle='-', alpha=0.3)
plt.legend(loc='upper left')

#
plt.show()