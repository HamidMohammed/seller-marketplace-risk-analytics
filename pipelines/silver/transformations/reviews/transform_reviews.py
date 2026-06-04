"""
transform_reviews.py

Objective:
Transform raw Bronze customer review records into
trusted Silver behavioral operational intelligence.

Pipeline Responsibilities:
- review standardization
- review-score standardization
- text normalization
- timestamp standardization
- behavioral integrity enforcement
- metadata enrichment
- validation-driven transformation

Project:
Olist Seller Intelligence Platform

Layer:
Silver

Dataset:
silver_reviews

Dataset Grain:
ONE ROW = ONE REVIEW EVENT
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
    trim,
    current_timestamp,
    lit,
    when,
    to_timestamp,
    datediff,
    row_number

)

from pyspark.sql.window import Window

from pyspark.sql.types import (
    IntegerType
)

from pipelines.silver.utils.config_loader import (
    load_config,
    resolve_path
)

from pipelines.silver.utils.spark_session import (
    create_spark_session
)

from pipelines.silver.validations.reviews_validation import (
    run_reviews_validation
)


# =========================================================
# CREATE SPARK SESSION
# =========================================================

spark = create_spark_session(
    "TransformSilverReviews"
)


# =========================================================
# LOAD CONFIGURATION
# =========================================================

config = load_config()

# ---------------------------------------------------------
# Bronze Paths
# ---------------------------------------------------------

BRONZE_REVIEWS_PATH = resolve_path(
    config["paths"]["bronze"]["reviews"],
    config
)

# ---------------------------------------------------------
# Silver Paths
# ---------------------------------------------------------

SILVER_REVIEWS_PATH = resolve_path(
    config["paths"]["silver"]["reviews"],
    config
)

SILVER_ORDERS_PATH = resolve_path(
    config["paths"]["silver"]["orders"],
    config
)

SILVER_REVIEWS_QUARANTINE_PATH = resolve_path(
    config["paths"]["silver"]["reviews_quarantine"],
    config
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
# LOAD SOURCE DATASET
# =========================================================

print("\n=================================================")
print("LOADING BRONZE REVIEWS DATASET")
print("=================================================")

reviews_df = spark.read.parquet(
    BRONZE_REVIEWS_PATH
)

print(
    f"Bronze Reviews Count: "
    f"{reviews_df.count()}"
)
print("\n=================================================")
print("LOADING SILVER ORDERS DATASET")
print("=================================================")


orders_df = spark.read.parquet(
    SILVER_ORDERS_PATH
)

orders_df = orders_df.select(

    "order_id",

    "delivery_duration_days",

    "delay_days",

    "delivery_status_category"
)

# =========================================================
# INITIAL DATA INSPECTION
# =========================================================

print("\n=================================================")
print("BRONZE REVIEWS SCHEMA")
print("=================================================")

reviews_df.printSchema()


# =========================================================
# START TRANSFORMATIONS
# =========================================================

print("\n=================================================")
print("STARTING SILVER TRANSFORMATIONS")
print("=================================================")

silver_reviews_df = reviews_df


# =========================================================
# REVIEW ID STANDARDIZATION
# =========================================================

"""
Standardize review business identifiers.
"""

print("\nApplying review ID standardization...")

silver_reviews_df = (

    silver_reviews_df

    .withColumn(
        "review_id",
        trim(col("review_id"))
    )

    .withColumn(
        "order_id",
        trim(col("order_id"))
    )

)


# =========================================================
# REVIEW SCORE STANDARDIZATION
# =========================================================

"""
Standardize review scores.
"""

print("\nApplying review score standardization...")

silver_reviews_df = (

    silver_reviews_df

    .withColumn(
        "review_score",
        col("review_score").cast(
            IntegerType()
        )
    )

)


# =========================================================
# TEXT NORMALIZATION
# =========================================================

"""
Normalize textual review fields while preserving
original customer intent.
"""

print("\nApplying text normalization...")

silver_reviews_df = (

    silver_reviews_df

    .withColumn(

        "review_comment_title",

        when(
            col("review_comment_title").isNotNull(),

            trim(
                col("review_comment_title")
            )

        ).otherwise(None)

    )

    .withColumn(

        "review_comment_message",

        when(
            col("review_comment_message").isNotNull(),

            trim(
                col("review_comment_message")
            )

        ).otherwise(None)

    )

)


# =========================================================
# TIMESTAMP STANDARDIZATION
# =========================================================

"""
Standardize temporal review attributes.
"""

print("\nApplying timestamp standardization...")

silver_reviews_df = (

    silver_reviews_df

    .withColumn(

        "review_creation_date",

        to_timestamp(
            col("review_creation_date"),
            "yyyy-MM-dd HH:mm:ss"
        )

    )

    .withColumn(

        "review_answer_timestamp",

        to_timestamp(
            col("review_answer_timestamp"),
            "yyyy-MM-dd HH:mm:ss"
        )

    )

)

# =========================================================
# REVIEW DEDUPLICATION
# =========================================================

print("\nApplying review deduplication...")

review_window = Window.partitionBy(
    "review_id"
).orderBy(
    col(
        "review_answer_timestamp"
    ).desc_nulls_last()
)

silver_reviews_df = (

    silver_reviews_df

    .withColumn(
        "row_num",
        row_number().over(
            review_window
        )
    )

    .filter(
        col("row_num") == 1
    )

    .drop("row_num")

)

print(
    f"Reviews After Deduplication: "
    f"{silver_reviews_df.count()}"
)


# =========================================================
# QUARANTINE RULE 1
# NULL ORDER ID
# =========================================================

print("\nIdentifying NULL order_id reviews...")

null_order_reviews_df = (

    silver_reviews_df

    .filter(
        col("order_id").isNull()
    )

    .withColumn(
        "quarantine_reason",
        lit("NULL_ORDER_ID")
    )

)


# =========================================================
# QUARANTINE RULE 2
# ORPHAN REVIEWS
# =========================================================

print("\nIdentifying orphan reviews...")

orphan_reviews_df = (

    silver_reviews_df

    .join(

        orders_df.select(
            "order_id"
        ),

        on="order_id",

        how="left_anti"

    )

    .withColumn(
        "quarantine_reason",
        lit("ORPHAN_REVIEW")
    )

)


# =========================================================
# QUARANTINE RULE 3
# MISSING REVIEW TIMESTAMPS
# =========================================================

print(
    "\nIdentifying reviews with missing timestamps..."
)

missing_timestamp_df = (

    silver_reviews_df

    .filter(

        col(
            "review_creation_date"
        ).isNull()

        &

        col(
            "review_answer_timestamp"
        ).isNull()

    )

    .withColumn(

        "quarantine_reason",

        lit(
            "MISSING_REVIEW_TIMESTAMPS"
        )

    )

)


# =========================================================
# BUILD QUARANTINE DATASET
# =========================================================

print("\nBuilding review quarantine dataset...")

reviews_quarantine_df = (

    null_order_reviews_df

    .unionByName(
        orphan_reviews_df
    )

    .unionByName(
        missing_timestamp_df
    )

    .dropDuplicates(
        ["review_id"]
    )

)

print(
    f"Quarantined Reviews: "
    f"{reviews_quarantine_df.count()}"
)


# =========================================================
# BUILD CLEAN DATASET
# =========================================================

print("\nBuilding clean reviews dataset...")

clean_reviews_df = (

    silver_reviews_df

    .join(

        reviews_quarantine_df.select(
            "review_id"
        ),

        on="review_id",

        how="left_anti"

    )

)

print(
    f"Clean Reviews: "
    f"{clean_reviews_df.count()}"
)


# =========================================================
# DELIVERY CONTEXT ENRICHMENT
# =========================================================

print("\nJoining delivery context...")

clean_reviews_df = clean_reviews_df.join(

    orders_df,

    on="order_id",

    how="left"

)


# =========================================================
# REVIEW LABEL
# =========================================================

print("\nDeriving review labels...")

clean_reviews_df = clean_reviews_df.withColumn(

    "review_label",

    when(
        col("review_score") <= 2,
        "Negative"
    )

    .when(
        col("review_score") == 3,
        "Neutral"
    )

    .otherwise(
        "Positive"
    )

)


# =========================================================
# REVIEW RESPONSE DAYS
# =========================================================

print("\nCalculating response days...")

clean_reviews_df = clean_reviews_df.withColumn(

    "review_response_days",

    datediff(

        col(
            "review_answer_timestamp"
        ),

        col(
            "review_creation_date"
        )

    )

)


# =========================================================
# REVIEW CONTEXT
# =========================================================

print("\nDeriving review context...")

clean_reviews_df = clean_reviews_df.withColumn(

    "review_context",

    when(

        (col("review_label") == "Negative")

        &

        (col("delay_days") > 0),

        "Delivery Related"

    )

    .when(

        (col("review_label") == "Negative")

        &

        (col("delay_days") <= 0),

        "Product Related"

    )

    .otherwise(
        "General Experience"
    )

)


# =========================================================
# METADATA ENRICHMENT
# =========================================================

print("\nApplying metadata enrichment...")

clean_reviews_df = (

    clean_reviews_df

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
# FINAL COLUMN ORDER
# =========================================================

clean_reviews_df = clean_reviews_df.select(

    "review_id",

    "order_id",

    "review_score",

    "review_comment_title",

    "review_comment_message",

    "review_creation_date",

    "review_answer_timestamp",

    "review_response_days",

    "review_label",

    "review_context",

    "delivery_duration_days",

    "delay_days",

    "delivery_status_category",

    "silver_loaded_at",

    "source_system",

    "transformation_version"

)


# =========================================================
# MATERIALIZE DATAFRAME
# =========================================================

print(
    "\nMaterializing clean reviews dataset..."
)

clean_reviews_df = clean_reviews_df.cache()

clean_reviews_df.count()


# =========================================================
# VALIDATIONS
# =========================================================

run_reviews_validation(

    source_df=reviews_df,

    transformed_df=clean_reviews_df,

    quarantine_df=reviews_quarantine_df

)


# =========================================================
# WRITE QUARANTINE
# =========================================================

print(
    "\nWriting reviews quarantine dataset..."
)

reviews_quarantine_df.write \
    .mode("overwrite") \
    .parquet(
        SILVER_REVIEWS_QUARANTINE_PATH
    )


# =========================================================
# WRITE CLEAN REVIEWS
# =========================================================

print(
    "\nWriting silver reviews dataset..."
)

clean_reviews_df.write \
    .mode("overwrite") \
    .parquet(
        SILVER_REVIEWS_PATH
    )


# =========================================================
# FINAL SUMMARY
# =========================================================

print("\n=================================================")
print("REVIEWS HARDENING COMPLETED")
print("=================================================")

print(
    f"Clean Reviews: "
    f"{clean_reviews_df.count()}"
)

print(
    f"Quarantined Reviews: "
    f"{reviews_quarantine_df.count()}"
)

spark.stop()
