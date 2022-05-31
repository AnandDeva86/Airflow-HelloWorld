from airflow.operators.python_operator import PythonOperator
from airflow import DAG
from datetime import datetime, timedelta


# passing values between functions
def third_function_execute(**context):
    context['ti'].xcom_push(key='myKey', value='Have a great day')
    return 'Hello from third_function_execute'


def fourth_function_execute(**context):
    instance = context.get('ti').xcom_pull(key='myKey')
    return f'Hello, {instance}'


default_args = {
    "owner": "Airflow",
    "retries": 1,
    "retry_delay": timedelta(minutes=5),
    "start_date": datetime(2022, 5, 5)
}

with DAG(
        dag_id='my_second_dag',
        schedule_interval="*/2 * * * *",
        default_args=default_args,
        catchup=False
) as dag:
    python_task_3 = PythonOperator(
        task_id='python_task_3',
        python_callable=third_function_execute,
        provide_context=True  # to pass values between functions
    )

    python_task_4 = PythonOperator(
        task_id='python_task_4',
        python_callable=fourth_function_execute,
        provide_context=True  # to pass values between functions
    )


python_task_3 >> python_task_4