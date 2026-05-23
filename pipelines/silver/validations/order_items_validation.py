"""
order_items_validation.py

Objective:
Validation framework for silver_order_items dataset.

This module protects:
- dataset grain integrity
- financial correctness
- logistics consistency
- seller accountability
- lifecycle integrity

Project:
Olist Seller Intelligence Platform

Layer:
Silver Validation Layer

Dataset:
silver_order_items
"""

# =========================================================
# PROJECT ROOT SETUP
# =========================================================

import sys
import os

project_root = os.path.abspath(
    os.path.join(os.path.dirname(__file__), "../../../")
)

if project_root not in sys.path:
    sys.path.append(project_root)


# =========================================================
# IMPORTS
# =========================================================

from pyspark.sql.functions import (
    col,
    count,
    when
)

from pipelines.silver.validations.validation_utils import (
    validate_row_count,
    validate_duplicates,
    validate_nulls,
    validate_positive_values
)


# =========================================================
# MAIN VALIDATION FUNCTION
# =========================================================

def run_order_items_validation(
    source_df,
    transformed_df
):
    """
    Runs complete validation suite for silver_order_items.

    Parameters
    ----------
    source_df : DataFrame
        Original Bronze dataframe.

    transformed_df : DataFrame
        Final transformed Silver dataframe.
    """

    print("\n=================================================")
    print("RUNNING ORDER ITEMS VALIDATION")
    print("=================================================")

    # =====================================================
    # 1. ROW COUNT VALIDATION
    # =====================================================

    print("\n[1] ROW COUNT VALIDATION")

    validate_row_count(
        source_df,
        transformed_df
        
    )

    # =====================================================
    # 2. GRAIN VALIDATION
    # =====================================================

    """
    Grain:
    ONE ROW = ONE ORDER ITEM EVENT

    Composite business grain:
    (order_id, order_item_id)
    """

    print("\n[2] GRAIN VALIDATION")

    validate_duplicates(
        df=transformed_df,
        key_columns=["order_id", "order_item_id"]
    )

    # =====================================================
    # 3. CRITICAL NULL VALIDATION
    # =====================================================

    print("\n[3] CRITICAL NULL VALIDATION")

    critical_columns = [
        "order_id",
        "order_item_id",
        "product_id",
        "seller_id",
        "price",
        "freight_value"
    ]

    validate_nulls(
        df=transformed_df,
        critical_columns=critical_columns
    )

    # =====================================================
    # 4. FINANCIAL VALIDATION
    # =====================================================

    print("\n[4] FINANCIAL VALIDATION")

    validate_positive_values(
        df=transformed_df,
        column_name="price"
    )

    validate_positive_values(
        df=transformed_df,
        column_name="freight_value"
    )

    # =====================================================
    # 5. FREIGHT RATIO VALIDATION
    # =====================================================

    """
    freight_ratio must never be negative.
    """

    print("\n[5] FREIGHT RATIO VALIDATION")

    negative_freight_ratio = (

        transformed_df

        .filter(
            col("freight_ratio") < 0
        )

        .count()

    )

    print(
        f"Negative Freight Ratio Records: "
        f"{negative_freight_ratio}"
    )

    if negative_freight_ratio > 0:

        raise ValueError(
            "FAILED: Negative freight ratios detected."
        )

    print("PASSED: Freight ratio validation.")

    # =====================================================
    # 6. PRODUCT VOLUME VALIDATION
    # =====================================================

    """
    Product volume should never be negative.
    """

    print("\n[6] PRODUCT VOLUME VALIDATION")

    negative_volume_count = (

        transformed_df

        .filter(
            col("product_volume_cm3") < 0
        )

        .count()

    )

    print(
        f"Negative Product Volume Records: "
        f"{negative_volume_count}"
    )

    if negative_volume_count > 0:

        raise ValueError(
            "FAILED: Negative product volumes detected."
        )

    print("PASSED: Product volume validation.")

    # =====================================================
    # 7. SELLER ACCOUNTABILITY VALIDATION
    # =====================================================

    """
    Every order item must belong to at least one seller.
    """

    print("\n[7] SELLER ACCOUNTABILITY VALIDATION")

    invalid_seller_count = (

        transformed_df

        .filter(
            col("seller_count") < 1
        )

        .count()

    )

    print(
        f"Invalid Seller Count Records: "
        f"{invalid_seller_count}"
    )

    if invalid_seller_count > 0:

        raise ValueError(
            "FAILED: Invalid seller_count values detected."
        )

    print("PASSED: Seller accountability validation.")

    # =====================================================
    # 8. SHIPPING DEADLINE VALIDATION
    # =====================================================

    """
    shipping_limit_date should occur after
    order purchase timestamp.

    Prevents impossible operational timelines.
    """

    print("\n[8] SHIPPING DEADLINE VALIDATION")

    invalid_shipping_timeline = (

        transformed_df

        .filter(

            col("shipping_limit_date")
            <
            col("order_purchase_timestamp")

        )

        .count()

    )

    print(
        f"Invalid Shipping Timeline Records: "
        f"{invalid_shipping_timeline}"
    )

    if invalid_shipping_timeline > 0:

        raise ValueError(
            "FAILED: Invalid shipping timelines detected."
        )

    print("PASSED: Shipping timeline validation.")

    # =====================================================
    # 9. MULTI-SELLER ORDER ANALYSIS
    # =====================================================

    """
    Informational operational insight.
    NOT a failure condition.
    """

    print("\n[9] MULTI-SELLER ORDER ANALYSIS")

    multi_seller_orders = (

        transformed_df

        .filter(
            col("is_multi_seller_order") == True
        )

        .select("order_id")

        .distinct()

        .count()

    )

    print(
        f"Multi-Seller Orders: "
        f"{multi_seller_orders}"
    )

    # =====================================================
    # 10. ORPHAN ENRICHMENT VALIDATION
    # =====================================================

    """
    Detect missing product enrichment joins.
    Important for logistics intelligence quality.
    """

    print("\n[10] ORPHAN ENRICHMENT VALIDATION")

    missing_product_dimensions = (

        transformed_df

        .filter(
            col("product_weight_g").isNull()
        )

        .count()

    )

    print(
        f"Missing Product Enrichment Records: "
        f"{missing_product_dimensions}"
    )

    if missing_product_dimensions > 0:

        print(
            "WARNING: Some products missing "
            "logistics enrichment."
        )

    else:

        print(
            "PASSED: Product enrichment validation."
        )

    # =====================================================
    # FINAL VALIDATION SUMMARY
    # =====================================================

    print("\n=================================================")
    print("ALL ORDER ITEMS VALIDATIONS COMPLETED")
    print("=================================================")

    print("""
Validation Summary:
- Row count integrity verified
- Grain integrity verified
- Critical null checks passed
- Financial validations passed
- Freight ratio validated
- Product volume validated
- Seller accountability validated
- Shipping lifecycle validated
- Product enrichment checked

silver_order_items is TRUSTED.
""")
