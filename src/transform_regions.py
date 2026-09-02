from pathlib import Path

import pandas as pd


RAW_FILE = Path("data/raw/country_regions.csv")
PROCESSED_DIR = Path("data/processed")
OUTPUT_FILE = PROCESSED_DIR / "country_regions_clean.csv"


def load_data():
    """Membaca country-region mapping dari folder raw."""

    return pd.read_csv(RAW_FILE)


def transform_data(df):
    """Membersihkan dan menstandarkan country-region mapping."""

    df = df.copy()

    # Rename columns
    df = df.rename(
        columns={
            "Entity": "country_name",
            "Code": "country_code",
            "Year": "year",
            "World regions according to UN M49 (1)": "region",
        }
    )

    # Pastikan hanya country-level entities
    df = df[df["country_code"].notna()].copy()

    # Pastikan tipe data
    df["country_name"] = df["country_name"].astype(str)
    df["country_code"] = df["country_code"].astype(str)
    df["year"] = df["year"].astype(int)
    df["region"] = df["region"].astype(str)

    # Hapus prefix "(UN M49)" dari nama region
    df["region"] = (
        df["region"]
        .str.replace(
            " (UN M49)",
            "",
            regex=False
        )
        .str.strip()
    )

    # Karena mapping hanya digunakan sebagai
    # country -> region, Year tidak diperlukan
    df = df[
        [
            "country_code",
            "country_name",
            "region"
        ]
    ]

    # Pastikan satu country hanya memiliki satu region
    df = df.drop_duplicates(
        subset=["country_code"]
    )

    # Urutkan berdasarkan country code
    df = df.sort_values(
        "country_code"
    ).reset_index(drop=True)

    return df


def save_data(df):
    """Menyimpan mapping hasil transformasi."""

    PROCESSED_DIR.mkdir(
        parents=True,
        exist_ok=True
    )

    df.to_csv(
        OUTPUT_FILE,
        index=False
    )


def main():

    print("Loading raw country-region mapping...")

    df = load_data()

    print(
        f"Raw rows: {len(df):,}"
    )

    print("\nTransforming mapping...")

    df_clean = transform_data(df)

    print(
        f"Processed rows: {len(df_clean):,}"
    )

    print(
        f"Countries: "
        f"{df_clean['country_code'].nunique()}"
    )

    print("\nRegions:")
    print(
        df_clean["region"]
        .value_counts()
    )

    print("\nSaving processed mapping...")

    save_data(df_clean)

    print(
        f"Saved to: {OUTPUT_FILE}"
    )

    print("\nFinal columns:")
    print(
        df_clean.columns.tolist()
    )

    print("\nFirst 10 rows:")
    print(
        df_clean.head(10)
    )


if __name__ == "__main__":
    main()