
"""
reviews_validation.py

Objective:
Validation framework for hardened silver_reviews dataset.

Sprint 3 Enhancements:
- quarantine validation
- orphan review governance
- review sentiment validation
- review context validation
- response timeline validation
- behavioral intelligence validation

Project:
Olist Seller Intelligence Platform

Layer:
Silver Validation Layer

Dataset:
silver_reviews
"""

# =========================================================
# PROJECT ROOT SETUP
# =========================================================

import sys
import os

project_root = os.path.abspath(
    os.path.join(
        os.path.dirname(__file__),
        "../../../"
    )
)

if project_root not in sys.path:
    sys.path.append(project_root)

# =========================================================
# IMPORTS
# =========================================================

from pyspark.sql.functions import (
    col
)

from pipelines.silver.validations.validation_utils import (
    validate_duplicates,
    validate_nulls
)

# =========================================================
# QUARANTINE VALIDATION
# =========================================================

def validate_quarantine_counts(
    quarantine_df
):

    print(
        "\n[VALIDATION] QUARANTINE SUMMARY"
    )

    quarantine_count = (
        quarantine_df.count()
    )

    print(
        f"Total Quarantined Reviews: "
        f"{quarantine_count}"
    )

    quarantine_df.groupBy(
        "quarantine_reason"
    ).count().show(
        truncate=False
    )

# =========================================================
# REVIEW LABEL VALIDATION
# =========================================================

def validate_review_labels(
    df
):

    print(
        "\n[VALIDATION] REVIEW LABELS"
    )

    invalid_labels = df.filter(

        ~col("review_label").isin(

            "Positive",
            "Neutral",
            "Negative"

        )

    ).count()

    print(
        f"Invalid Review Labels: "
        f"{invalid_labels}"
    )

    if invalid_labels > 0:

        raise ValueError(
            "FAILED: Invalid review labels detected."
        )

# =========================================================
# REVIEW CONTEXT VALIDATION
# =========================================================

def validate_review_context(
    df
):

    print(
        "\n[VALIDATION] REVIEW CONTEXT"
    )

    invalid_context = df.filter(

        ~col("review_context").isin(

            "Delivery Related",
            "Product Related",
            "General Experience"

        )

    ).count()

    print(
        f"Invalid Review Context: "
        f"{invalid_context}"
    )

    if invalid_context > 0:

        raise ValueError(
            "FAILED: Invalid review context detected."
        )

# =========================================================
# RESPONSE DAYS VALIDATION
# =========================================================

def validate_response_days(
    df
):

    print(
        "\n[VALIDATION] RESPONSE DAYS"
    )

    negative_response_days = df.filter(

        col("review_response_days") < 0

    ).count()

    print(
        f"Negative Response Days: "
        f"{negative_response_days}"
    )

# =========================================================
# REVIEW SCORE VALIDATION
# =========================================================

def validate_review_scores(
    df
):

    print(
        "\n[VALIDATION] REVIEW SCORES"
    )

    invalid_scores = df.filter(

        (
            col("review_score") < 1
        )

        |

        (
            col("review_score") > 5
        )

    ).count()

    print(
        f"Invalid Review Scores: "
        f"{invalid_scores}"
    )

    if invalid_scores > 0:

        raise ValueError(
            "FAILED: Invalid review scores."
        )

# =========================================================
# TIMESTAMP VALIDATION
# =========================================================

def validate_timestamps(
    df
):

    print(
        "\n[VALIDATION] TIMESTAMPS"
    )

    missing_creation = df.filter(

        col(
            "review_creation_date"
        ).isNull()

    ).count()

    print(
        f"Missing Creation Dates: "
        f"{missing_creation}"
    )

# =========================================================
# RESPONSE TIMELINE VALIDATION
# =========================================================

def validate_response_timeline(
    df
):

    print(
        "\n[VALIDATION] RESPONSE TIMELINE"
    )

    invalid_timeline = df.filter(

        col(
            "review_answer_timestamp"
        )

        <

        col(
            "review_creation_date"
        )

    ).count()

    print(
        f"Invalid Response Timeline: "
        f"{invalid_timeline}"
    )

# =========================================================
# EMPTY REVIEW ANALYSIS
# =========================================================

def validate_empty_reviews(
    df
):

    print(
        "\n[VALIDATION] EMPTY REVIEWS COMMENTS "
    )

    empty_reviews = df.filter(

        col(
            "review_comment_title"
        ).isNull()

        &

        col(
            "review_comment_message"
        ).isNull()

    ).count()

    print(
        f"Empty Reviews: "
        f"{empty_reviews}"
    )

def validate_empty_scores(
    df
):

    print(
        "\n[VALIDATION] EMPTY SCORE  "
    )

    empty_reviews = df.filter(

        col(
            "review_score"
        ).isNull()

        

    ).count()

    print(
        f"Empty Reviews: "
        f"{empty_reviews}"
    )

# =========================================================
# DISTRIBUTION ANALYSIS
# =========================================================

def validate_sentiment_distribution(
    df
):

    print(
        "\n[VALIDATION] SENTIMENT DISTRIBUTION"
    )

    df.groupBy(
        "review_label"
    ).count().show(
        truncate=False
    )

# =========================================================
# DELIVERY CONTEXT DISTRIBUTION
# =========================================================

def validate_context_distribution(
    df
):

    print(
        "\n[VALIDATION] CONTEXT DISTRIBUTION"
    )

    df.groupBy(
        "review_context"
    ).count().show(
        truncate=False
    )

# =========================================================
# MAIN VALIDATION RUNNER
# =========================================================

def run_reviews_validation(

    source_df,
    transformed_df,
    quarantine_df

):

    print(
        "\n================================================="
    )

    print(
        "RUNNING HARDENED REVIEWS VALIDATION"
    )

    print(
        "================================================="
    )

    source_count = (
        source_df.count()
    )

    transformed_count = (
        transformed_df.count()
    )

    quarantine_count = (
        quarantine_df.count()
    )

    print(
        f"Source Count: "
        f"{source_count}"
    )

    print(
        f"Clean Reviews: "
        f"{transformed_count}"
    )

    print(
        f"Quarantined Reviews: "
        f"{quarantine_count}"
    )

    if source_count != (
        transformed_count
        +
        quarantine_count
    ):

        print("""
WARNING:
Source count reconciliation mismatch.
Investigate duplicates and quarantines.
""")

    validate_duplicates(
        df=transformed_df,
        key_columns=["review_id"]
    )

    validate_nulls(
        df=transformed_df,
        critical_columns=[
            "review_id",
            "order_id",
            "review_score"
        ]
    )

    validate_review_scores(
        transformed_df
    )

    validate_review_labels(
        transformed_df
    )

    validate_review_context(
        transformed_df
    )

    validate_response_days(
        transformed_df
    )

    validate_timestamps(
        transformed_df
    )

    validate_response_timeline(
        transformed_df
    )

    validate_empty_reviews(
        transformed_df
    )
    
    validate_empty_scores(
        transformed_df
    )

    validate_sentiment_distribution(
        transformed_df
    )

    validate_context_distribution(
        transformed_df
    )

    validate_quarantine_counts(
        quarantine_df
    )

    print(
        "\n================================================="
    )

    print(
        "REVIEWS VALIDATION COMPLETED"
    )

    print(
        "================================================="
    )

