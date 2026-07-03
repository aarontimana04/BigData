import argparse
import json
from datetime import datetime
from pathlib import Path
from typing import Any

import pandas as pd

from config import LOCAL_RAW_DIR, LOCAL_PROCESSED_DIR, ensure_directories

REQUIRED_FIELDS = ["id", "type", "actor", "repo", "created_at"]


def is_valid_event(event: dict[str, Any]) -> bool:
    for field in REQUIRED_FIELDS:
        if field not in event or event[field] in (None, ""):
            return False

    actor = event.get("actor") or {}
    repo = event.get("repo") or {}

    if not actor.get("login"):
        return False
    if not repo.get("name"):
        return False

    return True


def normalize_event(event: dict[str, Any], source_file: str) -> dict[str, Any]:
    created_at = pd.to_datetime(event["created_at"], utc=True)
    org = event.get("org") or {}

    event["event_id"] = str(event.get("id"))
    event["event_date"] = created_at.date().isoformat()
    event["event_hour"] = int(created_at.hour)
    event["actor_id"] = event.get("actor", {}).get("id")
    event["actor_login"] = event.get("actor", {}).get("login")
    event["repo_id"] = event.get("repo", {}).get("id")
    event["repo_name"] = event.get("repo", {}).get("name")
    event["org_id"] = org.get("id")
    event["org_login"] = org.get("login")
    event["source_file"] = source_file
    event["ingestion_timestamp"] = datetime.utcnow().isoformat()

    return event


def clean_file(input_path: Path) -> Path:
    ensure_directories()

    valid_events: list[dict[str, Any]] = []
    seen_ids: set[str] = set()

    with input_path.open("r", encoding="utf-8") as file:
        for line_number, line in enumerate(file, start=1):
            try:
                event = json.loads(line)
            except json.JSONDecodeError:
                print(f"Skipping invalid JSON line {line_number}")
                continue

            if not is_valid_event(event):
                continue

            event_id = str(event["id"])
            if event_id in seen_ids:
                continue

            seen_ids.add(event_id)
            valid_events.append(normalize_event(event, source_file=input_path.name))

    output_path = LOCAL_PROCESSED_DIR / f"{input_path.stem}_clean.jsonl"

    with output_path.open("w", encoding="utf-8") as output:
        for event in valid_events:
            output.write(json.dumps(event, ensure_ascii=False) + "\n")

    print(f"Valid events: {len(valid_events)}")
    print(f"Saved clean file: {output_path}")
    return output_path


def main() -> None:
    parser = argparse.ArgumentParser(description="Validate and clean a GH Archive JSONL file.")
    parser.add_argument("--input", required=True, help="Input .json file path")
    args = parser.parse_args()

    clean_file(Path(args.input))


if __name__ == "__main__":
    main()
