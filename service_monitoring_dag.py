import datetime
import pendulum

from airflow import DAG
from airflow.operators.dummy import DummyOperator
from airflow.providers.cncf.kubernetes.operators.kubernetes_pod import KubernetesPodOperator

with DAG(
        dag_id='monitoring_dag',
        schedule_interval='* * * * *',
        start_date=pendulum.datetime(2022, 4, 29, tz="UTC"),
        dagrun_timeout=datetime.timedelta(minutes=60),
) as dag:

    start = DummyOperator(
        task_id='start',
    )

    end = DummyOperator(
        task_id='end',
    )

    service_monitoring_task = KubernetesPodOperator(
        namespace='default',
        name="service_monitoring",
        image="noeljohnk/kmd-nextgeneration:service-monitoring",
        #cmds=["bash", "-cx"],
        #arguments=["echo", "10"],
        #labels={"foo": "bar"},
        task_id="service_monitoring",
        #do_xcom_push=True,
        get_logs=True,
        image_pull_policy='Always',
        dag=dag
    )

start >> service_monitoring_task >> end
