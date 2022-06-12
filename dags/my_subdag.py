from airflow.models import DAG
from airflow.operators.bash_operator import BashOperator
from airflow.operators.subdag_operator import SubDagOperator
from airflow.executors.sequential_executor import SequentialExecutor
from airflow.operators.dummy_operator import DummyOperator
from airflow.executors.celery_executor import CeleryExecutor

from datetime import datetime, timedelta

from subdags.subdag import factory_subdag

DAG_NAME = 'subdag_demo'

default_args = {
    "owner": "Airflow",
    "retries": 1,
    "retry_delay": timedelta(minutes=5),
    "start_date": datetime(2022, 5, 5)
}

with DAG(dag_id=DAG_NAME,
         schedule_interval="@once",
         default_args=default_args,
         catchup=False
         ) as dag:
    start = DummyOperator(task_id="Start"
                          )
    subdag_1 = SubDagOperator(task_id='subdags-1',
                              subdag=factory_subdag(DAG_NAME, 'subdags-1', default_args),
                              executor= SequentialExecutor()  # to execute the task
                              )
    check = BashOperator(task_id="check",
                         bash_command="echo 'middle of 2 subdag'"
                         )
    subdag_2 = SubDagOperator(task_id='subdags-2',
                              subdag=factory_subdag(DAG_NAME, 'subdags-2', default_args),
                              executor=CeleryExecutor()
                              # to execute the subtask in parallel
                              # avoid using CeleryExecutor
                              )
    end = DummyOperator(task_id="End"
                        )

start >> subdag_1 >> check >> subdag_2 >> end