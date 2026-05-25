"""
dim_date_validation.py

Validation framework for:
dim_date

Objective:
Protect temporal dimension integrity,
calendar consistency,
and conformed time intelligence correctness.
"""

from pyspark.sql.functions import (
    col,
    min,
    max
)


# =========================================================
# MAIN VALIDATION RUNNER
# =========================================================

def run_dim_date_validation(df):

    print("\n=================================================")
    print("DIM DATE VALIDATION")
    print("=================================================")

    validate_row_count(df)

    validate_primary_key_uniqueness(df)

    validate_critical_nulls(df)

    validate_date_ranges(df)

    validate_weekend_logic(df)

    validate_month_logic(df)

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
# PRIMARY KEY VALIDATION
# =========================================================

def validate_primary_key_uniqueness(df):

    duplicates = df.groupBy(
        "date_sk"
    ).count().filter(
        col("count") > 1
    ).count()

    print(
        f"\nDuplicate date_sk Count: "
        f"{duplicates}"
    )

    if duplicates > 0:

        raise Exception(
            "FAILED: Duplicate date_sk values detected."
        )


# =========================================================
# CRITICAL NULL VALIDATION
# =========================================================

def validate_critical_nulls(df):

    critical_columns = [

        "date_sk",

        "full_date",

        "year",

        "month",

        "day",

        "day_name",

        "month_name"
    ]

    print("\nCritical Null Validation:")

    for column_name in critical_columns:

        null_count = df.filter(
            col(column_name).isNull()
        ).count()

        print(f"{column_name}: {null_count} nulls")


# =========================================================
# DATE RANGE VALIDATION
# =========================================================

def validate_date_ranges(df):

    min_date = df.select(
        min("full_date")
    ).collect()[0][0]

    max_date = df.select(
        max("full_date")
    ).collect()[0][0]

    print("\nDate Range Validation:")

    print(f"Minimum Date: {min_date}")

    print(f"Maximum Date: {max_date}")


# =========================================================
# WEEKEND VALIDATION
# =========================================================

def validate_weekend_logic(df):

    invalid_weekend_flags = df.filter(

        (
            col("day_name").isin(
                ["Saturday", "Sunday"]
            )
        ) &
        (
            col("is_weekend") == False
        )

    ).count()

    print(
        f"\nInvalid Weekend Flags: "
        f"{invalid_weekend_flags}"
    )


# =========================================================
# MONTH LOGIC VALIDATION
# =========================================================

def validate_month_logic(df):

    invalid_months = df.filter(

        (col("month") < 1) |
        (col("month") > 12)

    ).count()

    invalid_quarters = df.filter(

        (col("quarter") < 1) |
        (col("quarter") > 4)

    ).count()

    print("\nMonth Logic Validation:")

    print(
        f"Invalid Months: "
        f"{invalid_months}"
    )

    print(
        f"Invalid Quarters: "
        f"{invalid_quarters}"
    )