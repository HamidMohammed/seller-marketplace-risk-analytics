"""
transform_payments.py

Objective:
Transform raw Bronze payment operational records into
trusted Silver financial operational intelligence.

Pipeline Responsibilities:
- payment standardization
- payment-type normalization
- installment standardization
- financial integrity enforcement
- metadata enrichment
- validation-driven transformation

Project:
Olist Seller Intelligence Platform

Layer:
Silver

Dataset:
silver_payments

Dataset Grain:
ONE ROW = ONE PAYMENT EVENT
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
    lit
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

from pipelines.silver.validations.payments_validation import (
    run_payments_validation
)


# =========================================================
# CREATE SPARK SESSION
# =========================================================

spark = create_spark_session(
    "TransformSilverPayments"
)


# =========================================================
# LOAD CONFIGURATION
# =========================================================

config = load_config()

# ---------------------------------------------------------
# Bronze Paths
# ---------------------------------------------------------

BRONZE_PAYMENTS_PATH = (
    config["paths"]["bronze"]["payments"]
)

# ---------------------------------------------------------
# Silver Paths
# ---------------------------------------------------------

SILVER_PAYMENTS_PATH = (
    config["paths"]["silver"]["payments"]
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
print("LOADING BRONZE PAYMENTS DATASET")
print("=================================================")

payments_df = spark.read.parquet(
    BRONZE_PAYMENTS_PATH
)

print(
    f"Bronze Payments Count: "
    f"{payments_df.count()}"
)


# =========================================================
# INITIAL DATA INSPECTION
# =========================================================

print("\n=================================================")
print("BRONZE PAYMENTS SCHEMA")
print("=================================================")

payments_df.printSchema()


# =========================================================
# START TRANSFORMATIONS
# =========================================================

print("\n=================================================")
print("STARTING SILVER TRANSFORMATIONS")
print("=================================================")

silver_payments_df = payments_df


# =========================================================
# PAYMENT TYPE NORMALIZATION
# =========================================================

"""
Normalize payment methods for:
- deterministic grouping
- stable KPIs
- dashboard consistency
"""

print("\nApplying payment type normalization...")

silver_payments_df = (

    silver_payments_df

    .withColumn(
        "payment_type",
        lower(
            trim(col("payment_type"))
        )
    )

)


# =========================================================
# INSTALLMENT STANDARDIZATION
# =========================================================

"""
Standardize installment values.
"""

print("\nApplying installment standardization...")

silver_payments_df = (

    silver_payments_df

    .withColumn(
        "payment_sequential",
        col("payment_sequential").cast(
            IntegerType()
        )
    )

    .withColumn(
        "payment_installments",
        col("payment_installments").cast(
            IntegerType()
        )
    )

)


# =========================================================
# PAYMENT VALUE STANDARDIZATION
# =========================================================

"""
Standardize financial payment values.
"""

print("\nApplying payment value standardization...")

silver_payments_df = (

    silver_payments_df

    .withColumn(
        "payment_value",
        col("payment_value").cast(
            DecimalType(18, 2)
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

silver_payments_df = (

    silver_payments_df

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

silver_payments_df = silver_payments_df.select(

    "order_id",

    "payment_sequential",

    "payment_type",

    "payment_installments",

    "payment_value",

    "silver_loaded_at",
    "source_system",
    "transformation_version"

)


# =========================================================
# RUN VALIDATION SUITE
# =========================================================

run_payments_validation(
    source_df=payments_df,
    transformed_df=silver_payments_df
)


# =========================================================
# FINAL DATA PREVIEW
# =========================================================

print("\n=================================================")
print("SILVER PAYMENTS PREVIEW")
print("=================================================")

silver_payments_df.show(
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
    f"Silver Payments Count: "
    f"{silver_payments_df.count()}"
)


# =========================================================
# WRITE SILVER DATASET
# =========================================================

print("\n=================================================")
print("WRITING SILVER PAYMENTS DATASET")
print("=================================================")

silver_payments_df.write \
    .mode("overwrite") \
    .parquet(SILVER_PAYMENTS_PATH)

print(
    f"Silver Payments Written To: "
    f"{SILVER_PAYMENTS_PATH}"
)


# =========================================================
# STOP SPARK SESSION
# =========================================================

spark.stop()

print("\n=================================================")
print("SILVER PAYMENTS TRANSFORMATION COMPLETED")
print("=================================================")
