import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler


def preprocess_wafer_data(file_path):
    print("=== 반도체 웨이퍼 결함 데이터셋 전처리 시작 ===\n")

    # 1. 데이터 로드
    df = pd.read_csv(file_path)
    print(f"[초기 데이터] 총 웨이퍼 수: {df.shape[0]}개, 컬럼 수: {df.shape[1]}개")

    # =====================================================================
    # [1] 식별자 열 처리 (wafer_id)
    # =====================================================================
    if 'wafer_id' in df.columns:
        df = df.drop(columns=['wafer_id'])
        print("[1. 식별자 처리 완료] 예측에 무의미한 'wafer_id' 열을 제거했습니다.")

    # =====================================================================
    # [2] 범주형 메타데이터 인코딩 (process_step)
    # =====================================================================
    if 'process_step' in df.columns:
        df = pd.get_dummies(df, columns=['process_step'], dtype=int)
        print("[2. 범주형 데이터 변환 완료] 'process_step' 열을 원-핫 인코딩했습니다.")

    # =====================================================================
    # [3] 타겟 변수 분리 및 보존 (defect_label)
    # =====================================================================
    X = df.drop(columns=['defect_label'])
    y = df['defect_label']
    print("[3. 타겟 변수 분리 완료] 특징(X)과 정답지(y) 분할 완료.")

    # =====================================================================
    # [4] 데이터셋 3분할 (Train 70%, Validation 15%, Test 15%)
    # =====================================================================
    # 1차 분할: Train(70%) / Temp(30%)
    X_train, X_temp, y_train, y_temp = train_test_split(X, y, test_size=0.30, stratify=y, random_state=42)
    # 2차 분할: Validation(15%) / Test(15%) -> Temp의 절반씩
    X_val, X_test, y_val, y_test = train_test_split(X_temp, y_temp, test_size=0.50, stratify=y_temp, random_state=42)

    print("\n[4. 데이터셋 분할 완료 (Train:Val:Test = 70:15:15)]")
    print(f" - Train 세트: {X_train.shape[0]}개 (학습용)")
    print(f" - Validation 세트: {X_val.shape[0]}개 (하이퍼파라미터 튜닝용)")
    print(f" - Test 세트: {X_test.shape[0]}개 (최종 평가용)")

    # =====================================================================
    # [5] 센서 데이터 스케일링 (피처 크기 조정)
    # =====================================================================
    scaler = StandardScaler()

    # Train 데이터로만 기준(평균, 분산)을 학습(fit)하고 변환(transform)
    X_train_scaled = pd.DataFrame(scaler.fit_transform(X_train), columns=X_train.columns)

    # Train에서 얻은 기준을 그대로 Validation, Test 데이터에 적용(transform만 수행)
    X_val_scaled = pd.DataFrame(scaler.transform(X_val), columns=X_val.columns)
    X_test_scaled = pd.DataFrame(scaler.transform(X_test), columns=X_test.columns)
    print("\n[5. 피처 스케일링 완료] 센서 값의 단위 차이를 표준화(StandardScaler) 했습니다.")

    print("\n=== 전처리 파이프라인 완료 ===")

    # 학습, 검증, 테스트 셋업을 반환하여 모델링에 바로 사용할 수 있도록 함
    return X_train_scaled, X_val_scaled, X_test_scaled, y_train, y_val, y_test


# 실행 예시
if __name__ == "__main__":
    # 데이터셋 파일명 입력 (동일 폴더 내 존재 시)
    file_name = 'semiconductor_wafer_defect_dataset.csv'

    # 전처리 함수 호출
    X_train, X_val, X_test, y_train, y_val, y_test = preprocess_wafer_data(file_name)

    # 결과 확인 (예: 학습 데이터의 첫 3개 행 출력)
    print("\n[미리보기] 전처리된 Train Dataset (상위 3행):")
    print(X_train.head(3))