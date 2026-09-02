from pathlib import Path

import pandas as pd


DATA_FILE = Path("data/processed/energy_clean.csv")


def validate_data(df):
    print("=== DATA QUALITY CHECK ===")

    print("\n1. Missing values:")
    print(df.isna().sum())

    duplicate_count = df.duplicated(
        subset=["country_code", "year"]
    ).sum()

    print("\n2. Duplicate country-year:")
    print(duplicate_count)

    print("\n3. Number of countries:")
    print(df["country_code"].nunique())

    print("\n4. Year range:")
    print(
        f"{df['year'].min()} - "
        f"{df['year'].max()}"
    )

    negative_energy = (
        df["energy_per_capita"] < 0
    ).sum()

    print("\n5. Negative energy values:")
    print(negative_energy)

    zero_energy = (
        df["energy_per_capita"] == 0
    ).sum()

    print("\n6. Zero energy values:")
    print(zero_energy)

    print("\n7. Data types:")
    print(df.dtypes)

    valid = (
        df["country_code"].notna().all()
        and df["year"].notna().all()
        and df["energy_per_capita"].notna().all()
        and duplicate_count == 0
        and negative_energy == 0
    )

    print("\n=== VALIDATION RESULT ===")

    if valid:
        print("PASS - Dataset is valid.")
    else:
        print(
            "FAIL - Dataset requires "
            "further cleaning."
        )


def main():

    print("Loading processed energy dataset...")

    df = pd.read_csv(DATA_FILE)

    print(f"Rows: {len(df):,}")
    print(f"Columns: {len(df.columns)}")

    validate_data(df)


if __name__ == "__main__":
    main()