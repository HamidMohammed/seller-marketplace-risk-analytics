"""
dim_product_validation.py

Objective:
Validate Gold Product Dimension.

Dimension:
dim_product

Grain:
ONE ROW = ONE PRODUCT
"""

# =====================================================
# IMPORTS
# =====================================================

from pyspark.sql.functions import (
    col
)

# =====================================================
# VALIDATION
# =====================================================

def run_dim_product_validation(df):

    print("=" * 60)
    print("DIM PRODUCT VALIDATION")
    print("=" * 60)

    # =================================================
    # ROW COUNT
    # =================================================

    row_count = df.count()

    print(
        f"\nFinal Row Count: "
        f"{row_count:,}"
    )

    # =================================================
    # GRAIN VALIDATION
    # =================================================

    duplicate_products = (

        df.groupBy(
            "product_id"
        )

        .count()

        .filter(
            col("count") > 1
        )

        .count()
    )

    print(
        f"\nDuplicate Product Grain Violations: "
        f"{duplicate_products}"
    )

    # =================================================
    # SURROGATE KEY VALIDATION
    # =================================================

    duplicate_product_sk = (

        df.groupBy(
            "product_sk"
        )

        .count()

        .filter(
            col("count") > 1
        )

        .count()
    )

    print(
        f"Duplicate Product SK Count: "
        f"{duplicate_product_sk}"
    )

    # =================================================
    # CRITICAL NULL VALIDATION
    # =================================================

    print(
        "\nCritical Null Validation:"
    )

    critical_columns = [

        "product_sk",

        "product_id",

        "product_category_name_english",

        "product_size_category"

    ]

    for column_name in critical_columns:

        null_count = (

            df.filter(
                col(column_name).isNull()
            )

            .count()
        )

        print(
            f"{column_name}: "
            f"{null_count} nulls"
        )

    # =================================================
    # PRODUCT CATEGORY DISTRIBUTION
    # =================================================

    print(
        "\nTop Product Categories:"
    )

    df.groupBy(
        "product_category_name_english"
    ).count().orderBy(
        col("count").desc()
    ).show(
        20,
        truncate=False
    )

    # =================================================
    # PRODUCT SIZE DISTRIBUTION
    # =================================================

    print(
        "\nProduct Size Distribution:"
    )

    df.groupBy(
        "product_size_category"
    ).count().show(
        truncate=False
    )

    # =================================================
    # HEAVY PRODUCT ANALYSIS
    # =================================================

    heavy_products = (

        df.filter(
            col(
                "heavy_product_flag"
            ) == True
        )

        .count()
    )

    print(
        f"\nHeavy Products: "
        f"{heavy_products:,}"
    )

    # =================================================
    # LOGISTICS COMPLETENESS
    # =================================================

    incomplete_logistics = (

        df.filter(
            col(
                "logistics_completeness_flag"
            ) == False
        )

        .count()
    )

    print(
        f"Incomplete Logistics Profiles: "
        f"{incomplete_logistics:,}"
    )

    # =================================================
    # CATALOG COMPLETENESS
    # =================================================

    incomplete_catalog = (

        df.filter(
            col(
                "catalog_completeness_flag"
            ) == False
        )

        .count()
    )

    print(
        f"Incomplete Catalog Profiles: "
        f"{incomplete_catalog:,}"
    )

    # =================================================
    # PHYSICAL DIMENSIONS CHECK
    # =================================================

    missing_weight = (

        df.filter(
            col(
                "product_weight_g"
            ).isNull()
        )

        .count()
    )

    print(
        f"Products Missing Weight: "
        f"{missing_weight:,}"
    )

    missing_volume = (

        df.filter(
            col(
                "product_volume_cm3"
            ).isNull()
        )

        .count()
    )

    print(
        f"Products Missing Volume: "
        f"{missing_volume:,}"
    )

    # =================================================
    # RESULT
    # =================================================

    print("\nValidation Complete.")

    print("=" * 60)