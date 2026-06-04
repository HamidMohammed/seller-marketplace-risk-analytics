"""
migrate_bronze_layer.py

Objective:
Migrate all Bronze datasets from
local storage into MinIO Bronze bucket.

Project:
Olist Seller Intelligence Platform

Infrastructure Sprint 1

Migration:

Local Bronze
        ↓
MinIO Bronze
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
    "BronzeLayerMigration"
)

# =========================================================
# DATASETS
# =========================================================

DATASETS = {

    "orders":
    (
        "data/bronze/orders/",
        "s3a://bronze/orders/"
    ),

    "customers":
    (
        "data/bronze/customers/",
        "s3a://bronze/customers/"
    ),

    "sellers":
    (
        "data/bronze/sellers/",
        "s3a://bronze/sellers/"
    ),

    "products":
    (
        "data/bronze/products/",
        "s3a://bronze/products/"
    ),

    "payments":
    (
        "data/bronze/payments/",
        "s3a://bronze/payments/"
    ),

    "reviews":
    (
        "data/bronze/reviews/",
        "s3a://bronze/reviews/"
    ),

    "order_items":
    (
        "data/bronze/order_items/",
        "s3a://bronze/order_items/"
    ),

    "geolocation":
    (
        "data/bronze/geolocation/",
        "s3a://bronze/geolocation/"
    ),

    "category_translation":
    (
        "data/bronze/category_translation/",
        "s3a://bronze/category_translation/"
    ),

    "mql":
    (
        "data/bronze/mql/",
        "s3a://bronze/mql/"
    ),

    "closed_deals":
    (
        "data/bronze/closed_deals/",
        "s3a://bronze/closed_deals/"
    )

}

# =========================================================
# MIGRATION
# =========================================================

print("\n=================================================")
print("BRONZE LAYER MIGRATION STARTED")
print("=================================================")

for dataset_name, paths in DATASETS.items():

    local_path = paths[0]
    minio_path = paths[1]

    print("\n-------------------------------------------------")
    print(f"Migrating: {dataset_name}")
    print("-------------------------------------------------")

    try:

        df = spark.read.parquet(
            local_path
        )

        row_count = df.count()

        print(
            f"Rows Read: {row_count:,}"
        )

        df.write.mode(
            "overwrite"
        ).parquet(
            minio_path
        )

        print(
            f"SUCCESS -> {minio_path}"
        )

    except Exception as e:

        print(
            f"FAILED -> {dataset_name}"
        )

        print(
            f"Error: {str(e)}"
        )

        raise

# =========================================================
# SUMMARY
# =========================================================

print("\n=================================================")
print("BRONZE LAYER MIGRATION COMPLETED")
print("=================================================")

print(
    f"Datasets Migrated: {len(DATASETS)}"
)

spark.stop()