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
    max,
    count
)

from datetime import timedelta


# =========================================================
# MAIN VALIDATION RUNNER
# =========================================================

def run_dim_date_validation(df):

    print("\n=================================================")
    print("DIM DATE VALIDATION")
    print("=================================================")

    validate_row_count(df)

    validate_primary_key_uniqueness(df)

    validate_full_date_uniqueness(df)

    validate_critical_nulls(df)

    validate_date_ranges(df)

    validate_date_continuity(df)

    validate_weekend_logic(df)

    validate_business_day_logic(df)

    validate_month_logic(df)

    print("\n=================================================")
    print("ALL VALIDATIONS COMPLETED SUCCESSFULLY")
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

    duplicates = (

        df.groupBy("date_sk")
        .count()
        .filter(col("count") > 1)
        .count()

    )

    print(
        f"\nDuplicate date_sk Count: "
        f"{duplicates}"
    )

    if duplicates > 0:

        raise Exception(
            "FAILED: Duplicate date_sk values detected."
        )

    print("PASSED: date_sk uniqueness validation")


# =========================================================
# FULL DATE UNIQUENESS VALIDATION
# =========================================================

def validate_full_date_uniqueness(df):

    duplicates = (

        df.groupBy("full_date")
        .count()
        .filter(col("count") > 1)
        .count()

    )

    print(
        f"\nDuplicate full_date Count: "
        f"{duplicates}"
    )

    if duplicates > 0:

        raise Exception(
            "FAILED: Duplicate full_date values detected."
        )

    print("PASSED: full_date uniqueness validation")


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

        null_count = (

            df.filter(
                col(column_name).isNull()
            ).count()

        )

        print(
            f"{column_name}: "
            f"{null_count} nulls"
        )

        if null_count > 0:

            raise Exception(
                f"FAILED: Null values detected "
                f"in {column_name}"
            )

    print("PASSED: critical null validation")


# =========================================================
# DATE RANGE VALIDATION
# =========================================================

def validate_date_ranges(df):

    min_date = (

        df.select(
            min("full_date")
        ).collect()[0][0]

    )

    max_date = (

        df.select(
            max("full_date")
        ).collect()[0][0]

    )

    print("\nDate Range Validation:")

    print(f"Minimum Date: {min_date}")

    print(f"Maximum Date: {max_date}")


# =========================================================
# DATE CONTINUITY VALIDATION
# =========================================================

def validate_date_continuity(df):

    min_date = (

        df.select(
            min("full_date")
        ).collect()[0][0]

    )

    max_date = (

        df.select(
            max("full_date")
        ).collect()[0][0]

    )

    expected_days = (

        max_date - min_date
    ).days + 1

    actual_days = df.count()

    print("\nDate Continuity Validation:")

    print(
        f"Expected Days: "
        f"{expected_days}"
    )

    print(
        f"Actual Days: "
        f"{actual_days}"
    )

    if expected_days != actual_days:

        raise Exception(
            "FAILED: Missing dates detected "
            "inside dim_date."
        )

    print("PASSED: date continuity validation")


# =========================================================
# WEEKEND VALIDATION
# =========================================================

def validate_weekend_logic(df):

    invalid_weekend_flags = (

        df.filter(

            (
                col("day_name").isin(
                    ["Saturday", "Sunday"]
                )
            )

            &

            (
                col("is_weekend") == False
            )

        ).count()

    )

    print(
        f"\nInvalid Weekend Flags: "
        f"{invalid_weekend_flags}"
    )

    if invalid_weekend_flags > 0:

        raise Exception(
            "FAILED: Weekend flag logic invalid."
        )

    print("PASSED: weekend validation")


# =========================================================
# BUSINESS DAY VALIDATION
# =========================================================

def validate_business_day_logic(df):

    if "is_business_day" not in df.columns:

        print(
            "\nBusiness Day Validation: "
            "SKIPPED (column not found)"
        )

        return

    invalid_business_days = (

        df.filter(

            (col("is_weekend") == True)

            &

            (col("is_business_day") == True)

        ).count()

    )

    print(
        f"\nInvalid Business Day Flags: "
        f"{invalid_business_days}"
    )

    if invalid_business_days > 0:

        raise Exception(
            "FAILED: Business day logic invalid."
        )

    print("PASSED: business day validation")


# =========================================================
# MONTH LOGIC VALIDATION
# =========================================================

def validate_month_logic(df):

    invalid_months = (

        df.filter(

            (col("month") < 1)
            |
            (col("month") > 12)

        ).count()

    )

    invalid_quarters = (

        df.filter(

            (col("quarter") < 1)
            |
            (col("quarter") > 4)

        ).count()

    )

    print("\nMonth Logic Validation:")

    print(
        f"Invalid Months: "
        f"{invalid_months}"
    )

    print(
        f"Invalid Quarters: "
        f"{invalid_quarters}"
    )

    if invalid_months > 0:

        raise Exception(
            "FAILED: Invalid month values detected."
        )

    if invalid_quarters > 0:

        raise Exception(
            "FAILED: Invalid quarter values detected."
        )

    print("PASSED: month and quarter validation")