import pandas as pd
from pathlib import Path

def load_tsla_data():

    base_path = Path(r"C:\Users\JIN\PycharmProjects\PythonProject2")
    csv_path = base_path / "datasets" / "TSLA.csv"

    return pd.read_csv(csv_path)

if __name__ == "__main__":
    # Load data
    tsla_data = load_tsla_data()

    # Step 1: Initial check
    print("\nStep 1: Checking for missing values")
    print(tsla_data.isnull().sum())

    # Step 2: Processing
    print("\nStep 2: Selecting Missing Data Strategy")

    # [Option 1] Drop rows with missing values
    # tsla_data = tsla_data.dropna(subset=["Volume"])
    # print("Result: Dropped rows containing missing values.")

    # [Option 2] Drop the entire column
    # tsla_data = tsla_data.drop("Volume", axis=1)
    # print("Result: Dropped the 'Volume' column.")

    # [Option 3] Impute with median (Recommended)
    median = tsla_data["Volume"].median()
    tsla_data["Volume"] = tsla_data["Volume"].fillna(median)
    print(f"Result: Imputed missing values with median ({median}).")

    # Step 3: Final verification
    print("\nStep 3: Verification after processing")
    print(tsla_data.isnull().sum())