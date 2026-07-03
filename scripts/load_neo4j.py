import argparse
import json
from pathlib import Path

from neo4j import GraphDatabase

from config import NEO4J_PASSWORD, NEO4J_URI, NEO4J_USER


def create_constraints(session) -> None:
    constraints = [
        "CREATE CONSTRAINT user_login_unique IF NOT EXISTS FOR (u:User) REQUIRE u.login IS UNIQUE",
        "CREATE CONSTRAINT repository_name_unique IF NOT EXISTS FOR (r:Repository) REQUIRE r.name IS UNIQUE",
        "CREATE CONSTRAINT organization_login_unique IF NOT EXISTS FOR (o:Organization) REQUIRE o.login IS UNIQUE",
        "CREATE CONSTRAINT event_id_unique IF NOT EXISTS FOR (e:Event) REQUIRE e.event_id IS UNIQUE",
        "CREATE CONSTRAINT event_type_name_unique IF NOT EXISTS FOR (t:EventType) REQUIRE t.name IS UNIQUE",
    ]

    for constraint in constraints:
        session.run(constraint)


def upsert_event(session, event: dict) -> None:
    query = """
    MERGE (u:User {login: $actor_login})
      ON CREATE SET u.actor_id = $actor_id
    MERGE (r:Repository {name: $repo_name})
      ON CREATE SET r.repo_id = $repo_id
    MERGE (t:EventType {name: $event_type})
    MERGE (e:Event {event_id: $event_id})
      SET e.created_at = $created_at,
          e.event_date = $event_date,
          e.event_hour = $event_hour
    MERGE (u)-[:TRIGGERED]->(e)
    MERGE (e)-[:HAS_TYPE]->(t)
    MERGE (e)-[:ON_REPOSITORY]->(r)
    MERGE (u)-[:INTERACTED_WITH]->(r)
    WITH r
    WHERE $org_login IS NOT NULL
    MERGE (o:Organization {login: $org_login})
      ON CREATE SET o.org_id = $org_id
    MERGE (r)-[:BELONGS_TO]->(o)
    """

    session.run(
        query,
        event_id=event["event_id"],
        event_type=event["type"],
        actor_id=event.get("actor_id"),
        actor_login=event.get("actor_login"),
        repo_id=event.get("repo_id"),
        repo_name=event.get("repo_name"),
        org_id=event.get("org_id"),
        org_login=event.get("org_login"),
        created_at=event.get("created_at"),
        event_date=event.get("event_date"),
        event_hour=event.get("event_hour"),
    )


def load_to_neo4j(input_path: Path, limit: int | None = None) -> int:
    driver = GraphDatabase.driver(NEO4J_URI, auth=(NEO4J_USER, NEO4J_PASSWORD))
    count = 0

    with driver.session() as session:
        create_constraints(session)

        with input_path.open("r", encoding="utf-8") as file:
            for line in file:
                event = json.loads(line)
                upsert_event(session, event)
                count += 1

                if limit and count >= limit:
                    break

    driver.close()
    print(f"Neo4j events loaded: {count}")
    return count


def main() -> None:
    parser = argparse.ArgumentParser(description="Load clean GH Archive JSONL into Neo4j graph.")
    parser.add_argument("--input", required=True, help="Clean .jsonl file path")
    parser.add_argument("--limit", type=int, default=None, help="Optional limit for demo graph load")
    args = parser.parse_args()

    load_to_neo4j(Path(args.input), limit=args.limit)


if __name__ == "__main__":
    main()
