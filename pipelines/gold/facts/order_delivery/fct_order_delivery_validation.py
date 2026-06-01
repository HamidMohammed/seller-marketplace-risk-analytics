"""
order_delivery_fact_validation.py

Objective:
Validate Gold Order Delivery Fact Table

Fact:
fct_order_delivery

Grain:
ONE ROW = ONE CUSTOMER ORDER
"""

# =====================================================
# IMPORTS
# =====================================================

from pyspark.sql.functions import (
    col
)

# =====================================================
# VALIDATION
# =====================================================

def run_order_delivery_fact_validation(df):

    print("=" * 60)
    print("FCT ORDER DELIVERY VALIDATION")
    print("=" * 60)

    # =================================================
    # ROW COUNT
    # =================================================

    row_count = df.count()

    print(
        f"\nFinal Row Count: "
        f"{row_count:,}"
    )

    # =================================================
    # FACT GRAIN VALIDATION
    # =================================================

    duplicate_orders = (

        df.groupBy(
            "order_id"
        )

        .count()

        .filter(
            col("count") > 1
        )

        .count()
    )

    print(
        f"\nDuplicate Order Grain Violations: "
        f"{duplicate_orders}"
    )

    # =================================================
    # FACT SURROGATE KEY VALIDATION
    # =================================================

    duplicate_fact_sk = (

        df.groupBy(
            "delivery_fact_sk"
        )

        .count()

        .filter(
            col("count") > 1
        )

        .count()
    )

    print(
        f"Duplicate Fact SK Count: "
        f"{duplicate_fact_sk}"
    )

    # =================================================
    # FOREIGN KEY VALIDATION
    # =================================================

    print(
        "\nForeign Key Validation:"
    )

    fk_columns = [

        "customer_sk_fk",

        "purchase_date_sk",

        "estimated_delivery_date_sk"

    ]

    for fk in fk_columns:

        null_count = (

            df.filter(
                col(fk).isNull()
            )

            .count()
        )

        print(
            f"{fk}: "
            f"{null_count} nulls"
        )

    # =================================================
    # SELLER FK
    # =================================================

    seller_fk_nulls = (

        df.filter(
            col(
                "seller_sk_fk"
            ).isNull()
        )

        .count()
    )

    print(
        f"seller_sk_fk: "
        f"{seller_fk_nulls} nulls"
    )

    # =================================================
    # ACTUAL DELIVERY DATE FK
    # =================================================

    actual_delivery_fk_nulls = (

        df.filter(

            col(
                "actual_delivery_date_sk"
            ).isNull()

            &
            col(
                "order_delivered_customer_date"
            ).isNotNull()

        )

        .count()
    )

    print(
        f"actual_delivery_date_sk Missing: "
        f"{actual_delivery_fk_nulls}"
    )

    # =================================================
    # DELIVERY KPI VALIDATION
    # =================================================

    print(
        "\nDelivery KPI Validation:"
    )

    invalid_delivery_duration = (

        df.filter(
            col(
                "delivery_duration_days"
            ) < 0
        )

        .count()
    )

    print(
        f"Negative Delivery Duration: "
        f"{invalid_delivery_duration}"
    )

    # =================================================
    # FREIGHT VALIDATION
    # =================================================

    negative_freight = (

        df.filter(
            col(
                "freight_total_value"
            ) < 0
        )

        .count()
    )

    print(
        f"Negative Freight Values: "
        f"{negative_freight}"
    )

    # =================================================
    # ITEM COUNT VALIDATION
    # =================================================

    invalid_item_count = (

        df.filter(
            col(
                "total_items_count"
            ) <= 0
        )

        .count()
    )

    print(
        f"Invalid Item Counts: "
        f"{invalid_item_count}"
    )

    # =================================================
    # SELLER COUNT VALIDATION
    # =================================================

    invalid_seller_count = (

        df.filter(
            col(
                "seller_count"
            ) <= 0
        )

        .count()
    )

    print(
        f"Invalid Seller Counts: "
        f"{invalid_seller_count}"
    )

    # =================================================
    # ON TIME FLAG VALIDATION
    # =================================================

    inconsistent_on_time = (

        df.filter(

            (
                col("delay_days") <= 0
            )

            &

            (
                col(
                    "on_time_delivery_flag"
                ) == False
            )

        )

        .count()
    )

    print(
        f"Inconsistent On-Time Flags: "
        f"{inconsistent_on_time}"
    )

    # =================================================
    # LATE FLAG VALIDATION
    # =================================================

    inconsistent_late = (

        df.filter(

            (
                col("delay_days") > 0
            )

            &

            (
                col(
                    "late_delivery_flag"
                ) == False
            )

        )

        .count()
    )

    print(
        f"Inconsistent Late Flags: "
        f"{inconsistent_late}"
    )

    # =================================================
    # MULTI SELLER ANALYSIS
    # =================================================

    multi_seller_orders = (

        df.filter(
            col(
                "is_multi_seller_order"
            ) == True
        )

        .count()
    )

    print(
        f"\nMulti Seller Orders: "
        f"{multi_seller_orders:,}"
    )

    single_seller_orders = (

        df.filter(
            col(
                "is_multi_seller_order"
            ) == False
        )

        .count()
    )

    print(
        f"Single Seller Orders: "
        f"{single_seller_orders:,}"
    )

    # =================================================
    # DELIVERY STATUS DISTRIBUTION
    # =================================================

    print(
        "\nDelivery Status Distribution:"
    )

    df.groupBy(
        "delivery_status_category"
    ).count().show(
        truncate=False
    )

    # =================================================
    # DISTANCE DISTRIBUTION
    # =================================================

    print(
        "\nDistance Bucket Distribution:"
    )

    df.groupBy(
        "distance_bucket"
    ).count().show(
        truncate=False
    )

    # =================================================
    # KPI SUMMARY
    # =================================================

    on_time_orders = (

        df.filter(
            col(
                "on_time_delivery_flag"
            ) == True
        )

        .count()
    )

    late_orders = (

        df.filter(
            col(
                "late_delivery_flag"
            ) == True
        )

        .count()
    )

    print(
        f"\nOn-Time Orders: "
        f"{on_time_orders:,}"
    )

    print(
        f"Late Orders: "
        f"{late_orders:,}"
    )

    print("\nValidation Complete.")

    print("=" * 60)