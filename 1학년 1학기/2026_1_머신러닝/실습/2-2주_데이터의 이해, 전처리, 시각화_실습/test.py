import pandas as pd
from pathlib import Path


def load_housing_data():
    # [방법 1] 상대 경로 방식 (이미지 가이드에 따른 추천 방식)
    # 현재 실행 중인 파이썬 파일 위치를 기준으로 datasets 폴더 탐색
    base_path = Path(__file__).parent
    csv_path = base_path / "datasets" / "TSLA.csv"

    # [방법 2] 절대 경로 방식 (직접 경로를 지정할 학생만 주석 해제 후 사용)
    # csv_path = Path(r"C:\Users\LG\Desktop\lecture\week 2\project\datasets\housing.csv")

    # 데이터 로드
    return pd.read_csv(csv_path)


if __name__ == "__main__":
    # 1. 데이터 불러오기
    housing = load_housing_data()

    # 2. 데이터 확인 (상위 5개 행)
    print("--- Housing Data Head ---")
    print(housing.head())

    # 3. 데이터 요약 정보 확인
    print("\n--- Housing Data Info ---")
    print(housing.info())