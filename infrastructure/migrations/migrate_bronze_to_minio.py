import sys
import os

project_root = os.path.abspath(
    os.path.join(
        os.path.dirname(__file__),
        "../../"
    )
)

if project_root not in sys.path:
    sys.path.append(project_root)
print("Project root added to sys.path:", project_root)

from pyspark.sql import SparkSession

from pipelines.silver.utils.spark_session import (
    create_spark_session
)

spark = create_spark_session(
    "BronzeMigration"
)

local_orders = spark.read.parquet(
    "data/bronze/orders/"
)

local_orders.write.mode(
    "overwrite"
).parquet(
    "s3a://bronze/orders/"
)

print("Orders migrated")

spark.stop()