from datetime import datetime

from airflow import DAG
from airflow.operators.bash import BashOperator


with DAG(
    dag_id="ecommerce_elt_pipeline",
    start_date=datetime(2025, 1, 1),
    schedule_interval=None,
    catchup=False,
    tags=["portfolio", "bigquery", "dbt", "airflow"],
) as dag:

    generate_data = BashOperator(
        task_id="generate_data",
        bash_command="cd /opt/project && python scripts/generate_synthetic_ecommerce.py",
    )

    validate_data = BashOperator(
        task_id="validate_data",
        bash_command="cd /opt/project && python scripts/validate_synthetic.py",
    )

    load_to_bigquery = BashOperator(
        task_id="load_to_bigquery",
        bash_command="cd /opt/project && python scripts/load_to_bigquery.py",
    )

    run_dbt = BashOperator(
        task_id="run_dbt",
        bash_command=(
            "cd /opt/project/dbt_project && "
            "dbt run --profiles-dir /home/airflow/.dbt "
            "--target-path /tmp/dbt_target "
            "--log-path /tmp/dbt_logs"
        ),
    )

    test_dbt = BashOperator(
        task_id="test_dbt",
        bash_command=(
            "cd /opt/project/dbt_project && "
            "dbt test --profiles-dir /home/airflow/.dbt "
            "--target-path /tmp/dbt_target "
            "--log-path /tmp/dbt_logs"
        ),
    )
    generate_data >> validate_data >> load_to_bigquery >> run_dbt >> test_dbt