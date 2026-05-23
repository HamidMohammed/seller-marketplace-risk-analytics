"""
transform_category_translation.py

Objective:
Transform raw multilingual product category mappings into
trusted Silver semantic business enrichment.

Pipeline Responsibilities:
- multilingual category normalization
- semantic standardization
- translation consistency enforcement
- business readability enhancement
- metadata enrichment
- validation-driven transformation

Project:
Olist Seller Intelligence Platform

Layer:
Silver

Dataset:
silver_category_translation

Dataset Grain:
ONE ROW = ONE CATEGORY TRANSLATION
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
    lower,
    regexp_replace,
    current_timestamp,
    lit
)

from pipelines.silver.utils.config_loader import (
    load_config
)

from pipelines.silver.utils.spark_session import (
    create_spark_session
)

from pipelines.silver.validations.category_translation_validation import (
    run_category_translation_validation
)


# =========================================================
# CREATE SPARK SESSION
# =========================================================

spark = create_spark_session(
    "TransformSilverCategoryTranslation"
)


# =========================================================
# LOAD CONFIGURATION
# =========================================================

config = load_config()

# ---------------------------------------------------------
# Bronze Paths
# ---------------------------------------------------------

BRONZE_CATEGORY_TRANSLATION_PATH = (
    config["paths"]["bronze"]["category_translation"]
)

# ---------------------------------------------------------
# Silver Paths
# ---------------------------------------------------------

SILVER_CATEGORY_TRANSLATION_PATH = (
    config["paths"]["silver"]["category_translation"]
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
print("LOADING BRONZE CATEGORY TRANSLATION DATASET")
print("=================================================")

category_translation_df = spark.read.parquet(
    BRONZE_CATEGORY_TRANSLATION_PATH
)

print(
    f"Bronze Category Translation Count: "
    f"{category_translation_df.count()}"
)


# =========================================================
# INITIAL DATA INSPECTION
# =========================================================

print("\n=================================================")
print("BRONZE CATEGORY TRANSLATION SCHEMA")
print("=================================================")

category_translation_df.printSchema()


# =========================================================
# START TRANSFORMATIONS
# =========================================================

print("\n=================================================")
print("STARTING SILVER TRANSFORMATIONS")
print("=================================================")

silver_category_translation_df = category_translation_df


# =========================================================
# PORTUGUESE CATEGORY NORMALIZATION
# =========================================================

"""
Normalize Portuguese category labels for:
- deterministic joins
- semantic consistency
- stable enrichment behavior
"""

print("\nApplying Portuguese category normalization...")

silver_category_translation_df = (

    silver_category_translation_df

    .withColumn(
        "product_category_name",
        lower(
            trim(
                col("product_category_name")
            )
        )
    )

)


# =========================================================
# ENGLISH CATEGORY NORMALIZATION
# =========================================================

"""
Normalize English category labels for:
- executive readability
- analytical consistency
- deterministic grouping
"""

print("\nApplying English category normalization...")

silver_category_translation_df = (

    silver_category_translation_df

    .withColumn(
        "product_category_name_english",
        lower(
            trim(
                col("product_category_name_english")
            )
        )
    )

)


# =========================================================
# BUSINESS-FRIENDLY CATEGORY STANDARDIZATION
# =========================================================

"""
Standardize business-readable category formatting.
"""

print("\nApplying business-friendly formatting...")

silver_category_translation_df = (

    silver_category_translation_df

    .withColumn(

        "product_category_name_english",

        regexp_replace(
            col("product_category_name_english"),
            " ",
            "_"
        )

    )

)


# =========================================================
# REMOVE DUPLICATE TRANSLATIONS
# =========================================================

"""
Preserve deterministic category mappings.
"""

print("\nRemoving duplicate category translations...")

silver_category_translation_df = (
    silver_category_translation_df
    .dropDuplicates(["product_category_name"])
)


# =========================================================
# METADATA ENRICHMENT
# =========================================================

"""
Enterprise lineage metadata.
"""

print("\nApplying metadata enrichment...")

silver_category_translation_df = (

    silver_category_translation_df

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
# COLUMN REORDERING
# =========================================================

print("\nApplying final schema ordering...")

silver_category_translation_df = silver_category_translation_df.select(

    "product_category_name",

    "product_category_name_english",

    "silver_loaded_at",

    "source_system",

    "transformation_version"

)


# =========================================================
# MATERIALIZE DATAFRAME
# =========================================================

"""
Force Spark materialization before validations.
"""

print("\nMaterializing Silver Category Translation DataFrame...")

silver_category_translation_df = (
    silver_category_translation_df.cache()
)

silver_category_translation_df.count()


# =========================================================
# RUN VALIDATION SUITE
# =========================================================

run_category_translation_validation(
    source_df=category_translation_df,
    transformed_df=silver_category_translation_df
)


# =========================================================
# FINAL DATA PREVIEW
# =========================================================

print("\n=================================================")
print("SILVER CATEGORY TRANSLATION PREVIEW")
print("=================================================")

silver_category_translation_df.show(
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
    f"Silver Category Translation Count: "
    f"{silver_category_translation_df.count()}"
)


# =========================================================
# WRITE SILVER DATASET
# =========================================================

print("\n=================================================")
print("WRITING SILVER CATEGORY TRANSLATION DATASET")
print("=================================================")

silver_category_translation_df.write \
    .mode("overwrite") \
    .parquet(SILVER_CATEGORY_TRANSLATION_PATH)

print(
    f"Silver Category Translation Written To: "
    f"{SILVER_CATEGORY_TRANSLATION_PATH}"
)


# =========================================================
# STOP SPARK SESSION
# =========================================================

spark.stop()

print("\n=================================================")
print("SILVER CATEGORY TRANSLATION TRANSFORMATION COMPLETED")
print("=================================================")
