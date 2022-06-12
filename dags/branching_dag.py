import random
from datetime import datetime, timedelta

from airflow.models import DAG
from airflow.operators.dummy_operator import DummyOperator
from airflow.operators.python_operator import BranchPythonOperator


def check_number():
    n = random.randint(0, 20)
    if n < 9:
        return 'top_ten'
    else:
        return 'bottom_ten'


default_args = {
    "owner": "airflow",
    "retries": 1,
    "retry_delay": timedelta(minutes=5),
    "start_date": datetime(2022, 5, 5)
}

with DAG(dag_id='branching_dag',
         schedule_interval="@once",
         default_args=default_args,
         catchup=False
         ) as dag:
    # BranchPythonOperator
    # The next task depends on the return from the
    # python function check_number
    choose_number = BranchPythonOperator(task_id='choose_number',
                                         python_callable=check_number
                                         )
    top_ten = DummyOperator(task_id='top_ten')
    bottom_ten = DummyOperator(task_id='bottom_ten')
    end = DummyOperator(task_id='End',
                        trigger_rule='one_success'  # To execute the task after atleast one parent task
                                                    # in the branching task succeeded
                                                    # Different trigger rules available
                                                    # all_success
                                                    # all_failed
                                                    # all_done
                                                    # one_failed
                                                    # one_success
                                                    # none_failed
                                                    # none_skipped
                        )

# end depends on top_ten or bottom_ten

choose_number >> [top_ten, bottom_ten] >> end
