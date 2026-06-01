"""
seller_fulfillment_fact_validation.py

Objective:
Validate Gold Seller Fulfillment Fact Table

Fact:
fct_seller_fulfillment

Grain:
ONE ROW = ONE ORDER ITEM FULFILLED BY ONE SELLER
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

def run_seller_fulfillment_fact_validation(df):

    print("=" * 60)
    print("FCT SELLER FULFILLMENT VALIDATION")
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

    duplicate_grain = (

        df.groupBy(
            "order_id",
            "order_item_id"
        )

        .count()

        .filter(
            col("count") > 1
        )

        .count()
    )

    print(
        f"\nDuplicate Grain Violations: "
        f"{duplicate_grain}"
    )

    # =================================================
    # FACT SK VALIDATION
    # =================================================

    duplicate_fact_sk = (

        df.groupBy(
            "fulfillment_fact_sk"
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

        "seller_sk_fk",

        "product_sk_fk",

        "purchase_date_sk"

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
    # CRITICAL METRIC VALIDATION
    # =================================================

    print(
        "\nCritical Metric Validation:"
    )

    metric_columns = [

        "price",

        "freight_value",

        "seller_monthly_orders"

    ]

    for metric in metric_columns:

        null_count = (

            df.filter(
                col(metric).isNull()
            )

            .count()
        )

        print(
            f"{metric}: "
            f"{null_count} nulls"
        )

    # =================================================
    # PRICE VALIDATION
    # =================================================

    negative_price = (

        df.filter(
            col("price") < 0
        )

        .count()
    )

    print(
        f"\nNegative Price Values: "
        f"{negative_price}"
    )

    # =================================================
    # FREIGHT VALIDATION
    # =================================================

    negative_freight = (

        df.filter(
            col("freight_value") < 0
        )

        .count()
    )

    print(
        f"Negative Freight Values: "
        f"{negative_freight}"
    )

    # =================================================
    # FREIGHT RATIO VALIDATION
    # =================================================

    invalid_freight_ratio = (

        df.filter(
            col("freight_ratio") < 0
        )

        .count()
    )

    print(
        f"Invalid Freight Ratios: "
        f"{invalid_freight_ratio}"
    )

    # =================================================
    # WORKLOAD VALIDATION
    # =================================================

    invalid_monthly_orders = (

        df.filter(
            col("seller_monthly_orders") <= 0
        )

        .count()
    )

    print(
        f"Invalid Seller Monthly Orders: "
        f"{invalid_monthly_orders}"
    )

    # =================================================
    # HIGH WORKLOAD FLAG CONSISTENCY
    # =================================================

    inconsistent_high_workload = (

        df.filter(

            (
                col(
                    "workload_bucket"
                ).isin(
                    "High Volume",
                    "Overloaded"
                )
            )

            &

            (
                col(
                    "high_workload_flag"
                ) == False
            )

        )

        .count()
    )

    print(
        f"Inconsistent High Workload Flags: "
        f"{inconsistent_high_workload}"
    )

    # =================================================
    # OVERLOADED SELLER VALIDATION
    # =================================================

    overloaded_sellers = (

        df.filter(
            col(
                "is_overloaded_seller"
            ) == True
        )

        .count()
    )

    print(
        f"\nOverloaded Seller Records: "
        f"{overloaded_sellers:,}"
    )

    # =================================================
    # HIGH FREIGHT VALIDATION
    # =================================================

    high_freight_records = (

        df.filter(
            col(
                "high_freight_item_flag"
            ) == True
        )

        .count()
    )

    print(
        f"High Freight Items: "
        f"{high_freight_records:,}"
    )

    # =================================================
    # WORKLOAD DISTRIBUTION
    # =================================================

    print(
        "\nWorkload Distribution:"
    )

    df.groupBy(
        "workload_bucket"
    ).count().show(
        truncate=False
    )

    # =================================================
    # ACQUISITION SOURCE ANALYSIS
    # =================================================

    print(
        "\nAcquisition Source Distribution:"
    )

    df.groupBy(
        "acquisition_source"
    ).count().orderBy(
        col("count").desc()
    ).show(
        truncate=False
    )

    # =================================================
    # KPI SUMMARY
    # =================================================

    print(
        "\nKPI Summary:"
    )

    print(
        f"Total Fulfillment Records: "
        f"{row_count:,}"
    )

    print(
        f"High Freight Records: "
        f"{high_freight_records:,}"
    )

    print(
        f"Overloaded Seller Records: "
        f"{overloaded_sellers:,}"
    )
    

    print("\nValidation Complete.")

    print("=" * 60)

