"""
load_gold_to_postgres.py

Objective:
Load Gold Layer datasets from MinIO
into PostgreSQL Data Warehouse.

Architecture:

MinIO Gold
        ↓
Spark
        ↓ JDBC
PostgreSQL

Project:
Olist Seller Intelligence Platform
"""

# =========================================================
# PROJECT ROOT
# =========================================================

import os
import sys

project_root = os.path.abspath(
    os.path.join(
        os.path.dirname(__file__),
        "../../"
    )
)

if project_root not in sys.path:
    sys.path.append(project_root)

# =========================================================
# IMPORTS
# =========================================================

from pipelines.silver.utils.spark_session import (
    create_spark_session
)

# =========================================================
# SPARK SESSION
# =========================================================

spark = create_spark_session(
    "LoadGoldToPostgres"
)



IS_DOCKER = (
    os.getenv(
        "SPARK_DOCKER",
        "false"
    ).lower() == "true"
)

POSTGRES_HOST = (
    "postgres"
    if IS_DOCKER
    else "localhost"
)


# =========================================================
# POSTGRES CONFIG
# =========================================================

POSTGRES_URL = (
    f"jdbc:postgresql://{POSTGRES_HOST}:5432/olist_dw"
)

POSTGRES_PROPERTIES = {

    "user": "olist",

    "password": "olist123",

    "driver": "org.postgresql.Driver"
}

# =========================================================
# GOLD DATASETS
# =========================================================

GOLD_DATASETS = {

    # =====================================================
    # DIMENSIONS
    # =====================================================

    "dim_date":
        "s3a://gold/dim_date/",

    "dim_customer":
        "s3a://gold/dim_customer/",

    "dim_seller":
        "s3a://gold/dim_seller/",

    "dim_product":
        "s3a://gold/dim_product/",

    # =====================================================
    # FACTS
    # =====================================================

    "fct_order_delivery":
        "s3a://gold/fct_order_delivery/",

    "fct_seller_fulfillment":
        "s3a://gold/fct_seller_fulfillment/",

    "fct_customer_reviews":
        "s3a://gold/fct_customer_reviews/",

    "fct_order_sales":
        "s3a://gold/fct_order_sales/",

    # =====================================================
    # MARTS
    # =====================================================

    "seller_performance_mart":
        "s3a://gold/marts/seller_performance_mart/"
}

# =========================================================
# LOAD TABLES
# =========================================================

print("\n=================================================")
print("LOADING GOLD LAYER TO POSTGRESQL")
print("=================================================")

for table_name, source_path in GOLD_DATASETS.items():

    print("\n-------------------------------------------------")
    print(f"Loading: {table_name}")
    print("-------------------------------------------------")

    try:

        df = spark.read.parquet(
            source_path
        )

        row_count = df.count()

        print(
            f"Rows: {row_count:,}"
        )

        df.write \
            .mode("overwrite") \
            .jdbc(

                url=POSTGRES_URL,

                table=table_name,

                properties=POSTGRES_PROPERTIES
            )

        print(
            f"SUCCESS -> {table_name}"
        )

    except Exception as e:

        print(
            f"FAILED -> {table_name}"
        )

        print(str(e))

        raise

# =========================================================
# SUMMARY
# =========================================================

print("\n=================================================")
print("POSTGRES LOAD COMPLETED")
print("=================================================")

print(
    f"Tables Loaded: {len(GOLD_DATASETS)}"
)

spark.stop()