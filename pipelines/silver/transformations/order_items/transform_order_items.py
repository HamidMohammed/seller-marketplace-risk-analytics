"""
transform_order_items.py

Objective:
Transform Bronze order item fulfillment events into
trusted Silver operational logistics staging.

Pipeline Responsibilities:
- Read Bronze datasets
- Standardize schema
- Cast financial datatypes
- Parse timestamps
- Generate logistics intelligence metrics
- Generate seller accountability metrics
- Run business validations
- Write trusted Silver parquet

Project:
Olist Seller Intelligence Platform

Layer:
Silver

Dataset:
silver_order_items

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
    current_timestamp,
    lit,
    to_timestamp,
    when,
    countDistinct,
    datediff
)

#from pyspark.sql.window import Window

from pyspark.sql.types import DecimalType

from pipelines.silver.utils.config_loader import (
    load_config
)

from pipelines.silver.utils.spark_session import (
    create_spark_session
)

from pipelines.silver.validations.order_items_validation import (
    run_order_items_validation
)


# =========================================================
# CREATE SPARK SESSION
# =========================================================

spark = create_spark_session(
    "TransformSilverOrderItems"
)


# =========================================================
# LOAD CONFIGURATION
# =========================================================

config = load_config()

# ---------------------------------------------------------
# Bronze Paths
# ---------------------------------------------------------

BRONZE_ORDER_ITEMS_PATH = (
    config["paths"]["bronze"]["order_items"]
)

BRONZE_PRODUCTS_PATH = (
    config["paths"]["bronze"]["products"]
)

# ---------------------------------------------------------
# Silver Paths
# ---------------------------------------------------------

SILVER_ORDERS_PATH = (
    config["paths"]["silver"]["orders"]
)

SILVER_ORDER_ITEMS_PATH = (
    config["paths"]["silver"]["order_items"]
)

SILVER_ORDER_ITEMS_QUARANTINE_PATH = (
    config["paths"]["silver"]["order_items_quarantine"]
)
# ---------------------------------------------------------
# Metadata Configuration
# ---------------------------------------------------------

SOURCE_SYSTEM = (
    config["metadata"]["source_system"]
)

TRANSFORMATION_VERSION = (
    config["metadata"]["transformation_version"]
)


# =========================================================
# LOAD SOURCE DATASETS
# =========================================================

print("\n=================================================")
print("LOADING SOURCE DATASETS")
print("=================================================")

order_items_df = spark.read.parquet(
    BRONZE_ORDER_ITEMS_PATH
)

products_df = spark.read.parquet(
    BRONZE_PRODUCTS_PATH
)

orders_df = spark.read.parquet(
    SILVER_ORDERS_PATH
)

clean_orders_df = orders_df.select(
    "order_id"
).distinct()

print(f"Order Items Count: {order_items_df.count()}")
print(f"Products Count: {products_df.count()}")
print(f"Orders Count: {orders_df.count()}")


# =========================================================
# INITIAL DATA INSPECTION
# =========================================================

print("\n=================================================")
print("BRONZE ORDER ITEMS SCHEMA")
print("=================================================")

order_items_df.printSchema()


# =========================================================
# SELECT REQUIRED PRODUCT COLUMNS
# =========================================================

"""
Controlled enrichment strategy.

Avoid full unnecessary joins.
Only required logistics fields are selected.
"""

products_selected_df = products_df.select(
    "product_id",
    "product_weight_g",
    "product_length_cm",
    "product_height_cm",
    "product_width_cm"
)


# =========================================================
# SELECT REQUIRED ORDER COLUMNS
# =========================================================

orders_selected_df = orders_df.select(
    "order_id",
    "order_purchase_timestamp"
)


# =========================================================
# START TRANSFORMATIONS
# =========================================================

print("\n=================================================")
print("STARTING SILVER TRANSFORMATIONS")
print("=================================================")

# ---------------------------------------------------------
# Base Dataset
# ---------------------------------------------------------

# silver_order_items_df = order_items_df

silver_order_items_df = (

    order_items_df

    .join(
        clean_orders_df,
        on="order_id",
        how="inner"
    )
)

# =========================================================
# CASCADE QUARANTINE
# =========================================================

orphan_order_items_df = (

    order_items_df

    .join(
        clean_orders_df,
        on="order_id",
        how="left_anti"
    )

    .withColumn(
        "quarantine_reason",
        lit("ORPHAN_ORDER_ITEM")
    )
)

print(
    f"Orphan Order Items: "
    f"{orphan_order_items_df.count()}"
)

# =========================================================
# PRODUCT ENRICHMENT
# =========================================================

print("\nApplying product enrichment...")

silver_order_items_df = (

    silver_order_items_df.alias("oi")

    .join(
        products_selected_df.alias("p"),
        on="product_id",
        how="left"
    )

)


# =========================================================
# ORDER ENRICHMENT
# =========================================================

print("\nApplying order enrichment...")

silver_order_items_df = (

    silver_order_items_df.alias("oi")

    .join(
        orders_selected_df.alias("o"),
        on="order_id",
        how="left"
    )

)


# =========================================================
# FINANCIAL STANDARDIZATION
# =========================================================

"""
Purpose:
- KPI-safe aggregations
- consistent financial precision
- reliable freight analytics
"""

print("\nApplying financial standardization...")

silver_order_items_df = (

    silver_order_items_df

    .withColumn(
        "price",
        col("price").cast(DecimalType(12, 2))
    )

    .withColumn(
        "freight_value",
        col("freight_value").cast(DecimalType(12, 2))
    )

)


# =========================================================
# TIMESTAMP STANDARDIZATION
# =========================================================

"""
Purpose:
- lifecycle analytics
- fulfillment deadline analysis
- chronological validation
"""

print("\nApplying timestamp standardization...")

silver_order_items_df = (

    silver_order_items_df

    .withColumn(
        "shipping_limit_date",
        to_timestamp(col("shipping_limit_date"))
    )

)


# =========================================================
# PRODUCT VOLUME METRIC
# =========================================================

"""
Physical shipment volume.

