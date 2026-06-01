import os
import sys
import time
import subprocess

project_root = os.path.abspath(
    os.path.join(
        os.path.dirname(__file__),
        "../../"
    )
)

if project_root not in sys.path:
    sys.path.append(project_root)


from pipelines.bronze.utils.config_loader import (
    load_config
)

from pipelines.bronze.utils.spark_session import (
    create_spark_session
)

from pipelines.bronze.utils.bronze_ingestion import (
    ingest_dataset
)

config = load_config()

spark = create_spark_session(
    "RunBronzePipeline"
)

for dataset in config["bronze_pipeline"]["ingestion"]:

    source_path = (
        config["paths"]["raw"][dataset]
    )

    target_path = (
        config["paths"]["bronze"][dataset]
    )

    ingest_dataset(
        spark=spark,
        source_path=source_path,
        target_path=target_path,
        dataset_name=dataset
    )

spark.stop()