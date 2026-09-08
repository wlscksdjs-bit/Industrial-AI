import numpy as np

def sigmoid(z):
    return 1 / (1 + np.exp(-z))

def hyporthesis_function(x, theta):
    z = np.dot(x, theta)
    return sigmoid(z)

x_data = np.array([30, 0.8])
theta_data = np.array([0.1, 5.0])

prob = hyporthesis_function(x_data, theta_data)
print(f"종합 점수(z): {np.dot(x_data, theta_data)}")
print(f"최종 고장 확률: {prob * 100:.2f}%")
