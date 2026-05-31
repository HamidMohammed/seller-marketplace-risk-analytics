"""
products_validation.py

Objective:
Validation framework for silver_products dataset.

This module protects:
- product dimensional integrity
- logistics consistency
- category normalization
- dimensional metric validity
- freight intelligence reliability
- operational analytical trust

Project:
Olist Seller Intelligence Platform

Layer:
Silver Validation Layer

Dataset:
silver_products
"""

# =========================================================
# PROJECT ROOT SETUP
# =========================================================

import sys
import os

project_root = os.path.abspath(
    os.path.join(
        os.path.dirname(__file__),
        "../../../"
    )
)

if project_root not in sys.path:
    sys.path.append(project_root)

# =========================================================
# IMPORTS
# =========================================================

from pyspark.sql.functions import (
    col
)

from pipelines.silver.validations.validation_utils import (
    validate_duplicates,
    validate_nulls
)

# =========================================================
# QUARANTINE VALIDATION
# =========================================================

def validate_quarantine_counts(
    quarantine_df
):

    print(
        "\n[VALIDATION] QUARANTINE SUMMARY"
    )

    total_quarantined = (
        quarantine_df.count()
    )

    print(
        f"Total Quarantined Products: "
        f"{total_quarantined}"
    )

    quarantine_df.groupBy(
        "quarantine_reason"
    ).count().show(
        truncate=False
    )

# =========================================================
# PRODUCT SIZE CATEGORY VALIDATION
# =========================================================

def validate_product_size_category(
    df
):

    print(
        "\n[VALIDATION] PRODUCT SIZE CATEGORY"
    )

    invalid_categories = df.filter(

        ~col(
            "product_size_category"
        ).isin(

            "Small",
            "Medium",
            "Large",
            "Oversized"

        )

    ).count()

    print(
        f"Invalid Product Size Categories: "
        f"{invalid_categories}"
    )

    if invalid_categories > 0:

        raise ValueError(
            "FAILED: Invalid product size categories."
        )

# =========================================================
# LOGISTICS COMPLETENESS FLAG
# =========================================================

def validate_logistics_flag(
    df
):

    print(
        "\n[VALIDATION] LOGISTICS COMPLETENESS"
    )

    df.groupBy(
        "logistics_completeness_flag"
    ).count().show(
        truncate=False
    )

# =========================================================
# HEAVY PRODUCT FLAG
# =========================================================

def validate_heavy_product_flag(
    df
):

    print(
        "\n[VALIDATION] HEAVY PRODUCT FLAG"
    )

    df.groupBy(
        "heavy_product_flag"
    ).count().show(
        truncate=False
    )

# =========================================================
# CATALOG COMPLETENESS FLAG
# =========================================================

def validate_catalog_completeness_flag(
    df
):

    print(
        "\n[VALIDATION] CATALOG COMPLETENESS FLAG"
    )

    df.groupBy(
        "catalog_completeness_flag"
    ).count().show(
        truncate=False
    )
# =========================================================
# CATEGORY TRANSLATION VALIDATION
# =========================================================

def validate_category_translation(
    df
):

    print(
        "\n[VALIDATION] CATEGORY TRANSLATION"
    )

    missing_translation = df.filter(

        col(
            "product_category_name_english"
        ).isNull()

    ).count()

    print(
        f"Missing English Categories: "
        f"{missing_translation}"
    )

# =========================================================
# VOLUME VALIDATION
# =========================================================

def validate_product_volume(
    df
):

    print(
        "\n[VALIDATION] PRODUCT VOLUME"
    )

    negative_volume = df.filter(

        col(
            "product_volume_cm3"
        ) < 0

    ).count()

    print(
        f"Negative Product Volumes: "
        f"{negative_volume}"
    )

    if negative_volume > 0:

        raise ValueError(
            "FAILED: Negative product volumes detected."
        )

# =========================================================
# WEIGHT VALIDATION
# =========================================================

def validate_product_weight(
    df
):

    print(
        "\n[VALIDATION] PRODUCT WEIGHT"
    )

    negative_weight = df.filter(

        col(
            "product_weight_g"
        ) < 0

    ).count()

    print(
        f"Negative Product Weights: "
        f"{negative_weight}"
    )

    if negative_weight > 0:

        raise ValueError(
            "FAILED: Negative product weights detected."
        )

# =========================================================
# MAIN VALIDATION RUNNER
# =========================================================

def run_products_validation(

    source_df,
    transformed_df,
    quarantine_df

):

    print(
        "\n================================================="
    )

    print(
        "RUNNING HARDENED PRODUCTS VALIDATION"
    )

    print(
        "================================================="
    )

    source_count = (
        source_df.count()
    )

    transformed_count = (
        transformed_df.count()
    )

    quarantine_count = (
        quarantine_df.count()
    )

    print(
        f"Source Count: "
        f"{source_count}"
    )

    print(
        f"Clean Products: "
        f"{transformed_count}"
    )

    print(
        f"Quarantined Products: "
        f"{quarantine_count}"
    )

    if source_count != (
        transformed_count
        +
        quarantine_count
    ):

        print("""
WARNING:
Source reconciliation mismatch.
Investigate transformation logic.
""")

    # =====================================================
    # GRAIN
    # =====================================================

    validate_duplicates(

        df=transformed_df,

        key_columns=[
            "product_id"
        ]

    )

    # =====================================================
    # CRITICAL NULLS
    # =====================================================

    validate_nulls(

    df=transformed_df,

    critical_columns=[

        "product_id",

        "product_category_name_english",

        "product_size_category",

        "logistics_completeness_flag",

        "catalog_completeness_flag"

    ]

)

    # =====================================================
    # BUSINESS VALIDATIONS
    # =====================================================

    validate_product_size_category(
        transformed_df
    )

    validate_logistics_flag(
        transformed_df
    )

    validate_heavy_product_flag(
        transformed_df
    )

    validate_category_translation(
        transformed_df
    )
    
    validate_catalog_completeness_flag(
        transformed_df
    )

    validate_product_volume(
        transformed_df
    )

    validate_product_weight(
        transformed_df
    )

    validate_quarantine_counts(
        quarantine_df
    )

    print(
        "\n================================================="
    )

    print(
        "PRODUCTS VALIDATION COMPLETED"
    )

    print(
        "================================================="
    )

