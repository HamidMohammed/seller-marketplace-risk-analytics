"""
build_fct_order_delivery.py

Objective:
Build Gold Order Delivery Fact Table.

Fact:
fct_order_delivery

Grain:
ONE ROW = ONE CUSTOMER ORDER

Source:
order_delivery_staging

Dimensions:
dim_customer
dim_seller
dim_date
"""

# =====================================================
# IMPORTS
# =====================================================

import sys
import os

from pyspark.sql.window import Window

from pyspark.sql.functions import (
    col,
    current_timestamp,
    row_number,
    when,
    to_date,
    lit
)

# =====================================================
# PROJECT ROOT
# =====================================================

project_root = os.path.abspath(
    os.path.join(
        os.path.dirname(__file__),
        "../../../../"
    )
)

if project_root not in sys.path:
    sys.path.append(project_root)
print(f"Project Root Added: {project_root}")

# =====================================================
# PROJECT IMPORTS
# =====================================================

from pipelines.silver.utils.spark_session import (
    create_spark_session
)

from pipelines.silver.utils.config_loader import (
    load_config
)

from pipelines.gold.facts.order_delivery.fct_order_delivery_validation import (
    run_order_delivery_fact_validation
)

# =====================================================
# SPARK
# =====================================================

spark = create_spark_session(
    "BuildFactOrderDelivery"
)

# =====================================================
# CONFIG
# =====================================================

config = load_config()

ORDER_DELIVERY_STAGING_PATH = (
    config["paths"]["silver"][
        "order_delivery_staging"
    ]
)

DIM_CUSTOMER_PATH = (
    config["paths"]["gold"][
        "dim_customer"
    ]
)

DIM_SELLER_PATH = (
    config["paths"]["gold"][
        "dim_seller"
    ]
)

DIM_DATE_PATH = (
    config["paths"]["gold"][
        "dim_date"
    ]
)

FCT_ORDER_DELIVERY_PATH = (
    config["paths"]["gold"][
        "fct_order_delivery"
    ]
)

SOURCE_SYSTEM = (
    config["metadata"]["source_system"]
)

TRANSFORMATION_VERSION = (
    config["metadata"]["transformation_version"]
)

# =====================================================
# LOAD DATA
# =====================================================

staging_df = spark.read.parquet(
    ORDER_DELIVERY_STAGING_PATH
)

dim_customer_df = spark.read.parquet(
    DIM_CUSTOMER_PATH
)

dim_seller_df = spark.read.parquet(
    DIM_SELLER_PATH
)

dim_date_df = spark.read.parquet(
    DIM_DATE_PATH
)

# =====================================================
# CUSTOMER LOOKUP
# =====================================================

customer_lookup = dim_customer_df.select(
    "customer_id",
    "customer_sk"
)

fact_df = staging_df.join(
    customer_lookup,
    on="customer_id",
    how="left"
)

fact_df = fact_df.withColumnRenamed(
    "customer_sk",
    "customer_sk_fk"
)

# =====================================================
# SELLER LOOKUP
# =====================================================

seller_lookup = (

    dim_seller_df

    .filter(
        col("is_current") == True
    )

    .select(
        "seller_id",
        "seller_sk"
    )
)

fact_df = fact_df.join(

    seller_lookup,

    fact_df["primary_seller_id"] ==
    seller_lookup["seller_id"],

    "left"
)

fact_df = (

    fact_df

    .drop(
        seller_lookup["seller_id"]
    )

    .withColumnRenamed(
        "seller_sk",
        "seller_sk_fk"
    )
)

# =====================================================
# DATE LOOKUPS
# =====================================================

date_lookup = dim_date_df.select(
    "date_sk",
    "full_date"
)

# Purchase Date

fact_df = fact_df.withColumn(
    "purchase_date",
    to_date(
        col("order_purchase_timestamp")
    )
)

