"""
transform_seller_fulfillment_staging.py

Objective:
Assemble seller-level fulfillment staging dataset
from silver_order_items enriched with seller geography
and seller workload intelligence.

This staging dataset is the direct input to:
fct_seller_fulfillment

Project:
Olist Seller Intelligence Platform

Layer:
Silver Staging

Dataset:
seller_fulfillment_staging

Dataset Grain:
ONE ROW = ONE SELLER ITEM FULFILLMENT EVENT
"""

# =========================================================
# PROJECT ROOT SETUP
# =========================================================

import sys
import os

project_root = os.path.abspath(
    os.path.join(os.path.dirname(__file__), "../../../../")
)

if project_root not in sys.path:
    sys.path.append(project_root)

print(f"Project Root Added: {project_root}")


# =========================================================
# IMPORTS
# =========================================================

from pyspark.sql.functions import (
    col,
    count,
    month,
    year,
    when,
    current_timestamp,
    lit
)

from pyspark.sql.window import Window

from pipelines.silver.utils.config_loader import (
    load_config
)

from pipelines.silver.utils.spark_session import (
    create_spark_session
)

from pipelines.silver.validations.seller_fulfillment_staging_validation import (
    run_seller_fulfillment_staging_validation
)


# =========================================================
# CREATE SPARK SESSION
# =========================================================

spark = create_spark_session(
    "TransformSellerFulfillmentStaging"
)


# =========================================================
# LOAD CONFIGURATION
# =========================================================

config = load_config()

# ---------------------------------------------------------
# Silver Paths
# ---------------------------------------------------------

SILVER_ORDER_ITEMS_PATH = (
    config["paths"]["silver"]["order_items"]
)

SILVER_SELLERS_PATH = (
    config["paths"]["silver"]["sellers"]
)

# ---------------------------------------------------------
# Staging Output Path
# ---------------------------------------------------------

SELLER_FULFILLMENT_STAGING_PATH = (
    config["paths"]["silver"]["seller_fulfillment_staging"]
)

# ---------------------------------------------------------
# Metadata
# ---------------------------------------------------------

SOURCE_SYSTEM = (
    config["metadata"]["source_system"]
)

TRANSFORMATION_VERSION = (
    config["metadata"]["transformation_version"]
)


# =========================================================
# LOAD DATASETS
# =========================================================

print("\n=================================================")
print("LOADING SILVER DATASETS")
print("=================================================")

order_items_df = spark.read.parquet(
    SILVER_ORDER_ITEMS_PATH
)

sellers_df = spark.read.parquet(
    SILVER_SELLERS_PATH
)

print(f"Order Items Count: {order_items_df.count()}")
print(f"Sellers Count: {sellers_df.count()}")


# =========================================================
# SELECT SELLER ENRICHMENT COLUMNS
# =========================================================

print("\n=================================================")
print("SELECTING SELLER ENRICHMENT COLUMNS")
print("=================================================")

sellers_selected_df = sellers_df.select(

    "seller_id",

    "seller_state",

    col("median_latitude").alias(
        "seller_lat"
    ),

    col("median_longitude").alias(
        "seller_lng"
    ),

    "acquisition_source"
)


# =========================================================
# JOIN SELLER ENRICHMENT
# =========================================================

print("\n=================================================")
print("JOINING SELLER ENRICHMENT")
print("=================================================")

staging_df = order_items_df.join(
    sellers_selected_df,
    on="seller_id",
    how="left"
)


# =========================================================
# SELLER MONTHLY WORKLOAD
# =========================================================

print("\n=================================================")
print("DERIVING SELLER WORKLOAD METRICS")
print("=================================================")

seller_monthly_window = Window.partitionBy(

    "seller_id",

    year("order_purchase_timestamp"),

    month("order_purchase_timestamp")
)

staging_df = staging_df.withColumn(
    "seller_monthly_orders",

    count("order_id").over(
        seller_monthly_window
    ).cast("int")
)


# =========================================================
# WORKLOAD BUCKET CLASSIFICATION
# =========================================================

staging_df = staging_df.withColumn(

    "workload_bucket",

    when(
        col("seller_monthly_orders") <= 20,
        "Low Volume"

    ).when(
        col("seller_monthly_orders") <= 100,
        "Medium Volume"

    ).when(
        col("seller_monthly_orders") <= 500,
        "High Volume"

    ).otherwise(
        "Overloaded"
    )
)

# =========================================================
# OPTIONAL WORKLOAD RISK FLAG
# =========================================================

"""
Useful later for:
- operational monitoring
- seller risk scoring
- streaming alert prioritization
"""

print("\nApplying workload risk flags...")

staging_df = (

    staging_df

    .withColumn(

        "is_overloaded_seller",

        when(
            col("workload_bucket") == "Overloaded",
            True
        ).otherwise(False)

    )
)
# =========================================================
# METADATA ENRICHMENT
# =========================================================

staging_df = staging_df.withColumn(
    "silver_loaded_at",
    current_timestamp()
)

staging_df = staging_df.withColumn(
    "source_system",
    lit(SOURCE_SYSTEM)
)

staging_df = staging_df.withColumn(
    "transformation_version",
    lit(TRANSFORMATION_VERSION)
)


seller_order_window = Window.partitionBy(
    "order_id",
    "seller_id"
)

staging_df = staging_df.withColumn(
    "seller_item_count_in_order",
    count("order_item_id").over(
        seller_order_window
    ).cast("int")
)

# =========================================================
# FINAL COLUMN SELECTION
# =========================================================

print("\n=================================================")
print("FINAL COLUMN SELECTION")
print("=================================================")

staging_df = staging_df.select(

    "order_id",
    "order_item_id",

    "product_id",
    "seller_id",

    "order_purchase_timestamp",
    "shipping_limit_date",

    "price",
    "freight_value",

    "freight_ratio",

    "product_volume_cm3",

    "seller_item_count_in_order",

    "seller_state",

    "seller_lat",
    "seller_lng",

    "acquisition_source",

    "seller_monthly_orders",

    "workload_bucket",
    "is_overloaded_seller",

    "silver_loaded_at",
    "source_system",
    "transformation_version"
)


# =========================================================
# VALIDATIONS
# =========================================================

print("\n=================================================")
print("RUNNING VALIDATIONS")
print("=================================================")

run_seller_fulfillment_staging_validation(
    staging_df
)


# =========================================================
# WRITE STAGING DATASET
# =========================================================

print("\n=================================================")
print("WRITING SELLER FULFILLMENT STAGING")
print("=================================================")

staging_df.write.mode("overwrite").parquet(
    SELLER_FULFILLMENT_STAGING_PATH
)

print("Seller Fulfillment Staging Written Successfully")


# =========================================================
# FINAL SUMMARY
# =========================================================

print("\n=================================================")
print("SELLER FULFILLMENT STAGING PIPELINE COMPLETED")
print("=================================================")

print(f"Final Row Count: {staging_df.count()}")

staging_df.printSchema()

spark.stop()




