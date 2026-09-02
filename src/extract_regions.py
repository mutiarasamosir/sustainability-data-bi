from pathlib import Path

import pandas as pd
import requests
from io import StringIO


BASE_URL = "https://ourworldindata.org/grapher"
RAW_DIR = Path("data/raw")


def download_regions():
    """Mengambil country-region mapping dari OWID."""

    url = f"{BASE_URL}/world-regions-un1.csv"

    response = requests.get(
        url,
        timeout=30
    )

    response.raise_for_status()

    return pd.read_csv(
        StringIO(response.text)
    )


def main():

    print("Downloading country-region mapping...")

    RAW_DIR.mkdir(
        parents=True,
        exist_ok=True
    )

    df = download_regions()

    output_file = (
        RAW_DIR /
        "country_regions.csv"
    )

    df.to_csv(
        output_file,
        index=False
    )

    print("\nDownload completed.")

    print(
        f"Rows    : {len(df):,}"
    )

    print(
        f"Columns : {len(df.columns)}"
    )

    print(
        "\nColumns:"
    )

    print(
        df.columns.tolist()
    )

    print(
        "\nFirst 5 rows:"
    )

    print(
        df.head()
    )


if __name__ == "__main__":
    main()