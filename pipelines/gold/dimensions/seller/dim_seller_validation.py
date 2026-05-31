"""
dim_seller_validation.py

Validation framework for:
dim_seller

Objective:
Protect seller dimension integrity,
conformed dimension consistency,
SCD readiness,
and downstream fact-table reliability.
"""

from pyspark.sql.functions import (
    col
)


# =========================================================
# MAIN VALIDATION RUNNER
# =========================================================

def run_dim_seller_validation(df):

    print("\n=================================================")
    print("DIM SELLER VALIDATION")
    print("=================================================")

    validate_row_count(df)

    validate_surrogate_key_uniqueness(df)

    validate_business_key_uniqueness(df)

    validate_critical_nulls(df)

    validate_scd_integrity(df)

    validate_geography_integrity(df)

    validate_acquisition_integrity(df)

    validate_dimension_distribution(df)

    print("\n=================================================")
    print("ALL VALIDATIONS COMPLETED")
    print("=================================================")


# =========================================================
# ROW COUNT
# =========================================================

def validate_row_count(df):

    row_count = df.count()

    print(f"\nFinal Row Count: {row_count}")


# =========================================================
# SURROGATE KEY VALIDATION
# =========================================================

def validate_surrogate_key_uniqueness(df):

    duplicate_sk = (

        df.groupBy(
            "seller_sk"
        )

        .count()

        .filter(
            col("count") > 1
        )

        .count()
    )

    print(
        f"\nDuplicate seller_sk Count: "
        f"{duplicate_sk}"
    )

    if duplicate_sk > 0:

        raise Exception(
            "FAILED: Duplicate seller_sk detected."
        )


# =========================================================
# BUSINESS KEY VALIDATION
# =========================================================

def validate_business_key_uniqueness(df):

    duplicate_seller_id = (

        df.groupBy(
            "seller_id"
        )

        .count()

        .filter(
            col("count") > 1
        )

        .count()
    )

    print(
        f"Duplicate seller_id Count: "
        f"{duplicate_seller_id}"
    )

    if duplicate_seller_id > 0:

        raise Exception(
            "FAILED: Duplicate seller_id detected."
        )


# =========================================================
# CRITICAL NULL VALIDATION
# =========================================================

def validate_critical_nulls(df):

    critical_columns = [

        "seller_sk",

        "seller_id",

        "seller_city",

        "seller_state",

        "seller_region",

        "is_current"
    ]

    print("\nCritical Null Validation:")

    for column_name in critical_columns:

        null_count = (

            df.filter(
                col(column_name).isNull()
            )

            .count()
        )

        print(
            f"{column_name}: "
            f"{null_count} nulls"
        )


# =========================================================
# SCD VALIDATION
# =========================================================

def validate_scd_integrity(df):

    invalid_current_flags = (

        df.filter(
            col("is_current").isNull()
        )

        .count()
    )

    invalid_start_dates = (

        df.filter(
            col("effective_start_date").isNull()
        )

        .count()
    )

    print("\nSCD Integrity Validation:")

    print(
        f"Null is_current Flags: "
        f"{invalid_current_flags}"
    )

    print(
        f"Null effective_start_date: "
        f"{invalid_start_dates}"
    )


# =========================================================
# GEOGRAPHY VALIDATION
# =========================================================

def validate_geography_integrity(df):

    missing_state = (

        df.filter(
            col("seller_state").isNull()
        )

        .count()
    )

    missing_region = (

        df.filter(
            col("seller_region").isNull()
        )

        .count()
    )

    print("\nGeography Validation:")

    print(
        f"Missing States: "
        f"{missing_state}"
    )

    print(
        f"Missing Regions: "
        f"{missing_region}"
    )


# =========================================================
# ACQUISITION VALIDATION
# =========================================================

def validate_acquisition_integrity(df):

    unknown_acquisition = (

        df.filter(

            col(
                "acquisition_source"
            ) == "Unknown"

        )

        .count()
    )

    print("\nAcquisition Validation:")

    print(
        f"Unknown Acquisition Sources: "
        f"{unknown_acquisition}"
    )


# =========================================================
# DIMENSION DISTRIBUTIONS
# =========================================================

def validate_dimension_distribution(df):

    print("\nSeller Region Distribution:")

    df.groupBy(
        "seller_region"
    ).count().show(
        truncate=False
    )

    print("\nSeller Location Type Distribution:")

    df.groupBy(
        "seller_location_type"
    ).count().show(
        truncate=False
    )

    print("\nSeller Business Profile Distribution:")

    df.groupBy(
        "seller_business_profile"
    ).count().show(
        truncate=False
    )