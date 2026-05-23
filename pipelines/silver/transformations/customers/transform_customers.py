"""
transform_customers.py

Objective:
Transform raw Bronze customer registry data into
trusted Silver customer dimensional intelligence.

Pipeline Responsibilities:
- customer standardization
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
silver_customers

Dataset Grain:
ONE ROW = ONE CUSTOMER
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

from pipelines.silver.validations.customers_validation import (
    run_customers_validation
)


# =========================================================
# CREATE SPARK SESSION
# =========================================================

spark = create_spark_session(
    "TransformSilverCustomers"
)


# =========================================================
# LOAD CONFIGURATION
# =========================================================

config = load_config()

# ---------------------------------------------------------
# Bronze Paths
# ---------------------------------------------------------

BRONZE_CUSTOMERS_PATH = (
    config["paths"]["bronze"]["customers"]
)

# ---------------------------------------------------------
# Silver Paths
# ---------------------------------------------------------

SILVER_GEOLOCATION_PATH = (
    config["paths"]["silver"]["geolocation"]
)

SILVER_CUSTOMERS_PATH = (
    config["paths"]["silver"]["customers"]
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

customers_df = spark.read.parquet(
    BRONZE_CUSTOMERS_PATH
)

geolocation_df = spark.read.parquet(
    SILVER_GEOLOCATION_PATH
)

print(
    f"Customers Count: "
    f"{customers_df.count()}"
)

print(
    f"Geolocation Count: "
    f"{geolocation_df.count()}"
)


# =========================================================
# INITIAL DATA INSPECTION
# =========================================================

print("\n=================================================")
print("BRONZE CUSTOMERS SCHEMA")
print("=================================================")

customers_df.printSchema()


# =========================================================
# START TRANSFORMATIONS
# =========================================================

print("\n=================================================")
print("STARTING SILVER TRANSFORMATIONS")
print("=================================================")

silver_customers_df = customers_df


# =========================================================
# ZIP PREFIX STANDARDIZATION
# =========================================================

"""
Standardize customer ZIP-prefix
for deterministic geographic joins.
"""

print("\nApplying ZIP-prefix standardization...")

silver_customers_df = (

    silver_customers_df

    .withColumn(
        "customer_zip_code_prefix",
        col("customer_zip_code_prefix").cast("integer")
    )

)


# =========================================================
# CITY NORMALIZATION
# =========================================================

"""
Normalize customer city names.
"""

print("\nApplying city normalization...")

silver_customers_df = (

    silver_customers_df

    .withColumn(
        "customer_city",
        lower(
            trim(col("customer_city"))
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

silver_customers_df = (

    silver_customers_df

    .withColumn(
        "customer_state",
        upper(
            trim(col("customer_state"))
        )
    )

)


# =========================================================
# GEOLOCATION ENRICHMENT
# =========================================================

"""
Enrich customers using trusted
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

silver_customers_df = (

    silver_customers_df

    .join(

        geo_selected_df,

        silver_customers_df["customer_zip_code_prefix"]
        ==
        geo_selected_df["zip_code_prefix"],

        "left"

    )

)


# =========================================================
# REMOVE DUPLICATED JOIN COLUMN
# =========================================================

silver_customers_df = silver_customers_df.drop(
    "zip_code_prefix"
)


# =========================================================
# METADATA ENRICHMENT
# =========================================================

"""
Enterprise lineage metadata.
"""

print("\nApplying metadata enrichment...")

silver_customers_df = (

    silver_customers_df

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

silver_customers_df = silver_customers_df.select(

    "customer_id",
    "customer_unique_id",

    "customer_zip_code_prefix",

    "customer_city",
    "customer_state",

    "median_latitude",
    "median_longitude",

    "silver_loaded_at",
    "source_system",
    "transformation_version"

)


# =========================================================
# RUN VALIDATION SUITE
# =========================================================

run_customers_validation(
    source_df=customers_df,
    transformed_df=silver_customers_df
)


# =========================================================
# FINAL DATA PREVIEW
# =========================================================

print("\n=================================================")
print("SILVER CUSTOMERS PREVIEW")
print("=================================================")

silver_customers_df.show(
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
    f"Silver Customers Count: "
    f"{silver_customers_df.count()}"
)


# =========================================================
# WRITE SILVER DATASET
# =========================================================

print("\n=================================================")
print("WRITING SILVER CUSTOMERS DATASET")
print("=================================================")

silver_customers_df.write \
    .mode("overwrite") \
    .parquet(SILVER_CUSTOMERS_PATH)

print(
    f"Silver Customers Written To: "
    f"{SILVER_CUSTOMERS_PATH}"
)


# =========================================================
# STOP SPARK SESSION
# =========================================================

spark.stop()

print("\n=================================================")
print("SILVER CUSTOMERS TRANSFORMATION COMPLETED")
print("=================================================")
