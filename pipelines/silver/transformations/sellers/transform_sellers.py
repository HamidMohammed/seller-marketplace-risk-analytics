"""
transform_sellers.py

Objective:
Transform raw Bronze seller registry data into
trusted Silver seller dimensional intelligence.

Pipeline Responsibilities:
- seller standardization
- dimensional integrity enforcement
- ZIP-prefix normalization
- geographic enrichment
- city normalization
- state normalization
- metadata enrichment
- validation-driven transformation

Project:
Olist Seller Intelligence Platform

Layer:
Silver

Dataset:
silver_sellers

Dataset Grain:
ONE ROW = ONE SELLER
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
    lit
)

from pipelines.silver.utils.config_loader import (
    load_config
)

from pipelines.silver.utils.spark_session import (
    create_spark_session
)

from pipelines.silver.validations.sellers_validation import (
    run_sellers_validation
)


# =========================================================
# CREATE SPARK SESSION
# =========================================================

spark = create_spark_session(
    "TransformSilverSellers"
)


# =========================================================
# LOAD CONFIGURATION
# =========================================================

config = load_config()

# ---------------------------------------------------------
# Bronze Paths
# ---------------------------------------------------------

BRONZE_SELLERS_PATH = (
    config["paths"]["bronze"]["sellers"]
)

# ---------------------------------------------------------
# Silver Paths
# ---------------------------------------------------------

SILVER_GEOLOCATION_PATH = (
    config["paths"]["silver"]["geolocation"]
)

SILVER_SELLERS_PATH = (
    config["paths"]["silver"]["sellers"]
)

SILVER_CLOSED_DEALS_PATH = (
    config["paths"]["silver"]["closed_deals"]
)

SILVER_MQL_PATH = (
    config["paths"]["silver"]["mql"]
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
# LOAD SOURCE DATASETS
# =========================================================

print("\n=================================================")
print("LOADING SOURCE DATASETS")
print("=================================================")

sellers_df = spark.read.parquet(
    BRONZE_SELLERS_PATH
)

geolocation_df = spark.read.parquet(
    SILVER_GEOLOCATION_PATH
)

closed_deals_df = spark.read.parquet(
    SILVER_CLOSED_DEALS_PATH
)
# Load MQL for acquisition source (origin channel)
mql_df = spark.read.parquet(
    SILVER_MQL_PATH
    )


print(
    f"Sellers Count: "
    f"{sellers_df.count()}"
)

print(
    f"Geolocation Count: "
    f"{geolocation_df.count()}"
)

print(
    f"Closed Deals Count: "
    f"{closed_deals_df.count()}"
)

# Select only what dim_seller needs
acquisition_df = closed_deals_df.select(
    col("seller_id"),
    col("business_segment"),
    col("lead_type"),
    col("lead_behaviour_profile").alias("lead_behavior_profile")
)

# Join closed deals to MQL to get origin channel
acquisition_with_source_df = acquisition_df.join(
    closed_deals_df.select("mql_id", "seller_id"),
    on="seller_id",
    how="left"
).join(
    mql_df.select(
        col("mql_id"),
        col("origin").alias("acquisition_source")
    ),
    on="mql_id",
    how="left"
).drop("mql_id")



# =========================================================
# INITIAL DATA INSPECTION
# =========================================================

print("\n=================================================")
print("BRONZE SELLERS SCHEMA")
print("=================================================")

sellers_df.printSchema()


# =========================================================
# START TRANSFORMATIONS
# =========================================================

print("\n=================================================")
print("STARTING SILVER TRANSFORMATIONS")
print("=================================================")

silver_sellers_df = sellers_df


# =========================================================
# ZIP PREFIX STANDARDIZATION
# =========================================================

"""
Standardize seller ZIP-prefix
for deterministic geographic joins.
"""

print("\nApplying ZIP-prefix standardization...")

silver_sellers_df = (

    silver_sellers_df

    .withColumn(
        "seller_zip_code_prefix",
        col("seller_zip_code_prefix").cast("integer")
    )

)


# =========================================================
# CITY NORMALIZATION
# =========================================================

"""
Normalize seller city names.
"""

print("\nApplying city normalization...")

silver_sellers_df = (

    silver_sellers_df

    .withColumn(
        "seller_city",
        lower(
            trim(col("seller_city"))
        )
    )

)


# =========================================================
# STATE NORMALIZATION
# =========================================================

"""
Normalize Brazilian state abbreviations.
"""

print("\nApplying state normalization...")

silver_sellers_df = (

    silver_sellers_df

    .withColumn(
        "seller_state",
        upper(
            trim(col("seller_state"))
        )
    )

)


# =========================================================
# GEOLOCATION ENRICHMENT
# =========================================================

"""
Enrich sellers using trusted
silver_geolocation dataset.

