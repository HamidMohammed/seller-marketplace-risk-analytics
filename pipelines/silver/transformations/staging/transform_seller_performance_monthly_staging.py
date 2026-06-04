"""
transform_seller_performance_monthly_staging.py

Objective:
Build monthly seller behavioral performance intelligence
by aggregating:
- delivery performance
- customer satisfaction
- workload behavior

This staging dataset becomes the direct analytical input for:
fct_seller_performance

Project:
Olist Seller Intelligence Platform

Layer:
Silver Staging

Dataset:
seller_performance_monthly_staging

Dataset Grain:
ONE ROW = ONE SELLER PER MONTH
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
    avg,
    sum,
    count,
    when,
    year,
    month,
    lag,
    round,
    current_timestamp,
    lit
)

from pyspark.sql.window import Window

from pipelines.silver.utils.config_loader import (
    load_config,
    resolve_path
)

from pipelines.silver.utils.spark_session import (
    create_spark_session
)

from pipelines.silver.validations.seller_performance_monthly_staging_validation import (
    run_seller_performance_monthly_staging_validation
)


# =========================================================
# CREATE SPARK SESSION
# =========================================================

spark = create_spark_session(
    "TransformSellerPerformanceMonthlyStaging"
)


# =========================================================
# LOAD CONFIGURATION
# =========================================================

config = load_config()

# ---------------------------------------------------------
# Input Paths
# ---------------------------------------------------------

ORDER_DELIVERY_STAGING_PATH = resolve_path(
    config["paths"]["silver"][
        "order_delivery_staging"
    ],
    config
)

REVIEWS_STAGING_PATH = resolve_path(
    config["paths"]["silver"][
        "reviews_staging"
    ],
    config
)

SELLER_FULFILLMENT_STAGING_PATH =  resolve_path(
    config["paths"]["silver"][
        "seller_fulfillment_staging"
    ],
    config
)

# ---------------------------------------------------------
# Output Path
# ---------------------------------------------------------

SELLER_PERFORMANCE_MONTHLY_STAGING_PATH = resolve_path(
    config["paths"]["silver"][
        "seller_performance_monthly_staging"
    ],
    config
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
print("LOADING STAGING DATASETS")
print("=================================================")

delivery_df = spark.read.parquet(
    ORDER_DELIVERY_STAGING_PATH
)

reviews_df = spark.read.parquet(
    REVIEWS_STAGING_PATH
)

fulfillment_df = spark.read.parquet(
    SELLER_FULFILLMENT_STAGING_PATH
)

print(f"Delivery Rows: {delivery_df.count()}")
print(f"Reviews Rows: {reviews_df.count()}")
print(f"Fulfillment Rows: {fulfillment_df.count()}")


# =========================================================
# FILTER SINGLE-SELLER ACCOUNTABILITY
# =========================================================

"""
IMPORTANT BUSINESS RULE:

This staging dataset models:
SELLER ACCOUNTABILITY PERFORMANCE

Multi-seller orders are excluded because:
customer-level delivery outcomes cannot be
reliably attributed to one seller operationally.

