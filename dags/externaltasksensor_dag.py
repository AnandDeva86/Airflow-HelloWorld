import airflow.utils.dates
from airflow import DAG
from airflow.sensors.external_task_sensor import ExternalTaskSensor
from airflow.operators.dummy_operator import DummyOperator

default_args = {
    "owner": "airflow",
    "start_date": airflow.utils.dates.days_ago(1)
}

with DAG(
        dag_id="externalTaskSensor_dag",
        default_args=default_args,
        schedule_interval="@daily"
) as dag:
    sensor = ExternalTaskSensor(
        task_id='sensor',
        external_dag_id='my_first_dag',
        external_task_id='python_task_1'
    )

    final_task = DummyOperator(task_id="final_task")

sensor >> final_task