fact_df = fact_df.join(

    date_lookup.alias("purchase_date_dim"),

    fact_df["purchase_date"] ==
    col(
        "purchase_date_dim.full_date"
    ),

    "left"
)

fact_df = fact_df.withColumnRenamed(
    "date_sk",
    "purchase_date_sk"
)

# Estimated Delivery Date

fact_df = fact_df.withColumn(
    "estimated_delivery_date",
    to_date(
        col(
            "order_estimated_delivery_date"
        )
    )
)

estimated_lookup = (
    dim_date_df.select(
        col("date_sk").alias(
            "estimated_delivery_date_sk"
        ),
        col("full_date").alias(
            "estimated_delivery_date_key"
        )
    )
)

fact_df = fact_df.join(

    estimated_lookup,

    fact_df["estimated_delivery_date"] ==
    estimated_lookup[
        "estimated_delivery_date_key"
    ],

    "left"
)

# Actual Delivery Date

fact_df = fact_df.withColumn(
    "actual_delivery_date",
    to_date(
        col(
            "order_delivered_customer_date"
        )
    )
)

actual_lookup = (
    dim_date_df.select(
        col("date_sk").alias(
            "actual_delivery_date_sk"
        ),
        col("full_date").alias(
            "actual_delivery_date_key"
        )
    )
)

fact_df = fact_df.join(

    actual_lookup,

    fact_df["actual_delivery_date"] ==
    actual_lookup[
        "actual_delivery_date_key"
    ],

    "left"
)

# =====================================================
# KPI FLAGS
# =====================================================

fact_df = fact_df.withColumn(

    "on_time_delivery_flag",

    when(
        col("delay_days") <= 0,
        True
    ).otherwise(False)
)

fact_df = fact_df.withColumn(

    "late_delivery_flag",

    when(
        col("delay_days") > 0,
        True
    ).otherwise(False)
)

# =====================================================
# FACT SURROGATE KEY
# =====================================================

fact_window = Window.orderBy(
    "order_id"
)

fact_df = fact_df.withColumn(

    "delivery_fact_sk",

    row_number().over(
        fact_window
    )
)

# =====================================================
# AUDIT COLUMNS
# =====================================================

fact_df = fact_df.withColumn(
    "gold_loaded_at",
    current_timestamp()
)

fact_df = fact_df.withColumn(
    "source_system",
    lit(SOURCE_SYSTEM)
)

fact_df = fact_df.withColumn(
    "transformation_version",
    lit(TRANSFORMATION_VERSION)
)

print("=" * 60)
print("FACT SCHEMA BEFORE FINAL SELECT")
print("=" * 60)

fact_df.printSchema()
# =====================================================
# FINAL SELECT
# =====================================================

fact_df = fact_df.select(

    "delivery_fact_sk",

    "order_id",

    "customer_sk_fk",

    "seller_sk_fk",

    "purchase_date_sk",

    "estimated_delivery_date_sk",

    "actual_delivery_date_sk",

    "order_status",

    "order_purchase_timestamp",

    "order_approved_at",

    "order_delivered_carrier_date",

    "order_delivered_customer_date",

    "order_estimated_delivery_date",

    "delivery_duration_days",

    "delay_days",

    "buffer_days",

    "delivery_status_category",

    "freight_total_value",

    "total_items_count",

    "seller_count",

    "is_multi_seller_order",

    "distance_bucket",

    "seller_region",

    "customer_region",

    "on_time_delivery_flag",

    "late_delivery_flag",

    "source_system",

    "transformation_version",

    "gold_loaded_at"
)

# =====================================================
# VALIDATION
# =====================================================

run_order_delivery_fact_validation(
    fact_df
)

# =====================================================
# WRITE
# =====================================================

fact_df.write.mode(
    "overwrite"
).parquet(
    FCT_ORDER_DELIVERY_PATH
)

print(
    f"Final Row Count: "
    f"{fact_df.count()}"
)

spark.stop()

