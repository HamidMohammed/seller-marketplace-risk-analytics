"""
build_dim_seller.py

Objective:
Build Seller 360 Conformed Dimension.

Dimension:
dim_seller

Grain:
ONE ROW = ONE SELLER

Layer:
Gold
"""

# =====================================================
# IMPORTS
# =====================================================

import sys
import os

from pyspark.sql.functions import (
    col,
    when,
    lit,
    current_timestamp,
    current_date,
    row_number
)

from pyspark.sql.window import Window

# =====================================================
# PROJECT ROOT
# =====================================================

project_root = os.path.abspath(
    os.path.join(
        os.path.dirname(__file__),
        "../../../../"
    )
)

if project_root not in sys.path:
    sys.path.append(project_root)
print(f"Project Root Added: {project_root}")

# =====================================================
# PROJECT IMPORTS
# =====================================================

from pipelines.silver.utils.spark_session import (
    create_spark_session
)

from pipelines.silver.utils.config_loader import (
    load_config,
    resolve_path
)

from pipelines.gold.dimensions.seller.dim_seller_validation import (
    run_dim_seller_validation
)

# =====================================================
# SPARK
# =====================================================

spark = create_spark_session(
    "BuildDimSeller"
)

# =====================================================
# CONFIG
# =====================================================

config = load_config()

SILVER_SELLERS_PATH = resolve_path(
    config["paths"]["silver"]["sellers"],
    config
)

DIM_SELLER_PATH = resolve_path(
    config["paths"]["gold"]["dim_seller"],
    config
)

SELLER_ACQUISITION_STAGING_PATH = resolve_path(
    config["paths"]["silver"][
        "seller_acquisition_staging"
    ],
    config
)

SOURCE_SYSTEM = (
    config["metadata"]["source_system"]
)

TRANSFORMATION_VERSION = (
    config["metadata"]["transformation_version"]
)

# =====================================================
# LOAD SELLERS
# =====================================================

print("=" * 60)
print("LOADING SELLERS")
print("=" * 60)

seller_df = spark.read.parquet(
    SILVER_SELLERS_PATH
)

seller_acquisition_df = spark.read.parquet(
    SELLER_ACQUISITION_STAGING_PATH
)

seller_acquisition_df = seller_acquisition_df.select(

    "seller_id",

    col("marketing_origin"),

    col("business_segment").alias(
        "acquisition_business_segment"
    ),

    col("lead_type").alias(
        "acquisition_lead_type"
    ),

    col("lead_behaviour_profile").alias(
    "acquisition_lead_behaviour_profile"
    ),

    col("days_to_convert"),

    col("converted_flag"),

    col("seller_acquisition_segment")
)

seller_df = seller_df.join(

    seller_acquisition_df,

    on="seller_id",

    how="left"
)

seller_df = seller_df.fillna({

    "marketing_origin": "Not Tracked",

    "acquisition_business_segment": "Not Tracked",

    "acquisition_lead_type": "Not Tracked",

    "acquisition_lead_behaviour_profile": "Not Tracked",

    "seller_acquisition_segment": "Not Tracked"
})

print(
    f"Seller Count: {seller_df.count()}"
)

# =====================================================
# REGION CLASSIFICATION
# =====================================================

seller_df = seller_df.withColumn(

    "seller_region",

    when(
        col("seller_state").isin(
            "SP", "RJ", "MG", "ES"
        ),
        "Southeast"

    ).when(
        col("seller_state").isin(
            "PR", "SC", "RS"
        ),
        "South"

    ).when(
        col("seller_state").isin(
            "GO", "MT", "MS", "DF"
        ),
        "Central-West"

    ).when(
        col("seller_state").isin(
            "BA", "PE", "CE", "PB",
            "RN", "AL", "SE", "PI",
            "MA"
        ),
        "Northeast"

    ).when(
        col("seller_state").isin(
            "AM", "PA", "AC", "RO",
            "RR", "AP", "TO"
        ),
        "North"

    ).otherwise(
        "Unknown"
    )
)

# =====================================================
# LOCATION TYPE
# =====================================================

seller_df = seller_df.withColumn(

    "seller_location_type",

    when(
        col("seller_city").isin(
            "sao paulo",
            "rio de janeiro",
            "brasilia",
            "salvador",
            "fortaleza",
            "belo horizonte",
            "curitiba",
            "manaus",
            "recife",
            "porto alegre"
        ),

        "Metropolitan"

    ).when(
        col("seller_state").isin(
            "SP",
            "RJ",
            "MG"
        ),

        "Urban"

    ).otherwise(
        "Regional"
    )
)


# =====================================================
# SCD TYPE 2 COLUMNS
# =====================================================

seller_df = seller_df.withColumn(
    "effective_start_date",
    current_date()
)

seller_df = seller_df.withColumn(
    "effective_end_date",
    lit(None).cast("date")
)

seller_df = seller_df.withColumn(
    "is_current",
    lit(True)
)

# =====================================================
# SURROGATE KEY
# =====================================================

seller_window = Window.orderBy(
    "seller_id"
)

seller_df = seller_df.withColumn(

    "seller_sk",

    row_number().over(
        seller_window
    )
)

# =====================================================
# AUDIT COLUMNS
# =====================================================

seller_df = seller_df.withColumn(
    "gold_loaded_at",
    current_timestamp()
)

# =====================================================
# FINAL SELECT
# =====================================================

dim_seller_df = seller_df.select(

    "seller_sk",

    "seller_id",

    "seller_zip_code_prefix",

    "seller_city",

    "seller_state",

    "seller_region",

    "median_latitude",

    "median_longitude",
    # =====================================================
    # ACQUISITION ATTRIBUTES
    # =====================================================

    "marketing_origin",

    "acquisition_source",
    
    "acquisition_business_segment",

    "acquisition_lead_type",

    "acquisition_lead_behaviour_profile",

    "days_to_convert",

    "converted_flag",

    "seller_acquisition_segment",
    
    "seller_location_type",

    "effective_start_date",

    "effective_end_date",

    "is_current",

    "source_system",

    "transformation_version",

    "gold_loaded_at"
)

# =====================================================
# VALIDATION
# =====================================================

run_dim_seller_validation(
    dim_seller_df
)

# =====================================================
# WRITE
# =====================================================

print("=" * 60)
print("WRITING DIM SELLER")
print("=" * 60)

dim_seller_df.write.mode(
    "overwrite"
).parquet(
    DIM_SELLER_PATH
)

print(
    "dim_seller written successfully."
)

print(
    f"Final Row Count: "
    f"{dim_seller_df.count()}"
)

spark.stop()