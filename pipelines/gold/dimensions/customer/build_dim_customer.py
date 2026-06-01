"""
build_dim_customer.py

Objective:
Build Customer 360 Conformed Dimension.

Dimension:
dim_customer

Grain:
ONE ROW = ONE CUSTOMER

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
    current_timestamp,
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

# =====================================================
# PROJECT IMPORTS
# =====================================================

from pipelines.silver.utils.spark_session import (
    create_spark_session
)

from pipelines.silver.utils.config_loader import (
    load_config
)

from pipelines.gold.dimensions.customer.dim_customer_validation import (
    run_dim_customer_validation
)

# =====================================================
# SPARK
# =====================================================

spark = create_spark_session(
    "BuildDimCustomer"
)

# =====================================================
# CONFIG
# =====================================================

config = load_config()

SILVER_CUSTOMERS_PATH = (
    config["paths"]["silver"]["customers"]
)

DIM_CUSTOMER_PATH = (
    config["paths"]["gold"]["dim_customer"]
)

# =====================================================
# LOAD CUSTOMERS
# =====================================================

print("=" * 60)
print("LOADING CUSTOMERS")
print("=" * 60)

customer_df = spark.read.parquet(
    SILVER_CUSTOMERS_PATH
)

print(
    f"Customer Count: {customer_df.count()}"
)

# =====================================================
# REGION CLASSIFICATION
# =====================================================

customer_df = customer_df.withColumn(

    "customer_region",

    when(
        col("customer_state").isin(
            "SP", "RJ", "MG", "ES"
        ),
        "Southeast"

    ).when(
        col("customer_state").isin(
            "PR", "SC", "RS"
        ),
        "South"

    ).when(
        col("customer_state").isin(
            "GO", "MT", "MS", "DF"
        ),
        "Central-West"

    ).when(
        col("customer_state").isin(
            "BA", "PE", "CE", "PB",
            "RN", "AL", "SE", "PI",
            "MA"
        ),
        "Northeast"

    ).when(
        col("customer_state").isin(
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

customer_df = customer_df.withColumn(

    "customer_location_type",

    when(
        col("customer_city").isin(
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
        col("customer_state").isin(
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
# SURROGATE KEY
# =====================================================

customer_window = Window.orderBy(
    "customer_id"
)

customer_df = customer_df.withColumn(

    "customer_sk",

    row_number().over(
        customer_window
    )
)

# =====================================================
# AUDIT COLUMN
# =====================================================

customer_df = customer_df.withColumn(
    "gold_loaded_at",
    current_timestamp()
)

# =====================================================
# FINAL SELECT
# =====================================================

dim_customer_df = customer_df.select(

    "customer_sk",

    "customer_id",

    "customer_unique_id",

    "customer_zip_code_prefix",

    "customer_city",

    "customer_state",

    "customer_region",

    "customer_location_type",

    "median_latitude",

    "median_longitude",

    "source_system",

    "transformation_version",

    "gold_loaded_at"
)
customer_df.filter(
    col("median_latitude").isNull() |
    col("median_longitude").isNull()
).select(
    "customer_zip_code_prefix",
    "customer_city",
    "customer_state"
).show(
    20,
    truncate=False
)


customer_df.filter(
    col("median_latitude").isNull() |
    col("median_longitude").isNull()
).groupBy(
    "customer_state"
).count().orderBy(
    col("count").desc()
).show()
# =====================================================
# VALIDATION
# =====================================================

run_dim_customer_validation(
    dim_customer_df
)

# =====================================================
# WRITE
# =====================================================

print("=" * 60)
print("WRITING DIM CUSTOMER")
print("=" * 60)

dim_customer_df.write.mode(
    "overwrite"
).parquet(
    DIM_CUSTOMER_PATH
)

print(
    "dim_customer written successfully."
)

print(
    f"Final Row Count: "
    f"{dim_customer_df.count()}"
)

spark.stop()