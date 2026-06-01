"""
transform_reviews_staging.py

Objective:
Assemble customer review intelligence staging dataset
by enriching silver_reviews with delivery outcome context.

This staging dataset is the direct analytical input for:
fct_customer_reviews

Project:
Olist Seller Intelligence Platform

Layer:
Silver Staging

Dataset:
reviews_staging

Dataset Grain:
ONE ROW = ONE REVIEW EVENT FOR ONE ORDER
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

from pipelines.silver.validations.reviews_staging_validation import (
    run_reviews_staging_validation
)


# =========================================================
# CREATE SPARK SESSION
# =========================================================

spark = create_spark_session(
    "TransformReviewsStaging"
)


# =========================================================
# LOAD CONFIGURATION
# =========================================================

config = load_config()

# ---------------------------------------------------------
# Silver Paths
# ---------------------------------------------------------

SILVER_REVIEWS_PATH = (
    config["paths"]["silver"]["reviews"]
)

ORDER_DELIVERY_STAGING_PATH = (
    config["paths"]["silver"]["order_delivery_staging"]
)

# ---------------------------------------------------------
# Output Path
# ---------------------------------------------------------

REVIEWS_STAGING_PATH = (
    config["paths"]["silver"]["reviews_staging"]
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

reviews_df = spark.read.parquet(
    SILVER_REVIEWS_PATH
)

delivery_df = spark.read.parquet(
    ORDER_DELIVERY_STAGING_PATH
)

print(f"Reviews Count: {reviews_df.count()}")
print(f"Delivery Staging Count: {delivery_df.count()}")


# =========================================================
# SELECT DELIVERY CONTEXT COLUMNS
# =========================================================

print("\n=================================================")
print("SELECTING DELIVERY CONTEXT")
print("=================================================")

delivery_context_df = delivery_df.select(

    "order_id",

    "primary_seller_id",

    "order_status",

    "delivery_duration_days",

    "delay_days",

    "delivery_status_category",

    "distance_bucket",

    "is_multi_seller_order",

    "order_estimated_delivery_date",

    "order_delivered_customer_date"
)


# =========================================================
# JOIN REVIEWS + DELIVERY CONTEXT
# =========================================================
reviews_df = reviews_df.drop(
    "delay_days",
    "delivery_duration_days",
    "delivery_status_category"
)

print("\n=================================================")
print("JOINING DELIVERY CONTEXT")
print("=================================================")

staging_df = reviews_df.join(
    delivery_context_df,
    on="order_id",
    how="left"
)


# =========================================================
# SENTIMENT CATEGORY
# =========================================================

print("\n=================================================")
print("DERIVING SENTIMENT METRICS")
print("=================================================")

staging_df = staging_df.withColumn(

    "sentiment_category",

    when(
        col("review_score") <= 2,
        "Negative"

    ).when(
        col("review_score") == 3,
        "Neutral"

    ).otherwise(
        "Positive"
    )
)


# =========================================================
# REVIEW FLAGS
# =========================================================

staging_df = staging_df.withColumn(

    "negative_review_flag",

    when(
        col("review_score") <= 2,
        True
    ).otherwise(False)
)

staging_df = staging_df.withColumn(

    "neutral_review_flag",

    when(
        col("review_score") == 3,
        True
    ).otherwise(False)
)

staging_df = staging_df.withColumn(

    "positive_review_flag",

    when(
        col("review_score") >= 4,
        True
    ).otherwise(False)
)


# =========================================================
# REVIEW RESPONSE DAYS
# =========================================================

staging_df = staging_df.withColumn(

    "review_response_days",

    datediff(
        col("review_answer_timestamp"),
        col("review_creation_date")
    )
)


# =========================================================
# DELIVERY IMPACT FLAG
# =========================================================

staging_df = staging_df.withColumn(

    "delayed_delivery_review_flag",

    when(
        (col("delay_days") > 0) &
        (col("review_score") <= 2),
        True

    ).otherwise(False)
)


# =========================================================
# DELIVERY EXPERIENCE SEGMENT
# =========================================================

staging_df = staging_df.withColumn(

    "delivery_experience_segment",

    when(
        (col("delay_days") <= 0) &
        (col("review_score") >= 4),

        "Successful Delivery"

    ).when(
        (col("delay_days") > 0) &
        (col("review_score") <= 2),

        "Delivery Failure"

    ).when(
        col("is_multi_seller_order") == True,

        "Complex Fulfillment"

    ).otherwise(
        "Mixed Experience"
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

    "review_id",

    "order_id",

    "primary_seller_id",

    "review_score",

    "review_comment_title",

    "review_comment_message",

    "review_creation_date",

    "review_answer_timestamp",

    "review_response_days",

    "sentiment_category",

    "negative_review_flag",

    "neutral_review_flag",

    "positive_review_flag",

    "delayed_delivery_review_flag",

    "delivery_experience_segment",

    "order_status",

    "delivery_duration_days",

    "delay_days",

    "delivery_status_category",

    "distance_bucket",

    "is_multi_seller_order",

    "order_estimated_delivery_date",

    "order_delivered_customer_date",

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

run_reviews_staging_validation(
    staging_df
)


# =========================================================
# WRITE STAGING DATASET
# =========================================================

print("\n=================================================")
print("WRITING REVIEWS STAGING")
print("=================================================")

staging_df.write.mode("overwrite").parquet(
    REVIEWS_STAGING_PATH
)

print("Reviews Staging Written Successfully")


# =========================================================
# FINAL SUMMARY
# =========================================================

print("\n=================================================")
print("REVIEWS STAGING PIPELINE COMPLETED")
print("=================================================")

print(f"Final Row Count: {staging_df.count()}")

staging_df.printSchema()

spark.stop()