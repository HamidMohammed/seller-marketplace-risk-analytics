"""
seller_performance_monthly_staging_validation.py

Validation framework for:
seller_performance_monthly_staging

Objective:
Protect temporal seller-performance grain integrity,
behavioral metric correctness,
and longitudinal analytical trustworthiness.
"""

from pyspark.sql.functions import (
    col
)


# =========================================================
# MAIN VALIDATION RUNNER
# =========================================================

def run_seller_performance_monthly_staging_validation(df):

    print("\n=================================================")
    print("SELLER PERFORMANCE MONTHLY VALIDATION")
    print("=================================================")

    validate_row_count(df)

    validate_temporal_grain(df)

    validate_critical_nulls(df)

    validate_performance_ranges(df)

    validate_growth_rate_logic(df)

    validate_performance_distribution(df)
    
    validate_growth_category_distribution(df)
    
    

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
# TEMPORAL GRAIN VALIDATION
# =========================================================

def validate_temporal_grain(df):

    duplicates = df.groupBy(
        "seller_id",
        "performance_year",
        "performance_month"
    ).count().filter(
        col("count") > 1
    ).count()

    print(
        f"\nTemporal Grain Violations: "
        f"{duplicates}"
    )

    if duplicates > 0:

        raise Exception(
            "FAILED: Seller-month grain violation detected."
        )


# =========================================================
# CRITICAL NULL VALIDATION
# =========================================================

def validate_critical_nulls(df):

    critical_columns = [

        "seller_id",

        "performance_year",

        "performance_month",

        "monthly_orders",

        "on_time_rate",

        "seller_performance_category"
    ]

    print("\nCritical Null Validation:")

    for column_name in critical_columns:

        null_count = df.filter(
            col(column_name).isNull()
        ).count()

        print(f"{column_name}: {null_count} nulls")


# =========================================================
# PERFORMANCE RANGE VALIDATION
# =========================================================

def validate_performance_ranges(df):

    invalid_on_time_rates = df.filter(

        (col("on_time_rate") < 0) |
        (col("on_time_rate") > 1)

    ).count()

    invalid_review_scores = df.filter(

        (col("avg_review_score") < 1) |
        (col("avg_review_score") > 5)

    ).count()

    print("\nPerformance Range Validation:")

    print(
        f"Invalid On-Time Rates: "
        f"{invalid_on_time_rates}"
    )

    print(
        f"Invalid Review Scores: "
        f"{invalid_review_scores}"
    )


# =========================================================
# GROWTH RATE VALIDATION
# =========================================================

def validate_growth_rate_logic(df):

    extreme_growth_rates = df.filter(

        col("volume_growth_rate") > 10

    ).count()

    print(
        f"\nExtreme Growth Rates (>1000%): "
        f"{extreme_growth_rates}"
    )


# =========================================================
# PERFORMANCE DISTRIBUTION
# =========================================================

def validate_performance_distribution(df):

    print("\nPerformance Category Distribution:")

    df.groupBy(
        "seller_performance_category"
    ).count().show(truncate=False)
    
# =========================================================
# SELLLER GROWTH CATEGORY DISTRIBUTION
# =========================================================

def validate_growth_category_distribution(df):

    print("\nGrowth Category Distribution:")  

    print("\nPerformance Category Distribution:")

    df.groupBy(
        "seller_growth_category"
    ).count().show(truncate=False)