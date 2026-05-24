"""
reviews_staging_validation.py

Validation framework for:
reviews_staging

Objective:
Protect customer review grain integrity,
delivery-context enrichment quality,
and customer satisfaction analytics trustworthiness.
"""

from pyspark.sql.functions import (
    col
)


# =========================================================
# MAIN VALIDATION RUNNER
# =========================================================

def run_reviews_staging_validation(df):

    print("\n=================================================")
    print("REVIEWS STAGING VALIDATION")
    print("=================================================")

    validate_row_count(df)

    validate_review_grain(df)

    validate_critical_nulls(df)

    validate_review_score_range(df)

    validate_sentiment_distribution(df)

    validate_delivery_context(df)

    validate_delivery_correlation(df)

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
# REVIEW GRAIN VALIDATION
# =========================================================

def validate_review_grain(df):

    duplicates = df.groupBy(
    "review_id",
    "order_id"
    ).count().filter(
        col("count") > 1
    ).count()

    print(
        f"\nDuplicate review_id Count: {duplicates}"
    )

    if duplicates > 0:

        raise Exception(
            "FAILED: Review grain violation detected."
        )


# =========================================================
# CRITICAL NULL VALIDATION
# =========================================================

def validate_critical_nulls(df):

    critical_columns = [

        "review_id",

        "order_id",

        "review_score",

        "sentiment_category",

        "delivery_experience_segment"
    ]

    print("\nCritical Null Validation:")

    for column_name in critical_columns:

        null_count = df.filter(
            col(column_name).isNull()
        ).count()

        print(f"{column_name}: {null_count} nulls")


# =========================================================
# REVIEW SCORE VALIDATION
# =========================================================

def validate_review_score_range(df):

    invalid_scores = df.filter(

        (col("review_score") < 1) |
        (col("review_score") > 5)

    ).count()

    print(
        f"\nInvalid Review Scores: "
        f"{invalid_scores}"
    )


# =========================================================
# SENTIMENT DISTRIBUTION
# =========================================================

def validate_sentiment_distribution(df):

    print("\nSentiment Distribution:")

    df.groupBy(
        "sentiment_category"
    ).count().show(truncate=False)


# =========================================================
# DELIVERY CONTEXT VALIDATION
# =========================================================

def validate_delivery_context(df):

    missing_delivery_context = df.filter(

        col("delivery_status_category").isNull()

    ).count()

    print(
        f"\nReviews Missing Delivery Context: "
        f"{missing_delivery_context}"
    )


# =========================================================
# DELIVERY CORRELATION VALIDATION
# =========================================================

def validate_delivery_correlation(df):

    delayed_negative_reviews = df.filter(

        col("delayed_delivery_review_flag") == True

    ).count()

    print(
        f"\nDelayed Delivery Negative Reviews: "
        f"{delayed_negative_reviews}"
    )