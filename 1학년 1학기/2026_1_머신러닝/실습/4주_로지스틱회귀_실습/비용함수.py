import numpy as np

def sigmoid(z):
    return 1 / (1 + np.exp(-z))

def hypothesis_function(x, theta):
    z = np.dot(x, theta)
    return sigmoid(z)

def compute_cost(x, y, theta):
    m = y.shape[0]
    h = hypothesis_function(x, theta)

    term1 = y.T.dot(np.log(h))
    term2 = (1 - y).T.dot(np.log(1 - h))

    J = (-1.0 / m) * (term1 + term2)
    return J

X = np.array([
    [1, 2],
    [3, 4],
    [5, 6]
])

y= np.array([1, 0, 1])

theta = np.array([0.1, 0.2])

predictions = hypothesis_function(X, theta)
print("=== 1. 모델의 예측 확률 ===")
print(predictions)
print()

cost = compute_cost(X, y, theta)
print("=== 2. 현재 모델의 비용(Cost) ===")
print(f"반성 점수: {cost:.4f}")
