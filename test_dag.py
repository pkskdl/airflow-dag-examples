import datetime
#import pendulum

from airflow import DAG
from airflow.operators.bash import BashOperator
from airflow.operators.dummy import DummyOperator

with DAG(
    dag_id='test_dag',
    schedule_interval='0 0 * * *',
    #start_date=pendulum.datetime(2022, 1, 1, tz="UTC"),
    start_date=datetime.datetime.now(),
    dagrun_timeout=datetime.timedelta(minutes=60),
) as dag:

    start = DummyOperator(
        task_id='start',
    )

    end = DummyOperator(
        task_id='end',
    )

    task_1 = BashOperator(
        task_id='task_1',
        bash_command='echo 1',
    )

start >> task_1 >> end
