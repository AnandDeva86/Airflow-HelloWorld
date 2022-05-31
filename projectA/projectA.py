from airflow.operators.bash_operator import BashOperator
from airflow import DAG

from datetime import datetime, timedelta


def on_success_task(dict):
    print('on_success_dag')
    print(dict)


def on_failure_task(dict):
    print('on_failure_dag')
    print(dict)


default_args = {
    "owner": "Airflow",
    "retries": 1,
    "retry_delay": timedelta(seconds=60),
    "start_date": datetime(2022, 5, 5),
    "on_success_callback": on_success_task,
    "on_failure_callback": on_failure_task,
    "execution_timeout": timedelta(seconds=60)
}


def on_success_dag(dict):
    print('on_success_dag')
    print(dict)


def on_failure_dag(dict):
    print('on_failure_dag')
    print(dict)


with DAG(
        dag_id='projectA',
        schedule_interval="*/1 * * * *",  # Executed every minute
        default_args=default_args,
        catchup=False,
        dagrun_timeout=timedelta(seconds=25),  # DAG run will fail if it takes more than 25 sec to execute
        on_success_callback=on_success_dag,
        on_failure_callback=on_failure_dag
) as dag:
    bash_task_1 = BashOperator(task_id='bash_task_1',
                               bash_command="echo 'Hello bash1'",
                               )

    bash_task_2 = BashOperator(task_id='bash_task_2',
                               bash_command="echo 'Hello bash2'"
                               )


bash_task_1 >> bash_task_2
