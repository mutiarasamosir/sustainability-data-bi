from pathlib import Path

import pandas as pd


PROCESSED_DIR = Path("data/processed")

CO2_FILE = PROCESSED_DIR / "co2_clean.csv"
POPULATION_FILE = PROCESSED_DIR / "population_clean.csv"
ENERGY_FILE = PROCESSED_DIR / "energy_clean.csv"

OUTPUT_FILE = PROCESSED_DIR / "sustainability_integrated.csv"


START_YEAR = 2000
END_YEAR = 2023


def load_data():
    """Membaca seluruh dataset yang telah dibersihkan."""

    co2 = pd.read_csv(CO2_FILE)
    population = pd.read_csv(POPULATION_FILE)
    energy = pd.read_csv(ENERGY_FILE)

    return co2, population, energy


def filter_period(df):
    """Membatasi data pada periode analisis 2000-2023."""

    return df[
        df["year"].between(
            START_YEAR,
            END_YEAR
        )
    ].copy()


def integrate_data(co2, population, energy):
    """Menggabungkan CO2, population, dan energy."""

    co2 = filter_period(co2)
    population = filter_period(population)
    energy = filter_period(energy)

    print("\nRows after period filtering:")
    print(f"CO2        : {len(co2):,}")
    print(f"Population : {len(population):,}")
    print(f"Energy     : {len(energy):,}")

    # Gabungkan CO2 dengan population
    df = pd.merge(
        co2,
        population,
        on=["country_code", "year"],
        how="inner",
        suffixes=("_co2", "_population")
    )

    # Gabungkan hasil sebelumnya dengan energy
    df = pd.merge(
        df,
        energy,
        on=["country_code", "year"],
        how="inner",
        suffixes=("", "_energy")
    )

    # Menggunakan country_name dari CO2 sebagai nama negara utama
    df = df.rename(
        columns={
            "country_name": "country_name"
        }
    )

    # Menghitung CO2 per capita
    df["co2_per_capita"] = (
        df["co2_emissions"] /
        df["population"]
    )

    # Memilih kolom akhir
    df = df[
        [
            "country_code",
            "country_name",
            "year",
            "co2_emissions",
            "co2_per_capita",
            "population",
            "energy_per_capita"
        ]
    ]

    # Mengurutkan data
    df = df.sort_values(
        ["country_code", "year"]
    ).reset_index(drop=True)

    return df


def validate_integrated_data(df):
    """Melakukan validasi dataset hasil integrasi."""

    print("\n=== INTEGRATED DATA QUALITY CHECK ===")

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

    print("\n5. Data types:")
    print(df.dtypes)

    print("\n6. Negative values:")

    print(
        "CO2:",
        (df["co2_emissions"] < 0).sum()
    )

    print(
        "CO2 per capita:",
        (df["co2_per_capita"] < 0).sum()
    )

    print(
        "Population:",
        (df["population"] < 0).sum()
    )

    print(
        "Energy:",
        (df["energy_per_capita"] < 0).sum()
    )

    valid = (
        df["country_code"].notna().all()
        and df["country_name"].notna().all()
        and df["year"].notna().all()
        and df["co2_emissions"].notna().all()
        and df["co2_per_capita"].notna().all()
        and df["population"].notna().all()
        and df["energy_per_capita"].notna().all()
        and duplicate_count == 0
        and (df["co2_emissions"] >= 0).all()
        and (df["co2_per_capita"] >= 0).all()
        and (df["population"] >= 0).all()
        and (df["energy_per_capita"] >= 0).all()
    )

    print("\n=== VALIDATION RESULT ===")

    if valid:
        print("PASS - Integrated dataset is valid.")
    else:
        print(
            "FAIL - Integrated dataset "
            "requires further checking."
        )


def save_data(df):
    """Menyimpan dataset hasil integrasi."""

    PROCESSED_DIR.mkdir(
        parents=True,
        exist_ok=True
    )

    df.to_csv(
        OUTPUT_FILE,
        index=False
    )


def main():

    print("Loading cleaned datasets...")

    co2, population, energy = load_data()

    print(
        f"CO2 rows        : {len(co2):,}"
    )
    print(
        f"Population rows : {len(population):,}"
    )
    print(
        f"Energy rows     : {len(energy):,}"
    )

    print(
        f"\nAnalysis period: "
        f"{START_YEAR}-{END_YEAR}"
    )

    print("\nIntegrating datasets...")

    df_integrated = integrate_data(
        co2,
        population,
        energy
    )

    print(
        f"\nIntegrated rows: "
        f"{len(df_integrated):,}"
    )

    print(
        f"Countries: "
        f"{df_integrated['country_code'].nunique()}"
    )

    print(
        f"Year range: "
        f"{df_integrated['year'].min()} "
        f"- "
        f"{df_integrated['year'].max()}"
    )

    print("\nSaving integrated dataset...")

    save_data(df_integrated)

    print(
        f"Saved to: {OUTPUT_FILE}"
    )

    print("\nFinal columns:")
    print(
        df_integrated.columns.tolist()
    )

    print("\nFirst 5 rows:")
    print(
        df_integrated.head()
    )

    validate_integrated_data(
        df_integrated
    )


if __name__ == "__main__":
    main()