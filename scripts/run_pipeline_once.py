import argparse
from pathlib import Path

from extract_gharchive import decompress_gzip, download_hour_file
from generate_kpis import generate_kpis
from load_cassandra import load_to_cassandra
from load_mongodb import load_to_mongodb
from load_neo4j import load_to_neo4j
from validate_clean import clean_file


def run_pipeline(date: str, hour: int, neo4j_limit: int | None = 5000) -> None:
    raw_gz = download_hour_file(date, hour)
    raw_json = decompress_gzip(raw_gz)
    clean_jsonl = clean_file(Path(raw_json))

    load_to_mongodb(clean_jsonl)
    load_to_cassandra(clean_jsonl)
    load_to_neo4j(clean_jsonl, limit=neo4j_limit)
    generate_kpis(clean_jsonl)

    print("Pipeline finished successfully.")


def main() -> None:
    parser = argparse.ArgumentParser(description="Run one full GH Archive pipeline execution.")
    parser.add_argument("--date", required=True, help="Date in YYYY-MM-DD format")
    parser.add_argument("--hour", required=True, type=int, help="Hour from 0 to 23")
    parser.add_argument("--neo4j-limit", type=int, default=5000, help="Limit graph load for demo performance")
    args = parser.parse_args()

    run_pipeline(args.date, args.hour, neo4j_limit=args.neo4j_limit)


if __name__ == "__main__":
    main()
