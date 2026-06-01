"""
dim_customer_validation.py

Objective:
Validate Gold Customer Dimension.

Dimension:
dim_customer

Grain:
ONE ROW = ONE CUSTOMER
"""

# =====================================================
# IMPORTS
# =====================================================

from pyspark.sql.functions import (
    col,
    count,
    when
)

# =====================================================
# VALIDATION
# =====================================================

def run_dim_customer_validation(df):

    print("=" * 60)
    print("DIM CUSTOMER VALIDATION")
    print("=" * 60)

    # =================================================
    # ROW COUNT
    # =================================================

    row_count = df.count()

    print(f"\nFinal Row Count: {row_count:,}")

    # =================================================
    # GRAIN VALIDATION
    # =================================================

    duplicate_customers = (

        df.groupBy(
            "customer_id"
        )

        .count()

        .filter(
            col("count") > 1
        )

        .count()
    )

    print(
        f"\nDuplicate Customer Grain Violations: "
        f"{duplicate_customers}"
    )

    # =================================================
    # SURROGATE KEY VALIDATION
    # =================================================

    duplicate_sk = (

        df.groupBy(
            "customer_sk"
        )

        .count()

        .filter(
            col("count") > 1
        )

        .count()
    )

    print(
        f"Duplicate Customer SK Count: "
        f"{duplicate_sk}"
    )

    # =================================================
    # CRITICAL NULLS
    # =================================================

    print("\nCritical Null Validation:")

    critical_columns = [

        "customer_sk",

        "customer_id",

        "customer_unique_id",

        "customer_city",

        "customer_state",

        "customer_region"
    ]

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

    # =================================================
    # REGION DISTRIBUTION
    # =================================================

    print(
        "\nCustomer Region Distribution:"
    )

    df.groupBy(
        "customer_region"
    ).count().show(
        truncate=False
    )

    # =================================================
    # LOCATION TYPE DISTRIBUTION
    # =================================================

    print(
        "\nCustomer Location Type Distribution:"
    )

    df.groupBy(
        "customer_location_type"
    ).count().show(
        truncate=False
    )

    # =================================================
    # GEO COORDINATE VALIDATION
    # =================================================

    missing_coordinates = (

        df.filter(

            col("median_latitude").isNull()
            |
            col("median_longitude").isNull()

        ).count()
    )

    print(
        f"\nCustomers Missing Coordinates: "
        f"{missing_coordinates}"
    )
    
    # =================================================
    # ZIP CODE VALIDATION
    # =================================================

    missing_zip_codes = (

        df.filter(
            col("customer_zip_code_prefix").isNull()
            
        ).count()
    )

    print(
        f"\nCustomers Missing Zip Codes: "
        f"{missing_zip_codes}"
    )

    # =================================================
    # NO ADDRESS VALIDATION
    # =================================================

    missing_address_info = (

        df.filter(
            col("customer_zip_code_prefix").isNull()
            &
            col("median_latitude").isNull()
            &
            col("median_longitude").isNull()
            
        ).count()
    )

    print(
        f"\nCustomers Missing Address Information: "
        f"{missing_address_info}"
    )

    # =================================================
    # UNKNOWN REGION CHECK
    # =================================================

    unknown_regions = (

        df.filter(
            col("customer_region") == "Unknown"
        )

        .count()
    )

    print(
        f"Customers With Unknown Region: "
        f"{unknown_regions}"
    )

    # =================================================
    # RESULT
    # =================================================

    print("\nValidation Complete.")
    print("=" * 60)