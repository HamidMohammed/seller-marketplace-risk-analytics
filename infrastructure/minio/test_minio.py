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


from pipelines.silver.utils.spark_session import (
    create_spark_session
)

spark = create_spark_session(
    "MinIOTest"
)

df = spark.range(10)

df.write.mode(
    "overwrite"
).parquet(
    "s3a://bronze/test_dataset/"
)

print(
    "WRITE SUCCESS"
)

spark.stop()