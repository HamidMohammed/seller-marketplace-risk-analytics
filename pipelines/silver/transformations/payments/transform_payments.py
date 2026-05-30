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

SILVER_ORDERS_PATH = (
    config["paths"]["silver"]["orders"]
)

SILVER_PAYMENTS_QUARANTINE_PATH = (
    config["paths"]["silver"]["payments_quarantine"]
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

print("\n=================================================")
print("LOADING SILVER ORDERS DATASET")
print("=================================================")

orders_df = spark.read.parquet(
    SILVER_ORDERS_PATH
).select("order_id")

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
# QUARANTINE RULE 1
# NULL ORDER ID
# =========================================================

print("\nIdentifying NULL order_id payments...")

null_order_payments_df = (

    silver_payments_df

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
# ORPHAN PAYMENTS
# =========================================================

print("\nIdentifying orphan payments...")

orphan_payments_df = (

    silver_payments_df

    .join(

        orders_df,

        on="order_id",

        how="left_anti"

    )

    .withColumn(
        "quarantine_reason",
        lit("ORPHAN_PAYMENT")
    )

)


# =========================================================
# QUARANTINE RULE 3
# NEGATIVE PAYMENT VALUE
# =========================================================

print("\nIdentifying negative payments...")

negative_payment_df = (

    silver_payments_df

    .filter(
        col("payment_value") < 0
    )

    .withColumn(
        "quarantine_reason",
        lit("NEGATIVE_PAYMENT_VALUE")
    )

)


# =========================================================
# QUARANTINE RULE 4
# NEGATIVE INSTALLMENTS
# =========================================================

print("\nIdentifying negative installments...")

negative_installments_df = (

    silver_payments_df

    .filter(
        col("payment_installments") < 0
    )

    .withColumn(
        "quarantine_reason",
        lit("NEGATIVE_INSTALLMENTS")
    )

)


# =========================================================
# BUILD QUARANTINE DATASET
# =========================================================

print("\nBuilding payments quarantine dataset...")

payments_quarantine_df = (

    null_order_payments_df
    .unionByName(
        orphan_payments_df
    )
    .unionByName(
        negative_payment_df
    )
    .unionByName(
        negative_installments_df
    )
    .dropDuplicates(
        [
            "order_id",
            "payment_sequential"
        ]
    )

)

print(
    f"Quarantined Payments: "
    f"{payments_quarantine_df.count()}"
)


# =========================================================
# BUILD CLEAN DATASET
# =========================================================

print("\nBuilding clean payments dataset...")

clean_payments_df = (
    silver_payments_df
    .join(
        payments_quarantine_df.select(
            "order_id",
            "payment_sequential"
        ),
        on=[
            "order_id",
            "payment_sequential"
        ],
        how="left_anti"
    )

)

print(
    f"Clean Payments: "
    f"{clean_payments_df.count()}"
)


# =========================================================
# INSTALLMENT FLAG
# =========================================================

clean_payments_df = clean_payments_df.withColumn(

    "installment_flag",
    when(
        col("payment_installments") > 1,
        True
    ).otherwise(
        False
    )

)


# =========================================================
# HIGH INSTALLMENT FLAG
# =========================================================

clean_payments_df = clean_payments_df.withColumn(

    "high_installment_flag",

    when(
        col("payment_installments") >= 12,
        True
    ).otherwise(
        False
    )

)


# =========================================================
# PAYMENT SIZE CATEGORY
# =========================================================

clean_payments_df = clean_payments_df.withColumn(

    "payment_size_category",

    when(
        col("payment_value") < 100,
        "Small"
    )

    .when(
        col("payment_value") < 500,
        "Medium"
    )

    .when(
        col("payment_value") < 1000,
        "Large"
    )

    .otherwise(
        "Enterprise"
    )

)

# =========================================================
# METADATA ENRICHMENT
# =========================================================

print("\nApplying metadata enrichment...")

clean_payments_df = (

    clean_payments_df

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

print("\nApplying final schema ordering...")

clean_payments_df = clean_payments_df.select(

    "order_id",

    "payment_sequential",

    "payment_type",

    "payment_installments",

    "payment_value",

    "installment_flag",

    "high_installment_flag",

    "payment_size_category",

    "silver_loaded_at",
    "source_system",
    "transformation_version"

)


# =========================================================
# MATERIALIZE DATAFRAME
# =========================================================

print(
    "\nMaterializing clean payments dataset..."
)

clean_payments_df = clean_payments_df.cache()

clean_payments_df.count()


# =========================================================
# RUN VALIDATION SUITE
# =========================================================

run_payments_validation(

    source_df=payments_df,

    transformed_df=clean_payments_df,

    quarantine_df=payments_quarantine_df

)


# =========================================================
# QUARANTINE PREVIEW
# =========================================================

print("\n=================================================")
print("PAYMENTS QUARANTINE PREVIEW")
print("=================================================")

payments_quarantine_df.show(
    10,
    truncate=False
)


# =========================================================
# CLEAN DATA PREVIEW
# =========================================================

print("\n=================================================")
print("CLEAN PAYMENTS PREVIEW")
print("=================================================")

clean_payments_df.show(
    10,
    truncate=False
)


# =========================================================
# FINAL COUNTS
# =========================================================

print("\n=================================================")
print("FINAL ROW COUNTS")
print("=================================================")

print(
    f"Clean Payments Count: "
    f"{clean_payments_df.count()}"
)

print(
    f"Quarantined Payments Count: "
    f"{payments_quarantine_df.count()}"
)


# =========================================================
# WRITE QUARANTINE DATASET
# =========================================================

print("\n=================================================")
print("WRITING PAYMENTS QUARANTINE DATASET")
print("=================================================")

payments_quarantine_df.write \
    .mode("overwrite") \
    .parquet(
        SILVER_PAYMENTS_QUARANTINE_PATH
    )

print(
    f"Payments Quarantine Written To: "
    f"{SILVER_PAYMENTS_QUARANTINE_PATH}"
)


# =========================================================
# WRITE CLEAN PAYMENTS DATASET
# =========================================================

print("\n=================================================")
print("WRITING SILVER PAYMENTS DATASET")
print("=================================================")

clean_payments_df.write \
    .mode("overwrite") \
    .parquet(
        SILVER_PAYMENTS_PATH
    )

print(
    f"Silver Payments Written To: "
    f"{SILVER_PAYMENTS_PATH}"
)


# =========================================================
# FINAL SUMMARY
# =========================================================

print("\n=================================================")
print("PAYMENTS HARDENING COMPLETED")
print("=================================================")

print(
    f"Clean Payments: "
    f"{clean_payments_df.count()}"
)

print(
    f"Quarantined Payments: "
    f"{payments_quarantine_df.count()}"
)


# =========================================================
# STOP SPARK SESSION
# =========================================================

spark.stop()