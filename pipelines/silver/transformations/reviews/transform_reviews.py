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
    to_timestamp
)

from pyspark.sql.types import (
    IntegerType
)

from pipelines.silver.utils.config_loader import (
    load_config
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

BRONZE_REVIEWS_PATH = (
    config["paths"]["bronze"]["reviews"]
)

# ---------------------------------------------------------
# Silver Paths
# ---------------------------------------------------------

SILVER_REVIEWS_PATH = (
    config["paths"]["silver"]["reviews"]
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
# METADATA ENRICHMENT
# =========================================================

"""
Enterprise lineage metadata.
"""

print("\nApplying metadata enrichment...")

silver_reviews_df = (

    silver_reviews_df

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

print("\n=================================================")
print("BRONZE AFTER  SCHEMA")
print("=================================================")

silver_reviews_df.printSchema()



# =========================================================
# COLUMN REORDERING
# =========================================================

print("\nApplying final schema ordering...")

silver_reviews_df = silver_reviews_df.select(

    "review_id",

    "order_id",

    "review_score",

    "review_comment_title",

    "review_comment_message",

    "review_creation_date",

    "review_answer_timestamp",

    "silver_loaded_at",

    "source_system",

    "transformation_version"

)


# =========================================================
# MATERIALIZE DATAFRAME
# =========================================================

"""
Force Spark to materialize the transformed
dataframe before validations.

Prevents lazy-evaluation lineage issues.
"""

print("\nMaterializing Silver Reviews DataFrame...")

silver_reviews_df = silver_reviews_df.cache()

silver_reviews_df.count()


# =========================================================
# RUN VALIDATION SUITE
# =========================================================

run_reviews_validation(
    source_df=reviews_df,
    transformed_df=silver_reviews_df
)


# =========================================================
# FINAL DATA PREVIEW
# =========================================================

print("\n=================================================")
print("SILVER REVIEWS PREVIEW")
print("=================================================")

silver_reviews_df.show(
    10,
    truncate=False
)


# =========================================================
# FINAL ROW COUNT
# =========================================================

print("\n=================================================")
print("FINAL ROW COUNT")
print("=================================================")

print(
    f"Silver Reviews Count: "
    f"{silver_reviews_df.count()}"
)


# =========================================================
# WRITE SILVER DATASET
# =========================================================

print("\n=================================================")
print("WRITING SILVER REVIEWS DATASET")
print("=================================================")

silver_reviews_df.write \
    .mode("overwrite") \
    .parquet(SILVER_REVIEWS_PATH)

print(
    f"Silver Reviews Written To: "
    f"{SILVER_REVIEWS_PATH}"
)


# =========================================================
# STOP SPARK SESSION
# =========================================================

spark.stop()

print("\n=================================================")
print("SILVER REVIEWS TRANSFORMATION COMPLETED")
print("=================================================")
