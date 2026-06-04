"""
transform_products.py

Objective:
Transform raw Bronze product registry data into
trusted Silver product dimensional intelligence.

Pipeline Responsibilities:
- product standardization
- category normalization
- logistics standardization
- dimensional integrity enforcement
- product volume derivation
- metadata enrichment
- validation-driven transformation

Project:
Olist Seller Intelligence Platform

Layer:
Silver

Dataset:
silver_products

Dataset Grain:
ONE ROW = ONE PRODUCT
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
    load_config,
    resolve_path
)

from pipelines.silver.utils.spark_session import (
    create_spark_session
)

from pipelines.silver.validations.products_validation import (
    run_products_validation
)


# =========================================================
# CREATE SPARK SESSION
# =========================================================

spark = create_spark_session(
    "TransformSilverProducts"
)


# =========================================================
# LOAD CONFIGURATION
# =========================================================

config = load_config()

# ---------------------------------------------------------
# Bronze Paths
# ---------------------------------------------------------

BRONZE_PRODUCTS_PATH = resolve_path(
    config["paths"]["bronze"]["products"],
    config
)

BRONZE_CATEGORY_TRANSLATION_PATH = resolve_path(
    config["paths"]["bronze"]["category_translation"],
    config
)

# ---------------------------------------------------------
# Silver Paths
# ---------------------------------------------------------

SILVER_PRODUCTS_PATH = resolve_path(
    config["paths"]["silver"]["products"],
    config
)

SILVER_PRODUCTS_QUARANTINE_PATH = resolve_path(
    config["paths"]["silver"]["products_quarantine"],
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
print("LOADING BRONZE PRODUCTS DATASET")
print("=================================================")

products_df = spark.read.parquet(
    BRONZE_PRODUCTS_PATH
)


print(
    f"Bronze Products Count: "
    f"{products_df.count()}"
)
print("\n=================================================")
print("LOADING BRONZE CATEGORY TRANSLATION DATASET")
print("=================================================")
category_translation_df = spark.read.parquet(
    BRONZE_CATEGORY_TRANSLATION_PATH
)
category_translation_df = category_translation_df.select(
    "product_category_name",
    "product_category_name_english"
)

# =========================================================
# INITIAL DATA INSPECTION
# =========================================================

print("\n=================================================")
print("BRONZE PRODUCTS SCHEMA")
print("=================================================")

products_df.printSchema()


# =========================================================
# START TRANSFORMATIONS
# =========================================================

print("\n=================================================")
print("STARTING SILVER TRANSFORMATIONS")
print("=================================================")

silver_products_df = products_df


# =========================================================
# PRODUCT ID STANDARDIZATION
# =========================================================

"""
Standardize product business keys.
"""

print("\nApplying product ID standardization...")

silver_products_df = (

    silver_products_df

    .withColumn(
        "product_id",
        trim(col("product_id"))
    )

)


# =========================================================
# CATEGORY NORMALIZATION
# =========================================================

"""
Normalize product categories for
deterministic grouping consistency.
"""

print("\nApplying category normalization...")

silver_products_df = (

    silver_products_df

    .withColumn(

        "product_category_name",

        when(
            col("product_category_name").isNotNull(),

            lower(
                trim(col("product_category_name"))
            )

        ).otherwise("unknown_category")

    )

)


# =========================================================
# NUMERIC STANDARDIZATION
# =========================================================

"""
Standardize logistics and dimensional metrics.
"""

print("\nApplying numeric standardization...")

silver_products_df = (

    silver_products_df

    .withColumn(
        "product_name_lenght",
        col("product_name_lenght").cast(
            IntegerType()
        )
    )

    .withColumn(
        "product_description_lenght",
        col("product_description_lenght").cast(
            IntegerType()
        )
    )

    .withColumn(
        "product_photos_qty",
        col("product_photos_qty").cast(
            IntegerType()
        )
    )

    .withColumn(
        "product_weight_g",
        col("product_weight_g").cast(
            DecimalType(12, 2)
        )
    )

    .withColumn(
        "product_length_cm",
        col("product_length_cm").cast(
            DecimalType(12, 2)
        )
    )

    .withColumn(
        "product_height_cm",
        col("product_height_cm").cast(
            DecimalType(12, 2)
        )
    )

    .withColumn(
        "product_width_cm",
        col("product_width_cm").cast(
            DecimalType(12, 2)
        )
    )

)


# =========================================================
# PRODUCT VOLUME DERIVATION
# =========================================================

"""
Derive operational shipment volume metric.

