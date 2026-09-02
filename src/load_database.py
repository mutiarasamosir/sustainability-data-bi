from pathlib import Path

import pandas as pd
import psycopg2
from psycopg2.extras import execute_values


DATA_FILE = Path(
    "data/processed/sustainability_final.csv"
)


DB_CONFIG = {
    "host": "localhost",
    "port": 5432,
    "database": "sustainability_bi",
    "user": "postgres",
    "password": "samosir1304"
}


def load_csv():
    """Membaca dataset final."""

    df = pd.read_csv(DATA_FILE)

    return df


def connect_database():
    """Membuat koneksi ke PostgreSQL."""

    return psycopg2.connect(
        **DB_CONFIG
    )


def load_dim_country(
    cursor,
    df
):
    """Memasukkan data negara ke dim_country."""

    countries = (
        df[
            [
                "country_code",
                "country_name",
                "region"
            ]
        ]
        .drop_duplicates(
            subset=["country_code"]
        )
    )

    records = list(
        countries.itertuples(
            index=False,
            name=None
        )
    )

    query = """
        INSERT INTO dim_country (
            country_code,
            country_name,
            region
        )
        VALUES %s
        ON CONFLICT (country_code)
        DO UPDATE SET
            country_name = EXCLUDED.country_name,
            region = EXCLUDED.region;
    """

    execute_values(
        cursor,
        query,
        records
    )

    print(
        f"dim_country loaded: "
        f"{len(records):,} countries"
    )


def load_fact_sustainability(
    cursor,
    df
):
    """Memasukkan data sustainability ke fact table."""

    fact_data = df[
        [
            "country_code",
            "year",
            "co2_emissions",
            "population",
            "energy_per_capita"
        ]
    ].copy()

    records = list(
        fact_data.itertuples(
            index=False,
            name=None
        )
    )

    query = """
        INSERT INTO fact_sustainability (
            country_code,
            year,
            co2_emissions,
            population,
            energy_per_capita
        )
        VALUES %s
        ON CONFLICT (country_code, year)
        DO UPDATE SET
            co2_emissions =
                EXCLUDED.co2_emissions,
            population =
                EXCLUDED.population,
            energy_per_capita =
                EXCLUDED.energy_per_capita;
    """

    execute_values(
        cursor,
        query,
        records,
        page_size=1000
    )

    print(
        f"fact_sustainability loaded: "
        f"{len(records):,} rows"
    )


def check_database(cursor):
    """Mengecek jumlah data di database."""

    cursor.execute(
        "SELECT COUNT(*) FROM dim_country;"
    )

    country_count = cursor.fetchone()[0]

    cursor.execute(
        "SELECT COUNT(*) "
        "FROM fact_sustainability;"
    )

    fact_count = cursor.fetchone()[0]

    print("\n=== DATABASE CHECK ===")

    print(
        f"dim_country: "
        f"{country_count:,} rows"
    )

    print(
        f"fact_sustainability: "
        f"{fact_count:,} rows"
    )


def main():

    print("Loading final dataset...")

    df = load_csv()

    print(
        f"CSV rows: "
        f"{len(df):,}"
    )

    print(
        f"Countries: "
        f"{df['country_code'].nunique()}"
    )

    print("\nConnecting to PostgreSQL...")

    connection = connect_database()

    try:

        cursor = connection.cursor()

        print(
            "\nLoading country dimension..."
        )

        load_dim_country(
            cursor,
            df
        )

        print(
            "\nLoading sustainability fact..."
        )

        load_fact_sustainability(
            cursor,
            df
        )

        connection.commit()

        print(
            "\nTransaction committed."
        )

        check_database(cursor)

        cursor.close()

    except Exception as error:

        connection.rollback()

        print(
            "\nERROR:"
        )

        print(error)

        print(
            "\nTransaction rolled back."
        )

        raise

    finally:

        connection.close()

        print(
            "\nDatabase connection closed."
        )


if __name__ == "__main__":
    main()