Used for:
- logistics intelligence
- freight investigation
- oversized-product analysis
"""

print("\nCalculating product volume metric...")

silver_order_items_df = (

    silver_order_items_df

    .withColumn(

        "product_volume_cm3",

        (
            col("product_length_cm")
            *
            col("product_height_cm")
            *
            col("product_width_cm")
        ).cast(DecimalType(18, 2))

    )

)


# =========================================================
# FREIGHT RATIO METRIC
# =========================================================

"""
Measures shipping burden relative to product value.
"""

print("\nCalculating freight ratio metric...")

silver_order_items_df = (

    silver_order_items_df

    .withColumn(

        "freight_ratio",

        when(
            col("price") > 0,

            (
                col("freight_value")
                / col("price")
            ).cast(DecimalType(10, 4))

        ).otherwise(None)

    )

)


# =========================================================
# SELLER ACCOUNTABILITY METRICS
# =========================================================

"""
Critical for:
- multi-seller order analysis
- review attribution
- delivery accountability
"""


print("\nCalculating seller accountability metrics...")


# ---------------------------------------------------------
# Aggregate Seller Counts Per Order
# ---------------------------------------------------------

seller_count_df = (

    silver_order_items_df

    .groupBy("order_id")

    .agg(
        countDistinct("seller_id").alias("seller_count")
    )

)


# ---------------------------------------------------------
# Join Seller Counts Back
# ---------------------------------------------------------

silver_order_items_df = (

    silver_order_items_df

    .join(
        seller_count_df,
        on="order_id",
        how="left"
    )

)


# ---------------------------------------------------------
# Multi-Seller Flag
# ---------------------------------------------------------

silver_order_items_df = (

    silver_order_items_df

    .withColumn(

        "is_multi_seller_order",

        when(
            col("seller_count") > 1,
            True
        ).otherwise(False)

    )

)

# seller_preparation_days = days from purchase to shipping_limit_date
silver_order_items_df = silver_order_items_df.withColumn(
    "seller_preparation_days",
    datediff(
        col("shipping_limit_date"),
        col("order_purchase_timestamp")
    )
)

# shipping_pressure_flag = seller had 2 days or less
silver_order_items_df = silver_order_items_df.withColumn(
    "shipping_pressure_flag",
    when(col("seller_preparation_days") <= 2, True).otherwise(False)
)

# =========================================================
# METADATA ENRICHMENT
# =========================================================

"""
Enterprise lineage metadata.
"""

print("\nApplying metadata enrichment...")

silver_order_items_df = (

    silver_order_items_df

    .withColumn(
        "silver_loaded_at",
        current_timestamp()
    )

    .withColumn(
        "source_system",
        lit(SOURCE_SYSTEM)
    )

    .withColumn(
        "transformation_version",
        lit(TRANSFORMATION_VERSION)
    )

)


# =========================================================
# RUN VALIDATION SUITE
# =========================================================

run_order_items_validation(
    source_df=order_items_df,
    transformed_df=silver_order_items_df,
    quarantine_df=orphan_order_items_df
)


# =========================================================
# FINAL DATA PREVIEW
# =========================================================

print("\n=================================================")
print("SILVER ORDER ITEMS PREVIEW")
print("=================================================")

silver_order_items_df.select(
    "order_id",
    "order_item_id",
    "seller_id",
    "price",
    "freight_value",
    "freight_ratio",
    "seller_count",
    "seller_preparation_days",
    "shipping_pressure_flag",
    "is_multi_seller_order"
).show(10, truncate=False)


# =========================================================
# WRITE SILVER DATASET
# =========================================================

print("\n=================================================")
print("WRITING SILVER ORDER ITEMS")
print("=================================================")
orphan_order_items_df.write \
    .mode("overwrite") \
    .parquet(
        SILVER_ORDER_ITEMS_QUARANTINE_PATH
    )
print(
    f"QUARANTINE Order Items Written To: "
    f"{SILVER_ORDER_ITEMS_QUARANTINE_PATH}"
)

silver_order_items_df.write \
    .mode("overwrite") \
    .parquet(SILVER_ORDER_ITEMS_PATH)

print(
    f"Silver Order Items Written To: "
    f"{SILVER_ORDER_ITEMS_PATH}"
)


# =========================================================
# FINAL ROW COUNT
# =========================================================

print("\n=================================================")
print("FINAL ROW COUNT")
print("=================================================")

print(
    f"Silver Order Items Count: "
    f"{silver_order_items_df.count()}"
)


# =========================================================
# STOP SPARK SESSION
# =========================================================

spark.stop()

print("\n=================================================")
print("SILVER ORDER ITEMS TRANSFORMATION COMPLETED")
print("=================================================")
