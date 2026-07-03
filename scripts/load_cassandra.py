import argparse
import json
from collections import Counter, defaultdict
from datetime import date, datetime
from pathlib import Path

from cassandra.cluster import Cluster

from config import CASSANDRA_HOST, CASSANDRA_KEYSPACE, CASSANDRA_PORT


def to_cassandra_date(value: str) -> date:
    return date.fromisoformat(value)


def get_session():
    cluster = Cluster([CASSANDRA_HOST], port=CASSANDRA_PORT)
    session = cluster.connect()

    session.execute(
        f"""
        CREATE KEYSPACE IF NOT EXISTS {CASSANDRA_KEYSPACE}
        WITH replication = {{'class': 'SimpleStrategy', 'replication_factor': 1}}
        """
    )
    session.set_keyspace(CASSANDRA_KEYSPACE)
    return cluster, session


def aggregate_events(input_path: Path):
    events_by_day_type = Counter()
    repo_activity = defaultdict(lambda: {"total_events": 0, "actors": set()})
    actor_activity = defaultdict(lambda: Counter())
    day_summary = defaultdict(lambda: {"total": 0, "actors": set(), "repos": set(), "types": Counter()})

    with input_path.open("r", encoding="utf-8") as file:
        for line in file:
            event = json.loads(line)
            event_date = event["event_date"]
            event_hour = int(event["event_hour"])
            event_type = event["type"]
            repo_name = event["repo_name"]
            actor_login = event["actor_login"]

            events_by_day_type[(event_date, event_type, event_hour)] += 1

            repo_key = (event_date, repo_name, event_type)
            repo_activity[repo_key]["total_events"] += 1
            repo_activity[repo_key]["actors"].add(actor_login)

            actor_key = (event_date, actor_login)
            actor_activity[actor_key]["total_events"] += 1
            actor_activity[actor_key][event_type] += 1

            day_summary[event_date]["total"] += 1
            day_summary[event_date]["actors"].add(actor_login)
            day_summary[event_date]["repos"].add(repo_name)
            day_summary[event_date]["types"][event_type] += 1

    return events_by_day_type, repo_activity, actor_activity, day_summary


def create_tables(session) -> None:
    session.execute(
        """
        CREATE TABLE IF NOT EXISTS events_by_day_type (
            event_date date,
            event_type text,
            event_hour int,
            total_events int,
            PRIMARY KEY ((event_date), event_type, event_hour)
        )
        """
    )
    session.execute(
        """
        CREATE TABLE IF NOT EXISTS repo_activity_by_day (
            event_date date,
            repo_name text,
            event_type text,
            total_events int,
            unique_actors int,
            PRIMARY KEY ((event_date), repo_name, event_type)
        )
        """
    )
    session.execute(
        """
        CREATE TABLE IF NOT EXISTS actor_activity_by_day (
            event_date date,
            actor_login text,
            total_events int,
            push_events int,
            pull_request_events int,
            issue_events int,
            watch_events int,
            PRIMARY KEY ((event_date), actor_login)
        )
        """
    )
    session.execute(
        """
        CREATE TABLE IF NOT EXISTS kpis_by_day (
            event_date date,
            total_events int,
            unique_actors int,
            unique_repositories int,
            top_event_type text,
            generated_at timestamp,
            PRIMARY KEY ((event_date))
        )
        """
    )


def load_to_cassandra(input_path: Path) -> None:
    cluster, session = get_session()
    create_tables(session)

    events_by_day_type, repo_activity, actor_activity, day_summary = aggregate_events(input_path)

    for (event_date, event_type, event_hour), total in events_by_day_type.items():
        session.execute(
            """
            INSERT INTO events_by_day_type (event_date, event_type, event_hour, total_events)
            VALUES (%s, %s, %s, %s)
            """,
            (to_cassandra_date(event_date), event_type, event_hour, total),
        )

    for (event_date, repo_name, event_type), values in repo_activity.items():
        session.execute(
            """
            INSERT INTO repo_activity_by_day (event_date, repo_name, event_type, total_events, unique_actors)
            VALUES (%s, %s, %s, %s, %s)
            """,
            (to_cassandra_date(event_date), repo_name, event_type, values["total_events"], len(values["actors"])),
        )

    for (event_date, actor_login), counts in actor_activity.items():
        session.execute(
            """
            INSERT INTO actor_activity_by_day (
                event_date, actor_login, total_events, push_events,
                pull_request_events, issue_events, watch_events
            ) VALUES (%s, %s, %s, %s, %s, %s, %s)
            """,
            (
                to_cassandra_date(event_date),
                actor_login,
                counts["total_events"],
                counts["PushEvent"],
                counts["PullRequestEvent"],
                counts["IssuesEvent"],
                counts["WatchEvent"],
            ),
        )

    generated_at = datetime.utcnow()
    for event_date, values in day_summary.items():
        top_event_type = values["types"].most_common(1)[0][0] if values["types"] else None
        session.execute(
            """
            INSERT INTO kpis_by_day (
                event_date, total_events, unique_actors,
                unique_repositories, top_event_type, generated_at
            ) VALUES (%s, %s, %s, %s, %s, %s)
            """,
            (
                to_cassandra_date(event_date),
                values["total"],
                len(values["actors"]),
                len(values["repos"]),
                top_event_type,
                generated_at,
            ),
        )

    print("Cassandra aggregated tables loaded.")
    cluster.shutdown()


def main() -> None:
    parser = argparse.ArgumentParser(description="Load clean GH Archive JSONL into Cassandra aggregates.")
    parser.add_argument("--input", required=True, help="Clean .jsonl file path")
    args = parser.parse_args()

    load_to_cassandra(Path(args.input))


if __name__ == "__main__":
    main()
