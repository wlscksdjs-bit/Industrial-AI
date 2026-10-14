"""
anomaly_model.py — 학습된 설비 이상 탐지 모델 (제공, 수정하지 말 것)

사용법
    model = AnomalyModel()
    model.fit(warmup_samples)          # 학습 구간(정상) 샘플 리스트로 학습
    result = model.predict(sample)     # 샘플 1개 판정
    # result = {"anomaly": True/False, "type": "spike"|"drift"|"vib_noise"|"stuck"|None, "score": float}

sample은 텔레메트리 메시지(dict)를 그대로 넣는다: {"seq", "ts", "temp", "vib_rms", "current"}

판정 원리 (참고)
    - 전류로 온도·진동의 정상값을 예측하는 선형 회귀를 학습하고, 예측과의 차이(잔차)를 본다.
    - spike    : 진동 잔차가 순간적으로 매우 큼
    - vib_noise: 최근 진동 잔차의 흔들림(표준편차)이 정상의 2.5배 이상
    - stuck    : 최근 온도 값이 거의 변하지 않음 (센서 고착)
    - drift    : 온도 잔차가 정상 범위를 넘어 한쪽으로 커짐
"""
from collections import deque
import numpy as np


class AnomalyModel:
    WINDOW = 15  # 최근 샘플 창 크기

    def fit(self, samples):
        cur = np.array([s["current"] for s in samples])
        temp = np.array([s["temp"] for s in samples])
        vib = np.array([s["vib_rms"] for s in samples])
        A = np.vstack([cur, np.ones_like(cur)]).T
        self.temp_coef = np.linalg.lstsq(A, temp, rcond=None)[0]
        self.vib_coef = np.linalg.lstsq(A, vib, rcond=None)[0]
        self.temp_sd = float(np.std(temp - A @ self.temp_coef))
        self.vib_sd = float(np.std(vib - A @ self.vib_coef))
        temp_windows = [np.std(temp[i:i + self.WINDOW]) for i in range(len(temp) - self.WINDOW)]
        self.temp_win_sd = float(np.median(temp_windows))
        self.recent_temp = deque(maxlen=self.WINDOW)
        self.recent_vib_res = deque(maxlen=self.WINDOW)

    def predict(self, sample):
        c = sample["current"]
        temp_res = (sample["temp"] - (self.temp_coef[0] * c + self.temp_coef[1])) / self.temp_sd
        vib_res = (sample["vib_rms"] - (self.vib_coef[0] * c + self.vib_coef[1])) / self.vib_sd
        self.recent_temp.append(sample["temp"])
        self.recent_vib_res.append(vib_res)
        full = len(self.recent_temp) == self.WINDOW

        if vib_res > 16:
            return {"anomaly": True, "type": "spike", "score": round(float(vib_res), 2)}
        if full:
            vib_spread = float(np.std(self.recent_vib_res))
            if vib_spread > 2.5:
                return {"anomaly": True, "type": "vib_noise", "score": round(vib_spread, 2)}
            temp_spread = float(np.std(self.recent_temp)) / self.temp_win_sd
            if temp_spread < 0.15:
                return {"anomaly": True, "type": "stuck", "score": round(1 / max(temp_spread, 1e-3), 2)}
        if temp_res > 5:
            return {"anomaly": True, "type": "drift", "score": round(float(temp_res), 2)}
        return {"anomaly": False, "type": None, "score": round(float(max(abs(temp_res), abs(vib_res))), 2)}
