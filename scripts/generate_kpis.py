import argparse
import json
from collections import Counter
from pathlib import Path

from config import LOCAL_PROCESSED_DIR, ensure_directories


def generate_kpis(input_path: Path) -> Path:
    ensure_directories()

    total_events = 0
    actors = set()
    repositories = set()
    event_types = Counter()

    with input_path.open("r", encoding="utf-8") as file:
        for line in file:
            event = json.loads(line)
            total_events += 1
            actors.add(event.get("actor_login"))
            repositories.add(event.get("repo_name"))
            event_types[event.get("type")] += 1

    kpis = {
        "source_file": input_path.name,
        "total_events": total_events,
        "unique_actors": len(actors),
        "unique_repositories": len(repositories),
        "top_event_type": event_types.most_common(1)[0][0] if event_types else None,
        "event_types": dict(event_types.most_common()),
    }

    output_path = LOCAL_PROCESSED_DIR / f"{input_path.stem}_kpis.json"
    output_path.write_text(json.dumps(kpis, indent=2, ensure_ascii=False), encoding="utf-8")

    print(f"Generated KPI file: {output_path}")
    return output_path


def main() -> None:
    parser = argparse.ArgumentParser(description="Generate KPI summary from clean JSONL file.")
    parser.add_argument("--input", required=True, help="Clean .jsonl file path")
    args = parser.parse_args()

    generate_kpis(Path(args.input))


if __name__ == "__main__":
    main()
