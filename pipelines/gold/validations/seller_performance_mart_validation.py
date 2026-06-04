"""
seller_performance_mart_validation.py

Objective:
Validate Seller Performance Mart quality,
business logic, KPI integrity,
and score classification accuracy.

Project:
Olist Seller Intelligence Platform

Layer:
Gold Mart Validation

Dataset:
seller_performance_mart
"""

# =========================================================
# IMPORTS
# =========================================================

from pyspark.sql.functions import (
    col,
    count,
    when
)


# =========================================================
# VALIDATION FUNCTION
# =========================================================

def run_seller_performance_mart_validation(
    mart_df
):

    print("\n" + "=" * 70)
    print("SELLER PERFORMANCE MART VALIDATION")
    print("=" * 70)

    # =====================================================
    # ROW COUNT
    # =====================================================

    print(
        f"\nFinal Row Count: "
        f"{mart_df.count():,}"
    )

    # =====================================================
    # GRAIN VALIDATION
    # =====================================================

    duplicate_grain = mart_df.groupBy(

        "seller_id",

        "performance_year",

        "performance_month"

    ).count().filter(

        col("count") > 1

    ).count()

    print(
        f"\nDuplicate Seller-Month Records: "
        f"{duplicate_grain}"
    )

    # =====================================================
    # FOREIGN KEY VALIDATION
    # =====================================================

    print("\nForeign Key Validation:")

    fk_columns = [

        "seller_sk_fk"
    ]

    for column_name in fk_columns:

        null_count = mart_df.filter(
            col(column_name).isNull()
        ).count()

        print(
            f"{column_name}: "
            f"{null_count:,} nulls"
        )

    # =====================================================
    # SCORE VALIDATION
    # =====================================================

    invalid_scores = mart_df.filter(

        (col("seller_score") < 0) |

        (col("seller_score") > 100)

    ).count()

    print(
        f"\nInvalid Seller Scores: "
        f"{invalid_scores:,}"
    )

    # =====================================================
    # CRITICAL NULL VALIDATION
    # =====================================================

    print("\nCritical Null Validation:")

    critical_columns = [

        "seller_id",

        "performance_year",

        "performance_month",

        "seller_score",

        "seller_risk_level",

        "seller_rank_tier"

    ]

    for column_name in critical_columns:

        null_count = mart_df.filter(
            col(column_name).isNull()
        ).count()

        print(
            f"{column_name}: "
            f"{null_count:,} nulls"
        )

    # =====================================================
    # KPI VALIDATION
    # =====================================================

    negative_orders = mart_df.filter(
        col("monthly_orders") < 0
    ).count()

    invalid_review_scores = mart_df.filter(

        (col("avg_review_score") < 0) |

        (col("avg_review_score") > 5)

    ).count()

    invalid_on_time_rates = mart_df.filter(

        (col("on_time_rate") < 0) |

        (col("on_time_rate") > 100)

    ).count()

    negative_workload = mart_df.filter(
        col("avg_monthly_workload") < 0
    ).count()

    print("\nKPI Validation:")

    print(
        f"Negative Monthly Orders: "
        f"{negative_orders:,}"
    )

    print(
        f"Invalid Review Scores: "
        f"{invalid_review_scores:,}"
    )

    print(
        f"Invalid On-Time Rates: "
        f"{invalid_on_time_rates:,}"
    )

    print(
        f"Negative Workload Values: "
        f"{negative_workload:,}"
    )

    # =====================================================
    # RISK LEVEL DISTRIBUTION
    # =====================================================

    print("\nRisk Level Distribution:")

    mart_df.groupBy(
        "seller_risk_level"
    ).count().show(
        truncate=False
    )

    # =====================================================
    # SELLER TIER DISTRIBUTION
    # =====================================================

    print("\nSeller Tier Distribution:")

    mart_df.groupBy(
        "seller_rank_tier"
    ).count().show(
        truncate=False
    )

    # =====================================================
    # PERFORMANCE CATEGORY DISTRIBUTION
    # =====================================================

    print("\nPerformance Category Distribution:")

    mart_df.groupBy(
        "seller_performance_category"
    ).count().show(
        truncate=False
    )

    # =====================================================
    # SCORE SUMMARY
    # =====================================================

    print("\nKPI Summary:")

    healthy_sellers = mart_df.filter(
        col("seller_risk_level") == "Healthy"
    ).count()

    warning_sellers = mart_df.filter(
        col("seller_risk_level") == "Warning"
    ).count()

    at_risk_sellers = mart_df.filter(
        col("seller_risk_level") == "At Risk"
    ).count()

    critical_sellers = mart_df.filter(
        col("seller_risk_level") == "Critical"
    ).count()

    print(
        f"Healthy Sellers: "
        f"{healthy_sellers:,}"
    )

    print(
        f"Warning Sellers: "
        f"{warning_sellers:,}"
    )

    print(
        f"At Risk Sellers: "
        f"{at_risk_sellers:,}"
    )

    print(
        f"Critical Sellers: "
        f"{critical_sellers:,}"
    )

    print("\nValidation Completed Successfully.")
