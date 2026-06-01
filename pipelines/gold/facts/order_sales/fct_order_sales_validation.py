"""
fct_order_sales_validation.py

Objective:
Validate Gold Order Sales Fact Table

Fact:
fct_order_sales

Grain:
ONE ROW = ONE ORDER ITEM SOLD
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

def run_fct_order_sales_validation(df):

    print("=" * 60)
    print("FCT ORDER SALES VALIDATION")
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
            "sales_fact_sk"
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

        "product_sk_fk",

        "seller_sk_fk",
        
        "customer_sk_fk",

        "sales_date_sk"

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
    # CRITICAL NULL VALIDATION
    # =================================================

    print(
        "\nCritical Null Validation:"
    )

    critical_columns = [

        "order_id",

        "order_item_id",

        "price",

        "allocated_payment_value"

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
    # REVENUE VALIDATION
    # =================================================

    negative_price_values = (

        df.filter(
            col("price") < 0
        )

        .count()
    )

    print(
        f"\nNegative Price Values: "
        f"{negative_price_values}"
    )

    negative_payment_values = (

        df.filter(
            col(
                "allocated_payment_value"
            ) < 0
        )

        .count()
    )

    print(
        f"Negative Payment Values: "
        f"{negative_payment_values}"
    )

    negative_order_values = (

        df.filter(
            col(
                "total_order_item_value"
            ) < 0
        )

        .count()
    )

    print(
        f"Negative Order Values: "
        f"{negative_order_values}"
    )

    # =================================================
    # FREIGHT VALIDATION
    # =================================================

    negative_freight_values = (

        df.filter(
            col(
                "freight_value"
            ) < 0
        )

        .count()
    )

    print(
        f"Negative Freight Values: "
        f"{negative_freight_values}"
    )

    invalid_freight_below_ratio = (

        df.filter(

            (
                col("freight_ratio") < 0
            )

        )

        .count()
    )
    invalid_freight_above_ratio = (

    df.filter(

        (
            col("freight_ratio") > 1
        )

        )

        .count()
    )
    
    print(
        f"Freight Ratios above 1 : "
        f"{invalid_freight_above_ratio}"
    )
    
    print(
        f"Invalid Freight Ratios below 0 : "
        f"{invalid_freight_below_ratio}"
    )

    # =================================================
    # ITEM SALES RATIO VALIDATION
    # =================================================

    invalid_item_sales_ratio = (

        df.filter(

            (
                col("item_sales_ratio") < 0
            )

            |

            (
                col("item_sales_ratio") > 1
            )

        )

        .count()
    )

    print(
        f"Invalid Item Sales Ratios: "
        f"{invalid_item_sales_ratio}"
    )

    # =================================================
    # PRODUCT VOLUME VALIDATION
    # =================================================

    invalid_product_volume = (

        df.filter(
            col(
                "product_volume_cm3"
            ) < 0
        )

        .count()
    )

    print(
        f"Invalid Product Volume: "
        f"{invalid_product_volume}"
    )

    # =================================================
    # SELLER ITEM COUNT VALIDATION
    # =================================================

    invalid_seller_item_count = (

        df.filter(
            col(
                "seller_item_count_in_order"
            ) <= 0
        )

        .count()
    )

    print(
        f"Invalid Seller Item Counts: "
        f"{invalid_seller_item_count}"
    )

    # =================================================
    # INSTALLMENT VALIDATION
    # =================================================

    invalid_installments = (

        df.filter(
            col(
                "total_payment_installments"
            ) <= 0
        )

        .count()
    )

    print(
        f"Invalid Installment Counts: "
        f"{invalid_installments}"
    )

    # =================================================
    # FLAG CONSISTENCY VALIDATION
    # =================================================

    inconsistent_installment_flag = (

        df.filter(

            (
                col(
                    "total_payment_installments"
                ) > 1
            )

            &

            (
                col(
                    "installment_flag"
                ) == False
            )

        )

        .count()
    )

    print(
        f"Inconsistent Installment Flags: "
        f"{inconsistent_installment_flag}"
    )

    # =================================================
    # HIGH FREIGHT FLAG VALIDATION
    # =================================================

    inconsistent_high_freight = (

        df.filter(

            (
                col(
                    "freight_ratio"
                ) > 0.30
            )

            &

            (
                col(
                    "high_freight_item_flag"
                ) == False
            )

        )

        .count()
    )

    print(
        f"Inconsistent High Freight Flags: "
        f"{inconsistent_high_freight}"
    )

    # =================================================
    # HIGH TICKET DISTRIBUTION
    # =================================================

    high_ticket_count = (

        df.filter(
            col(
                "high_ticket_order_flag"
            ) == True
        )

        .count()
    )

    print(
        f"\nHigh Ticket Records: "
        f"{high_ticket_count:,}"
    )

    # =================================================
    # INSTALLMENT DISTRIBUTION
    # =================================================

    installment_count = (

        df.filter(
            col(
                "installment_flag"
            ) == True
        )

        .count()
    )

    print(
        f"Installment Records: "
        f"{installment_count:,}"
    )

    # =================================================
    # HIGH FREIGHT DISTRIBUTION
    # =================================================

    high_freight_count = (

        df.filter(
            col(
                "high_freight_item_flag"
            ) == True
        )

        .count()
    )

    print(
        f"High Freight Records: "
        f"{high_freight_count:,}"
    )

    # =================================================
    # KPI SUMMARY
    # =================================================

    print("\nKPI Summary:")

    print(
        f"Total Sales Records: "
        f"{row_count:,}"
    )

    print(
        f"High Ticket Records: "
        f"{high_ticket_count:,}"
    )

    print(
        f"Installment Records: "
        f"{installment_count:,}"
    )

    print(
        f"High Freight Records: "
        f"{high_freight_count:,}"
    )

    print("\nValidation Complete.")

    print("=" * 60)

