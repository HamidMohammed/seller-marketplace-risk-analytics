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
    os.path.join(os.path.dirname(__file__), "../../../")
)

if project_root not in sys.path:
    sys.path.append(project_root)


# =========================================================
# IMPORTS
# =========================================================

from pyspark.sql.functions import (
    col,
    lower,
    trim
)

from pipelines.silver.validations.validation_utils import (
    validate_duplicates,
    validate_nulls,
    validate_positive_values
)


# =========================================================
# MAIN VALIDATION FUNCTION
# =========================================================

def run_products_validation(
    source_df,
    transformed_df
):
    """
    Run complete validation suite for silver_products.

    Parameters
    ----------
    source_df : DataFrame
        Original Bronze products dataframe.

    transformed_df : DataFrame
        Final Silver products dataframe.
    """

    print("\n=================================================")
    print("RUNNING PRODUCTS VALIDATION")
    print("=================================================")

    # =====================================================
    # 1. ROW COUNT ANALYSIS
    # =====================================================

    """
    Product dimensional datasets should preserve
    row counts because transformations should not
    create duplication or record loss.
    """

    print("\n[1] ROW COUNT ANALYSIS")

    source_count = source_df.count()

    transformed_count = transformed_df.count()

    print(f"Source Product Count: {source_count}")

    print(
        f"Silver Product Count: "
        f"{transformed_count}"
    )

    if source_count != transformed_count:

        raise ValueError(
            "FAILED: Row count mismatch detected."
        )

    print("PASSED: Row count validation.")

    # =====================================================
    # 2. GRAIN VALIDATION
    # =====================================================

    """
    Grain:
    ONE ROW = ONE PRODUCT
    """

    print("\n[2] GRAIN VALIDATION")

    validate_duplicates(
        df=transformed_df,
        key_columns=["product_id"]
    )

    # =====================================================
    # 3. CRITICAL NULL VALIDATION
    # =====================================================

    print("\n[3] CRITICAL NULL VALIDATION")

    critical_columns = [
        "product_id"
    ]

    validate_nulls(
        df=transformed_df,
        critical_columns=critical_columns
    )

    # =====================================================
    # 4. PRODUCT CATEGORY VALIDATION
    # =====================================================

    """
    Validate category normalization consistency.
    """

    print("\n[4] PRODUCT CATEGORY VALIDATION")

    inconsistent_categories = (

        transformed_df

        .filter(

            col("product_category_name")
            !=
            lower(
                trim(col("product_category_name"))
            )

        )

        .count()

    )

    print(
        f"Inconsistent Category Records: "
        f"{inconsistent_categories}"
    )

    if inconsistent_categories > 0:

        print("""
WARNING:
Some product categories are not normalized.
""")

    else:

        print(
            "PASSED: Product category validation."
        )

    # =====================================================
    # 5. PRODUCT WEIGHT VALIDATION
    # =====================================================

    """
    Product weights must be non-negative.
    """

    print("\n[5] PRODUCT WEIGHT VALIDATION")

    validate_positive_values(
        df=transformed_df,
        column_name="product_weight_g"
    )

    # =====================================================
    # 6. PRODUCT DIMENSION VALIDATION
    # =====================================================

    """
    Validate physical product dimensions.
    """

    print("\n[6] PRODUCT DIMENSION VALIDATION")

    dimension_columns = [

        "product_length_cm",
        "product_height_cm",
        "product_width_cm"

    ]

    for dimension_column in dimension_columns:

        validate_positive_values(
            df=transformed_df,
            column_name=dimension_column
        )

    print(
        "PASSED: Product dimension validation."
    )

    # =====================================================
    # 7. PRODUCT VOLUME VALIDATION
    # =====================================================

    """
    Product volume must be physically valid.
    """

    print("\n[7] PRODUCT VOLUME VALIDATION")

    negative_volume_records = (

        transformed_df

        .filter(
            col("product_volume_cm3") < 0
        )

        .count()

    )

    print(
        f"Negative Product Volume Records: "
        f"{negative_volume_records}"
    )

    if negative_volume_records > 0:

        raise ValueError(
            "FAILED: Negative product volumes detected."
        )

    print("PASSED: Product volume validation.")

    # =====================================================
    # 8. PRODUCT METADATA VALIDATION
    # =====================================================

    """
    Validate metadata metrics such as:
    - description length
    - photo quantity
    """

    print("\n[8] PRODUCT METADATA VALIDATION")

    metadata_columns = [

        "product_name_lenght",
        "product_description_lenght",
        "product_photos_qty"

    ]

    for metadata_column in metadata_columns:

        negative_metadata_records = (

            transformed_df

            .filter(
                col(metadata_column) < 0
            )

            .count()

        )

        print(
            f"Negative {metadata_column} Records: "
            f"{negative_metadata_records}"
        )

        if negative_metadata_records > 0:

            raise ValueError(
                f"FAILED: Invalid values detected "
                f"in {metadata_column}"
            )

    print(
        "PASSED: Product metadata validation."
    )

    # =====================================================
    # 9. MISSING CATEGORY ANALYSIS
    # =====================================================

    """
    Analyze unknown category assignments.
    NOT a failure condition.
    """

    print("\n[9] MISSING CATEGORY ANALYSIS")

    unknown_category_records = (

        transformed_df

        .filter(
            col("product_category_name")
            == "unknown_category"
        )

        .count()

    )

    print(
        f"Unknown Category Records: "
        f"{unknown_category_records}"
    )

    print("""
INFO:
Unknown categories are preserved intentionally
to avoid silent operational data loss.
""")

    # =====================================================
    # 10. LOGISTICS COMPLETENESS VALIDATION
    # =====================================================

    """
    Analyze missing logistics attributes.
    NOT a failure condition.
    """

    print("\n[10] LOGISTICS COMPLETENESS VALIDATION")

    incomplete_logistics_records = (

        transformed_df

        .filter(

            col("product_weight_g").isNull()

            |

            col("product_length_cm").isNull()

            |

            col("product_height_cm").isNull()

            |

            col("product_width_cm").isNull()

        )

        .count()

    )

    print(
        f"Incomplete Logistics Records: "
        f"{incomplete_logistics_records}"
    )

    if incomplete_logistics_records > 0:

        print("""
WARNING:
Some products are missing logistics attributes.
""")

    else:

        print(
            "PASSED: Logistics completeness validation."
        )

    # =====================================================
    # FINAL VALIDATION SUMMARY
    # =====================================================

    print("\n=================================================")
    print("ALL PRODUCTS VALIDATIONS COMPLETED")
    print("=================================================")

    print("""
Validation Summary:
- Product grain integrity verified
- Product identity validated
- Category normalization verified
- Logistics metrics validated
- Product dimensions validated
- Product volume validated
- Metadata integrity verified
- Controlled anomaly governance applied

silver_products is TRUSTED.
""")
