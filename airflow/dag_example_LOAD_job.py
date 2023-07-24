from datetime import datetime, timedelta

from airflow import DAG
from airflow.operators.python import PythonOperator

from src import load_job

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
# execution every day, at 6 AM
dag = DAG(
    'dag_load_job_for_tramway_line_T4',
    default_args=default_args,
    description='DAG Load job for the tramway line T4',
    schedule="0 6 * * *",
    catchup=False
)

task_load = PythonOperator(
    task_id='load_job',
    dag=dag,
    python_callable=load_job
)

task_load