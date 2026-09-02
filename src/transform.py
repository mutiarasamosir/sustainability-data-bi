from pathlib import Path

import pandas as pd


RAW_FILE = Path("data/raw/annual-co2-emissions-per-country.csv")
PROCESSED_DIR = Path("data/processed")
OUTPUT_FILE = PROCESSED_DIR / "co2_clean.csv"


def load_data():
    """Membaca dataset CO2 dari folder raw."""

    df = pd.read_csv(RAW_FILE)

    return df


def transform_data(df):
    """Membersihkan dan menstandarkan dataset CO2."""

    # Hanya mempertahankan entitas yang memiliki country code
    df = df[df["Code"].notna()].copy()

    # Mengubah nama kolom menjadi format yang konsisten
    df = df.rename(
        columns={
            "Entity": "country_name",
            "Code": "country_code",
            "Year": "year",
            "Annual COâ\x82\x82 emissions": "co2_emissions",
        }
    )

    # Memastikan tipe data sesuai
    df["country_name"] = df["country_name"].astype(str)
    df["country_code"] = df["country_code"].astype(str)
    df["year"] = df["year"].astype(int)
    df["co2_emissions"] = pd.to_numeric(
        df["co2_emissions"],
        errors="coerce"
    )

    # Menghapus baris yang memiliki nilai CO2 kosong
    df = df.dropna(subset=["co2_emissions"])

    # Menghapus duplikasi country-year
    df = df.drop_duplicates(
        subset=["country_code", "year"]
    )

    # Mengurutkan data
    df = df.sort_values(
        ["country_code", "year"]
    ).reset_index(drop=True)

    return df


def save_data(df):
    """Menyimpan dataset hasil transformasi."""

    PROCESSED_DIR.mkdir(
        parents=True,
        exist_ok=True
    )

    df.to_csv(
        OUTPUT_FILE,
        index=False
    )


def main():

    print("Loading raw CO2 dataset...")

    df = load_data()

    print(f"Raw rows: {len(df):,}")

    print("\nTransforming dataset...")

    df_clean = transform_data(df)

    print(f"Processed rows: {len(df_clean):,}")
    print(f"Countries: {df_clean['country_code'].nunique()}")
    print(
        f"Year range: "
        f"{df_clean['year'].min()} "
        f"to "
        f"{df_clean['year'].max()}"
    )

    print("\nSaving processed dataset...")

    save_data(df_clean)

    print(f"Saved to: {OUTPUT_FILE}")

    print("\nFinal columns:")
    print(df_clean.columns.tolist())

    print("\nFirst 5 rows:")
    print(df_clean.head())


if __name__ == "__main__":
    main()