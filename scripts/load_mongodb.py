import argparse
import json
from pathlib import Path

from pymongo import MongoClient, UpdateOne

from config import MONGO_COLLECTION, MONGO_DATABASE, MONGO_URI


def load_to_mongodb(input_path: Path) -> int:
    client = MongoClient(MONGO_URI)
    collection = client[MONGO_DATABASE][MONGO_COLLECTION]

    operations = []
    count = 0

    with input_path.open("r", encoding="utf-8") as file:
        for line in file:
            event = json.loads(line)
            event["_id"] = event["event_id"]
            operations.append(
                UpdateOne(
                    {"_id": event["_id"]},
                    {"$set": event},
                    upsert=True,
                )
            )

            if len(operations) >= 1000:
                result = collection.bulk_write(operations, ordered=False)
                count += result.upserted_count + result.modified_count
                operations.clear()

    if operations:
        result = collection.bulk_write(operations, ordered=False)
        count += result.upserted_count + result.modified_count

    print(f"MongoDB loaded/updated records: {count}")
    client.close()
    return count


def main() -> None:
    parser = argparse.ArgumentParser(description="Load clean GH Archive JSONL into MongoDB.")
    parser.add_argument("--input", required=True, help="Clean .jsonl file path")
    args = parser.parse_args()

    load_to_mongodb(Path(args.input))


if __name__ == "__main__":
    main()
