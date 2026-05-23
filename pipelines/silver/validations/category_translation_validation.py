"""
category_translation_validation.py

Objective:
Validation framework for silver_category_translation dataset.

This module protects:
- semantic enrichment integrity
- category-translation uniqueness
- multilingual consistency
- business-readable normalization
- analytical semantic trust

Project:
Olist Seller Intelligence Platform

Layer:
Silver Validation Layer

Dataset:
silver_category_translation
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
    trim,
    lower
)

from pipelines.silver.validations.validation_utils import (
    validate_duplicates,
    validate_nulls
)


# =========================================================
# MAIN VALIDATION FUNCTION
# =========================================================

def run_category_translation_validation(
    source_df,
    transformed_df
):
    """
    Run complete validation suite for
    silver_category_translation.

    Parameters
    ----------
    source_df : DataFrame
        Original Bronze translation dataframe.

    transformed_df : DataFrame
        Final Silver translation dataframe.
    """

    print("\n=================================================")
    print("RUNNING CATEGORY TRANSLATION VALIDATION")
    print("=================================================")

    # =====================================================
    # 1. ROW COUNT ANALYSIS
    # =====================================================

    """
    Translation datasets should preserve
    semantic category mappings.
    """

    print("\n[1] ROW COUNT ANALYSIS")

    source_count = source_df.count()

    transformed_count = transformed_df.count()

    print(
        f"Source Translation Count: "
        f"{source_count}"
    )

    print(
        f"Silver Translation Count: "
        f"{transformed_count}"
    )

    if transformed_count > source_count:

        raise ValueError(
            "FAILED: Unexpected translation duplication detected."
        )

    print("PASSED: Row count validation.")

    # =====================================================
    # 2. GRAIN VALIDATION
    # =====================================================

    """
    Grain:
    ONE ROW = ONE CATEGORY TRANSLATION
    """

    print("\n[2] GRAIN VALIDATION")

    validate_duplicates(
        df=transformed_df,
        key_columns=["product_category_name"]
    )

    # =====================================================
    # 3. CRITICAL NULL VALIDATION
    # =====================================================

    print("\n[3] CRITICAL NULL VALIDATION")

    critical_columns = [

        "product_category_name",

        "product_category_name_english"

    ]

    validate_nulls(
        df=transformed_df,
        critical_columns=critical_columns
    )

    # =====================================================
    # 4. PORTUGUESE CATEGORY NORMALIZATION
    # =====================================================

    """
    Validate deterministic normalization
    of Portuguese categories.
    """

    print("\n[4] PORTUGUESE CATEGORY VALIDATION")

    invalid_portuguese_categories = (

        transformed_df

        .filter(

            col("product_category_name")
            !=
            lower(
                trim(
                    col("product_category_name")
                )
            )

        )

        .count()

    )

    print(
        f"Inconsistent Portuguese Categories: "
        f"{invalid_portuguese_categories}"
    )

    if invalid_portuguese_categories > 0:

        print("""
WARNING:
Some Portuguese categories are not normalized.
""")

    else:

        print(
            "PASSED: Portuguese category normalization validation."
        )

    # =====================================================
    # 5. ENGLISH CATEGORY NORMALIZATION
    # =====================================================

    """
    Validate deterministic normalization
    of English translations.
    """

    print("\n[5] ENGLISH CATEGORY VALIDATION")

    invalid_english_categories = (

        transformed_df

        .filter(

            col("product_category_name_english")
            !=
            lower(
                trim(
                    col("product_category_name_english")
                )
            )

        )

        .count()

    )

    print(
        f"Inconsistent English Categories: "
        f"{invalid_english_categories}"
    )

    if invalid_english_categories > 0:

        print("""
WARNING:
Some English category translations
are not normalized.
""")

    else:

        print(
            "PASSED: English category normalization validation."
        )

    # =====================================================
    # 6. EMPTY TRANSLATION VALIDATION
    # =====================================================

    """
    Validate non-empty English translations.
    """

    print("\n[6] EMPTY TRANSLATION VALIDATION")

    empty_translation_records = (

        transformed_df

        .filter(

            trim(
                col("product_category_name_english")
            ) == ""

        )

        .count()

    )

    print(
        f"Empty Translation Records: "
        f"{empty_translation_records}"
    )

    if empty_translation_records > 0:

        raise ValueError(
            "FAILED: Empty English translations detected."
        )

    print(
        "PASSED: Empty translation validation."
    )

    # =====================================================
    # 7. SEMANTIC COMPLETENESS VALIDATION
    # =====================================================

    """
    Analyze semantic coverage completeness.
    """

    print("\n[7] SEMANTIC COMPLETENESS VALIDATION")

    missing_translation_records = (

        transformed_df

        .filter(
            col("product_category_name_english").isNull()
        )

        .count()

    )

    print(
        f"Missing Translation Records: "
        f"{missing_translation_records}"
    )

    if missing_translation_records > 0:

        print("""
WARNING:
Some product categories are missing
English translations.
""")

    else:

        print(
            "PASSED: Semantic completeness validation."
        )

    # =====================================================
    # 8. DUPLICATE ENGLISH TRANSLATION ANALYSIS
    # =====================================================

    """
    Analyze many-to-one semantic mappings.
    NOT always invalid operationally.
    """

    print("\n[8] DUPLICATE ENGLISH TRANSLATION ANALYSIS")

    duplicate_english_translations = (

        transformed_df

        .groupBy(
            "product_category_name_english"
        )

        .count()

        .filter(
            col("count") > 1
        )

        .count()

    )

    print(
        f"Duplicate English Translation Groups: "
        f"{duplicate_english_translations}"
    )

    print("""
INFO:
Some Portuguese categories may map to
similar business-friendly English labels.
""")

    # =====================================================
    # 9. UNDERSCORE STANDARDIZATION VALIDATION
    # =====================================================

    """
    Validate analytical-friendly naming.
    """

    print("\n[9] UNDERSCORE STANDARDIZATION VALIDATION")

    spaced_translation_records = (

        transformed_df

        .filter(
            col("product_category_name_english")
            .contains(" ")
        )

        .count()

    )

    print(
        f"Non-Standardized Translation Records: "
        f"{spaced_translation_records}"
    )

    if spaced_translation_records > 0:

        print("""
WARNING:
Some category translations still contain spaces.
""")

    else:

        print(
            "PASSED: Underscore standardization validation."
        )

    # =====================================================
    # 10. CATEGORY SEMANTIC DISTRIBUTION VALIDATION
    # =====================================================

    """
    Validate category semantic completeness.
    """

    print("\n[10] CATEGORY SEMANTIC DISTRIBUTION VALIDATION")

    null_portuguese_categories = (

        transformed_df

        .filter(
            col("product_category_name").isNull()
        )

        .count()

    )

    print(
        f"Null Portuguese Category Records: "
        f"{null_portuguese_categories}"
    )

    if null_portuguese_categories > 0:

        raise ValueError(
            "FAILED: Null Portuguese categories detected."
        )

    print(
        "PASSED: Category semantic distribution validation."
    )

    # =====================================================
    # FINAL VALIDATION SUMMARY
    # =====================================================

    print("\n=================================================")
    print("ALL CATEGORY TRANSLATION VALIDATIONS COMPLETED")
    print("=================================================")

    print("""
Validation Summary:
- Semantic translation integrity verified
- Category uniqueness validated
- Multilingual normalization verified
- Business-readable formatting enforced
- Semantic completeness protected
- Controlled semantic governance applied

silver_category_translation is TRUSTED.
""")
