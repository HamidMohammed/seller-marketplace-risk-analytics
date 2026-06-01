"""
build_dim_product.py

Gold Layer

Conformed Product Dimension

Objective:
Build Product 360 Dimension
for seller fulfillment,
delivery performance,
sales analytics,
and product intelligence.

Grain:
ONE ROW = ONE PRODUCT
"""

# =========================================================
# PROJECT ROOT SETUP
# =========================================================

import sys
import os

project_root = os.path.abspath(
    os.path.join(
        os.path.dirname(__file__),
        "../../../../"
    )
)

if project_root not in sys.path:
    sys.path.append(project_root)

# =========================================================
# IMPORTS
# =========================================================

from pyspark.sql.window import Window

from pyspark.sql.functions import (
    row_number,
    current_timestamp,
    col
)

from pipelines.silver.utils.spark_session import (
    create_spark_session
)

from pipelines.silver.utils.config_loader import (
    load_config
)

from pipelines.gold.dimensions.product.dim_product_validation import (
    run_dim_product_validation
)

# =========================================================
# SPARK SESSION
# =========================================================

spark = create_spark_session(
    "BuildDimProduct"
)

# =========================================================
# CONFIG
# =========================================================

config = load_config()

SILVER_PRODUCTS_PATH = (
    config["paths"]["silver"]["products"]
)

DIM_PRODUCT_PATH = (
    config["paths"]["gold"]["dim_product"]
)

# =========================================================
# LOAD PRODUCTS
# =========================================================

print("=" * 60)
print("LOADING PRODUCTS")
print("=" * 60)

product_df = spark.read.parquet(
    SILVER_PRODUCTS_PATH
)

print(
    f"Product Count: {product_df.count()}"
)

# =========================================================
# SURROGATE KEY
# =========================================================

product_window = Window.orderBy(
    "product_id"
)

product_df = product_df.withColumn(

    "product_sk",

    row_number().over(
        product_window
    )
)

# =========================================================
# AUDIT COLUMN
# =========================================================

product_df = product_df.withColumn(

    "gold_loaded_at",

    current_timestamp()
)

# =========================================================
# FINAL SELECT
# =========================================================

dim_product_df = product_df.select(

    # Surrogate Key

    "product_sk",

    # Business Key

    "product_id",

    # Category Attributes

    "product_category_name",

    "product_category_name_english",

    # Catalog Attributes

    "product_name_lenght",

    "product_description_lenght",

    "product_photos_qty",

    # Physical Attributes

    "product_weight_g",

    "product_length_cm",

    "product_height_cm",

    "product_width_cm",

    "product_volume_cm3",

    # Business Classifications

    "product_size_category",

    "heavy_product_flag",

    "logistics_completeness_flag",

    "catalog_completeness_flag",

    # Governance

    "source_system",

    "transformation_version",

    "gold_loaded_at"
)

# =========================================================
# VALIDATION
# =========================================================

run_dim_product_validation(
    dim_product_df
)

# =========================================================
# WRITE
# =========================================================

print("=" * 60)
print("WRITING DIM PRODUCT")
print("=" * 60)

dim_product_df.write.mode(
    "overwrite"
).parquet(
    DIM_PRODUCT_PATH
)

print(
    f"Dim Product Written To: "
    f"{DIM_PRODUCT_PATH}"
)

print(
    f"Final Row Count: "
    f"{dim_product_df.count()}"
)

# =========================================================
# STOP SPARK
# =========================================================

spark.stop()