import json
from io import StringIO
from pathlib import Path

import pandas as pd
import requests


BASE_URL = "https://ourworldindata.org/grapher"
RAW_DIR = Path("data/raw")


def download_metadata(slug: str):
    """Mengambil metadata dataset dari OWID Grapher API."""

    url = f"{BASE_URL}/{slug}.metadata.json"

    response = requests.get(url, timeout=30)
    response.raise_for_status()

    return response.json()


def download_csv(slug: str) -> pd.DataFrame:
    """Mengambil dataset CSV dari OWID Grapher."""

    url = f"{BASE_URL}/{slug}.csv"

    response = requests.get(url, timeout=60)
    response.raise_for_status()

    return pd.read_csv(StringIO(response.text))


def main():

    slug = "per-capita-energy-use"

    RAW_DIR.mkdir(parents=True, exist_ok=True)

    print("Downloading metadata...")
    metadata = download_metadata(slug)

    print("Downloading dataset...")
    df = download_csv(slug)

    # Simpan raw CSV
    data_path = RAW_DIR / f"{slug}.csv"
    df.to_csv(data_path, index=False)

    # Simpan metadata JSON
    metadata_path = RAW_DIR / f"{slug}.metadata.json"

    with open(metadata_path, "w", encoding="utf-8") as file:
        json.dump(
            metadata,
            file,
            indent=2,
            ensure_ascii=False
        )

    print("\nExtraction completed.")
    print(f"Rows     : {len(df):,}")
    print(f"Columns  : {len(df.columns)}")
    print(f"Data     : {data_path}")
    print(f"Metadata : {metadata_path}")

    print("\nColumns:")
    print(df.columns.tolist())

    print("\nFirst 5 rows:")
    print(df.head())


if __name__ == "__main__":
    main()

