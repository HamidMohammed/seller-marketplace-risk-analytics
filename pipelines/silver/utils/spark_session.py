from pyspark.sql import SparkSession
import os


def create_spark_session(app_name: str):

    is_docker = (
        os.getenv(
            "SPARK_DOCKER",
            "false"
        ).lower()
        == "true"
    )

    S3_ENDPOINT = (
        "http://minio:9000"
        if is_docker
        else "http://localhost:9000"
    )
    spark = (

        SparkSession.builder

        .appName(app_name)
        # all in /opt/spark/jars/
        # .config(
        # "spark.jars.packages",
        # ",".join([
        #     "org.apache.hadoop:hadoop-aws:3.3.4",
        #     "org.postgresql:postgresql:42.7.4"
        # ])
    # )

        .config(
            "spark.hadoop.fs.s3a.endpoint",
            S3_ENDPOINT
        )

        .config(
            "spark.hadoop.fs.s3a.access.key",
            "admin"
        )

        .config(
            "spark.hadoop.fs.s3a.secret.key",
            "admin123"
        )

        .config(
            "spark.hadoop.fs.s3a.path.style.access",
            "true"
        )

        .config(
            "spark.hadoop.fs.s3a.connection.ssl.enabled",
            "false"
        )

        .config(
            "spark.hadoop.fs.s3a.impl",
            "org.apache.hadoop.fs.s3a.S3AFileSystem"
        )

        .getOrCreate()

    )

    spark.sparkContext.setLogLevel("WARN")

    return spark