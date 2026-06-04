# test_s3a.py

from pyspark.sql import SparkSession

spark = (
    SparkSession.builder
    .appName("CheckS3A")
    .getOrCreate()
)

jvm = spark.sparkContext._jvm

try:
    cls = jvm.java.lang.Class.forName(
        "org.apache.hadoop.fs.s3a.S3AFileSystem"
    )

    print("S3A FOUND")

except Exception as e:
    print("S3A NOT FOUND")
    print(e)

spark.stop()