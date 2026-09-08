import pandas as pd
import numpy as np


def clean_secom_data(file_path):
    print("=== SECOM 반도체 공정 데이터 정제 시작 ===")

    # 1. 데이터 로드
    # 업로드해주신 단일 csv 파일('uci-secom.csv')을 기준으로 로드합니다.
    df = pd.read_csv(file_path)
    print(f"[초기 데이터 크기] 레코드 수: {df.shape[0]}건, 컬럼 수: {df.shape[1]}개\n")

    # =====================================================================
    # [1] 'Time' (시간 스탬프) 열
    # =====================================================================
    if 'Time' in df.columns:
        df['Time'] = pd.to_datetime(df['Time'], errors='coerce')
        df = df.sort_values(by='Time').reset_index(drop=True)
        print("[1. 시간 스탬프 처리 완료] 데이터를 시간순으로 정렬했습니다.")

    # =====================================================================
    # [2] 타겟 변수 (Pass/Fail 결과) 열
    # =====================================================================
    # 데이터셋에 따라 타겟 컬럼명이 다를 수 있으므로 탐색 로직 적용 ('Pass/Fail' 등)
    target_col = [col for col in df.columns if col.lower() in ['pass/fail', 'class', 'target', 'label']]
    if target_col:
        target_name = target_col[0]
        # 합격(보통 -1, 0.1, 0 등으로 표현됨) -> 0 / 불합격(보통 1) -> 1
        df[target_name] = df[target_name].apply(lambda x: 1 if x == 1 else 0)
        print(f"[2. 타겟 변수 처리 완료] '{target_name}' 열을 양품(0), 불량(1)로 변환했습니다.")

    # 센서 데이터 컬럼만 추출 (시간과 타겟 변수 제외)
    sensor_cols = [col for col in df.columns if col not in ['Time', target_name]]

    # =====================================================================
    # [3] 결측치가 너무 많은 센서 데이터 열 (결측값 처리)
    # =====================================================================
    missing_ratio = df[sensor_cols].isnull().mean()
    # 결측률이 50% 이상인 열의 이름 추출
    drop_cols_missing = missing_ratio[missing_ratio >= 0.5].index.tolist()

    df = df.drop(columns=drop_cols_missing)
    sensor_cols = [col for col in sensor_cols if col not in drop_cols_missing]  # 센서 리스트 업데이트
    print(f"[3. 심각한 결측치 열 제거 완료] 결측치 50% 이상인 센서 {len(drop_cols_missing)}개 열을 삭제했습니다.")

    # =====================================================================
    # [4] 변화가 없는 단일 값 센서 열 (분산이 0인 Feature)
    # =====================================================================
    drop_cols_constant = [col for col in sensor_cols if df[col].nunique(dropna=True) <= 1]

    df = df.drop(columns=drop_cols_constant)
    sensor_cols = [col for col in sensor_cols if col not in drop_cols_constant]  # 센서 리스트 업데이트
    print(f"[4. 무의미한 센서 제거 완료] 분산이 0인(값이 일정한) 센서 {len(drop_cols_constant)}개 열을 삭제했습니다.")

    # =====================================================================
    # [5] 잔여 결측치 보간 (Imputation)
    # =====================================================================
    # 중앙값으로 결측치 보간
    df[sensor_cols] = df[sensor_cols].fillna(df[sensor_cols].median())
    print("[5. 잔여 결측치 보간 완료] 남은 센서의 결측치를 '중앙값(Median)'으로 채웠습니다.\n")

    # 최종 결과 요약
    print("=== [최종 결과] 정제된 데이터셋 ===")
    print(f" - 최종 레코드 수: {df.shape[0]}건")
    print(f" - 최종 확보된 유효 센서 특징 수: {len(sensor_cols)}개 (초기 590여개 대비 대폭 감소)")
    print("===================================")

    # 정제된 데이터를 새로운 파일로 저장
    output_filename = 'secom_cleaned.csv'
    df.to_csv(output_filename, index=False)
    print(f"성공적으로 정제된 데이터가 '{output_filename}'로 저장되었습니다.")

    return df

if __name__ == "__main__":

    cleaned_dataframe = clean_secom_data('uci-secom.csv')