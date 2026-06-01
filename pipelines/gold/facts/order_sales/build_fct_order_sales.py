"""
build_fct_order_sales.py

Objective:
Build Gold Order Sales Fact Table

Fact:
fct_order_sales

Grain:
ONE ROW = ONE ORDER ITEM SOLD
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

from pipelines.gold.facts.order_sales.fct_order_sales_validation import (
    run_fct_order_sales_validation
)

# =====================================================
# SPARK
# =====================================================

spark = create_spark_session(
    "BuildFactOrderSales"
)

# =====================================================
# CONFIG
# =====================================================

config = load_config()

SALES_STAGING_PATH = (
    config["paths"]["silver"][
        "sales_staging"
    ]
)

DIM_PRODUCT_PATH = (
    config["paths"]["gold"][
        "dim_product"
    ]
)

DIM_SELLER_PATH = (
    config["paths"]["gold"][
        "dim_seller"
    ]
)

DIM_DATE_PATH = (
    config["paths"]["gold"][
        "dim_date"
    ]
)

DIM_CUSTOMER_PATH = (
    config["paths"]["gold"][
        "dim_customer"
    ]
)

FCT_ORDER_SALES_PATH = (
    config["paths"]["gold"][
        "fct_order_sales"
    ]
)

SOURCE_SYSTEM = (
    config["metadata"]["source_system"]
)

TRANSFORMATION_VERSION = (
    config["metadata"]["transformation_version"]
)

# =====================================================
# LOAD DATA
# =====================================================

sales_df = spark.read.parquet(
    SALES_STAGING_PATH
)

dim_product_df = spark.read.parquet(
    DIM_PRODUCT_PATH
)

dim_seller_df = spark.read.parquet(
    DIM_SELLER_PATH
)

dim_date_df = spark.read.parquet(
    DIM_DATE_PATH
)

dim_customer_df = spark.read.parquet(
    DIM_CUSTOMER_PATH
)

# =====================================================
# PRODUCT LOOKUP
# =====================================================

product_lookup = dim_product_df.select(
    "product_id",
    "product_sk"
)

customer_lookup = dim_customer_df.select(

    "customer_id",

    "customer_sk"

)
fact_df = sales_df.join(

    product_lookup,

    on="product_id",

    how="left"
)

fact_df = fact_df.withColumnRenamed(
    "product_sk",
    "product_sk_fk"
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

fact_df = fact_df.join(

    seller_lookup,

    on="seller_id",

    how="left"
)

fact_df = fact_df.withColumnRenamed(
    "seller_sk",
    "seller_sk_fk"
)

# =====================================================
# CUSTOMER LOOKUP
# =====================================================

fact_df = fact_df.join(

    customer_lookup,

    on="customer_id",

    how="left"

)

fact_df = fact_df.withColumnRenamed(

    "customer_sk",

    "customer_sk_fk"

)
# =====================================================
# DATE LOOKUP
# =====================================================

fact_df = fact_df.withColumn(

    "sales_date",

    to_date(
        col(
            "order_purchase_timestamp"
        )
    )
)

date_lookup = dim_date_df.select(

    col("date_sk").alias(
        "sales_date_sk"
    ),

    col("full_date").alias(
        "sales_date_key"
    )
)

fact_df = fact_df.join(

    date_lookup,

    fact_df["sales_date"] ==
    date_lookup["sales_date_key"],

    "left"
)

fact_df = fact_df.drop(
    "sales_date",
    "sales_date_key"
)

# =====================================================
# HIGH FREIGHT FLAG
# =====================================================

fact_df = fact_df.withColumn(

    "high_freight_item_flag",

    when(
        col("freight_ratio") > 0.30,
        True
    ).otherwise(False)
)

# =====================================================
# FACT SK
# =====================================================

fact_window = Window.orderBy(

    "order_id",

    "order_item_id"
)

fact_df = fact_df.withColumn(

    "sales_fact_sk",

    row_number().over(
        fact_window
    )
)

# =====================================================
# AUDIT
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

# =====================================================
# FINAL SELECT
# =====================================================

fact_df = fact_df.select(

    "sales_fact_sk",

    "order_id",

    "order_item_id",

    "product_sk_fk",

    "seller_sk_fk",
    
    "customer_sk_fk",

    "sales_date_sk",

    "price",

    "freight_value",

    "gross_item_value",

    "total_order_item_value",

    "allocated_payment_value",

    "item_sales_ratio",

    "freight_ratio",

    "product_volume_cm3",

    "seller_item_count_in_order",

    "total_payment_installments",

    "installment_flag",

    "high_ticket_order_flag",

    "high_freight_item_flag",

    "source_system",

    "transformation_version",

    "gold_loaded_at"
)

# =====================================================
# VALIDATION
# =====================================================

run_fct_order_sales_validation(
    fact_df
)

# =====================================================
# WRITE
# =====================================================

fact_df.write.mode(
    "overwrite"
).parquet(
    FCT_ORDER_SALES_PATH
)

print(
    f"Final Row Count: "
    f"{fact_df.count():,}"
)

spark.stop()