"""
transform_seller_acquisition_staging.py

Objective:
Assemble seller acquisition intelligence staging dataset
by combining:
- marketing-qualified leads
- seller conversion outcomes
- seller operational enrichment

This staging dataset becomes the direct analytical input for:
fct_seller_acquisition

Project:
Olist Seller Intelligence Platform

Layer:
Silver Staging

Dataset:
seller_acquisition_staging

Dataset Grain:
ONE ROW = ONE SELLER ACQUISITION EVENT
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
    when,
    datediff,
    current_timestamp,
    lit,concat
)

from pipelines.silver.utils.config_loader import (
    load_config,
    resolve_path
)

from pipelines.silver.utils.spark_session import (
    create_spark_session
)

from pipelines.silver.validations.seller_acquisition_staging_validation import (
    run_seller_acquisition_staging_validation
)


# =========================================================
# CREATE SPARK SESSION
# =========================================================

spark = create_spark_session(
    "TransformSellerAcquisitionStaging"
)


# =========================================================
# LOAD CONFIGURATION
# =========================================================

config = load_config()

# ---------------------------------------------------------
# Silver Paths
# ---------------------------------------------------------

SILVER_MQL_PATH = resolve_path(
    config["paths"]["silver"]["mql"],
    config
)

SILVER_CLOSED_DEALS_PATH = resolve_path(
    config["paths"]["silver"]["closed_deals"],
    config
)


SILVER_SELLERS_PATH = resolve_path(
    config["paths"]["silver"]["sellers"],
    config
)

# ---------------------------------------------------------
# Output Path
# ---------------------------------------------------------

SELLER_ACQUISITION_STAGING_PATH = resolve_path(
    config["paths"]["silver"][
        "seller_acquisition_staging"
    ],
    config
)

# ---------------------------------------------------------
# Metadata
# ---------------------------------------------------------

SOURCE_SYSTEM = (
    config["metadata"]["source_system"]
)

TRANSFORMATION_VERSION = (
    config["metadata"]["transformation_version"]
)


# =========================================================
# LOAD DATASETS
# =========================================================

print("\n=================================================")
print("LOADING SOURCE DATASETS")
print("=================================================")

mql_df = spark.read.parquet(
    SILVER_MQL_PATH
)

closed_deals_df = spark.read.parquet(
    SILVER_CLOSED_DEALS_PATH
)

sellers_df = spark.read.parquet(
    SILVER_SELLERS_PATH
)

print(f"MQL Count: {mql_df.count()}")
print(f"Closed Deals Count: {closed_deals_df.count()}")
print(f"Sellers Count: {sellers_df.count()}")


# =========================================================
# SELECT MQL COLUMNS
# =========================================================

mql_selected_df = mql_df.select(

    "mql_id",

    "first_contact_date",

    "landing_page_id",

    col("origin").alias(
        "marketing_origin"
    )
)


# =========================================================
# SELECT CLOSED DEALS COLUMNS
# =========================================================

closed_deals_selected_df = closed_deals_df.select(

    "mql_id",

    "seller_id",

    "won_date",

    "business_segment",

    "lead_type",

    "lead_behaviour_profile",

    "declared_monthly_revenue"
)


# =========================================================
# SELECT SELLER ENRICHMENT
# =========================================================

sellers_selected_df = sellers_df.select(

    "seller_id",

    "seller_city",

    "seller_state",

    "acquisition_source"
)


# =========================================================
# JOIN MQL + CLOSED DEALS
# =========================================================

print("\n=================================================")
print("JOINING ACQUISITION DATASETS")
print("=================================================")

staging_df = mql_selected_df.join(

    closed_deals_selected_df,

    on="mql_id",

    how="left"
)


# =========================================================
# JOIN SELLER ENRICHMENT
# =========================================================

staging_df = staging_df.join(

    sellers_selected_df,

    on="seller_id",

    how="left"
)


# =========================================================
# DERIVE CONVERSION METRICS
# =========================================================

print("\n=================================================")
print("DERIVING CONVERSION METRICS")
print("=================================================")

staging_df = staging_df.withColumn(

    "days_to_convert",

    datediff(
        col("won_date"),
        col("first_contact_date")
    )
)


# =========================================================
# CONVERTED FLAG
# =========================================================

staging_df = staging_df.withColumn(

    "converted_flag",

    when(
        col("seller_id").isNotNull(),
        True
    ).otherwise(False)
)


# =========================================================
# HIGH VALUE SELLER FLAG
# =========================================================

staging_df = staging_df.withColumn(

    "high_value_seller_flag",

    when(
        col("declared_monthly_revenue") >= 100000,
        True
    ).otherwise(False)
)


# =========================================================
# SELLER ACQUISITION SEGMENT
# =========================================================

staging_df = staging_df.withColumn(

    "seller_acquisition_segment",

    # -------------------------------------
    # Premium Prospects
    # -------------------------------------
    when(
        (
            col("declared_monthly_revenue") >= 100000
        ) &
        (
            col("days_to_convert") <= 7
        ),

        "Premium Prospect"
    )

    # -------------------------------------
    # Strategic Prospects
    # -------------------------------------
    .when(
        (
            col("declared_monthly_revenue") >= 100000
        ) &
        (
            col("days_to_convert") > 7
        ),

        "Strategic Prospect"
    )

    # -------------------------------------
    # Growth Sellers
    # -------------------------------------
    .when(
        (
            col("declared_monthly_revenue") >= 10000
        ) &
        (
            col("declared_monthly_revenue") < 100000
        ),

        "Growth Seller"
    )

    # -------------------------------------
    # Small Business Sellers
    # -------------------------------------
    .when(
        (
            col("declared_monthly_revenue") > 0
        ) &
        (
            col("declared_monthly_revenue") < 10000
        ),

        "Small Business"
    )

    # -------------------------------------
    # Behavioral Fallback
    # -------------------------------------
    .when(
        col("declared_monthly_revenue").isNull() &
        col("lead_behaviour_profile").isNotNull(),

        concat(
            lit("Behavior: "),
            col("lead_behaviour_profile")
        )
    )

    # -------------------------------------
    # Segment Fallback
    # -------------------------------------
    .when(
        col("declared_monthly_revenue").isNull() &
        col("business_segment").isNotNull(),

        concat(
            lit("Segment: "),
            col("business_segment")
        )
    )

    # -------------------------------------
    # Unknown
    # -------------------------------------
    .otherwise(
        "Unclassified"
    )
)

# =========================================================
# METADATA ENRICHMENT
# =========================================================

staging_df = staging_df.withColumn(
    "silver_loaded_at",
    current_timestamp()
)

staging_df = staging_df.withColumn(
    "source_system",
    lit(SOURCE_SYSTEM)
)

staging_df = staging_df.withColumn(
    "transformation_version",
    lit(TRANSFORMATION_VERSION)
)


# =========================================================
# FINAL COLUMN SELECTION
# =========================================================

print("\n=================================================")
print("FINAL COLUMN SELECTION")
print("=================================================")

staging_df = staging_df.select(

    "mql_id",

    "seller_id",

    "first_contact_date",

    "won_date",

    "landing_page_id",

    "marketing_origin",

    "acquisition_source",

    "business_segment",

    "lead_type",

    "lead_behaviour_profile",

    "declared_monthly_revenue",

    "seller_city",

    "seller_state",

    "days_to_convert",

    "converted_flag",

    "high_value_seller_flag",

    "seller_acquisition_segment",

    "silver_loaded_at",
    
    "source_system",

    "transformation_version"
)


# =========================================================
# VALIDATIONS
# =========================================================

print("\n=================================================")
print("RUNNING VALIDATIONS")
print("=================================================")

run_seller_acquisition_staging_validation(
    staging_df
)


# =========================================================
# WRITE STAGING DATASET
# =========================================================

print("\n=================================================")
print("WRITING SELLER ACQUISITION STAGING")
print("=================================================")

staging_df.write.mode("overwrite").parquet(
    SELLER_ACQUISITION_STAGING_PATH
)

print("Seller Acquisition Staging Written Successfully")


# =========================================================
# FINAL SUMMARY
# =========================================================

print("\n=================================================")
print("SELLER ACQUISITION STAGING COMPLETED")
print("=================================================")

print(f"Final Row Count: {staging_df.count()}")

staging_df.printSchema()

spark.stop()