from datetime import datetime , timedelta
from airflow import DAG
from docker.types import Mount
from airflow.operators.python_operator import PythonOperator
from airflow.operators.bash import BashOperator
from airflow.providers.docker.operators.docker import DockerOperator
from airflow.utils.dates import days_ago
import subprocess

default_args = {
    'owner': 'airflow',
    'depends_on_past': False,
    'email_on_failure': False,
    'email_on_retry': False
}

def run_elt_script():
  script_path = "/opt/airflow/elt/elt_script.py"
  result = subprocess.run(["python", script_path], capture_output=True,text=True)
  if result.returncode != 0:
    raise ValueError("ELT script failed")
  else :
    print("ELT script completed successfully")

dag = DAG(
  'elt_and_dbt',
  default_args=default_args,
  description='ETL and DBT pipeline',
  start_date=days_ago(1),
  catchup=False
)

t1 = PythonOperator(
  task_id='run_elt_script',
  python_callable=run_elt_script,
  dag=dag
)

t2 = DockerOperator(
    task_id='dbt-run',
    image='ghcr.io/dbt-labs/dbt-postgres:1.4.7',
    command=[
        "run",
        "--profiles-dir",
        "/root",
        "--project-dir",
        "/opt/dbt"
      ],
    auto_remove=True,
    docker_url="unix://var/run/docker.sock",
    network_mode="bridge",
    mounts=[
      Mount(source="E:/data eng/etl/custom_postgres",target='/opt/dbt',type='bind'),
      Mount(source="C:/Users/John/.dbt",target='/root',type='bind')
    ] ,
    dag=dag
)

t1>>t2