from pathlib import Path

import pandas as pd


DATA_FILE = Path("data/processed/co2_clean.csv")


def validate_data(df):
    """Melakukan validasi dataset CO2 yang telah dibersihkan."""

    print("=== DATA QUALITY CHECK ===")

    # 1. Missing values
    print("\n1. Missing values:")
    print(df.isna().sum())

    # 2. Duplicate country-year
    duplicate_count = df.duplicated(
        subset=["country_code", "year"]
    ).sum()

    print("\n2. Duplicate country-year:")
    print(duplicate_count)

    # 3. Country count
    print("\n3. Number of countries:")
    print(df["country_code"].nunique())

    # 4. Year range
    print("\n4. Year range:")
    print(f"{df['year'].min()} - {df['year'].max()}")

    # 5. CO2 negative values
    negative_co2 = (df["co2_emissions"] < 0).sum()

    print("\n5. Negative CO2 values:")
    print(negative_co2)

    # 6. Zero CO2 values
    zero_co2 = (df["co2_emissions"] == 0).sum()

    print("\n6. Zero CO2 values:")
    print(zero_co2)

    # 7. Data types
    print("\n7. Data types:")
    print(df.dtypes)

    # 8. Final validation status
    valid = (
        df["country_code"].notna().all()
        and df["year"].notna().all()
        and df["co2_emissions"].notna().all()
        and duplicate_count == 0
        and negative_co2 == 0
    )

    print("\n=== VALIDATION RESULT ===")

    if valid:
        print("PASS - Dataset is valid.")
    else:
        print("FAIL - Dataset requires further cleaning.")


def main():

    print("Loading processed CO2 dataset...")

    df = pd.read_csv(DATA_FILE)

    print(f"Rows: {len(df):,}")
    print(f"Columns: {len(df.columns)}")

    validate_data(df)


if __name__ == "__main__":
    main()
