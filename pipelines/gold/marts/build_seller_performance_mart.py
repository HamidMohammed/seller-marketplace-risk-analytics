"""
build_seller_performance_mart.py

Objective:
Build the Seller Performance Mart by combining
historical seller KPIs with seller dimension
intelligence and deriving:

- Seller Score
- Seller Risk Level
- Seller Rank Tier

Project:
Olist Seller Intelligence Platform

Layer:
Gold Mart

Dataset:
seller_performance_mart

Grain:
ONE ROW = SELLER + MONTH
"""

# =========================================================
# PROJECT ROOT SETUP
# =========================================================

import sys
import os

project_root = os.path.abspath(
    os.path.join(
        os.path.dirname(__file__),
        "../../../"
    )
)

if project_root not in sys.path:
    sys.path.append(project_root)


# =========================================================
# IMPORTS
# =========================================================

from pyspark.sql.functions import (
    col,
    when,
    round,
    current_timestamp,
    lit
)

from pipelines.gold.utils.config_loader import (
    load_config
)

from pipelines.silver.utils.spark_session import (
    create_spark_session
)


# =========================================================
# CREATE SPARK SESSION
# =========================================================

spark = create_spark_session(
    "BuildSellerPerformanceMart"
)


# =========================================================
# LOAD CONFIG
# =========================================================

config = load_config()

SELLER_PERFORMANCE_STAGING_PATH = (
    config["paths"]["silver"][
        "seller_performance_monthly_staging"
    ]
)

DIM_SELLER_PATH = (
    config["paths"]["gold"][
        "dim_seller"
    ]
)

SELLER_PERFORMANCE_MART_PATH = (
    config["paths"]["gold"][
        "seller_performance_mart"
    ]
)

SOURCE_SYSTEM = (
    config["metadata"]["source_system"]
)

TRANSFORMATION_VERSION = (
    config["metadata"][
        "transformation_version"
    ]
)


# =========================================================
# LOAD DATA
# =========================================================

print("\nLoading Seller Performance Staging")

performance_df = spark.read.parquet(
    SELLER_PERFORMANCE_STAGING_PATH
)

print("\nLoading Seller Dimension")

dim_seller_df = spark.read.parquet(
    DIM_SELLER_PATH
)


# =========================================================
# SELLER LOOKUP
# =========================================================

seller_lookup_df = dim_seller_df.select(

    "seller_sk",

    "seller_id"
)

performance_df = performance_df.join(

    seller_lookup_df,

    on="seller_id",

    how="left"
)

performance_df = performance_df.withColumnRenamed(

    "seller_sk",

    "seller_sk_fk"
)


# =========================================================
# REVIEW COMPONENT
# =========================================================

performance_df = performance_df.withColumn(

    "review_component",

    (
        col("avg_review_score") / 5
    ) * 100
)


# =========================================================
# GROWTH COMPONENT
# =========================================================

performance_df = performance_df.withColumn(

    "growth_component",

    when(
        col("volume_growth_rate") >= 20,
        100

    ).when(
        col("volume_growth_rate") >= 0,
        80

    ).when(
        col("volume_growth_rate") >= -20,
        50

    ).otherwise(20)
)


# =========================================================
# WORKLOAD COMPONENT
# =========================================================

performance_df = performance_df.withColumn(

    "workload_component",

    when(
        col("avg_monthly_workload") <= 20,
        100

    ).when(
        col("avg_monthly_workload") <= 50,
        80

    ).otherwise(60)
)


# =========================================================
# SELLER SCORE
# =========================================================

performance_df = performance_df.withColumn(

    "seller_score",

    round(

        (
            col("on_time_rate") * 0.40
        ) +

        (
            col("review_component") * 0.30
        ) +

        (
            col("growth_component") * 0.20
        ) +

        (
            col("workload_component") * 0.10
        ),

        2
    )
)


# =========================================================
# SELLER RISK LEVEL
# =========================================================

performance_df = performance_df.withColumn(

    "seller_risk_level",

    when(
        col("seller_score") >= 85,
        "Healthy"

    ).when(
        col("seller_score") >= 70,
        "Warning"

    ).when(
        col("seller_score") >= 50,
        "At Risk"

    ).otherwise(
        "Critical"
    )
)


# =========================================================
# SELLER RANK TIER
# =========================================================

performance_df = performance_df.withColumn(

    "seller_rank_tier",

    when(
        col("seller_score") >= 90,
        "Elite Seller"

    ).when(
        col("seller_score") >= 80,
        "Top Seller"

    ).when(
        col("seller_score") >= 65,
        "Standard Seller"

    ).otherwise(
        "Underperforming Seller"
    )
)


# =========================================================
# METADATA
# =========================================================

performance_df = performance_df.withColumn(

    "gold_loaded_at",

    current_timestamp()
)

performance_df = performance_df.withColumn(

    "source_system",

    lit(SOURCE_SYSTEM)
)

performance_df = performance_df.withColumn(

    "transformation_version",

    lit(
        TRANSFORMATION_VERSION
    )
)


# =========================================================
# FINAL SELECT
# =========================================================

performance_df = performance_df.select(

    "seller_sk_fk",

    "seller_id",

    "performance_year",

    "performance_month",

    "monthly_orders",

    "avg_shipping_days",

    "on_time_rate",

    "avg_delay_days",

    "delayed_orders_count",

    "avg_review_score",

    "negative_review_rate",

    "monthly_review_count",

    "avg_monthly_workload",

    "avg_freight_ratio",

    "avg_product_volume_cm3",

    "previous_month_orders",

    "is_new_seller_month",

    "volume_growth_rate",

    "seller_growth_category",

    "seller_performance_category",

    "seller_score",

    "seller_risk_level",

    "seller_rank_tier",

    "gold_loaded_at",

    "source_system",

    "transformation_version"
)


# =========================================================
# WRITE MART
# =========================================================

performance_df.write.mode(
    "overwrite"
).parquet(
    SELLER_PERFORMANCE_MART_PATH
)


print(
    "\nSeller Performance Mart Written Successfully"
)

print(
    f"Rows: {performance_df.count()}"
)

performance_df.printSchema()

spark.stop()