Used for:
- freight analysis
- logistics intelligence
- oversized shipment detection
"""

print("\nCalculating product volume metric...")

silver_products_df = (

    silver_products_df

    .withColumn(

        "product_volume_cm3",

        when(

            col("product_length_cm").isNotNull()
            &
            col("product_height_cm").isNotNull()
            &
            col("product_width_cm").isNotNull(),

            (
                col("product_length_cm")
                *
                col("product_height_cm")
                *
                col("product_width_cm")
            ).cast(DecimalType(18, 2))

        ).otherwise(None)

    )

)


# =========================================================
# CATEGORY TRANSLATION ENRICHMENT
# =========================================================

print("\nApplying category translation...")

silver_products_df = silver_products_df.join(

    category_translation_df,

    on="product_category_name",

    how="left"

)

silver_products_df = silver_products_df.withColumn(

    "product_category_name_english",

    when(

        col(
            "product_category_name_english"
        ).isNull(),

        "unknown_category"

    ).otherwise(

        col(
            "product_category_name_english"
        )

    )

)


# =========================================================
# QUARANTINE RULE
# MISSING LOGISTICS ATTRIBUTES
# =========================================================

print(
    "\nIdentifying products with missing logistics..."
)

products_quarantine_df = (

    silver_products_df

    .filter(

        col("product_weight_g").isNull()

        |

        col("product_length_cm").isNull()

        |

        col("product_height_cm").isNull()

        |

        col("product_width_cm").isNull()

    )

    .withColumn(

        "quarantine_reason",

        lit(
            "MISSING_LOGISTICS_ATTRIBUTES"
        )

    )

)

print(
    f"Quarantined Products: "
    f"{products_quarantine_df.count()}"
)


# =========================================================
# BUILD CLEAN DATASET
# =========================================================

print(
    "\nBuilding clean products dataset..."
)

clean_products_df = (

    silver_products_df

    .join(

        products_quarantine_df.select(
            "product_id"
        ),

        on="product_id",

        how="left_anti"

    )

)

print(
    f"Clean Products: "
    f"{clean_products_df.count()}"
)


# =========================================================
# LOGISTICS COMPLETENESS FLAG
# =========================================================

clean_products_df = clean_products_df.withColumn(

    "logistics_completeness_flag",

    when(

        col("product_weight_g").isNotNull()

        &

        col("product_length_cm").isNotNull()

        &

        col("product_height_cm").isNotNull()

        &

        col("product_width_cm").isNotNull(),

        True

    ).otherwise(False)

)


# =========================================================
# HEAVY PRODUCT FLAG
# =========================================================

clean_products_df = clean_products_df.withColumn(

    "heavy_product_flag",

    when(
        col("product_weight_g") >= 5000,
        True
    ).otherwise(False)

)


# =========================================================
# PRODUCT SIZE CATEGORY
# =========================================================

clean_products_df = clean_products_df.withColumn(

    "product_size_category",

    when(
        col("product_volume_cm3") < 1000,
        "Small"
    )

    .when(
        col("product_volume_cm3") < 10000,
        "Medium"
    )

    .when(
        col("product_volume_cm3") < 50000,
        "Large"
    )

    .otherwise(
        "Oversized"
    )

)

catalog_complete_condition = (

    (col("product_category_name") != "unknown_category")

    &

    (col("product_name_lenght").isNotNull())

    &

    (col("product_description_lenght").isNotNull())

    &

    (col("product_photos_qty").isNotNull())

)

clean_products_df = clean_products_df.withColumn(

    "catalog_completeness_flag",

    when(
        catalog_complete_condition,
        True
    ).otherwise(False)

)

# =========================================================
# METADATA ENRICHMENT
# =========================================================

print("\nApplying metadata enrichment...")

clean_products_df = (

    clean_products_df

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

clean_products_df = clean_products_df.select(

    "product_id",

    "product_category_name",

    "product_category_name_english",

    "product_name_lenght",

    "product_description_lenght",

    "product_photos_qty",

    "product_weight_g",

    "product_length_cm",

    "product_height_cm",

    "product_width_cm",

    "product_volume_cm3",

    "product_size_category",

    "heavy_product_flag",

    "logistics_completeness_flag",
    
    "catalog_completeness_flag",

    "silver_loaded_at",

    "source_system",

    "transformation_version"

)


# =========================================================
# MATERIALIZE DATAFRAME
# =========================================================

print(
    "\nMaterializing clean products dataset..."
)

clean_products_df = clean_products_df.cache()

clean_products_df.count()


# =========================================================
# RUN VALIDATION SUITE
# =========================================================

run_products_validation(

    source_df=products_df,

    transformed_df=clean_products_df,

    quarantine_df=products_quarantine_df

)


# =========================================================
# QUARANTINE PREVIEW
# =========================================================

print("\n=================================================")
print("PRODUCTS QUARANTINE PREVIEW")
print("=================================================")

products_quarantine_df.show(
    10,
    truncate=False
)


# =========================================================
# CLEAN DATA PREVIEW
# =========================================================

print("\n=================================================")
print("CLEAN PRODUCTS PREVIEW")
print("=================================================")

clean_products_df.show(
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
    f"Clean Products Count: "
    f"{clean_products_df.count()}"
)

print(
    f"Quarantined Products Count: "
    f"{products_quarantine_df.count()}"
)


# =========================================================
# WRITE QUARANTINE DATASET
# =========================================================

print("\n=================================================")
print("WRITING PRODUCTS QUARANTINE DATASET")
print("=================================================")

products_quarantine_df.write \
    .mode("overwrite") \
    .parquet(
        SILVER_PRODUCTS_QUARANTINE_PATH
    )

print(
    f"Products Quarantine Written To: "
    f"{SILVER_PRODUCTS_QUARANTINE_PATH}"
)


# =========================================================
# WRITE CLEAN PRODUCTS DATASET
# =========================================================

print("\n=================================================")
print("WRITING SILVER PRODUCTS DATASET")
print("=================================================")

clean_products_df.write \
    .mode("overwrite") \
    .parquet(
        SILVER_PRODUCTS_PATH
    )

print(
    f"Silver Products Written To: "
    f"{SILVER_PRODUCTS_PATH}"
)


# =========================================================
# FINAL SUMMARY
# =========================================================

print("\n=================================================")
print("PRODUCT ENRICHMENT & LOGISTICS GOVERNANCE COMPLETED")
print("=================================================")

print(
    f"Clean Products: "
    f"{clean_products_df.count()}"
)

print(
    f"Quarantined Products: "
    f"{products_quarantine_df.count()}"
)



# =========================================================
# STOP SPARK SESSION
# =========================================================

spark.stop()