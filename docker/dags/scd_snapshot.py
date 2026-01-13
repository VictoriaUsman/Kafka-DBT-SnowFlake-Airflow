from airflow import DAG
from airflow.operators.bash import BashOperator
from datetime import datetime, timedelta

# Defining paths as variables makes the code cleaner
DBT_PROJECT_DIR = "'/Users/iantristancultura/Documents/Data Engineer/Kafka-DBT-SnowFlake-Airflow/ian_dbt'"
DBT_PROFILES_DIR = "'/Users/iantristancultura/.dbt'"
VENV_ACTIVATE = "'/Users/iantristancultura/Documents/Data Engineer/Kafka-DBT-SnowFlake-Airflow/.venv/bin/activate'"

default_args = {
    "owner": "airflow",
    "depends_on_past": False,
    "retries": 1,
    "retry_delay": timedelta(minutes=1),
}

with DAG(
    dag_id="SCD2_snapshots",
    default_args=default_args,
    description="Run dbt snapshots for SCD2",
    schedule_interval="@daily",
    start_date=datetime(2025, 9, 1),
    catchup=False,
    tags=["dbt", "snapshots"],
) as dag:

    # Task 1: Run Snapshots
    dbt_snapshot_task = BashOperator(
        task_id="dbt_snapshot",
        # Adding quotes around the variable interpolations
        bash_command=f"source {VENV_ACTIVATE} && cd {DBT_PROJECT_DIR} && dbt snapshot --profiles-dir {DBT_PROFILES_DIR}"
    )

    # Task 2: Run Marts (Dimensions)
    dbt_run_marts_task = BashOperator(
        task_id="dbt_run_marts",
        bash_command=f"source {VENV_ACTIVATE} && cd {DBT_PROJECT_DIR} && dbt run --select marts --profiles-dir {DBT_PROFILES_DIR}"
    )

    # Dependency: Snapshot must finish successfully before Marts start
    dbt_snapshot_task >> dbt_run_marts_task