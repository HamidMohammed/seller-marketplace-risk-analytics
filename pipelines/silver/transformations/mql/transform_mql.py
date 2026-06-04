"""
transform_mql.py

Objective:
Transform raw Bronze marketing-qualified lead records into
trusted Silver CRM acquisition intelligence.

Pipeline Responsibilities:
- lead standardization
- acquisition-source normalization
- landing-page normalization
- timestamp standardization
- CRM integrity enforcement
- metadata enrichment
- validation-driven transformation

Project:
Olist Seller Intelligence Platform

Layer:
Silver

Dataset:
silver_mql

Dataset Grain:
ONE ROW = ONE QUALIFIED LEAD EVENT
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
    current_timestamp,
    lit,
    to_timestamp,
    when
)

from pipelines.silver.utils.config_loader import (
    load_config,
    resolve_path
)

from pipelines.silver.utils.spark_session import (
    create_spark_session
)

from pipelines.silver.validations.mql_validation import (
    run_mql_validation
)


# =========================================================
# CREATE SPARK SESSION
# =========================================================

spark = create_spark_session(
    "TransformSilverMQL"
)


# =========================================================
# LOAD CONFIGURATION
# =========================================================

config = load_config()

# ---------------------------------------------------------
# Bronze Paths
# ---------------------------------------------------------

BRONZE_MQL_PATH = resolve_path(
    config["paths"]["bronze"]["mql"],
    config
)

# ---------------------------------------------------------
# Silver Paths
# ---------------------------------------------------------

SILVER_MQL_PATH = resolve_path(
    config["paths"]["silver"]["mql"],
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
print("LOADING BRONZE MQL DATASET")
print("=================================================")

mql_df = spark.read.parquet(
    BRONZE_MQL_PATH
)

print(
    f"Bronze MQL Count: "
    f"{mql_df.count()}"
)


# =========================================================
# INITIAL DATA INSPECTION
# =========================================================

print("\n=================================================")
print("BRONZE MQL SCHEMA")
print("=================================================")

mql_df.printSchema()


# =========================================================
# START TRANSFORMATIONS
# =========================================================

print("\n=================================================")
print("STARTING SILVER TRANSFORMATIONS")
print("=================================================")

silver_mql_df = mql_df


# =========================================================
# MQL ID STANDARDIZATION
# =========================================================

"""
Standardize CRM lead identifiers.
"""

print("\nApplying MQL ID standardization...")

silver_mql_df = (

    silver_mql_df

    .withColumn(
        "mql_id",
        trim(col("mql_id"))
    )

)


# =========================================================
# ACQUISITION SOURCE NORMALIZATION
# =========================================================

"""
Normalize acquisition source semantics for:
- attribution consistency
- deterministic grouping
- executive readability
"""

print("\nApplying acquisition source normalization...")

silver_mql_df = (

    silver_mql_df

    .withColumn(

        "origin",

        when(
            col("origin").isNotNull(),

            lower(
                trim(
                    col("origin")
                )
            )

        ).otherwise(None)

    )

)


# =========================================================
# LANDING PAGE NORMALIZATION
# =========================================================

"""
Normalize landing-page identifiers.
"""

print("\nApplying landing page normalization...")

silver_mql_df = (

    silver_mql_df

    .withColumn(

        "landing_page_id",

        when(
            col("landing_page_id").isNotNull(),

            lower(
                trim(
                    col("landing_page_id")
                )
            )

        ).otherwise(None)

    )

)


# =========================================================
# TIMESTAMP STANDARDIZATION
# =========================================================

"""
Standardize acquisition chronology timestamps.
"""

print("\nApplying timestamp standardization...")

silver_mql_df = (

    silver_mql_df

    .withColumn(

        "first_contact_date",

        to_timestamp(
            col("first_contact_date"),
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

silver_mql_df = (

    silver_mql_df

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

silver_mql_df = silver_mql_df.select(

    "mql_id",

    "first_contact_date",

    "landing_page_id",

    "origin",

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

print("\nMaterializing Silver MQL DataFrame...")

silver_mql_df = silver_mql_df.cache()

silver_mql_df.count()


# =========================================================
# RUN VALIDATION SUITE
# =========================================================

run_mql_validation(
    source_df=mql_df,
    transformed_df=silver_mql_df
)


# =========================================================
# FINAL DATA PREVIEW
# =========================================================

print("\n=================================================")
print("SILVER MQL PREVIEW")
print("=================================================")

silver_mql_df.show(
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
    f"Silver MQL Count: "
    f"{silver_mql_df.count()}"
)


# =========================================================
# WRITE SILVER DATASET
# =========================================================

print("\n=================================================")
print("WRITING SILVER MQL DATASET")
print("=================================================")

silver_mql_df.write \
    .mode("overwrite") \
    .parquet(SILVER_MQL_PATH)

print(
    f"Silver MQL Written To: "
    f"{SILVER_MQL_PATH}"
)


# =========================================================
# STOP SPARK SESSION
# =========================================================

spark.stop()

print("\n=================================================")
print("SILVER MQL TRANSFORMATION COMPLETED")
print("=================================================")
