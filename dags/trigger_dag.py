from airflow import DAG
import airflow.utils.dates
from airflow.operators.dummy_operator import DummyOperator
from airflow.operators.dagrun_operator import TriggerDagRunOperator

from datetime import datetime, timedelta


def conditionally_trigger(context, dag_run_obj):
    if context['params']['condition_param']:
        dag_run_obj.payload = {
                'message': context['params']['message']
            }
        return dag_run_obj

default_args = {
    "owner": "Airflow",
    "retries": 1,
    "retry_delay": timedelta(minutes=5),
    "start_date": airflow.utils.dates.days_ago(1),
}
with DAG(dag_id='trigger_dag',
         schedule_interval="@once",
         default_args=default_args,
         catchup=False
         ) as dag:
    trigger = TriggerDagRunOperator(
        task_id="trigger",
        trigger_dag_id="target_dag",  # DAG to be triggered
        provide_context=True,
        python_callable=conditionally_trigger,
        params={
            'condition_param': True,
            'message': 'Hi from the trigger'
        },
    )

    next_task = DummyOperator(task_id="next_task")

trigger >> next_task
