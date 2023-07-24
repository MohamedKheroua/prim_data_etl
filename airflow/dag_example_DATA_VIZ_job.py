from datetime import datetime, timedelta

from airflow import DAG
from airflow.operators.python import PythonOperator

from src.custom.data_viz_functions import bar_chart_data_viz

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

def save_data_viz(**kwargs):
    # Dag execution time (timestamp)
    date = datetime.fromisoformat(kwargs['ts'])
    
    # Visualisation is done for the previous day
    dataviz_date = date - timedelta(days=1)

    bar_chart_data_viz(day_of_month=dataviz_date.day,
                       month=dataviz_date.month,
                       year=dataviz_date.year,
                       destination='Aulnay-sous-Bois',
                       html_file= "data/" + date.strftime('%Y%m%d') + "_my_bar_graph.html")

task_load = PythonOperator(
    task_id='load_job',
    dag=dag,
    python_callable=save_data_viz
)

task_load