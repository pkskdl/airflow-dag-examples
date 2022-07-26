import datetime
# import pendulum
from airflow import DAG
from airflow.operators.dummy import DummyOperator
from airflow.providers.cncf.kubernetes.operators.kubernetes_pod import KubernetesPodOperator
#from airflow.contrib.kubernetes.volume import Volume
#from airflow.contrib.kubernetes.volume_mount import VolumeMount

version = "0.1.0"

topic='jsontopic'
load_type='full_load'
log_type='Warn'
broker='localhost:29092'
encryption_algorithm='aes256'
with DAG(
        dag_id='ftp_full_load2',
        schedule_interval=None,
        # start_date=pendulum.datetime(2022, 5, 20, tz="UTC"),
         start_date=datetime.datetime.now() - datetime.timedelta(days=1),
         dagrun_timeout=datetime.timedelta(minutes=60),
         #default_args=default_args
) as dag:
    start = DummyOperator(
        task_id='start',
    )

    end = DummyOperator(
        task_id='end',
    )
    

    # volume_mount = VolumeMount('test-volume',
                               # mount_path='/root/mount_file',
                               # sub_path=None,
                               # read_only=True)

    # volume_config = {
        # 'persistentVolumeClaim':
            # {
                # 'claimName': 'test-volume'
            # }
    # }
    
    #volume = Volume(name='test-volume', configs=volume_config)

    ftp_fullload2 = KubernetesPodOperator(
        namespace='service-monitoring',
        name="ftp_fullload",
        image="priyesh2020/dagtest2:latest",
        #cmds=["python dagtest.py"],
        arguments=[f'-t={topic}',f'-s={load_type}',f'-l={log_type}',f'-b={broker}',f'-a={encryption_algorithm}'],
        # labels={"foo": "bar"},
        task_id="ftp_fullload",
        # do_xcom_push=True,
        get_logs=True,
        image_pull_policy='Always',
        # List of Volume objects to pass to the Pod.
        #volumes=[volume],
        # List of VolumeMount objects to pass to the Pod.
        #volume_mounts=[volume_mount],
        dag=dag
    )

start >> ftp_fullload2 >> end
