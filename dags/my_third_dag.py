from airflow.operators.python_operator import PythonOperator
from airflow.operators.bash_operator import BashOperator
from airflow import DAG

from datetime import datetime, timedelta


def fifth_function_execute():
    return 'Hello from fifth_function_execute'


def sixth_function_execute():
    return 'Hello from sixth_function_execute'


default_args = {
    "owner": "Airflow",
    "retries": 1,
    "retry_delay": timedelta(minutes=5),
    "start_date": datetime(2022, 5, 5)
}

with DAG(
        dag_id='my_third_dag',
        schedule_interval="*/1 * * * *",  # Executed every minute
        default_args=default_args,
        catchup=False
) as dag:
    bash_task_1 = BashOperator(task_id='bash_task_1',
                               bash_command="echo 'Hello bash'",
                               wait_for_downstream=True
                               # Task directly in the downstream should be executed
                               # successfully in the previous DAG run in order for
                               # this to be executed in the current DAG run.
                               )

    python_task_5 = PythonOperator(task_id='python_task_5',
                                   python_callable=fifth_function_execute,
                                   depend_on_past=True
                                   # This Task depends on previous DAG run's instance same task.
                                   # If previous DAG run is a failure then the current will a failure.
                                   # The downstream tasks will not be executed in the current DAG run.
                                   # Task in the future DAG run will not even be queued for execution.
                                   )

    python_task_6 = PythonOperator(
        task_id='python_task_6',
        python_callable=sixth_function_execute,
    )

bash_task_1 >> python_task_5 >> python_task_6
