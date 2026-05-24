"""
transform_order_delivery_staging.py

Objective:
Assemble the order-level delivery staging dataset
by joining silver_orders with aggregated order_items.

This is the direct input to fct_order_delivery.

Project:
Olist Seller Intelligence Platform

Layer:
Silver Staging

Dataset:
order_delivery_staging

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

from pyspark.sql.functions import (
    col,
    sum,
    count,
    countDistinct,
    first,
    when,
    datediff,
    current_timestamp,
    lit
)

from pipelines.silver.utils.config_loader import (
    load_config
)

from pipelines.silver.utils.spark_session import (
    create_spark_session
)

from pipelines.silver.validations.order_delivery_staging_validation import (
    run_order_delivery_staging_validation
)


# =========================================================
# CREATE SPARK SESSION
# =========================================================

spark = create_spark_session(
    "TransformOrderDeliveryStaging"
)


# =========================================================
# LOAD CONFIGURATION
# =========================================================

config = load_config()

# ---------------------------------------------------------
# Silver Paths
# ---------------------------------------------------------

SILVER_ORDERS_PATH = (
    config["paths"]["silver"]["orders"]
)

SILVER_ORDER_ITEMS_PATH = (
    config["paths"]["silver"]["order_items"]
)

SILVER_SELLERS_PATH = (
    config["paths"]["silver"]["sellers"]
)

SILVER_CUSTOMERS_PATH = (
    config["paths"]["silver"]["customers"]
)

# ---------------------------------------------------------
# Staging Output Path
# ---------------------------------------------------------

ORDER_DELIVERY_STAGING_PATH = (
    config["paths"]["silver"]["order_delivery_staging"]
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

orders_df = spark.read.parquet(
    SILVER_ORDERS_PATH
)

order_items_df = spark.read.parquet(
    SILVER_ORDER_ITEMS_PATH
)

sellers_df = spark.read.parquet(
    SILVER_SELLERS_PATH
)

customers_df = spark.read.parquet(
    SILVER_CUSTOMERS_PATH
)

print(f"Orders Count: {orders_df.count()}")
print(f"Order Items Count: {order_items_df.count()}")
print(f"Sellers Count: {sellers_df.count()}")
print(f"Customers Count: {customers_df.count()}")


# =========================================================
# AGGREGATE ORDER ITEMS TO ORDER LEVEL
# =========================================================

print("\n=================================================")
print("AGGREGATING ORDER ITEMS")
print("=================================================")

order_items_agg = order_items_df.groupBy(
    "order_id"
).agg(

    sum("freight_value").alias(
        "freight_total_value"
    ),

    count("order_item_id").alias(
        "total_items_count"
    ),

    countDistinct("seller_id").alias(
        "seller_count"
    ),

    first("seller_id").alias(
        "primary_seller_id"
    )

)

# ---------------------------------------------------------
# MULTI SELLER FLAG
# ---------------------------------------------------------

order_items_agg = order_items_agg.withColumn(
    "is_multi_seller_order",
    when(
        col("seller_count") > 1,
        True
    ).otherwise(False)
)

print(f"Aggregated Orders Count: {order_items_agg.count()}")


# =========================================================
# JOIN ORDERS + AGGREGATED ITEMS
# =========================================================

print("\n=================================================")
print("JOINING ORDER LIFECYCLE + FULFILLMENT")
print("=================================================")

staging_df = orders_df.join(
    order_items_agg,
    on="order_id",
    how="left"
)


# =========================================================
# LOAD SELLER GEOGRAPHY
# =========================================================

sellers_geo_df = sellers_df.select(
    col("seller_id"),
    col("seller_state"),
    col("median_latitude").alias("seller_lat"),
    col("median_longitude").alias("seller_lng")
)


# =========================================================
# LOAD CUSTOMER GEOGRAPHY
# =========================================================

customers_geo_df = customers_df.select(
    col("customer_id"),
    col("customer_state"),
    col("median_latitude").alias("customer_lat"),
    col("median_longitude").alias("customer_lng")
)


# =========================================================
# JOIN SELLER GEOGRAPHY
# =========================================================

staging_df = staging_df.join(
    sellers_geo_df,
    staging_df["primary_seller_id"] == sellers_geo_df["seller_id"],
    how="left"
).drop(sellers_geo_df["seller_id"])


# =========================================================
# JOIN CUSTOMER GEOGRAPHY
# =========================================================

staging_df = staging_df.join(
    customers_geo_df,
    on="customer_id",
    how="left"
)


# =========================================================
# BRAZILIAN MACRO-REGION MAPPING
# =========================================================

print("\n=================================================")
print("DERIVING BRAZILIAN MACRO-REGIONS")
print("=================================================")

# ---------------------------------------------------------
# Macro Region Definitions
# ---------------------------------------------------------

southeast = ["SP", "RJ", "MG", "ES"]

south = ["PR", "SC", "RS"]

northeast = [
    "BA", "SE", "AL", "PE",
    "PB", "RN", "CE", "PI", "MA"
]

north = [
    "PA", "AM", "AC", "RO",
    "RR", "AP", "TO"
]

central_west = [
    "GO", "MT", "MS", "DF"
]


# =========================================================
# SELLER REGION DERIVATION
# =========================================================

staging_df = staging_df.withColumn(

    "seller_region",

    when(
        col("seller_state").isin(southeast),
        "Southeast"

    ).when(
        col("seller_state").isin(south),
        "South"

    ).when(
        col("seller_state").isin(northeast),
        "Northeast"

    ).when(
        col("seller_state").isin(north),
        "North"

    ).when(
        col("seller_state").isin(central_west),
        "Central-West"

    ).otherwise("Unknown")
)


# =========================================================
# CUSTOMER REGION DERIVATION
# =========================================================

staging_df = staging_df.withColumn(

    "customer_region",

    when(
        col("customer_state").isin(southeast),
        "Southeast"

    ).when(
        col("customer_state").isin(south),
        "South"

    ).when(
        col("customer_state").isin(northeast),
        "Northeast"

    ).when(
        col("customer_state").isin(north),
        "North"

    ).when(
        col("customer_state").isin(central_west),
        "Central-West"

    ).otherwise("Unknown")
)


# =========================================================
# DISTANCE BUCKET DERIVATION
# =========================================================

print("\n=================================================")
print("DERIVING DISTANCE BUCKETS")
print("=================================================")

staging_df = staging_df.withColumn(

    "distance_bucket",

    when(
        col("seller_state").isNull() |
        col("customer_state").isNull(),
        "Unknown"

    ).when(
        col("seller_state") ==
        col("customer_state"),
        "Same State"

    ).when(
        col("seller_region") ==
        col("customer_region"),
        "Same Region"

    ).otherwise(
        "Cross Region"
    )
)


# =========================================================
# BUFFER DAYS METRIC
# =========================================================

staging_df = staging_df.withColumn(
    "buffer_days",

    datediff(
        col("order_estimated_delivery_date"),
        col("order_purchase_timestamp")
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


# =========================================================
# FINAL COLUMN SELECTION
# =========================================================

print("\n=================================================")
print("FINAL COLUMN SELECTION")
print("=================================================")

staging_df = staging_df.select(

    "order_id",
    "customer_id",
    "primary_seller_id",

    "order_status",

    "order_purchase_timestamp",
    "order_approved_at",
    "order_delivered_carrier_date",
    "order_delivered_customer_date",
    "order_estimated_delivery_date",

    "delivery_duration_days",
    "delay_days",
    "delivery_status_category",

    "buffer_days",

    "freight_total_value",
    "total_items_count",

    "seller_count",
    "is_multi_seller_order",

    "distance_bucket",

    "seller_state",
    "customer_state",

    # NEW REGION COLUMNS
    "seller_region",
    "customer_region",

    "seller_lat",
    "seller_lng",

    "customer_lat",
    "customer_lng",

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

run_order_delivery_staging_validation(
    staging_df
)


# =========================================================
# WRITE STAGING DATASET
# =========================================================

print("\n=================================================")
print("WRITING ORDER DELIVERY STAGING")
print("=================================================")

staging_df.write.mode("overwrite").parquet(
    ORDER_DELIVERY_STAGING_PATH
)

print("Order Delivery Staging Written Successfully")


# =========================================================
# FINAL SUMMARY
# =========================================================

print("\n=================================================")
print("ORDER DELIVERY STAGING PIPELINE COMPLETED")
print("=================================================")

print(f"Final Row Count: {staging_df.count()}")

staging_df.printSchema()

spark.stop()