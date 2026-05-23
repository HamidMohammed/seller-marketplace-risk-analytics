"""
transform_products.py

Objective:
Transform raw Bronze product registry data into
trusted Silver product dimensional intelligence.

Pipeline Responsibilities:
- product standardization
- category normalization
- logistics standardization
- dimensional integrity enforcement
- product volume derivation
- metadata enrichment
- validation-driven transformation

Project:
Olist Seller Intelligence Platform

Layer:
Silver

Dataset:
silver_products

Dataset Grain:
ONE ROW = ONE PRODUCT
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
    lower,
    trim,
    current_timestamp,
    lit,
    when
)

from pyspark.sql.types import (
    IntegerType,
    DecimalType
)

from pipelines.silver.utils.config_loader import (
    load_config
)

from pipelines.silver.utils.spark_session import (
    create_spark_session
)

from pipelines.silver.validations.products_validation import (
    run_products_validation
)


# =========================================================
# CREATE SPARK SESSION
# =========================================================

spark = create_spark_session(
    "TransformSilverProducts"
)


# =========================================================
# LOAD CONFIGURATION
# =========================================================

config = load_config()

# ---------------------------------------------------------
# Bronze Paths
# ---------------------------------------------------------

BRONZE_PRODUCTS_PATH = (
    config["paths"]["bronze"]["products"]
)

# ---------------------------------------------------------
# Silver Paths
# ---------------------------------------------------------

SILVER_PRODUCTS_PATH = (
    config["paths"]["silver"]["products"]
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
print("LOADING BRONZE PRODUCTS DATASET")
print("=================================================")

products_df = spark.read.parquet(
    BRONZE_PRODUCTS_PATH
)

print(
    f"Bronze Products Count: "
    f"{products_df.count()}"
)


# =========================================================
# INITIAL DATA INSPECTION
# =========================================================

print("\n=================================================")
print("BRONZE PRODUCTS SCHEMA")
print("=================================================")

products_df.printSchema()


# =========================================================
# START TRANSFORMATIONS
# =========================================================

print("\n=================================================")
print("STARTING SILVER TRANSFORMATIONS")
print("=================================================")

silver_products_df = products_df


# =========================================================
# PRODUCT ID STANDARDIZATION
# =========================================================

"""
Standardize product business keys.
"""

print("\nApplying product ID standardization...")

silver_products_df = (

    silver_products_df

    .withColumn(
        "product_id",
        trim(col("product_id"))
    )

)


# =========================================================
# CATEGORY NORMALIZATION
# =========================================================

"""
Normalize product categories for
deterministic grouping consistency.
"""

print("\nApplying category normalization...")

silver_products_df = (

    silver_products_df

    .withColumn(

        "product_category_name",

        when(
            col("product_category_name").isNotNull(),

            lower(
                trim(col("product_category_name"))
            )

        ).otherwise("unknown_category")

    )

)


# =========================================================
# NUMERIC STANDARDIZATION
# =========================================================

"""
Standardize logistics and dimensional metrics.
"""

print("\nApplying numeric standardization...")

silver_products_df = (

    silver_products_df

    .withColumn(
        "product_name_lenght",
        col("product_name_lenght").cast(
            IntegerType()
        )
    )

    .withColumn(
        "product_description_lenght",
        col("product_description_lenght").cast(
            IntegerType()
        )
    )

    .withColumn(
        "product_photos_qty",
        col("product_photos_qty").cast(
            IntegerType()
        )
    )

    .withColumn(
        "product_weight_g",
        col("product_weight_g").cast(
            DecimalType(12, 2)
        )
    )

    .withColumn(
        "product_length_cm",
        col("product_length_cm").cast(
            DecimalType(12, 2)
        )
    )

    .withColumn(
        "product_height_cm",
        col("product_height_cm").cast(
            DecimalType(12, 2)
        )
    )

    .withColumn(
        "product_width_cm",
        col("product_width_cm").cast(
            DecimalType(12, 2)
        )
    )

)


# =========================================================
# PRODUCT VOLUME DERIVATION
# =========================================================

"""
Derive operational shipment volume metric.

Used for:
- freight analysis
- logistics intelligence
- oversized shipment detection
"""

print("\nCalculating product volume metric...")

silver_products_df = (

    silver_products_df

    .withColumn(

        "product_volume_cm3",

        when(

            col("product_length_cm").isNotNull()
            &
            col("product_height_cm").isNotNull()
            &
            col("product_width_cm").isNotNull(),

            (
                col("product_length_cm")
                *
                col("product_height_cm")
                *
                col("product_width_cm")
            ).cast(DecimalType(18, 2))

        ).otherwise(None)

    )

)


# =========================================================
# METADATA ENRICHMENT
# =========================================================

"""
Enterprise lineage metadata.
"""

print("\nApplying metadata enrichment...")

silver_products_df = (

    silver_products_df

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

silver_products_df = silver_products_df.select(

    "product_id",

    "product_category_name",

    "product_name_lenght",
    "product_description_lenght",
    "product_photos_qty",

    "product_weight_g",

    "product_length_cm",
    "product_height_cm",
    "product_width_cm",

    "product_volume_cm3",

    "silver_loaded_at",
    "source_system",
    "transformation_version"

)


# =========================================================
# RUN VALIDATION SUITE
# =========================================================

run_products_validation(
    source_df=products_df,
    transformed_df=silver_products_df
)


# =========================================================
# FINAL DATA PREVIEW
# =========================================================

print("\n=================================================")
print("SILVER PRODUCTS PREVIEW")
print("=================================================")

silver_products_df.show(
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
    f"Silver Products Count: "
    f"{silver_products_df.count()}"
)


# =========================================================
# WRITE SILVER DATASET
# =========================================================

print("\n=================================================")
print("WRITING SILVER PRODUCTS DATASET")
print("=================================================")

silver_products_df.write \
    .mode("overwrite") \
    .parquet(SILVER_PRODUCTS_PATH)

print(
    f"Silver Products Written To: "
    f"{SILVER_PRODUCTS_PATH}"
)


# =========================================================
# STOP SPARK SESSION
# =========================================================

spark.stop()

print("\n=================================================")
print("SILVER PRODUCTS TRANSFORMATION COMPLETED")
print("=================================================")
