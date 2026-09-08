import pandas as pd
from pathlib import Path
from sklearn.preprocessing import StandardScaler, MinMaxScaler


def load_housing_data():
    base_path = Path(__file__).parent
    csv_path = base_path / "datasets" / "TSLA.csv"
    return pd.read_csv(csv_path)

if __name__ == "__main__":
    housing = load_housing_data()

    median = housing["low"].median()
    housing["low"] = housing["low"].fillna(median)

    # 3. Step 4: Check original statistics before scaling
    print("\nStep 4: Check original statistics before scaling")
    print("-" * 50)
    # Select only numeric features (Drop 'ocean_proximity' for scaling)
    num_housing = housing.drop(labels="ocean_proximity", axis=1)
    print(num_housing.describe())

    # 4. Step 5: Scaling & Normalization
    std_scaler = StandardScaler()  # Standardization
    min_max_scaler = MinMaxScaler()  # Normalization

    # fit_transform returns a Numpy array
    housing_std = std_scaler.fit_transform(num_housing)
    housing_minmax = min_max_scaler.fit_transform(num_housing)

    print("\nStep 5: Compare results of Scaling (median_income column)")
    print("-" * 50)
    # median_income is at index 7
    print(f"Original value:        {num_housing['median_income'].iloc[0]}")
    print(f"Standardized result: {housing_std[0, 7]:.4f}")
    print(f"Normalized result:   {housing_minmax[0, 7]:.4f}")

    # 5. Step 6: Min/Max verification
    print("\nStep 6: Min/Max values after Normalization")
    print("-" * 50)
    print(f"Min value (All features): {housing_minmax.min()}")
    print(f"Max value (All features): {housing_minmax.max()}")