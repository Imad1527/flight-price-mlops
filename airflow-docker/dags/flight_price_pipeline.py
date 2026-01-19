from airflow import DAG
from airflow.operators.bash import BashOperator
from datetime import datetime

with DAG(
    dag_id="flight_price_training_pipeline",
    start_date=datetime(2024, 1, 1),
    schedule_interval="@daily",
    catchup=False
) as dag:

    train_model = BashOperator(
        task_id="train_model",
        bash_command="python /opt/airflow/dags/../training/train_flight_price_model.py"
    )

    train_model
