# =========================================================
# Bronze Layer Ingestion Pipeline
# File: pipelines/bronze/ingest_to_bronze.py
# =========================================================

from pyspark.sql import SparkSession
from pyspark.sql.functions import (
    current_timestamp,
    current_date,
    lit,
    input_file_name
)

import yaml
import os
from datetime import datetime


# =========================================================
# SPARK SESSION
# =========================================================

spark = (
    SparkSession.builder
    .appName("Olist Bronze Ingestion")
    .getOrCreate()
)

spark.sparkContext.setLogLevel("WARN")


# =========================================================
# LOAD CONFIG FILES
# =========================================================

with open("configs/paths.yaml", "r") as file:
    paths_config = yaml.safe_load(file)

with open("configs/datasets.yaml", "r") as file:
    datasets_config = yaml.safe_load(file)


RAW_PATH = paths_config["raw_path"]
BRONZE_PATH = paths_config["bronze_path"]


# =========================================================
# INGESTION FUNCTION
# =========================================================

def ingest_dataset(
    dataset_name,
    csv_filename,
    read_options=None
):
    """
    Generic Bronze ingestion function.

    Steps:
    1. Read raw CSV
    2. Infer schema
    3. Add ingestion metadata
    4. Write parquet to Bronze layer
    5. Validate row counts
    """

    print("=" * 60)
    print(f"STARTING BRONZE INGESTION: {dataset_name}")
    print("=" * 60)

    input_path = os.path.join(RAW_PATH, csv_filename)
    output_path = os.path.join(BRONZE_PATH, dataset_name)

    print(f"Reading from: {input_path}")
    print(f"Writing to : {output_path}")

    # =====================================================
    # STEP 1 — READ RAW CSV
    # =====================================================

    reader = (

    spark.read

    .option("header", True)

    .option("inferSchema", True)

    )

    # =====================================================
    # APPLY OPTIONAL DATASET READ OPTIONS
    # =====================================================

    if read_options:

        for option_key, option_value in read_options.items():

            reader = reader.option(
                option_key,
                option_value
            )

    # =====================================================
    # LOAD CSV
    # =====================================================

    df = reader.csv(input_path)
    # =====================================================
    # STEP 2 — ADD INGESTION METADATA
    # =====================================================

    df = (
        df
        .withColumn("ingestion_timestamp", current_timestamp())
        .withColumn("ingestion_date", current_date())
        .withColumn("source_file", lit(csv_filename))
    )

    # =====================================================
    # STEP 3 — WRITE TO BRONZE AS PARQUET
    # =====================================================

    (
        df.write
        .mode("overwrite")
        .parquet(output_path)
    )

    print("Parquet write completed.")

    # =====================================================
    # STEP 4 — VALIDATION
    # =====================================================

    print("Running validation checks...")

    csv_count = df.count()

    parquet_df = spark.read.parquet(output_path)
    parquet_count = parquet_df.count()

    # -----------------------------------------------------
    # ROW COUNT VALIDATION
    # -----------------------------------------------------

    if csv_count != parquet_count:
        raise Exception(
            f"Row count mismatch! "
            f"CSV: {csv_count}, "
            f"Parquet: {parquet_count}"
        )

    # -----------------------------------------------------
    # SCHEMA DISPLAY
    # -----------------------------------------------------

    print("Schema:")
    parquet_df.printSchema()

    # -----------------------------------------------------
    # SUCCESS MESSAGE
    # -----------------------------------------------------

    print(f"SUCCESS: {dataset_name} ingested successfully.")
    print(f"Rows Loaded: {parquet_count}")

    print("=" * 60)
    print()


# =========================================================
# MAIN EXECUTION
# =========================================================

if __name__ == "__main__":

    start_time = datetime.now()

    print("\n")
    print("=" * 60)
    print("OLIST BRONZE INGESTION PIPELINE STARTED")
    print("=" * 60)

    # =====================================================
    # LOOP THROUGH ALL DATASETS
    # =====================================================

    for dataset in datasets_config["datasets"]:

        dataset_name = dataset["name"]
        csv_filename = dataset["file"]

        read_options = dataset.get(
        "read_options",
        None
        )

        ingest_dataset(
            dataset_name,
            csv_filename,
            read_options
        )

    # =====================================================
    # PIPELINE FINISH
    # =====================================================

    end_time = datetime.now()
    duration = end_time - start_time

    print("=" * 60)
    print("BRONZE INGESTION PIPELINE FINISHED")
    print(f"Execution Time: {duration}")
    print("=" * 60)



    # At end of ingest_to_bronze.py
    validation_report = {
        'run_timestamp': datetime.now().isoformat(),
        'datasets': {
            name: {'rows': count, 'status': 'PASSED'}
            for name, count in ingestion_counts.items()
        }
    }

    with open(f'reports/bronze/ingestion_{date}.json', 'w') as f:
        json.dump(validation_report, f, indent=2)
        
    spark.stop()