This preserves:
- KPI accountability clarity
- non-duplicated seller metrics
- trusted seller performance scoring
"""

delivery_df = delivery_df.filter(
    col("is_multi_seller_order") == False
)

reviews_df = reviews_df.filter(
    col("is_multi_seller_order") == False
)


# =========================================================
# DELIVERY PERFORMANCE AGGREGATION
# =========================================================

print("\n=================================================")
print("AGGREGATING DELIVERY PERFORMANCE")
print("=================================================")

delivery_monthly_df = delivery_df.withColumn(
    "performance_year",
    year("order_purchase_timestamp")
).withColumn(
    "performance_month",
    month("order_purchase_timestamp")
)

delivery_monthly_df = delivery_monthly_df.groupBy(

    "primary_seller_id",

    "performance_year",

    "performance_month"

).agg(

    count("order_id").alias(
        "monthly_orders"
    ),

    avg("delivery_duration_days").alias(
        "avg_shipping_days"
    ),

    avg(
        when(
            col("delay_days") <= 0,
            1
        ).otherwise(0)
    ).alias(
        "on_time_rate"
    ),

    avg("delay_days").alias(
        "avg_delay_days"
    ),

    sum(
        when(
            col("delay_days") > 0,
            1
        ).otherwise(0)
    ).alias(
        "delayed_orders_count"
    )
)


# =========================================================
# REVIEW PERFORMANCE AGGREGATION
# =========================================================

print("\n=================================================")
print("AGGREGATING REVIEW PERFORMANCE")
print("=================================================")

reviews_monthly_df = reviews_df.withColumn(
    "performance_year",
    year("review_creation_date")
).withColumn(
    "performance_month",
    month("review_creation_date")
)

reviews_monthly_df = reviews_monthly_df.groupBy(

    "primary_seller_id",

    "performance_year",

    "performance_month"

).agg(

    avg("review_score").alias(
        "avg_review_score"
    ),

    avg(
        when(
            col("negative_review_flag") == True,
            1
        ).otherwise(0)
    ).alias(
        "negative_review_rate"
    ),

    count("review_id").alias(
        "monthly_review_count"
    )
)


# =========================================================
# WORKLOAD PERFORMANCE AGGREGATION
# =========================================================

print("\n=================================================")
print("AGGREGATING WORKLOAD PERFORMANCE")
print("=================================================")

workload_monthly_df = fulfillment_df.withColumn(
    "performance_year",
    year("order_purchase_timestamp")
).withColumn(
    "performance_month",
    month("order_purchase_timestamp")
)

workload_monthly_df = workload_monthly_df.groupBy(

    "seller_id",

    "performance_year",

    "performance_month"

).agg(

    avg("seller_monthly_orders").alias(
        "avg_monthly_workload"
    ),

    avg("freight_ratio").alias(
        "avg_freight_ratio"
    ),

    avg("product_volume_cm3").alias(
        "avg_product_volume_cm3"
    )
)


# =========================================================
# JOIN PERFORMANCE DOMAINS
# =========================================================

print("\n=================================================")
print("JOINING PERFORMANCE DOMAINS")
print("=================================================")

staging_df = delivery_monthly_df.join(

    reviews_monthly_df,

    on=[
        delivery_monthly_df[
            "primary_seller_id"
        ] ==
        reviews_monthly_df[
            "primary_seller_id"
        ],

        delivery_monthly_df[
            "performance_year"
        ] ==
        reviews_monthly_df[
            "performance_year"
        ],

        delivery_monthly_df[
            "performance_month"
        ] ==
        reviews_monthly_df[
            "performance_month"
        ]
    ],

    how="left"
)

staging_df = staging_df.join(

    workload_monthly_df,

    on=[
        delivery_monthly_df[
            "primary_seller_id"
        ] ==
        workload_monthly_df[
            "seller_id"
        ],

        delivery_monthly_df[
            "performance_year"
        ] ==
        workload_monthly_df[
            "performance_year"
        ],

        delivery_monthly_df[
            "performance_month"
        ] ==
        workload_monthly_df[
            "performance_month"
        ]
    ],

    how="left"
)


# =========================================================
# CLEAN DUPLICATE JOIN COLUMNS
# =========================================================

staging_df = staging_df.select(

    delivery_monthly_df[
        "primary_seller_id"
    ].alias("seller_id"),

    delivery_monthly_df[
        "performance_year"
    ],

    delivery_monthly_df[
        "performance_month"
    ],

    "monthly_orders",

    round(
        col("avg_shipping_days"),
        2
    ).alias("avg_shipping_days"),

    round(
        col("on_time_rate"),
        4
    ).alias("on_time_rate"),

    round(
        col("avg_delay_days"),
        2
    ).alias("avg_delay_days"),

    "delayed_orders_count",

    round(
        col("avg_review_score"),
        2
    ).alias("avg_review_score"),

    round(
        col("negative_review_rate"),
        4
    ).alias("negative_review_rate"),

    "monthly_review_count",

    round(
        col("avg_monthly_workload"),
        2
    ).alias("avg_monthly_workload"),

    round(
        col("avg_freight_ratio"),
        4
    ).alias("avg_freight_ratio"),

    round(
        col("avg_product_volume_cm3"),
        2
    ).alias("avg_product_volume_cm3")
)


# =========================================================
# TEMPORAL PERFORMANCE METRICS
# =========================================================

print("\n=================================================")
print("DERIVING TEMPORAL PERFORMANCE METRICS")
print("=================================================")

growth_window = Window.partitionBy(
    "seller_id"
).orderBy(
    "performance_year",
    "performance_month"
)

# ---------------------------------------------------------
# Previous Month Orders
# ---------------------------------------------------------

staging_df = staging_df.withColumn(

    "previous_month_orders",

    lag("monthly_orders").over(
        growth_window
    )
)

# ---------------------------------------------------------
# New Seller Lifecycle Flag
# ---------------------------------------------------------

staging_df = staging_df.withColumn(

    "is_new_seller_month",

    when(
        col("previous_month_orders").isNull(),
        True
    ).otherwise(False)
)

# ---------------------------------------------------------
# Volume Growth Rate
# ---------------------------------------------------------

staging_df = staging_df.withColumn(

    "volume_growth_rate",

    when(
        col("is_new_seller_month") == True,
        None

    ).when(
        col("previous_month_orders") > 0,

        (
            col("monthly_orders")
            - col("previous_month_orders")
        ) / col("previous_month_orders")
    )
)

# ---------------------------------------------------------
# Seller Growth Category
# ---------------------------------------------------------

staging_df = staging_df.withColumn(

    "seller_growth_category",

    when(
        col("is_new_seller_month") == True,

        "New Seller"

    ).when(
        col("volume_growth_rate") >= 0.50,

        "High Growth"

    ).when(
        col("volume_growth_rate") > 0,

        "Moderate Growth"

    ).when(
        col("volume_growth_rate") < 0,

        "Declining"

    ).otherwise(
        "Stable"
    )
)


# =========================================================
# PERFORMANCE RISK CATEGORY
# =========================================================

staging_df = staging_df.withColumn(

    "seller_performance_category",

    when(
        col("is_new_seller_month") == True,

        "New Seller"

    ).when(
        (
            col("on_time_rate") >= 0.95
        ) &
        (
            col("avg_review_score") >= 4.5
        ),

        "Top Performer"

    ).when(
        (
            col("monthly_orders") >= 5
        ) &
        (
            (
                col("on_time_rate") < 0.80
            ) |
            (
                col("negative_review_rate") > 0.30
            )
        ),

        "At Risk"

    ).otherwise(
        "Stable"
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

run_seller_performance_monthly_staging_validation(
    staging_df
)


# =========================================================
# WRITE DATASET
# =========================================================

print("\n=================================================")
print("WRITING SELLER PERFORMANCE MONTHLY STAGING")
print("=================================================")

staging_df.write.mode("overwrite").parquet(
    SELLER_PERFORMANCE_MONTHLY_STAGING_PATH
)

print(
    "Seller Performance Monthly Staging "
    "Written Successfully"
)


# =========================================================
# FINAL SUMMARY
# =========================================================

print("\n=================================================")
print("SELLER PERFORMANCE MONTHLY STAGING COMPLETED")
print("=================================================")

print(f"Final Row Count: {staging_df.count()}")

staging_df.printSchema()



spark.stop()