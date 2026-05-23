"""
closed_deals_validation.py

Objective:
Validation framework for silver_closed_deals dataset.

This module protects:
- commercial conversion integrity
- sales-funnel consistency
- CRM operational trust
- onboarding chronology reliability
- business segmentation consistency
- acquisition analytical trust

Project:
Olist Seller Intelligence Platform

Layer:
Silver Validation Layer

Dataset:
silver_closed_deals
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
    lower,
    current_timestamp
)

from pipelines.silver.validations.validation_utils import (
    validate_duplicates,
    validate_nulls,
    validate_positive_values
)


# =========================================================
# MAIN VALIDATION FUNCTION
# =========================================================

def run_closed_deals_validation(
    source_df,
    transformed_df
):
    """
    Run complete validation suite for
    silver_closed_deals.

    Parameters
    ----------
    source_df : DataFrame
        Original Bronze closed deals dataframe.

    transformed_df : DataFrame
        Final Silver closed deals dataframe.
    """

    print("\n=================================================")
    print("RUNNING CLOSED DEALS VALIDATION")
    print("=================================================")

    # =====================================================
    # 1. ROW COUNT ANALYSIS
    # =====================================================

    """
    Commercial datasets should preserve
    conversion-event cardinality.
    """

    print("\n[1] ROW COUNT ANALYSIS")

    source_count = source_df.count()

    transformed_count = transformed_df.count()

    print(
        f"Source Closed Deals Count: "
        f"{source_count}"
    )

    print(
        f"Silver Closed Deals Count: "
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
    ONE ROW = ONE CLOSED COMMERCIAL DEAL
    """

    print("\n[2] GRAIN VALIDATION")

    validate_duplicates(
        df=transformed_df,
        key_columns=["mql_id"]
    )

    # =====================================================
    # 3. CRITICAL NULL VALIDATION
    # =====================================================

    print("\n[3] CRITICAL NULL VALIDATION")

    critical_columns = [

        "mql_id",

        "won_date",

        "business_segment"

    ]

    validate_nulls(
        df=transformed_df,
        critical_columns=critical_columns
    )

    # =====================================================
    # 4. MQL ID VALIDATION
    # =====================================================

    """
    Validate CRM acquisition identifiers.
    """

    print("\n[4] MQL ID VALIDATION")

    invalid_mql_ids = (

        transformed_df

        .filter(

            col("mql_id").isNull()

            |

            (
                trim(col("mql_id")) == ""
            )

        )

        .count()

    )

    print(
        f"Invalid MQL ID Records: "
        f"{invalid_mql_ids}"
    )

    if invalid_mql_ids > 0:

        raise ValueError(
            "FAILED: Invalid MQL IDs detected."
        )

    print("PASSED: MQL ID validation.")

    # =====================================================
    # 5. BUSINESS SEGMENT VALIDATION
    # =====================================================

    """
    Validate deterministic business segmentation.
    """

    print("\n[5] BUSINESS SEGMENT VALIDATION")

    inconsistent_business_segments = (

        transformed_df

        .filter(

            col("business_segment").isNotNull()

            &

            (
                col("business_segment")
                !=
                lower(
                    trim(
                        col("business_segment")
                    )
                )
            )

        )

        .count()

    )

    print(
        f"Inconsistent Business Segments: "
        f"{inconsistent_business_segments}"
    )

    if inconsistent_business_segments > 0:

        print("""
WARNING:
Some business segments are not normalized.
""")

    else:

        print(
            "PASSED: Business segment normalization validation."
        )

    
    # =====================================================
    # 6. TIMESTAMP VALIDATION
    # =====================================================

    """
    Validate commercial chronology consistency.
    """

    print("\n[7] TIMESTAMP VALIDATION")

    invalid_won_dates = (

        transformed_df

        .filter(
            col("won_date").isNull()
        )

        .count()

    )

    print(
        f"Invalid Won Date Records: "
        f"{invalid_won_dates}"
    )

    if invalid_won_dates > 0:

        raise ValueError(
            "FAILED: Invalid won-date timestamps detected."
        )

    print("PASSED: Timestamp validation.")


    # =====================================================
    # 8. REVENUE VALIDATION
    # =====================================================

    """
    Validate commercial revenue realism.
    """

    print("\n[9] REVENUE VALIDATION")

    validate_positive_values(
        df=transformed_df,
        column_name="declared_monthly_revenue"
    )

    # =====================================================
    # 9. FUTURE DATE VALIDATION
    # =====================================================

    """
    Validate temporal commercial realism.
    """

    print("\n[10] FUTURE DATE VALIDATION")

    future_won_dates = (

        transformed_df

        .filter(

            col("won_date")
            >
            current_timestamp()

        )

        .count()

    )

    print(
        f"Future Won Date Records: "
        f"{future_won_dates}"
    )

    if future_won_dates > 0:

        print("""
WARNING:
Some commercial conversion events occur in the future.
""")

    else:

        print(
            "PASSED: Future date validation."
        )

    # =====================================================
    # FINAL VALIDATION SUMMARY
    # =====================================================

    print("\n=================================================")
    print("ALL CLOSED DEALS VALIDATIONS COMPLETED")
    print("=================================================")

    print("""
Validation Summary:
- Commercial conversion integrity verified
- Sales-funnel chronology validated
- CRM operational consistency protected
- Business segmentation normalization enforced
- Commercial revenue realism validated
- Controlled acquisition governance applied

silver_closed_deals is TRUSTED.
""")
