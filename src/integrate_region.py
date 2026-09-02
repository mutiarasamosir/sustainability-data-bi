from pathlib import Path

import pandas as pd


PROCESSED_DIR = Path("data/processed")

SUSTAINABILITY_FILE = (
    PROCESSED_DIR /
    "sustainability_integrated.csv"
)

REGION_FILE = (
    PROCESSED_DIR /
    "country_regions_clean.csv"
)

OUTPUT_FILE = (
    PROCESSED_DIR /
    "sustainability_final.csv"
)


def load_data():
    """Membaca dataset sustainability dan mapping region."""

    sustainability = pd.read_csv(
        SUSTAINABILITY_FILE
    )

    regions = pd.read_csv(
        REGION_FILE
    )

    return sustainability, regions

def integrate_region(
    sustainability,
    regions
):
    """Menggabungkan sustainability dengan region."""

    df = pd.merge(
        sustainability,
        regions[
            [
                "country_code",
                "region"
            ]
        ],
        on="country_code",
        how="left"
    )

    # Entitas aggregate OWID tidak digunakan
    # karena analisis kita berada pada level negara.
    aggregate_codes = [
        "OWID_AFR",
        "OWID_ASI",
        "OWID_EU27",
        "OWID_EUR",
        "OWID_HIC",
        "OWID_LIC",
        "OWID_LMC",
        "OWID_NAM",
        "OWID_OCE",
        "OWID_SAM",
        "OWID_UMC",
        "OWID_WRL",
    ]

    df = df[
        ~df["country_code"].isin(
            aggregate_codes
        )
    ].copy()

    # Beberapa country/area tidak memiliki
    # kecocokan langsung pada mapping yang digunakan.
    # Region ditetapkan berdasarkan klasifikasi geografis UN M49.
    manual_regions = {
        "PSE": "Asia",
        "TWN": "Asia",
        "OWID_KOS": "Europe",
    }

    for code, region in manual_regions.items():
        df.loc[
            df["country_code"] == code,
            "region"
        ] = region

    # Atur urutan kolom
    df = df[
        [
            "country_code",
            "country_name",
            "region",
            "year",
            "co2_emissions",
            "co2_per_capita",
            "population",
            "energy_per_capita"
        ]
    ]

    # Urutkan data
    df = df.sort_values(
        [
            "country_code",
            "year"
        ]
    ).reset_index(drop=True)

    return df

def validate_region_mapping(df):
    """Memastikan seluruh negara memiliki region."""

    print("\n=== REGION MAPPING CHECK ===")

    missing_region = (
        df["region"].isna().sum()
    )

    print(
        f"Missing region: "
        f"{missing_region}"
    )

    print("\nCountries by region:")

    print(
        df[
            [
                "country_code",
                "region"
            ]
        ]
        .drop_duplicates()
        ["region"]
        .value_counts()
    )

    print("\nCountries without region:")

    missing_countries = (
        df.loc[
            df["region"].isna(),
            [
                "country_code",
                "country_name"
            ]
        ]
        .drop_duplicates()
    )

    if len(missing_countries) > 0:
        print(
            missing_countries
            .to_string(index=False)
        )
    else:
        print("None")

    return missing_region == 0


def save_data(df):
    """Menyimpan dataset final."""

    df.to_csv(
        OUTPUT_FILE,
        index=False
    )


def main():

    print(
        "Loading integrated sustainability data..."
    )

    sustainability, regions = load_data()

    print(
        f"Sustainability rows: "
        f"{len(sustainability):,}"
    )

    print(
        f"Region mapping rows: "
        f"{len(regions):,}"
    )

    print("\nIntegrating region information...")

    df_final = integrate_region(
        sustainability,
        regions
    )

    print(
        f"Final rows: "
        f"{len(df_final):,}"
    )

    print(
        f"Countries: "
        f"{df_final['country_code'].nunique()}"
    )

    print(
        f"Year range: "
        f"{df_final['year'].min()} "
        f"- "
        f"{df_final['year'].max()}"
    )

    mapping_valid = validate_region_mapping(
        df_final
    )

    print("\n=== FINAL DATASET CHECK ===")

    duplicate_count = df_final.duplicated(
        subset=[
            "country_code",
            "year"
        ]
    ).sum()

    print(
        f"Duplicate country-year: "
        f"{duplicate_count}"
    )

    print(
        f"Missing values:\n"
        f"{df_final.isna().sum()}"
    )

    print("\nSaving final dataset...")

    save_data(df_final)

    print(
        f"Saved to: {OUTPUT_FILE}"
    )

    print("\nFinal columns:")

    print(
        df_final.columns.tolist()
    )

    print("\nFirst 5 rows:")

    print(
        df_final.head()
    )

    print("\n=== FINAL VALIDATION RESULT ===")

    if (
        df_final["region"].notna().all()
        and duplicate_count == 0
        and df_final.isna().sum().sum() == 0
        and df_final["year"].min() == 2000
        and df_final["year"].max() == 2023
    ):
        print(
            "PASS - Final dataset is ready."
        )
    else:
        print(
            "FAIL - Final dataset requires checking."
        )


if __name__ == "__main__":
    main()