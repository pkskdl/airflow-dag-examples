import datetime
from airflow import DAG
from airflow.operators.dummy import DummyOperator
from airflow.providers.cncf.kubernetes.operators.kubernetes_pod import KubernetesPodOperator

version = "0.1.0"

topic='jsontopic'
load_type='full_load'
log_type='Warn'
broker='localhost'
encryption_algorithm='aes256'
with DAG(
        dag_id='ftp_full_load_dynamic',
        schedule_interval=None,
        start_date=datetime.datetime.now() - datetime.timedelta(days=1),
        dagrun_timeout=datetime.timedelta(minutes=60)
        
) as dag:
    start = DummyOperator(
        task_id='start',
    )

    end = DummyOperator(
        task_id='end',
    )
    
    ftp_fullload_dynamic = KubernetesPodOperator(
        namespace='service-monitoring',
        name="ftp_fullload_dynamic",
        image="priyesh2020/dagtest2:latest",
        arguments=[f'-t={topic}',f'-s={load_type}',f'-l={log_type}',f'-b={broker}',f'-a={encryption_algorithm}'],
        task_id="ftp_fullload_dynamic",
        get_logs=True,
        image_pull_policy='Always',
        # List of Volume objects to pass to the Pod.
        #volumes=[volume],
        # List of VolumeMount objects to pass to the Pod.
        #volume_mounts=[volume_mount],
        dag=dag
    )

start >> ftp_fullload_dynamic >> end
