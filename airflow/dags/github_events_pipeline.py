from __future__ import annotations

from datetime import datetime, timedelta
from pathlib import Path
import subprocess

from airflow import DAG
from airflow.operators.python import PythonOperator

SCRIPTS_DIR = Path("/opt/airflow/scripts")
DATA_DIR = Path("/opt/airflow/data")

DEFAULT_DATE = "2026-06-01"
DEFAULT_HOUR = 0


def run_command(command: list[str]) -> None:
    print("Running:", " ".join(command))
    subprocess.run(command, check=True)


def extract(**context) -> str:
    date = context["params"].get("date", DEFAULT_DATE)
    hour = int(context["params"].get("hour", DEFAULT_HOUR))
    run_command(["python", str(SCRIPTS_DIR / "extract_gharchive.py"), "--date", date, "--hour", str(hour)])
    return str(DATA_DIR / "raw" / f"{date}-{hour}.json")


def validate(**context) -> str:
    raw_json = context["ti"].xcom_pull(task_ids="extract_gharchive_file")
    run_command(["python", str(SCRIPTS_DIR / "validate_clean.py"), "--input", raw_json])
    input_path = Path(raw_json)
    return str(DATA_DIR / "processed" / f"{input_path.stem}_clean.jsonl")


def load_mongo(**context) -> None:
    clean_file = context["ti"].xcom_pull(task_ids="validate_and_clean_events")
    run_command(["python", str(SCRIPTS_DIR / "load_mongodb.py"), "--input", clean_file])


def load_cassandra(**context) -> None:
    clean_file = context["ti"].xcom_pull(task_ids="validate_and_clean_events")
    run_command(["python", str(SCRIPTS_DIR / "load_cassandra.py"), "--input", clean_file])


def load_neo4j(**context) -> None:
    clean_file = context["ti"].xcom_pull(task_ids="validate_and_clean_events")
    run_command(["python", str(SCRIPTS_DIR / "load_neo4j.py"), "--input", clean_file, "--limit", "5000"])


def generate_kpis(**context) -> None:
    clean_file = context["ti"].xcom_pull(task_ids="validate_and_clean_events")
    run_command(["python", str(SCRIPTS_DIR / "generate_kpis.py"), "--input", clean_file])


with DAG(
    dag_id="github_events_pipeline",
    description="Incremental GH Archive pipeline for MongoDB, Cassandra and Neo4j.",
    start_date=datetime(2026, 6, 1),
    schedule_interval="@hourly",
    catchup=False,
    default_args={
        "owner": "bigdata-team",
        "retries": 1,
        "retry_delay": timedelta(minutes=3),
    },
    params={
        "date": DEFAULT_DATE,
        "hour": DEFAULT_HOUR,
    },
    tags=["bigdata", "github", "multimodel"],
) as dag:
    t1 = PythonOperator(
        task_id="extract_gharchive_file",
        python_callable=extract,
    )

    t2 = PythonOperator(
        task_id="validate_and_clean_events",
        python_callable=validate,
    )

    t3 = PythonOperator(
        task_id="load_to_mongodb",
        python_callable=load_mongo,
    )

    t4 = PythonOperator(
        task_id="transform_and_load_to_cassandra",
        python_callable=load_cassandra,
    )

    t5 = PythonOperator(
        task_id="build_graph_and_load_to_neo4j",
        python_callable=load_neo4j,
    )

    t6 = PythonOperator(
        task_id="generate_indicators",
        python_callable=generate_kpis,
    )

    t1 >> t2 >> [t3, t4, t5] >> t6
