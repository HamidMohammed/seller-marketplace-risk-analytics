"""
order_delivery_staging_validation.py

Validation framework for:
order_delivery_staging

Objective:
Protect order-level grain integrity and delivery KPI trustworthiness.
"""

from pyspark.sql.functions import (
    col,
    count,
    when
)


# =========================================================
# MAIN VALIDATION RUNNER
# =========================================================

def run_order_delivery_staging_validation(df):

    print("\n=================================================")
    print("ORDER DELIVERY STAGING VALIDATION")
    print("=================================================")

    validate_row_count(df)

    validate_order_grain(df)

    validate_critical_nulls(df)

    validate_delivery_lifecycle(df)

    validate_delivered_orders(df)

    validate_seller_accountability(df)

    validate_distance_bucket(df)

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

def validate_order_grain(df):

    duplicates = df.groupBy(
        "order_id"
    ).count().filter(
        col("count") > 1
    ).count()

    print(f"\nDuplicate order_id Count: {duplicates}")

    if duplicates > 0:
        raise Exception(
            "FAILED: Order grain violation detected."
        )


# =========================================================
# CRITICAL NULL VALIDATION
# =========================================================

def validate_critical_nulls(df):

    critical_columns = [
        "order_id",
        "customer_id",
        "order_status",
        "order_purchase_timestamp",
        "seller_count",
        "distance_bucket"
    ]

    print("\nCritical Null Validation:")

    for column_name in critical_columns:

        null_count = df.filter(
            col(column_name).isNull()
        ).count()

        print(f"{column_name}: {null_count} nulls")


# =========================================================
# DELIVERY LIFECYCLE VALIDATION
# =========================================================

def validate_delivery_lifecycle(df):

    invalid_approval = df.filter(
        col("order_approved_at") <
        col("order_purchase_timestamp")
    ).count()

    invalid_delivery = df.filter(
        col("order_delivered_customer_date") <
        col("order_purchase_timestamp")
    ).count()

    print("\nLifecycle Validation:")

    print(
        f"Invalid Approval Timelines: {invalid_approval}"
    )

    print(
        f"Invalid Delivery Timelines: {invalid_delivery}"
    )


# =========================================================
# DELIVERED ORDER VALIDATION
# =========================================================

def validate_delivered_orders(df):

    invalid_delivered_orders = df.filter(

        (col("order_status") == "delivered") &

        (
            col(
                "order_delivered_customer_date"
            ).isNull()
        )

    ).count()

    print(
        f"\nDelivered Orders Missing Delivery Timestamp: "
        f"{invalid_delivered_orders}"
    )


# =========================================================
# SELLER ACCOUNTABILITY VALIDATION
# =========================================================

def validate_seller_accountability(df):

    multi_seller_orders = df.filter(
        col("is_multi_seller_order") == True
    ).count()

    single_seller_orders = df.filter(
        col("is_multi_seller_order") == False
    ).count()

    print("\nSeller Accountability Validation:")

    print(f"Multi Seller Orders: {multi_seller_orders}")

    print(f"Single Seller Orders: {single_seller_orders}")


# =========================================================
# DISTANCE BUCKET VALIDATION
# =========================================================

def validate_distance_bucket(df):

    print("\nDistance Bucket Distribution:")

    df.groupBy(
        "distance_bucket"
    ).count().show(truncate=False)
    
# =========================================================
# REGION DISTRIBUTION VALIDATION
# =========================================================

def validate_region_distribution(df):

    print("\nSeller Region Distribution:")

    df.groupBy(
        "seller_region"
    ).count().show(truncate=False)

    print("\nCustomer Region Distribution:")

    df.groupBy(
        "customer_region"
    ).count().show(truncate=False)