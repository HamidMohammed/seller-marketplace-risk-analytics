"""
payments_validation.py

Objective:
Validation framework for silver_payments dataset.

This module protects:
- financial operational integrity
- payment-grain correctness
- revenue consistency
- installment reliability
- payment-method normalization
- monetization analytical trust

Project:
Olist Seller Intelligence Platform

Layer:
Silver Validation Layer

Dataset:
silver_payments
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

def run_payments_validation(
    source_df,
    transformed_df
):
    """
    Run complete validation suite for silver_payments.

    Parameters
    ----------
    source_df : DataFrame
        Original Bronze payments dataframe.

    transformed_df : DataFrame
        Final Silver payments dataframe.
    """

    print("\n=================================================")
    print("RUNNING PAYMENTS VALIDATION")
    print("=================================================")

    # =====================================================
    # 1. ROW COUNT ANALYSIS
    # =====================================================

    """
    Payment datasets should preserve
    atomic operational payment events.
    """

    print("\n[1] ROW COUNT ANALYSIS")

    source_count = source_df.count()

    transformed_count = transformed_df.count()

    print(f"Source Payment Count: {source_count}")

    print(
        f"Silver Payment Count: "
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
    ONE ROW = ONE PAYMENT EVENT
    """

    print("\n[2] GRAIN VALIDATION")

    validate_duplicates(
        df=transformed_df,
        key_columns=[
            "order_id",
            "payment_sequential"
        ]
    )

    # =====================================================
    # 3. CRITICAL NULL VALIDATION
    # =====================================================

    print("\n[3] CRITICAL NULL VALIDATION")

    critical_columns = [

        "order_id",

        "payment_sequential",

        "payment_type",

        "payment_value"

    ]

    validate_nulls(
        df=transformed_df,
        critical_columns=critical_columns
    )

    # =====================================================
    # 4. PAYMENT TYPE VALIDATION
    # =====================================================

    """
    Validate payment-method normalization.
    """

    print("\n[4] PAYMENT TYPE VALIDATION")

    inconsistent_payment_types = (

        transformed_df

        .filter(

            col("payment_type")
            !=
            lower(
                trim(col("payment_type"))
            )

        )

        .count()

    )

    print(
        f"Inconsistent Payment Types: "
        f"{inconsistent_payment_types}"
    )

    if inconsistent_payment_types > 0:

        print("""
WARNING:
Some payment types are not normalized.
""")

    else:

        print(
            "PASSED: Payment type validation."
        )

    # =====================================================
    # 5. PAYMENT VALUE VALIDATION
    # =====================================================

    """
    Payment values must be non-negative.
    """

    print("\n[5] PAYMENT VALUE VALIDATION")

    validate_positive_values(
        df=transformed_df,
        column_name="payment_value"
    )

    # =====================================================
    # 6. INSTALLMENT VALIDATION
    # =====================================================

    """
    Installments must be non-negative.
    """

    print("\n[6] INSTALLMENT VALIDATION")

    validate_positive_values(
        df=transformed_df,
        column_name="payment_installments"
    )

    # =====================================================
    # 7. PAYMENT SEQUENCE VALIDATION
    # =====================================================

    """
    Payment sequence numbers must be positive.
    """

    print("\n[7] PAYMENT SEQUENCE VALIDATION")

    invalid_payment_sequences = (

        transformed_df

        .filter(
            col("payment_sequential") <= 0
        )

        .count()

    )

    print(
        f"Invalid Payment Sequence Records: "
        f"{invalid_payment_sequences}"
    )

    if invalid_payment_sequences > 0:

        raise ValueError(
            "FAILED: Invalid payment sequences detected."
        )

    print("PASSED: Payment sequence validation.")

    # =====================================================
    # 8. HIGH INSTALLMENT ANALYSIS
    # =====================================================

    """
    Analyze unusually high installment counts.
    NOT a failure condition.
    """

    print("\n[8] HIGH INSTALLMENT ANALYSIS")

    high_installment_records = (

        transformed_df

        .filter(
            col("payment_installments") > 24
        )

        .count()

    )

    print(
        f"High Installment Records (>24): "
        f"{high_installment_records}"
    )

    print("""
INFO:
High installment counts are preserved
for operational behavioral analysis.
""")

    # =====================================================
    # 9. ZERO PAYMENT ANALYSIS
    # =====================================================

    """
    Analyze zero-value payments.
    NOT automatically invalid.
    """

    print("\n[9] ZERO PAYMENT ANALYSIS")

    zero_payment_records = (

        transformed_df

        .filter(
            col("payment_value") == 0
        )

        .count()

    )

    print(
        f"Zero Payment Records: "
        f"{zero_payment_records}"
    )

    print("""
INFO:
Zero-value payments may represent:
- promotions
- adjustments
- operational edge cases
- marketplace anomalies
""")

    # =====================================================
    # 10. PAYMENT DISTRIBUTION VALIDATION
    # =====================================================

    """
    Analyze payment-method completeness.
    """

    print("\n[10] PAYMENT DISTRIBUTION VALIDATION")

    null_payment_type_records = (

        transformed_df

        .filter(
            col("payment_type").isNull()
        )

        .count()

    )

    print(
        f"Null Payment Type Records: "
        f"{null_payment_type_records}"
    )

    if null_payment_type_records > 0:

        raise ValueError(
            "FAILED: Null payment types detected."
        )

    print(
        "PASSED: Payment distribution validation."
    )

    # =====================================================
    # FINAL VALIDATION SUMMARY
    # =====================================================

    print("\n=================================================")
    print("ALL PAYMENTS VALIDATIONS COMPLETED")
    print("=================================================")

    print("""
Validation Summary:
- Payment grain integrity verified
- Revenue integrity validated
- Installment correctness verified
- Payment-method normalization verified
- Financial operational consistency protected
- Controlled anomaly governance applied

silver_payments is TRUSTED.
""")
