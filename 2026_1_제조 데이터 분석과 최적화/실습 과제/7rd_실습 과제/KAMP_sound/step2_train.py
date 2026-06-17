import os
import glob
import numpy as np
import pandas as pd
import librosa
from sklearn.model_selection import train_test_split
from sklearn.tree import DecisionTreeClassifier
import joblib # 모델 저장을 위한 라이브러리 추가

# 1. 주파수 스펙트럼 추출 함수 정의
def mk_Frequency(y, sr):
    fft = np.fft.fft(y)
    magnitude = np.abs(fft)
    fre = np.linspace(0, sr, len(magnitude))
    
    haf_spectrum = magnitude[:int(len(magnitude)/2)]
    haf_fre = fre[:int(len(magnitude)/2)]
    return haf_spectrum, haf_fre

# 2. 데이터 경로 설정 및 특성 추출 (EDA 단계와 동일)
ok_path = 'FAN_sound_OK/*'
err_path = 'FAN_sound_error/*'

ok_files = glob.glob(ok_path)
err_files = glob.glob(err_path)

spectrum_mins, spectrum_maxs, mfcc_mins, mfcc_maxs, labels = [], [], [], [], []

print("데이터 특성 추출을 시작합니다...")
# (학생들에게는 이전에 작성한 반복문 코드가 이 자리에 들어간다고 설명해주시면 됩니다)
for path in ok_files:
    y, sr = librosa.load(path, sr=100)
    haf_spectrum, _ = mk_Frequency(y, sr)
    mfcc = librosa.feature.mfcc(y=y, sr=sr, n_fft=2048, hop_length=512, n_mfcc=13)
    spectrum_mins.append(np.min(haf_spectrum)); spectrum_maxs.append(np.max(haf_spectrum))
    mfcc_mins.append(np.min(mfcc)); mfcc_maxs.append(np.max(mfcc))
    labels.append(0)

for path in err_files:
    y, sr = librosa.load(path, sr=100)
    haf_spectrum, _ = mk_Frequency(y, sr)
    mfcc = librosa.feature.mfcc(y=y, sr=sr, n_fft=2048, hop_length=512, n_mfcc=13)
    spectrum_mins.append(np.min(haf_spectrum)); spectrum_maxs.append(np.max(haf_spectrum))
    mfcc_mins.append(np.min(mfcc)); mfcc_maxs.append(np.max(mfcc))
    labels.append(1)

df_sound = pd.DataFrame({
    'mfcc_min': mfcc_mins, 'mfcc_max': mfcc_maxs,
    'spectrum_min': spectrum_mins, 'spectrum_max': spectrum_maxs,
    'NG': labels,
    'filepath': ok_files + err_files
})

# 3. 데이터 분리 및 저장
data = df_sound[['mfcc_min', 'mfcc_max', 'spectrum_min', 'spectrum_max', 'filepath']] 
target = df_sound['NG']

X_train, X_test, y_train, y_test = train_test_split(
    data, target, test_size=0.3, shuffle=True, stratify=target, random_state=34
)

# 파일 경로는 학습에 사용되지 않으므로 따로 분리합니다.
test_filepaths = X_test['filepath']
X_train = X_train.drop(columns=['filepath'])
X_test = X_test.drop(columns=['filepath'])

# 차후 평가 파일에서 사용하기 위해 테스트 데이터를 CSV로 저장합니다.
X_test.to_csv('X_test.csv', index=False)
y_test.to_csv('y_test.csv', index=False)
test_filepaths.to_csv('test_filepaths.csv', index=False)
print("테스트 데이터(X_test.csv, y_test.csv, test_filepaths.csv)를 성공적으로 저장했습니다.")

# 4. 모델링 및 학습
print("의사결정나무 모델 학습을 시작합니다...")
Dtc = DecisionTreeClassifier(criterion='entropy', max_depth=3, random_state=0)
Dtc.fit(X_train, y_train)

# 5. 학습된 모델 저장 (.pkl 형식)
joblib.dump(Dtc, 'dtc_sound_model.pkl')
print("모델이 'dtc_sound_model.pkl' 이름으로 성공적으로 저장되었습니다!")