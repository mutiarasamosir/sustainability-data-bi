from pathlib import Path

import pandas as pd


RAW_FILE = Path("data/raw/per-capita-energy-use.csv")
PROCESSED_DIR = Path("data/processed")
OUTPUT_FILE = PROCESSED_DIR / "energy_clean.csv"


def load_data():
    """Membaca dataset energy dari folder raw."""

    df = pd.read_csv(RAW_FILE)

    return df


def transform_data(df):
    """Membersihkan dan menstandarkan dataset energy."""

    # Memastikan hanya country-level entities
    df = df[df["Code"].notna()].copy()

    # Mengubah nama kolom
    df = df.rename(
        columns={
            "Entity": "country_name",
            "Code": "country_code",
            "Year": "year",
            "Total energy supply": "energy_per_capita",
        }
    )

    # Memastikan tipe data
    df["country_name"] = df["country_name"].astype(str)
    df["country_code"] = df["country_code"].astype(str)
    df["year"] = df["year"].astype(int)

    df["energy_per_capita"] = pd.to_numeric(
        df["energy_per_capita"],
        errors="coerce"
    )

    # Menghapus nilai energy yang kosong
    df = df.dropna(
        subset=["energy_per_capita"]
    )

    # Menghapus duplicate country-year
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

    print("Loading raw energy dataset...")

    df = load_data()

    print(f"Raw rows: {len(df):,}")

    print("\nTransforming dataset...")

    df_clean = transform_data(df)

    print(f"Processed rows: {len(df_clean):,}")
    print(
        f"Countries: "
        f"{df_clean['country_code'].nunique()}"
    )
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