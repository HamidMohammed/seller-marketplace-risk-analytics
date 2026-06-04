from datetime import datetime

from airflow import DAG
from airflow.operators.bash import BashOperator


with DAG(

    dag_id="olist_master_pipeline",

    start_date=datetime(
        2025,
        1,
        1
    ),

    schedule=None,

    catchup=False,

    tags=[
        "olist",
        "data-platform"
    ]

) as dag:

    run_pipeline = BashOperator(

        task_id="run_olist_platform",

        # bash_command="""
        # cd /workspace/project &&
        # python run_pipeline.py
        # """
        bash_command="""
        docker exec spark-master \
        /opt/spark/bin/spark-submit \
        /workspace/project/pipelines/run_pipeline.py
        """
    )
    
    
