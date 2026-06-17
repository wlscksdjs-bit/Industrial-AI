import numpy as np


def sigmoid(z):
    return 1 / (1 + np.exp(-z))


def hypothesis_function(x, theta):
    z = np.dot(x, theta)
    return sigmoid(z)


def compute_cost(x, y, theta):
    m = y.shape[0]
    h = hypothesis_function(x, theta)
    term1 = y.T.dot(np.log(h + 1e-5))
    term2 = (1 - y).T.dot(np.log(1 - h + 1e-5))
    return (-1.0 / m) * (term1 + term2)


def minimize_gradient(x, y, theta, iterations=1000, alpha=0.01):
    m = y.size
    cost_history = []

    for _ in range(iterations):
        h = hypothesis_function(x, theta)

        # ✅ 추가된 부분: 예측값(h)과 실제 정답(y)의 오차(loss)를 계산합니다.
        loss = h - y

        # 이제 loss가 정의되었으므로 gradient를 정상적으로 계산할 수 있습니다.
        gradient = x.T.dot(loss) / m
        theta = theta - (alpha * gradient)

        if (_ % 100) == 0:
            current_cost = compute_cost(x, y, theta)
            cost_history.append(current_cost)
            print(f"반복 횟수 {_:>4} : 현재 비용(Cost) = {current_cost:.5f}")

    return theta, cost_history


# 테스트 데이터 준비
X_test = np.array([[1, 2], [3, 4], [5, 6]])  # 컴마(,) 오타 수정: [3, 4,] -> [3, 4]
y_test = np.array([1, 0, 1])
initial_theta = np.array([0.0, 0.0])

print(" 학습을 시작합니다... ")
final_theta, history = minimize_gradient(X_test, y_test, initial_theta, iterations=1000, alpha=0.01)

print("\n 학습 완료! ")
print(f"최종 가중치(theta): {final_theta}")
print(f"최종 비용(Cost): {compute_cost(X_test, y_test, final_theta):.5f}")