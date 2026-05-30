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
        f"Total Quarantined Payments: "
        f"{total_quarantined}"
    )

    quarantine_df.groupBy(
        "quarantine_reason"
    ).count().show(
        truncate=False
    )


# =========================================================
# PAYMENT SIZE DISTRIBUTION
# =========================================================

def validate_payment_size_distribution(
    df
):

    print(
        "\n[VALIDATION] PAYMENT SIZE DISTRIBUTION"
    )

    df.groupBy(
        "payment_size_category"
    ).count().show(
        truncate=False
    )


# =========================================================
# INSTALLMENT FLAGS
# =========================================================

def validate_installment_flags(
    df
):

    print(
        "\n[VALIDATION] INSTALLMENT FLAGS"
    )

    df.groupBy(
        "installment_flag"
    ).count().show(
        truncate=False
    )

    df.groupBy(
        "high_installment_flag"
    ).count().show(
        truncate=False
    )


# =========================================================
# PAYMENT SEQUENCE VALIDATION
# =========================================================

def validate_payment_sequences(
    df
):

    print(
        "\n[VALIDATION] PAYMENT SEQUENCES"
    )

    invalid_sequences = (

        df

        .filter(
            col("payment_sequential") <= 0
        )

        .count()

    )

    print(
        f"Invalid Payment Sequences: "
        f"{invalid_sequences}"
    )

    if invalid_sequences > 0:

        raise ValueError(
            "FAILED: Invalid payment sequences."
        )


# =========================================================
# PAYMENT TYPE VALIDATION
# =========================================================

def validate_payment_types(
    df
):

    print(
        "\n[VALIDATION] PAYMENT TYPES"
    )

    inconsistent_types = (

        df

        .filter(

            col("payment_type")
            !=
            lower(
                trim(
                    col("payment_type")
                )
            )

        )

        .count()

    )

    print(
        f"Inconsistent Payment Types: "
        f"{inconsistent_types}"
    )


# =========================================================
# HIGH INSTALLMENT ANALYSIS
# =========================================================

def validate_high_installments(
    df
):

    print(
        "\n[VALIDATION] HIGH INSTALLMENTS"
    )

    high_installments = (

        df

        .filter(
            col(
                "payment_installments"
            ) > 24
        )

        .count()

    )

    print(
        f"Installments >24: "
        f"{high_installments}"
    )


# =========================================================
# ZERO PAYMENT ANALYSIS
# =========================================================

def validate_zero_payments(
    df
):

    print(
        "\n[VALIDATION] ZERO PAYMENTS"
    )

    zero_payments = (

        df

        .filter(
            col("payment_value") == 0
        )

        .count()

    )

    print(
        f"Zero Payment Records: "
        f"{zero_payments}"
    )


# =========================================================
# MAIN VALIDATION RUNNER
# =========================================================

def run_payments_validation(

    source_df,
    transformed_df,
    quarantine_df

):

    print(
        "\n================================================="
    )

    print(
        "RUNNING CLENSING PAYMENTS VALIDATION"
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
        f"Clean Payments: "
        f"{transformed_count}"
    )

    print(
        f"Quarantined Payments: "
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
Investigate duplicates and quarantine logic.
""")

    # =====================================================
    # GRAIN
    # =====================================================

    validate_duplicates(

        df=transformed_df,

        key_columns=[
            "order_id",
            "payment_sequential"
        ]

    )

    # =====================================================
    # CRITICAL NULLS
    # =====================================================

    validate_nulls(

        df=transformed_df,

        critical_columns=[

            "order_id",

            "payment_sequential",

            "payment_type",

            "payment_value"

        ]

    )

    # =====================================================
    # POSITIVE VALUES
    # =====================================================

    validate_positive_values(

        df=transformed_df,

        column_name="payment_value"

    )

    validate_positive_values(

        df=transformed_df,

        column_name="payment_installments"

    )

    # =====================================================
    # CUSTOM VALIDATIONS
    # =====================================================

    validate_payment_sequences(
        transformed_df
    )

    validate_payment_types(
        transformed_df
    )

    validate_high_installments(
        transformed_df
    )

    validate_zero_payments(
        transformed_df
    )

    validate_payment_size_distribution(
        transformed_df
    )

    validate_installment_flags(
        transformed_df
    )

    validate_quarantine_counts(
        quarantine_df
    )

    print(
        "\n================================================="
    )

    print(
        "PAYMENTS VALIDATION COMPLETED"
    )

    print(
        "================================================="
    )

