import airflow.utils.dates
from airflow import DAG
from airflow.operators.python_operator import PythonOperator
from airflow.operators.bash_operator import BashOperator

from datetime import datetime, timedelta


def remote_value(**context):
    print("Value {} for key=message received from the trigger DAG".format(context["dag_run"].conf["message"]))


default_args = {
    "start_date": airflow.utils.dates.days_ago(1),
    "owner": "Airflow"
}

with DAG(dag_id='target_dag',
         schedule_interval=None,
         default_args=default_args,
         catchup=False
         ) as dag:
    py_task = PythonOperator(task_id='py_task',
                             provide_context=True,
                             python_callable=remote_value)
    bash_task = BashOperator(
        task_id="bash_task",
        bash_command='echo Message: {{ dag_run.conf["message"] if dag_run else "" }}')

py_task >> bash_task