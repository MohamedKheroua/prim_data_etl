from datetime import datetime, timedelta

from airflow import DAG
from airflow.operators.python import PythonOperator

from src import extract_and_transform_job

# DAG parameters
default_args = {
    'owner': 'airflow',
    'depends_on_past': False,
    'start_date': datetime(2023,7,1,0,0,0),
    'retries': 2,
    'retry_delay': timedelta(seconds=20),
    'provide_context': True
}

# DAG creation
# execution every day, every 15 mins, to ensure that all the available data are collected
dag = DAG(
    'dag_et_job_for_tramway_line_T4',
    default_args=default_args,
    description='DAG Extract and Transform job for the tramway line T4',
    schedule="*/15 * * * *",
    catchup=False
)

task_extract = PythonOperator(
    task_id='extract_and_transform_job',
    dag=dag,
    python_callable=extract_and_transform_job
)

extract_and_transform_job