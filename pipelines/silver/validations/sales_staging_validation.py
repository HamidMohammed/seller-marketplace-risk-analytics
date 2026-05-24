"""
sales_staging_validation.py

Validation framework for:
sales_staging

Objective:
Protect sales grain integrity,
payment allocation correctness,
and financial reconciliation trustworthiness.
"""

from pyspark.sql.functions import (
    col,
    sum,
    round
)


# =========================================================
# MAIN VALIDATION RUNNER
# =========================================================

def run_sales_staging_validation(df):

    print("\n=================================================")
    print("SALES STAGING VALIDATION")
    print("=================================================")

    validate_row_count(df)

    validate_sales_grain(df)

    validate_critical_nulls(df)

    validate_negative_financials(df)

    validate_payment_allocation(df)

    validate_sales_ratio(df)

    validate_installment_distribution(df)

    print("\n=================================================")
    print("ALL VALIDATIONS COMPLETED")
    print("=================================================")


# =========================================================
# ROW COUNT VALIDATION
# =========================================================

def validate_row_count(df):

    row_count = df.count()

    print(f"\nFinal Row Count: {row_count}")


# =========================================================
# SALES GRAIN VALIDATION
# =========================================================

def validate_sales_grain(df):

    duplicates = df.groupBy(
        "order_id",
        "order_item_id"
    ).count().filter(
        col("count") > 1
    ).count()

    print(
        f"\nDuplicate Sales Grain Violations: "
        f"{duplicates}"
    )

    if duplicates > 0:

        raise Exception(
            "FAILED: Sales grain violation detected."
        )


# =========================================================
# CRITICAL NULL VALIDATION
# =========================================================

def validate_critical_nulls(df):

    critical_columns = [

        "order_id",

        "order_item_id",

        "seller_id",

        "gross_item_value",

        "allocated_payment_value",

        "item_sales_ratio"
    ]

    print("\nCritical Null Validation:")

    for column_name in critical_columns:

        null_count = df.filter(
            col(column_name).isNull()
        ).count()

        print(f"{column_name}: {null_count} nulls")


# =========================================================
# NEGATIVE FINANCIAL VALIDATION
# =========================================================

def validate_negative_financials(df):

    negative_prices = df.filter(
        col("price") < 0
    ).count()

    negative_freight = df.filter(
        col("freight_value") < 0
    ).count()

    negative_allocations = df.filter(
        col("allocated_payment_value") < 0
    ).count()

    print("\nNegative Financial Validation:")

    print(
        f"Negative Prices: "
        f"{negative_prices}"
    )

    print(
        f"Negative Freight Values: "
        f"{negative_freight}"
    )

    print(
        f"Negative Allocated Payments: "
        f"{negative_allocations}"
    )


# =========================================================
# PAYMENT RECONCILIATION VALIDATION
# =========================================================

def validate_payment_allocation(df):

    allocation_check = df.groupBy(
        "order_id"
    ).agg(

        round(
            sum("allocated_payment_value"),
            2
        ).alias("allocated_total"),

        round(
            sum("total_payment_value"),
            2
        ).alias("payment_total")
    )

    mismatches = allocation_check.filter(

        col("allocated_total") !=
        col("payment_total")

    ).count()

    print(
        f"\nPayment Allocation Mismatches: "
        f"{mismatches}"
    )


# =========================================================
# SALES RATIO VALIDATION
# =========================================================

def validate_sales_ratio(df):

    invalid_ratios = df.filter(

        (col("item_sales_ratio") < 0) |
        (col("item_sales_ratio") > 1)

    ).count()

    print(
        f"\nInvalid Sales Ratios: "
        f"{invalid_ratios}"
    )


# =========================================================
# INSTALLMENT DISTRIBUTION
# =========================================================

def validate_installment_distribution(df):

    print("\nInstallment Distribution:")

    df.groupBy(
        "installment_flag"
    ).count().show(truncate=False)