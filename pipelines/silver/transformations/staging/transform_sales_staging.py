"""
transform_sales_staging.py

Objective:
Assemble payment-aware sales intelligence staging dataset
by reconciling:
- order item sales
- payment transactions
- seller attribution
- proportional payment allocation

This staging dataset becomes the direct analytical input for:
fct_order_sales

Project:
Olist Seller Intelligence Platform

Layer:
Silver Staging

Dataset:
sales_staging

Dataset Grain:
ONE ROW = ONE ORDER ITEM SALES EVENT
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
    sum,
    when,
    current_timestamp,
    count,
    lit,
    max
)

from pyspark.sql.window import Window

from pipelines.silver.utils.config_loader import (
    load_config
)

from pipelines.silver.utils.spark_session import (
    create_spark_session
)

from pipelines.silver.validations.sales_staging_validation import (
    run_sales_staging_validation
)


# =========================================================
# CREATE SPARK SESSION
# =========================================================

spark = create_spark_session(
    "TransformSalesStaging"
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

SILVER_PAYMENTS_PATH = (
    config["paths"]["silver"]["payments"]
)

# ---------------------------------------------------------
# Output Path
# ---------------------------------------------------------

SALES_STAGING_PATH = (
    config["paths"]["silver"]["sales_staging"]
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
print("LOADING SOURCE DATASETS")
print("=================================================")

order_items_df = spark.read.parquet(
    SILVER_ORDER_ITEMS_PATH
)

payments_df = spark.read.parquet(
    SILVER_PAYMENTS_PATH
)

print(f"Order Items Count: {order_items_df.count()}")
print(f"Payments Count: {payments_df.count()}")


# =========================================================
# AGGREGATE PAYMENTS TO ORDER LEVEL
# =========================================================

print("\n=================================================")
print("AGGREGATING PAYMENTS")
print("=================================================")

payments_agg_df = payments_df.groupBy(
    "order_id"
).agg(

    sum("payment_value").alias(
        "total_payment_value"
    ),

    max("payment_installments").alias(
        "total_payment_installments"
    )
)

print(
    f"Aggregated Payment Orders: "
    f"{payments_agg_df.count()}"
)


# =========================================================
# CALCULATE ORDER TOTAL VALUE
# =========================================================

print("\n=================================================")
print("CALCULATING ORDER TOTALS")
print("=================================================")

order_totals_df = order_items_df.groupBy(
    "order_id"
).agg(

    sum(
        col("price") + col("freight_value")
    ).alias(
        "total_order_item_value"
    )
)


# =========================================================
# JOIN ORDER TOTALS
# =========================================================

staging_df = order_items_df.join(

    order_totals_df,

    on="order_id",

    how="left"
)


# =========================================================
# ITEM SALES RATIO
# =========================================================

staging_df = staging_df.withColumn(

    "gross_item_value",

    col("price") + col("freight_value")
)

staging_df = staging_df.withColumn(

    "item_sales_ratio",

    when(
        col("total_order_item_value") > 0,

        col("gross_item_value") /
        col("total_order_item_value")

    ).otherwise(0)
)


# =========================================================
# JOIN PAYMENTS
# =========================================================

print("\n=================================================")
print("JOINING PAYMENT INTELLIGENCE")
print("=================================================")

staging_df = staging_df.join(

    payments_agg_df,

    on="order_id",

    how="left"
)


# =========================================================
# PAYMENT ALLOCATION
# =========================================================

print("\n=================================================")
print("ALLOCATING PAYMENTS")
print("=================================================")

staging_df = staging_df.withColumn(

    "allocated_payment_value",

    col("total_payment_value") *
    col("item_sales_ratio")
)


# =========================================================
# INSTALLMENT FLAG
# =========================================================

staging_df = staging_df.withColumn(

    "installment_flag",

    when(
        col("total_payment_installments") > 1,
        True
    ).otherwise(False)
)


# =========================================================
# HIGH TICKET FLAG
# =========================================================

staging_df = staging_df.withColumn(

    "high_ticket_order_flag",

    when(
        col("gross_item_value") >= 1000,
        True
    ).otherwise(False)
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

    "shipping_limit_date",

    "price",

    "freight_value",

    "gross_item_value",

    "total_order_item_value",

    "item_sales_ratio",

    "total_payment_value",

    "allocated_payment_value",

    "total_payment_installments",

    "installment_flag",

    "high_ticket_order_flag",

    "freight_ratio",

    "product_volume_cm3",

    "seller_item_count_in_order",

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

run_sales_staging_validation(
    staging_df
)


# =========================================================
# WRITE STAGING DATASET
# =========================================================

print("\n=================================================")
print("WRITING SALES STAGING")
print("=================================================")

staging_df.write.mode("overwrite").parquet(
    SALES_STAGING_PATH
)

print("Sales Staging Written Successfully")


# =========================================================
# FINAL SUMMARY
# =========================================================

print("\n=================================================")
print("SALES STAGING PIPELINE COMPLETED")
print("=================================================")

print(f"Final Row Count: {staging_df.count()}")

staging_df.printSchema()

spark.stop()