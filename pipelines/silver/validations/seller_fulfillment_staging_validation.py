"""
seller_fulfillment_staging_validation.py

Validation framework for:
seller_fulfillment_staging

Objective:
Protect seller fulfillment grain integrity,
workload intelligence consistency,
and logistics enrichment quality.
"""

from pyspark.sql.functions import (
    col
)


# =========================================================
# MAIN VALIDATION RUNNER
# =========================================================

def run_seller_fulfillment_staging_validation(df):

    print("\n=================================================")
    print("SELLER FULFILLMENT STAGING VALIDATION")
    print("=================================================")

    validate_row_count(df)

    validate_grain(df)

    validate_critical_nulls(df)

    validate_workload_distribution(df)

    validate_seller_geography(df)

    validate_freight_metrics(df)

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
# GRAIN VALIDATION
# =========================================================

def validate_grain(df):

    duplicates = df.groupBy(
        "order_id",
        "order_item_id"
    ).count().filter(
        col("count") > 1
    ).count()

    print(
        f"\nDuplicate Grain Violations: {duplicates}"
    )

    if duplicates > 0:

        raise Exception(
            "FAILED: Seller fulfillment grain violation detected."
        )


# =========================================================
# CRITICAL NULL VALIDATION
# =========================================================

def validate_critical_nulls(df):

    critical_columns = [

        "order_id",
        "order_item_id",

        "seller_id",

        "price",
        "freight_value",

        "seller_monthly_orders",

        "workload_bucket"
    ]

    print("\nCritical Null Validation:")

    for column_name in critical_columns:

        null_count = df.filter(
            col(column_name).isNull()
        ).count()

        print(f"{column_name}: {null_count} nulls")


# =========================================================
# WORKLOAD DISTRIBUTION VALIDATION
# =========================================================

def validate_workload_distribution(df):

    print("\nWorkload Bucket Distribution:")

    df.groupBy(
        "workload_bucket"
    ).count().show(truncate=False)


# =========================================================
# SELLER GEOGRAPHY VALIDATION
# =========================================================

def validate_seller_geography(df):

    missing_geo = df.filter(

        col("seller_state").isNull()

    ).count()

    print(
        f"\nOrders Missing Seller Geography: "
        f"{missing_geo}"
    )


# =========================================================
# FREIGHT METRIC VALIDATION
# =========================================================

def validate_freight_metrics(df):

    negative_freight = df.filter(
        col("freight_value") < 0
    ).count()

    negative_price = df.filter(
        col("price") < 0
    ).count()

    print("\nFreight Metric Validation:")

    print(
        f"Negative Freight Values: "
        f"{negative_freight}"
    )

    print(
        f"Negative Price Values: "
        f"{negative_price}"
    )