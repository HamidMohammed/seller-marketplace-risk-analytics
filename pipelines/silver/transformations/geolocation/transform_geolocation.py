"""
transform_geolocation.py

Objective:
Transform noisy Bronze geolocation records into
trusted Silver geographic enrichment intelligence.

Pipeline Responsibilities:
- geographic deduplication
- ZIP-prefix standardization
- coordinate aggregation
- city normalization
- state normalization
- geographic validation
- metadata enrichment
- trusted enrichment generation

Project:
Olist Seller Intelligence Platform

Layer:
Silver

Dataset:
silver_geolocation

Dataset Grain:
ONE ROW = ONE ZIP CODE PREFIX AREA
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
    upper,
    trim,
    current_timestamp,
    lit,
    expr,
    first
)

from pipelines.silver.utils.config_loader import (
    load_config
)

from pipelines.silver.utils.spark_session import (
    create_spark_session
)

from pipelines.silver.validations.geolocation_validation import (
    run_geolocation_validation
)


# =========================================================
# CREATE SPARK SESSION
# =========================================================

spark = create_spark_session(
    "TransformSilverGeolocation"
)


# =========================================================
# LOAD CONFIGURATION
# =========================================================

config = load_config()

# ---------------------------------------------------------
# Bronze Paths
# ---------------------------------------------------------

BRONZE_GEOLOCATION_PATH = (
    config["paths"]["bronze"]["geolocation"]
)

# ---------------------------------------------------------
# Silver Paths
# ---------------------------------------------------------

SILVER_GEOLOCATION_PATH = (
    config["paths"]["silver"]["geolocation"]
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
# LOAD BRONZE DATASET
# =========================================================

print("\n=================================================")
print("LOADING BRONZE GEOLOCATION DATASET")
print("=================================================")

bronze_geo_df = spark.read.parquet(
    BRONZE_GEOLOCATION_PATH
)

print(
    f"Bronze Geolocation Count: "
    f"{bronze_geo_df.count()}"
)


# =========================================================
# INITIAL DATA INSPECTION
# =========================================================

print("\n=================================================")
print("BRONZE GEOLOCATION SCHEMA")
print("=================================================")

bronze_geo_df.printSchema()


# =========================================================
# START TRANSFORMATIONS
# =========================================================

print("\n=================================================")
print("STARTING SILVER TRANSFORMATIONS")
print("=================================================")

silver_geo_df = bronze_geo_df


# =========================================================
# ZIP PREFIX STANDARDIZATION
# =========================================================

"""
Standardize geographic business key.
"""

print("\nApplying ZIP prefix standardization...")

silver_geo_df = (

    silver_geo_df

    .withColumn(
        "zip_code_prefix",
        col("geolocation_zip_code_prefix").cast("integer")
    )

)


# =========================================================
# CITY NORMALIZATION
# =========================================================

"""
Normalize city naming consistency.
"""

print("\nApplying city normalization...")

silver_geo_df = (

    silver_geo_df

    .withColumn(
        "city",
        lower(trim(col("geolocation_city")))
    )

)


# =========================================================
# STATE NORMALIZATION
# =========================================================

"""
Normalize Brazilian state abbreviations.
"""

print("\nApplying state normalization...")

silver_geo_df = (

    silver_geo_df

    .withColumn(
        "state",
        upper(trim(col("geolocation_state")))
    )

)


# =========================================================
# COORDINATE STANDARDIZATION
# =========================================================

"""
Ensure numeric coordinate consistency.
"""

print("\nStandardizing coordinates...")

silver_geo_df = (

    silver_geo_df

    .withColumn(
        "latitude",
        col("geolocation_lat").cast("double")
    )

    .withColumn(
        "longitude",
        col("geolocation_lng").cast("double")
    )

)


# =========================================================
# MEDIAN COORDINATE AGGREGATION
# =========================================================

"""
Critical geographic governance logic.

Goal:
Convert multiple noisy coordinates into
one stable representative geographic point
per ZIP-prefix region.

Median aggregation is more robust than average
against outliers and noisy coordinates.
"""

print("\nApplying geographic aggregation strategy...")

silver_geo_df = (

    silver_geo_df

    .groupBy(
        "zip_code_prefix"
    )

    .agg(

        expr(
            "percentile_approx(latitude, 0.5)"
        ).alias("median_latitude"),

        expr(
            "percentile_approx(longitude, 0.5)"
        ).alias("median_longitude"),

        first("city").alias("city"),

        first("state").alias("state")

    )

)


# =========================================================
# METADATA ENRICHMENT
# =========================================================

"""
Enterprise lineage metadata.
"""

print("\nApplying metadata enrichment...")

silver_geo_df = (

    silver_geo_df

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

silver_geo_df = silver_geo_df.select(

    "zip_code_prefix",

    "median_latitude",
    "median_longitude",

    "city",
    "state",

    "silver_loaded_at",
    "source_system",
    "transformation_version"

)


# =========================================================
# RUN VALIDATION SUITE
# =========================================================

run_geolocation_validation(
    source_df=bronze_geo_df,
    transformed_df=silver_geo_df
)


# =========================================================
# FINAL DATA PREVIEW
# =========================================================

print("\n=================================================")
print("SILVER GEOLOCATION PREVIEW")
print("=================================================")

silver_geo_df.show(
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
    f"Silver Geolocation Count: "
    f"{silver_geo_df.count()}"
)


# =========================================================
# WRITE SILVER DATASET
# =========================================================

print("\n=================================================")
print("WRITING SILVER GEOLOCATION DATASET")
print("=================================================")

silver_geo_df.write \
    .mode("overwrite") \
    .parquet(SILVER_GEOLOCATION_PATH)

print(
    f"Silver Geolocation Written To: "
    f"{SILVER_GEOLOCATION_PATH}"
)


# =========================================================
# STOP SPARK SESSION
# =========================================================

spark.stop()

print("\n=================================================")
print("SILVER GEOLOCATION TRANSFORMATION COMPLETED")
print("=================================================")
