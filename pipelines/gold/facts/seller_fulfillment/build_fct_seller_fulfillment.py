"""
build_fct_seller_fulfillment.py

Objective:
Build Gold Seller Fulfillment Fact Table.

Fact:
fct_seller_fulfillment

Grain:
ONE ROW = ONE ORDER ITEM FULFILLED BY ONE SELLER

Source:
seller_fulfillment_staging

Dimensions:
dim_seller
dim_product
dim_date
"""

# =====================================================
# IMPORTS
# =====================================================

import sys
import os

from pyspark.sql.window import Window

from pyspark.sql.functions import (
    col,
    current_timestamp,
    row_number,
    when,
    to_date,
    lit
)

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

from pipelines.gold.facts.seller_fulfillment.fct_seller_fulfillment_validation import (
    run_seller_fulfillment_fact_validation
)

# =====================================================
# SPARK
# =====================================================

spark = create_spark_session(
    "BuildFactSellerFulfillment"
)

# =====================================================
# CONFIG
# =====================================================

config = load_config()

SELLER_FULFILLMENT_STAGING_PATH = (
    config["paths"]["silver"][
        "seller_fulfillment_staging"
    ]
)

SILVER_PRODUCTS_PATH = (
    config["paths"]["silver"][
        "products"
    ]
)

DIM_SELLER_PATH = (
    config["paths"]["gold"][
        "dim_seller"
    ]
)

DIM_PRODUCT_PATH = (
    config["paths"]["gold"][
        "dim_product"
    ]
)

DIM_DATE_PATH = (
    config["paths"]["gold"][
        "dim_date"
    ]
)

FCT_SELLER_FULFILLMENT_PATH = (
    config["paths"]["gold"][
        "fct_seller_fulfillment"
    ]
)

SOURCE_SYSTEM = (
    config["metadata"]["source_system"]
)

TRANSFORMATION_VERSION = (
    config["metadata"]["transformation_version"]
)

# =====================================================
# LOAD DATASETS
# =====================================================

staging_df = spark.read.parquet(
    SELLER_FULFILLMENT_STAGING_PATH
)

silver_products_df = spark.read.parquet(
    SILVER_PRODUCTS_PATH
)


dim_seller_df = spark.read.parquet(
    DIM_SELLER_PATH
)

dim_product_df = spark.read.parquet(
    DIM_PRODUCT_PATH
)

dim_date_df = spark.read.parquet(
    DIM_DATE_PATH
)

# =====================================================
# SELLER LOOKUP
# =====================================================

seller_lookup = (

    dim_seller_df

    .filter(
        col("is_current") == True
    )

    .select(
        "seller_id",
        "seller_sk"
    )
)

fact_df = staging_df.join(

    seller_lookup,

    staging_df["seller_id"] ==
    seller_lookup["seller_id"],

    "left"
)

fact_df = (

    fact_df

    .drop(
        seller_lookup["seller_id"]
    )

    .withColumnRenamed(
        "seller_sk",
        "seller_sk_fk"
    )
)

# =====================================================
# PRODUCT LOOKUP
# =====================================================

product_lookup = dim_product_df.select(
    "product_id",
    "product_sk"
)

fact_df = fact_df.join(

    product_lookup,

    on="product_id",

    how="left"
)

fact_df = fact_df.withColumnRenamed(
    "product_sk",
    "product_sk_fk"
)

# =====================================================
# DATE LOOKUP
# =====================================================

fact_df = fact_df.withColumn(

    "purchase_date",

    to_date(
        col(
            "order_purchase_timestamp"
        )
    )
)

date_lookup = dim_date_df.select(
    "date_sk",
    "full_date"
)

fact_df = fact_df.join(

    date_lookup,

    fact_df["purchase_date"] ==
    date_lookup["full_date"],

    "left"
)

fact_df = fact_df.withColumnRenamed(
    "date_sk",
    "purchase_date_sk"
)

# =====================================================
# BUSINESS KPI FLAGS
# =====================================================

fact_df = fact_df.withColumn(

    "high_freight_item_flag",

    when(
        col("freight_ratio") >= 0.30,
        True
    ).otherwise(False)
)

fact_df = fact_df.withColumn(

    "high_workload_flag",

    when(
        col("workload_bucket").isin(
            "High Volume",
            "Overloaded"
        ),
        True
    ).otherwise(False)
)

# =====================================================
# FACT SURROGATE KEY
# =====================================================

fact_window = Window.orderBy(
    "order_id",
    "order_item_id"
)

fact_df = fact_df.withColumn(

    "fulfillment_fact_sk",

    row_number().over(
        fact_window
    )
)

# =====================================================
# AUDIT COLUMNS
# =====================================================

fact_df = fact_df.withColumn(
    "gold_loaded_at",
    current_timestamp()
)

fact_df = fact_df.withColumn(
    "source_system",
    lit(SOURCE_SYSTEM)
)

fact_df = fact_df.withColumn(
    "transformation_version",
    lit(TRANSFORMATION_VERSION)
)

fact_df.filter(
col("product_sk_fk").isNull()
).groupBy(
    "product_id"
).count().show(
    50,
    truncate=False
)
silver_products_df.filter(

    col("product_id").isin(

        "5eb564652db742ff8f28759cd8d2652a",

        "09ff539a621711667c43eba6a3bd8466"

    )

).show(
    truncate=False
)

dim_product_df.filter(

    col("product_id").isin(

        "5eb564652db742ff8f28759cd8d2652a",

        "09ff539a621711667c43eba6a3bd8466"

    )

).show(
    truncate=False
)

# =====================================================
# FINAL SELECT
# =====================================================

fact_df = fact_df.select(

    "fulfillment_fact_sk",

    "order_id",
    "order_item_id",

    "seller_sk_fk",
    "product_sk_fk",

    "purchase_date_sk",

    "price",
    "freight_value",

    "freight_ratio",

    "product_volume_cm3",

    "seller_item_count_in_order",

    "seller_monthly_orders",

    "workload_bucket",

    "is_overloaded_seller",

    "high_workload_flag",

    "high_freight_item_flag",

    "acquisition_source",

    "source_system",

    "transformation_version",

    "gold_loaded_at"
)

# =====================================================
# VALIDATION
# =====================================================

run_seller_fulfillment_fact_validation(
    fact_df
)

# =====================================================
# WRITE
# =====================================================

fact_df.write.mode(
    "overwrite"
).parquet(
    FCT_SELLER_FULFILLMENT_PATH
)

print(
    f"Final Row Count: "
    f"{fact_df.count():,}"
)

print(
    "Seller Fulfillment Fact Written Successfully"
)




spark.stop()

