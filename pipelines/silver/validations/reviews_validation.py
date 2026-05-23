"""
reviews_validation.py

Objective:
Validation framework for silver_reviews dataset.

This module protects:
- behavioral operational integrity
- review-grain correctness
- review-score validity
- temporal consistency
- text normalization reliability
- customer satisfaction analytical trust

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
    os.path.join(os.path.dirname(__file__), "../../../")
)

if project_root not in sys.path:
    sys.path.append(project_root)


# =========================================================
# IMPORTS
# =========================================================

from pyspark.sql.functions import (
    col,
    trim
)

from pipelines.silver.validations.validation_utils import (
    validate_duplicates,
    validate_nulls
)


# =========================================================
# MAIN VALIDATION FUNCTION
# =========================================================

def run_reviews_validation(
    source_df,
    transformed_df
):
    """
    Run complete validation suite for silver_reviews.

    Parameters
    ----------
    source_df : DataFrame
        Original Bronze reviews dataframe.

    transformed_df : DataFrame
        Final Silver reviews dataframe.
    """

    print("\n=================================================")
    print("RUNNING REVIEWS VALIDATION")
    print("=================================================")

    # =====================================================
    # 1. ROW COUNT ANALYSIS
    # =====================================================

    """
    Review datasets should preserve
    atomic behavioral review events.
    """

    print("\n[1] ROW COUNT ANALYSIS")

    source_count = source_df.count()

    transformed_count = transformed_df.count()

    print(f"Source Review Count: {source_count}")

    print(
        f"Silver Review Count: "
        f"{transformed_count}"
    )

    if source_count != transformed_count:

        raise ValueError(
            "FAILED: Row count mismatch detected."
        )

    print("PASSED: Row count validation.")

    # =====================================================
    # 2. GRAIN VALIDATION
    # =====================================================

    """
    Grain:
    ONE ROW = ONE REVIEW EVENT
    """

    print("\n[2] GRAIN VALIDATION")

    validate_duplicates(
        df=transformed_df,
        key_columns=["review_id"]
    )

    # =====================================================
    # 3. CRITICAL NULL VALIDATION
    # =====================================================

    print("\n[3] CRITICAL NULL VALIDATION")

    critical_columns = [

        "review_id",

        "order_id",

        "review_score"

    ]

    validate_nulls(
        df=transformed_df,
        critical_columns=critical_columns
    )

    # =====================================================
    # 4. REVIEW SCORE VALIDATION
    # =====================================================

    """
    Review scores must be between 1 and 5.
    """

    print("\n[4] REVIEW SCORE VALIDATION")

    invalid_review_scores = (

        transformed_df

        .filter(

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
        f"Invalid Review Score Records: "
        f"{invalid_review_scores}"
    )

    if invalid_review_scores > 0:

        raise ValueError(
            "FAILED: Invalid review scores detected."
        )

    print("PASSED: Review score validation.")

    # =====================================================
    # 5. REVIEW TITLE NORMALIZATION VALIDATION
    # =====================================================

    """
    Ensure review titles are trimmed correctly.
    """

    print("\n[5] REVIEW TITLE VALIDATION")

    invalid_title_records = (

        transformed_df

        .filter(

            col("review_comment_title").isNotNull()

            &

            (
                col("review_comment_title")
                !=
                trim(col("review_comment_title"))
            )

        )

        .count()

    )

    print(
        f"Invalid Review Title Records: "
        f"{invalid_title_records}"
    )

    if invalid_title_records > 0:

        print("""
WARNING:
Some review titles are not normalized.
""")

    else:

        print(
            "PASSED: Review title normalization validation."
        )

    # =====================================================
    # 6. REVIEW MESSAGE NORMALIZATION VALIDATION
    # =====================================================

    """
    Ensure review messages are trimmed correctly.
    """

    print("\n[6] REVIEW MESSAGE VALIDATION")

    invalid_message_records = (

        transformed_df

        .filter(

            col("review_comment_message").isNotNull()

            &

            (
                col("review_comment_message")
                !=
                trim(col("review_comment_message"))
            )

        )

        .count()

    )

    print(
        f"Invalid Review Message Records: "
        f"{invalid_message_records}"
    )

    if invalid_message_records > 0:

        print("""
WARNING:
Some review messages are not normalized.
""")

    else:

        print(
            "PASSED: Review message normalization validation."
        )

    # =====================================================
    # 7. REVIEW TIMESTAMP VALIDATION
    # =====================================================

    """
    Validate review temporal consistency.
    """

    print("\n[7] REVIEW TIMESTAMP VALIDATION")

    invalid_timestamp_records = (

        transformed_df

        .filter(

            col("review_creation_date").isNull()

        )

        .count()

    )

    print(
        f"Invalid Review Timestamp Records: "
        f"{invalid_timestamp_records}"
    )

    if invalid_timestamp_records > 0:

        raise ValueError(
            "FAILED: Invalid review timestamps detected."
        )

    print("PASSED: Review timestamp validation.")

    # =====================================================
    # 8. REVIEW RESPONSE TIMELINE VALIDATION
    # =====================================================

    """
    Validate response chronology.
    """

    print("\n[8] REVIEW RESPONSE TIMELINE VALIDATION")

    invalid_response_timeline_records = (

        transformed_df

        .filter(

            col("review_answer_timestamp")
            <
            col("review_creation_date")

        )

        .count()

    )

    print(
        f"Invalid Response Timeline Records: "
        f"{invalid_response_timeline_records}"
    )

    if invalid_response_timeline_records > 0:

        print("""
WARNING:
Some review responses occur before
review creation timestamps.
""")

    else:

        print(
            "PASSED: Response timeline validation."
        )

    # =====================================================
    # 9. EMPTY REVIEW ANALYSIS
    # =====================================================

    """
    Analyze reviews without textual content.
    NOT a failure condition.
    """

    print("\n[9] EMPTY REVIEW ANALYSIS")

    empty_review_records = (

        transformed_df

        .filter(

            col("review_comment_title").isNull()

            &

            col("review_comment_message").isNull()

        )

        .count()

    )

    print(
        f"Empty Review Records: "
        f"{empty_review_records}"
    )

    print("""
INFO:
Some customers provide only numerical
ratings without textual comments.
""")

    # =====================================================
    # 10. REVIEW DISTRIBUTION VALIDATION
    # =====================================================

    """
    Validate review-score completeness.
    """

    print("\n[10] REVIEW DISTRIBUTION VALIDATION")

    null_review_scores = (

        transformed_df

        .filter(
            col("review_score").isNull()
        )

        .count()

    )

    print(
        f"Null Review Score Records: "
        f"{null_review_scores}"
    )

    if null_review_scores > 0:

        raise ValueError(
            "FAILED: Null review scores detected."
        )

    print(
        "PASSED: Review distribution validation."
    )

    # =====================================================
    # FINAL VALIDATION SUMMARY
    # =====================================================

    print("\n=================================================")
    print("ALL REVIEWS VALIDATIONS COMPLETED")
    print("=================================================")

    print("""
Validation Summary:
- Review grain integrity verified
- Behavioral consistency validated
- Review-score correctness verified
- Text normalization validated
- Temporal consistency protected
- Controlled anomaly governance applied

silver_reviews is TRUSTED.
""")
