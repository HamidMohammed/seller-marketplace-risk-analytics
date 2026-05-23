"""
transform_orders.py

Objective:
Transform Bronze orders dataset into trusted Silver orders dataset.

Pipeline Responsibilities:
- Read Bronze parquet
- Standardize schema
- Cast timestamps
- Generate delivery intelligence metrics
- Apply Silver enrichment
- Run business validations
- Write trusted Silver parquet

Project:
Olist Seller Intelligence Platform

Layer:
Silver

Dataset:
silver_orders

Dataset Grain:
ONE ROW = ONE CUSTOMER ORDER
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

from pyspark.sql import SparkSession

from pyspark.sql.functions import (
    col,
    lower,
    trim,
    to_timestamp,
    datediff,
    when,
    current_timestamp,
    lit
)

from pipelines.silver.utils.config_loader import (
    load_config
)

from pipelines.silver.validations.orders_validation import (
    run_orders_validation
)


# =========================================================
# CREATE SPARK SESSION
# =========================================================

spark = SparkSession.builder \
    .appName("TransformSilverOrders") \
    .getOrCreate()


# =========================================================
# LOAD CONFIGURATION
# =========================================================

config = load_config()

BRONZE_ORDERS_PATH = config["paths"]["bronze"]["orders"]

SILVER_ORDERS_PATH = config["paths"]["silver"]["orders"]

SOURCE_SYSTEM = config["metadata"]["source_system"]

TRANSFORMATION_VERSION = config["metadata"]["transformation_version"]


# =========================================================
# LOAD BRONZE DATA
# =========================================================

print("\n=================================================")
print("LOADING BRONZE ORDERS DATA")
print("=================================================")

bronze_orders_df = spark.read.parquet(
    BRONZE_ORDERS_PATH
)

print(f"Bronze Orders Count: {bronze_orders_df.count()}")


# =========================================================
# INITIAL DATA INSPECTION
# =========================================================

print("\n=================================================")
print("BRONZE ORDERS SCHEMA")
print("=================================================")

bronze_orders_df.printSchema()


# =========================================================
# START TRANSFORMATIONS
# =========================================================

print("\n=================================================")
print("STARTING SILVER TRANSFORMATIONS")
print("=================================================")

silver_orders_df = bronze_orders_df


# =========================================================
# 1. STANDARDIZE ORDER STATUS
# =========================================================

"""
Purpose:
- KPI consistency
- Prevent casing inconsistencies
- Improve grouping reliability
"""

silver_orders_df = silver_orders_df.withColumn(
    "order_status",
    lower(
        trim(col("order_status"))
    )
)


# =========================================================
# 2. CAST TIMESTAMP COLUMNS
# =========================================================

"""
Purpose:
- lifecycle analytics
- delivery calculations
- timestamp validation
"""

timestamp_columns = [
    "order_purchase_timestamp",
    "order_approved_at",
    "order_delivered_carrier_date",
    "order_delivered_customer_date",
    "order_estimated_delivery_date"
]

for column_name in timestamp_columns:

    silver_orders_df = silver_orders_df.withColumn(
        column_name,
        to_timestamp(col(column_name))
    )


# =========================================================
# 3. DELIVERY DURATION METRIC
# =========================================================

"""
Measures:
actual customer delivery duration
"""

silver_orders_df = silver_orders_df.withColumn(
    "delivery_duration_days",

    datediff(
        col("order_delivered_customer_date"),
        col("order_purchase_timestamp")
    )
)


# =========================================================
# 4. DELIVERY DELAY METRIC
# =========================================================

"""
Positive:
Late delivery

Negative:
Early delivery

Zero:
On-time delivery
"""

silver_orders_df = silver_orders_df.withColumn(
    "delay_days",

    datediff(
        col("order_delivered_customer_date"),
        col("order_estimated_delivery_date")
    )
)


# =========================================================
# 5. ESTIMATED DELIVERY WINDOW
# =========================================================

silver_orders_df = silver_orders_df.withColumn(
    "estimated_delivery_window_days",

    datediff(
        col("order_estimated_delivery_date"),
        col("order_purchase_timestamp")
    )
)


# =========================================================
# 6. DELIVERY STATUS CATEGORY
# =========================================================

"""
Business-friendly KPI classification
"""

silver_orders_df = silver_orders_df.withColumn(
    "delivery_status_category",

    when(
        col("delay_days") > 0,
        "Late"
    ).when(
        col("delay_days") < 0,
        "Early"
    ).when(
        col("delay_days") == 0,
        "On Time"
    ).otherwise(
        "Unknown"
    )
)


# =========================================================
# 7. SUCCESSFUL DELIVERY FLAG
# =========================================================

silver_orders_df = silver_orders_df.withColumn(
    "is_successfully_delivered",

    when(
        col("order_status") == "delivered",
        1
    ).otherwise(0)
)


# =========================================================
# 8. SILVER METADATA COLUMNS
# =========================================================

"""
Enterprise lineage metadata
"""

silver_orders_df = silver_orders_df.withColumn(
    "silver_loaded_at",
    current_timestamp()
)

silver_orders_df = silver_orders_df.withColumn(
    "source_system",
    lit(SOURCE_SYSTEM)
)

silver_orders_df = silver_orders_df.withColumn(
    "transformation_version",
    lit(TRANSFORMATION_VERSION)
)


# =========================================================
# RUN ORDERS VALIDATION SUITE
# =========================================================

run_orders_validation(
    source_df=bronze_orders_df,
    transformed_df=silver_orders_df
)


# =========================================================
# FINAL DATA PREVIEW
# =========================================================

print("\n=================================================")
print("SILVER ORDERS PREVIEW")
print("=================================================")

silver_orders_df.select(
    "order_id",
    "order_status",
    "delivery_duration_days",
    "delay_days",
    "delivery_status_category",
    "is_successfully_delivered"
).show(10, truncate=False)


# =========================================================
# WRITE SILVER DATASET
# =========================================================

print("\n=================================================")
print("WRITING SILVER ORDERS")
print("=================================================")

silver_orders_df.write \
    .mode("overwrite") \
    .parquet(SILVER_ORDERS_PATH)

print(f"Silver Orders Written To: {SILVER_ORDERS_PATH}")


# =========================================================
# FINAL ROW COUNT
# =========================================================

print("\n=================================================")
print("FINAL ROW COUNT")
print("=================================================")

print(f"Silver Orders Count: {silver_orders_df.count()}")


# =========================================================
# STOP SPARK SESSION
# =========================================================

spark.stop()

print("\n=================================================")
print("SILVER ORDERS TRANSFORMATION COMPLETED")
print("=================================================")
