"""
customer_reviews_fact_validation.py

Objective:
Validate Gold Customer Reviews Fact Table

Fact:
fct_customer_reviews

Grain:
ONE ROW = ONE CUSTOMER REVIEW
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

def run_customer_reviews_fact_validation(df):

    print("=" * 60)
    print("FCT CUSTOMER REVIEWS VALIDATION")
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

    duplicate_reviews = (

        df.groupBy(
            "review_id"
        )

        .count()

        .filter(
            col("count") > 1
        )

        .count()
    )

    print(
        f"\nDuplicate Review Grain Violations: "
        f"{duplicate_reviews}"
    )

    # =================================================
    # FACT SK VALIDATION
    # =================================================

    duplicate_fact_sk = (

        df.groupBy(
            "review_fact_sk"
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

        "review_date_sk"

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
    # RESPONSE DATE VALIDATION
    # =================================================

    response_date_nulls = (

        df.filter(

            col(
                "response_date_sk"
            ).isNull()

            &

            col(
                "review_response_days"
            ).isNotNull()

        )

        .count()
    )

    print(
        f"response_date_sk Missing: "
        f"{response_date_nulls}"
    )

    # =================================================
    # REVIEW SCORE VALIDATION
    # =================================================

    invalid_review_scores = (

        df.filter(

            (
                col("review_score") < 1
            )

            |

            (
                col("review_score") > 5
            )

        )

        .count()
    )

    print(
        f"\nInvalid Review Scores: "
        f"{invalid_review_scores}"
    )

    # =================================================
    # CRITICAL NULL VALIDATION
    # =================================================

    print(
        "\nCritical Null Validation:"
    )

    critical_columns = [

        "review_id",

        "order_id",

        "review_score",

        "sentiment_category"

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
    # RESPONSE TIME VALIDATION
    # =================================================

    negative_response_days = (

        df.filter(
            col(
                "review_response_days"
            ) < 0
        )

        .count()
    )

    print(
        f"\nNegative Response Days: "
        f"{negative_response_days}"
    )

    # =================================================
    # DELIVERY KPI VALIDATION
    # =================================================

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
    # FLAG CONSISTENCY VALIDATION
    # =================================================

    inconsistent_negative_flags = (

        df.filter(

            (
                col("review_score") <= 2
            )

            &

            (
                col(
                    "negative_review_flag"
                ) == False
            )

        )

        .count()
    )

    print(
        f"Inconsistent Negative Review Flags: "
        f"{inconsistent_negative_flags}"
    )

    inconsistent_positive_flags = (

        df.filter(

            (
                col("review_score") >= 4
            )

            &

            (
                col(
                    "positive_review_flag"
                ) == False
            )

        )

        .count()
    )

    print(
        f"Inconsistent Positive Review Flags: "
        f"{inconsistent_positive_flags}"
    )

    # =================================================
    # LOW RATING FLAG VALIDATION
    # =================================================

    inconsistent_low_rating = (

        df.filter(

            (
                col("review_score") <= 2
            )

            &

            (
                col(
                    "low_rating_flag"
                ) == False
            )

        )

        .count()
    )

    print(
        f"Inconsistent Low Rating Flags: "
        f"{inconsistent_low_rating}"
    )

    # =================================================
    # EXCELLENT FLAG VALIDATION
    # =================================================

    inconsistent_excellent_rating = (

        df.filter(

            (
                col("review_score") == 5
            )

            &

            (
                col(
                    "excellent_rating_flag"
                ) == False
            )

        )

        .count()
    )

    print(
        f"Inconsistent Excellent Rating Flags: "
        f"{inconsistent_excellent_rating}"
    )

    # =================================================
    # SENTIMENT DISTRIBUTION
    # =================================================

    print(
        "\nSentiment Distribution:"
    )

    df.groupBy(
        "sentiment_category"
    ).count().show(
        truncate=False
    )

    # =================================================
    # DELIVERY EXPERIENCE DISTRIBUTION
    # =================================================

    print(
        "\nDelivery Experience Distribution:"
    )

    df.groupBy(
        "delivery_experience_segment"
    ).count().show(
        truncate=False
    )

    # =================================================
    # DELIVERY COMPLAINT ANALYSIS
    # =================================================

    delayed_negative_reviews = (

        df.filter(
            col(
                "delayed_delivery_review_flag"
            ) == True
        )

        .count()
    )

    print(
        f"\nDelayed Delivery Negative Reviews: "
        f"{delayed_negative_reviews:,}"
    )

    # =================================================
    # DISTANCE ANALYSIS
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

    positive_reviews = (

        df.filter(
            col(
                "positive_review_flag"
            ) == True
        )

        .count()
    )

    negative_reviews = (

        df.filter(
            col(
                "negative_review_flag"
            ) == True
        )

        .count()
    )

    low_ratings = (

        df.filter(
            col(
                "low_rating_flag"
            ) == True
        )

        .count()
    )

    excellent_ratings = (

        df.filter(
            col(
                "excellent_rating_flag"
            ) == True
        )

        .count()
    )

    print(
        "\nKPI Summary:"
    )

    print(
        f"Positive Reviews: "
        f"{positive_reviews:,}"
    )

    print(
        f"Negative Reviews: "
        f"{negative_reviews:,}"
    )

    print(
        f"Low Ratings: "
        f"{low_ratings:,}"
    )

    print(
        f"Excellent Ratings: "
        f"{excellent_ratings:,}"
    )

    print("\nValidation Complete.")

    print("=" * 60)

