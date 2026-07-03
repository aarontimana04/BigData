import argparse
import gzip
import shutil
from pathlib import Path

import requests

from config import GHARCHIVE_BASE_URL, LOCAL_RAW_DIR, ensure_directories


def build_gharchive_url(date: str, hour: int) -> str:
    return f"{GHARCHIVE_BASE_URL}/{date}-{hour}.json.gz"


def download_hour_file(date: str, hour: int) -> Path:
    ensure_directories()

    url = build_gharchive_url(date, hour)
    output_path = LOCAL_RAW_DIR / f"{date}-{hour}.json.gz"

    print(f"Downloading: {url}")
    response = requests.get(url, stream=True, timeout=120)
    response.raise_for_status()

    with output_path.open("wb") as file:
        for chunk in response.iter_content(chunk_size=1024 * 1024):
            if chunk:
                file.write(chunk)

    print(f"Saved raw file: {output_path}")
    return output_path


def decompress_gzip(input_path: Path) -> Path:
    output_path = input_path.with_suffix("")

    with gzip.open(input_path, "rb") as source:
        with output_path.open("wb") as target:
            shutil.copyfileobj(source, target)

    print(f"Decompressed file: {output_path}")
    return output_path


def main() -> None:
    parser = argparse.ArgumentParser(description="Download one GH Archive hourly file.")
    parser.add_argument("--date", required=True, help="Date in YYYY-MM-DD format")
    parser.add_argument("--hour", required=True, type=int, help="Hour from 0 to 23")
    args = parser.parse_args()

    raw_file = download_hour_file(args.date, args.hour)
    decompress_gzip(raw_file)


if __name__ == "__main__":
    main()
