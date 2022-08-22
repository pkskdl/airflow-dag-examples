import datetime
from airflow import DAG
from airflow.operators.dummy import DummyOperator
from airflow.providers.cncf.kubernetes.operators.kubernetes_pod import KubernetesPodOperator

version = "0.1.0"

with DAG(
        dag_id='ftp_cleanup1',
        schedule_interval=None,
        start_date=datetime.datetime.now() - datetime.timedelta(days=1),
        dagrun_timeout=datetime.timedelta(minutes=60),
) as dag:
    start = DummyOperator(
        task_id='start',
    )

    end = DummyOperator(
        task_id='end',
    )
    ftp_cleanup1 = KubernetesPodOperator(
        namespace='service-monitoring',
        name="ftp_cleanup1",
        image="priyesh2020/cleanup:latest",
        arguments=['-ho=ipaddress','-u=username','-p=pswd','-dp=/test'],
        task_id="ftp_cleanup1",
        get_logs=True,
        image_pull_policy='Always',
        dag=dag
    )
start >> ftp_cleanup1 >> end
