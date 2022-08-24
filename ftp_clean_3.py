import datetime
# import pendulum
from airflow import DAG
from airflow.operators.dummy import DummyOperator
from airflow.providers.cncf.kubernetes.operators.kubernetes_pod import KubernetesPodOperator
#from airflow.contrib.kubernetes.volume import Volume
#from airflow.contrib.kubernetes.volume_mount import VolumeMount

version = "0.1.0"

with DAG(
        dag_id='ftp_clean_load2',
        schedule_interval=None,
        # start_date=pendulum.datetime(2022, 5, 20, tz="UTC"),
         start_date=datetime.datetime.now() - datetime.timedelta(days=1),
         dagrun_timeout=datetime.timedelta(minutes=60),
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

    ftp_clean2 = KubernetesPodOperator(
        namespace='service-monitoring',
        name="ftp_clean3",
        image="priyesh2020/cleanup:latest",
        #cmds=["python dagtest.py"],
        arguments=['-ho=ipaddress','-u=username','-p=pswd','-dp=/test'],
        # labels={"foo": "bar"},
        task_id="ftp_clean3",
        # do_xcom_push=True,
        get_logs=True,
        image_pull_policy='Always',
        # List of Volume objects to pass to the Pod.
        #volumes=[volume],
        # List of VolumeMount objects to pass to the Pod.
        #volume_mounts=[volume_mount],
        dag=dag
    )

start >> ftp_clean2 >> end