"""
build_fct_customer_reviews.py

Objective:
Build Gold Customer Reviews Fact Table

Fact:
fct_customer_reviews

Grain:
ONE ROW = ONE CUSTOMER REVIEW

Source:
reviews_staging

Dimensions:
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

# =====================================================
# PROJECT IMPORTS
# =====================================================

from pipelines.silver.utils.spark_session import (
    create_spark_session
)

from pipelines.silver.utils.config_loader import (
    load_config,
    resolve_path
)

from pipelines.gold.facts.customer_reviews.fct_customer_reviews_validation import (
    run_customer_reviews_fact_validation
)

# =====================================================
# SPARK
# =====================================================

spark = create_spark_session(
    "BuildFactCustomerReviews"
)

# =====================================================
# CONFIG
# =====================================================

config = load_config()

REVIEWS_STAGING_PATH = resolve_path(
    config["paths"]["silver"][
        "reviews_staging"
    ],
    config
)

DIM_SELLER_PATH = resolve_path(
    config["paths"]["gold"][
        "dim_seller"
    ],
    config
)

DIM_DATE_PATH = resolve_path(
    config["paths"]["gold"][
        "dim_date"
    ],
    config
)

FCT_CUSTOMER_REVIEWS_PATH = resolve_path(
    config["paths"]["gold"][
        "fct_customer_reviews"
    ],
    config
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

reviews_df = spark.read.parquet(
    REVIEWS_STAGING_PATH
)

dim_seller_df = spark.read.parquet(
    DIM_SELLER_PATH
)

dim_date_df = spark.read.parquet(
    DIM_DATE_PATH
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

fact_df = reviews_df.join(

    seller_lookup,

    reviews_df["primary_seller_id"] ==
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
# REVIEW DATE LOOKUP
# =====================================================

fact_df = fact_df.withColumn(

    "review_date",

    to_date(
        col(
            "review_creation_date"
        )
    )
)

review_date_lookup = dim_date_df.select(
    col("date_sk").alias(
        "review_date_sk"
    ),
    col("full_date").alias(
        "review_date_key"
    )
)

fact_df = fact_df.join(

    review_date_lookup,

    fact_df["review_date"] ==
    review_date_lookup[
        "review_date_key"
    ],

    "left"
)

# =====================================================
# RESPONSE DATE LOOKUP
# =====================================================

fact_df = fact_df.withColumn(

    "response_date",

    to_date(
        col(
            "review_answer_timestamp"
        )
    )
)

response_date_lookup = dim_date_df.select(
    col("date_sk").alias(
        "response_date_sk"
    ),
    col("full_date").alias(
        "response_date_key"
    )
)

fact_df = fact_df.join(

    response_date_lookup,

    fact_df["response_date"] ==
    response_date_lookup[
        "response_date_key"
    ],

    "left"
)

# =====================================================
# REVIEW KPI FLAGS
# =====================================================

fact_df = fact_df.withColumn(

    "low_rating_flag",

    when(
        col("review_score") <= 2,
        True
    ).otherwise(False)
)

fact_df = fact_df.withColumn(

    "excellent_rating_flag",

    when(
        col("review_score") == 5,
        True
    ).otherwise(False)
)

# =====================================================
# FACT SURROGATE KEY
# =====================================================

fact_window = Window.orderBy(
    "review_id"
)

fact_df = fact_df.withColumn(

    "review_fact_sk",

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

# =====================================================
# FINAL SELECT
# =====================================================

fact_df = fact_df.select(

    "review_fact_sk",

    "review_id",

    "order_id",

    "seller_sk_fk",

    "review_date_sk",

    "response_date_sk",

    "review_score",

    "review_response_days",

    "delivery_duration_days",

    "delay_days",

    "negative_review_flag",

    "neutral_review_flag",

    "positive_review_flag",

    "delayed_delivery_review_flag",

    "low_rating_flag",

    "excellent_rating_flag",

    "is_multi_seller_order",

    "sentiment_category",

    "delivery_experience_segment",

    "delivery_status_category",

    "distance_bucket",

    "source_system",

    "transformation_version",

    "gold_loaded_at"
)

# =====================================================
# VALIDATION
# =====================================================

run_customer_reviews_fact_validation(
    fact_df
)

# =====================================================
# WRITE
# =====================================================

fact_df.write.mode(
    "overwrite"
).parquet(
    FCT_CUSTOMER_REVIEWS_PATH
)

print(
    f"Final Row Count: "
    f"{fact_df.count():,}"
)

spark.stop()

