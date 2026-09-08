import pandas as pd
from pathlib import Path
from sklearn.model_selection import train_test_split


def load_housing_data():
    base_path = Path(__file__).parent
    csv_path = base_path / "datasets" / "TSLA.csv"
    return pd.read_csv(csv_path)


if __name__ == "__main__":
    # 1. 데이터 로드
    housing = load_housing_data()
    base_path = Path(__file__).parent
    output_dir = base_path / "datasets"  # 저장할 폴더 위치

    # 2. 데이터 분할 (6:2:2)
    # [Step A] 전체의 20%를 Test 세트로 분리
    train_valid_set, test_set = train_test_split(
        housing, test_size=0.2, random_state=42
    )

    # [Step B] 남은 80% 중 25%를 Validation 세트로 분리 (전체의 20% 효과)
    train_set, valid_set = train_test_split(
        train_valid_set, test_size=0.25, random_state=42
    )

    # 3. 분할된 결과 출력 (검증)
    print("\nStep 9: Raw Data Splitting Results (6:2:2)")
    print("-" * 50)
    print(f"Total dataset:       {len(housing)} rows")
    print(f"Training set (60%):  {len(train_set)} rows")
    print(f"Validation set (20%): {len(valid_set)} rows")
    print(f"Test set (20%):      {len(test_set)} rows")

    # 4. 파일로 저장 (index=False 옵션으로 불필요한 번호 생성을 막습니다)
    train_set.to_csv(output_dir / "housing_train.csv", index=False)
    valid_set.to_csv(output_dir / "housing_valid.csv", index=False)
    test_set.to_csv(output_dir / "housing_test.csv", index=False)

    print("\nStep 10: Saving Files Complete")
    print("-" * 50)
    print(f"Files saved in: {output_dir}")