Layered enrichment architecture:
DO NOT rebuild geo logic again.
"""

print("\nApplying geographic enrichment...")

geo_selected_df = geolocation_df.select(

    col("zip_code_prefix"),

    col("median_latitude"),

    col("median_longitude")

)

silver_sellers_df = (

    silver_sellers_df

    .join(

        geo_selected_df,

        silver_sellers_df["seller_zip_code_prefix"]
        ==
        geo_selected_df["zip_code_prefix"],

        "left"

    )

)

print("\nApplying Left join acquisition into sellers...")
# Left join acquisition into sellers
# Preserve all sellers — 73% won't have acquisition records
silver_sellers_df = silver_sellers_df.join(
    acquisition_with_source_df,
    on="seller_id",
    how="left"
)

# Fill unknown acquisition for sellers not in funnel
silver_sellers_df = silver_sellers_df.fillna(
    "unknown", 
    subset=["acquisition_source", "business_segment", 
            "lead_type", "lead_behavior_profile"]
)


# =========================================================
# REMOVE DUPLICATED JOIN COLUMN
# =========================================================

silver_sellers_df = silver_sellers_df.drop(
    "zip_code_prefix"
)


# =========================================================
# METADATA ENRICHMENT
# =========================================================

"""
Enterprise lineage metadata.
"""

print("\nApplying metadata enrichment...")

silver_sellers_df = (

    silver_sellers_df

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

silver_sellers_df = silver_sellers_df.select(

    # -----------------------------------------------------
    # Seller Identity
    # -----------------------------------------------------

    "seller_id",

    # -----------------------------------------------------
    # Seller Geography
    # -----------------------------------------------------

    "seller_zip_code_prefix",

    "seller_city",

    "seller_state",

    "median_latitude",

    "median_longitude",

    # -----------------------------------------------------
    # Acquisition Intelligence
    # -----------------------------------------------------

    "acquisition_source",

    "business_segment",

    "lead_type",

    "lead_behavior_profile",

    # -----------------------------------------------------
    # Metadata
    # -----------------------------------------------------

    "silver_loaded_at",

    "source_system",

    "transformation_version"

)


# =========================================================
# RUN VALIDATION SUITE
# =========================================================

run_sellers_validation(
    source_df=sellers_df,
    transformed_df=silver_sellers_df
)


# =========================================================
# FINAL DATA PREVIEW
# =========================================================

print("\n=================================================")
print("SILVER SELLERS PREVIEW")
print("=================================================")

silver_sellers_df.show(
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
    f"Silver Sellers Count: "
    f"{silver_sellers_df.count()}"
)


# =========================================================
# WRITE SILVER DATASET
# =========================================================

print("\n=================================================")
print("WRITING SILVER SELLERS DATASET")
print("=================================================")

silver_sellers_df.write \
    .mode("overwrite") \
    .parquet(SILVER_SELLERS_PATH)

print(
    f"Silver Sellers Written To: "
    f"{SILVER_SELLERS_PATH}"
)


# =========================================================
# STOP SPARK SESSION
# =========================================================

spark.stop()

print("\n=================================================")
print("SILVER SELLERS TRANSFORMATION COMPLETED")
print("=================================================")
