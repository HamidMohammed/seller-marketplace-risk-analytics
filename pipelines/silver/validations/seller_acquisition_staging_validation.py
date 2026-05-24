"""
seller_acquisition_staging_validation.py

Validation framework for:
seller_acquisition_staging

Objective:
Protect seller acquisition grain integrity,
conversion lifecycle correctness,
and acquisition intelligence trustworthiness.
"""

from pyspark.sql.functions import (
    col
)


# =========================================================
# MAIN VALIDATION RUNNER
# =========================================================

def run_seller_acquisition_staging_validation(df):

    print("\n=================================================")
    print("SELLER ACQUISITION STAGING VALIDATION")
    print("=================================================")

    validate_row_count(df)

    validate_mql_grain(df)

    validate_critical_nulls(df)

    validate_conversion_logic(df)

    validate_revenue_quality(df)

    validate_acquisition_distribution(df)

    validate_risk_distribution(df)

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
# MQL GRAIN VALIDATION
# =========================================================

def validate_mql_grain(df):

    duplicates = df.groupBy(
        "mql_id"
    ).count().filter(
        col("count") > 1
    ).count()

    print(
        f"\nDuplicate mql_id Count: {duplicates}"
    )

    if duplicates > 0:

        raise Exception(
            "FAILED: Acquisition grain violation detected."
        )


# =========================================================
# CRITICAL NULL VALIDATION
# =========================================================

def validate_critical_nulls(df):

    critical_columns = [

        "mql_id",

        "marketing_origin",

        "converted_flag",

        "acquisition_risk_category"
    ]

    print("\nCritical Null Validation:")

    for column_name in critical_columns:

        null_count = df.filter(
            col(column_name).isNull()
        ).count()

        print(f"{column_name}: {null_count} nulls")


# =========================================================
# CONVERSION LOGIC VALIDATION
# =========================================================

def validate_conversion_logic(df):

    invalid_conversion_dates = df.filter(

        col("days_to_convert") < 0

    ).count()

    print(
        f"\nInvalid Conversion Timelines: "
        f"{invalid_conversion_dates}"
    )


# =========================================================
# REVENUE QUALITY VALIDATION
# =========================================================

def validate_revenue_quality(df):

    negative_revenue = df.filter(

        col("declared_monthly_revenue") < 0

    ).count()

    print(
        f"\nNegative Revenue Values: "
        f"{negative_revenue}"
    )


# =========================================================
# ACQUISITION DISTRIBUTION
# =========================================================

def validate_acquisition_distribution(df):

    print("\nAcquisition Source Distribution:")

    df.groupBy(
        "marketing_origin"
    ).count().show(truncate=False)


# =========================================================
# RISK DISTRIBUTION
# =========================================================

def validate_risk_distribution(df):

    print("\nAcquisition Risk Distribution:")

    df.groupBy(
        "acquisition_risk_category"
    ).count().show(truncate=False)