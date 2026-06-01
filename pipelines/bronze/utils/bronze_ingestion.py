from pyspark.sql.functions import (
    current_timestamp,
    current_date,
    input_file_name
)


def ingest_dataset(
    spark,
    source_path,
    target_path,
    dataset_name
):

    print("\n" + "=" * 60)
    print(f"INGESTING: {dataset_name}")
    print("=" * 60)

    df = spark.read.option(
        "header",
        True
    ).csv(
        source_path
    )

    df = df.withColumn(
        "ingestion_timestamp",
        current_timestamp()
    )

    df = df.withColumn(
        "ingestion_date",
        current_date()
    )

    df = df.withColumn(
        "source_file",
        input_file_name()
    )

    df.write.mode(
        "overwrite"
    ).parquet(
        target_path
    )

    print(
        f"Rows Written: {df.count()}"
    )