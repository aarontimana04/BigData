from pathlib import Path
import os
from dotenv import load_dotenv

load_dotenv()

PROJECT_ROOT = Path(__file__).resolve().parents[1]

LOCAL_RAW_DIR = Path(os.getenv("LOCAL_RAW_DIR", PROJECT_ROOT / "data" / "raw"))
LOCAL_PROCESSED_DIR = Path(os.getenv("LOCAL_PROCESSED_DIR", PROJECT_ROOT / "data" / "processed"))

GHARCHIVE_BASE_URL = os.getenv("GHARCHIVE_BASE_URL", "https://data.gharchive.org")

USE_GCS = os.getenv("USE_GCS", "false").lower() == "true"
GCP_PROJECT_ID = os.getenv("GCP_PROJECT_ID", "")
GCS_BUCKET = os.getenv("GCS_BUCKET", "")

MONGO_URI = os.getenv("MONGO_URI", "mongodb://admin:admin@localhost:27017/?authSource=admin")
MONGO_DATABASE = os.getenv("MONGO_DATABASE", "github_events")
MONGO_COLLECTION = os.getenv("MONGO_COLLECTION", "github_events_raw")

CASSANDRA_HOST = os.getenv("CASSANDRA_HOST", "localhost")
CASSANDRA_PORT = int(os.getenv("CASSANDRA_PORT", "9042"))
CASSANDRA_KEYSPACE = os.getenv("CASSANDRA_KEYSPACE", "github_events")

NEO4J_URI = os.getenv("NEO4J_URI", "bolt://localhost:7687")
NEO4J_USER = os.getenv("NEO4J_USER", "neo4j")
NEO4J_PASSWORD = os.getenv("NEO4J_PASSWORD", "password123")


def ensure_directories() -> None:
    LOCAL_RAW_DIR.mkdir(parents=True, exist_ok=True)
    LOCAL_PROCESSED_DIR.mkdir(parents=True, exist_ok=True)
