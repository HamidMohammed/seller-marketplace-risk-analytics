"""
transform_closed_deals.py

Objective:
Transform raw Bronze commercial conversion records into
trusted Silver sales operational intelligence.

Pipeline Responsibilities:
- commercial deal standardization
- business-segment normalization
- sales-channel normalization
- seller-type normalization
- timestamp standardization
- commercial integrity enforcement
- metadata enrichment
- validation-driven transformation

Project:
Olist Seller Intelligence Platform

Layer:
Silver

Dataset:
silver_closed_deals

Dataset Grain:
ONE ROW = ONE CLOSED COMMERCIAL DEAL
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
    load_config
)

from pipelines.silver.utils.spark_session import (
    create_spark_session
)

from pipelines.silver.validations.closed_deals_validation import (
    run_closed_deals_validation
)


# =========================================================
# CREATE SPARK SESSION
# =========================================================

spark = create_spark_session(
    "TransformSilverClosedDeals"
)


# =========================================================
# LOAD CONFIGURATION
# =========================================================

config = load_config()

# ---------------------------------------------------------
# Bronze Paths
# ---------------------------------------------------------

BRONZE_CLOSED_DEALS_PATH = (
    config["paths"]["bronze"]["closed_deals"]
)

# ---------------------------------------------------------
# Silver Paths
# ---------------------------------------------------------

SILVER_CLOSED_DEALS_PATH = (
    config["paths"]["silver"]["closed_deals"]
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
print("LOADING BRONZE CLOSED DEALS DATASET")
print("=================================================")

closed_deals_df = spark.read.parquet(
    BRONZE_CLOSED_DEALS_PATH
)

print(
    f"Bronze Closed Deals Count: "
    f"{closed_deals_df.count()}"
)


# =========================================================
# INITIAL DATA INSPECTION
# =========================================================

print("\n=================================================")
print("BRONZE CLOSED DEALS SCHEMA")
print("=================================================")

closed_deals_df.printSchema()


# =========================================================
# START TRANSFORMATIONS
# =========================================================

print("\n=================================================")
print("STARTING SILVER TRANSFORMATIONS")
print("=================================================")

silver_closed_deals_df = closed_deals_df


# =========================================================
# MQL ID STANDARDIZATION
# =========================================================

"""
Standardize CRM acquisition identifiers.
"""

print("\nApplying MQL ID standardization...")

silver_closed_deals_df = (

    silver_closed_deals_df

    .withColumn(
        "mql_id",
        trim(col("mql_id"))
    )

)


# =========================================================
# BUSINESS SEGMENT NORMALIZATION
# =========================================================

"""
Normalize business-segment semantics.
"""

print("\nApplying business segment normalization...")

silver_closed_deals_df = (

    silver_closed_deals_df

    .withColumn(

        "business_segment",

        when(
            col("business_segment").isNotNull(),

            lower(
                trim(
                    col("business_segment")
                )
            )

        ).otherwise(None)

    )

)




# =========================================================
# BUSINESS TYPE NORMALIZATION
# =========================================================

"""
Normalize business-type semantics.
"""

print("\nApplying business type normalization...")

silver_closed_deals_df = (

    silver_closed_deals_df

    .withColumn(

        "business_type",

        when(
            col("business_type").isNotNull(),

            lower(
                trim(
                    col("business_type")
                )
            )

        ).otherwise(None)

    )

)


# =========================================================
# TIMESTAMP STANDARDIZATION
# =========================================================

"""
Standardize commercial funnel chronology.
"""

print("\nApplying timestamp standardization...")

silver_closed_deals_df = (

    silver_closed_deals_df

    .withColumn(

        "won_date",

        to_timestamp(
            col("won_date"),
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

silver_closed_deals_df = (

    silver_closed_deals_df

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

silver_closed_deals_df = silver_closed_deals_df.select(

    "mql_id",

    "seller_id",

    "sdr_id",

    "sr_id",

    "won_date",

    "business_segment",

    "lead_type",

    "lead_behaviour_profile",

    "has_company",

    "has_gtin",

    "average_stock",

    "business_type",

    "declared_product_catalog_size",

    "declared_monthly_revenue",

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

print("\nMaterializing Silver Closed Deals DataFrame...")

silver_closed_deals_df = (
    silver_closed_deals_df.cache()
)

silver_closed_deals_df.count()


# =========================================================
# RUN VALIDATION SUITE
# =========================================================

run_closed_deals_validation(
    source_df=closed_deals_df,
    transformed_df=silver_closed_deals_df
)


# =========================================================
# FINAL DATA PREVIEW
# =========================================================

print("\n=================================================")
print("SILVER CLOSED DEALS PREVIEW")
print("=================================================")

silver_closed_deals_df.show(
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
    f"Silver Closed Deals Count: "
    f"{silver_closed_deals_df.count()}"
)


# =========================================================
# WRITE SILVER DATASET
# =========================================================

print("\n=================================================")
print("WRITING SILVER CLOSED DEALS DATASET")
print("=================================================")

silver_closed_deals_df.write \
    .mode("overwrite") \
    .parquet(SILVER_CLOSED_DEALS_PATH)

print(
    f"Silver Closed Deals Written To: "
    f"{SILVER_CLOSED_DEALS_PATH}"
)


# =========================================================
# STOP SPARK SESSION
# =========================================================

spark.stop()

print("\n=================================================")
print("SILVER CLOSED DEALS TRANSFORMATION COMPLETED")
print("=================================================")
