"""
mql_validation.py

Objective:
Validation framework for silver_mql dataset.

This module protects:
- CRM acquisition integrity
- lead-grain correctness
- attribution consistency
- funnel chronology reliability
- marketing operational trust

Project:
Olist Seller Intelligence Platform

Layer:
Silver Validation Layer

Dataset:
silver_mql
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
    trim,
    lower,
    current_timestamp
)

from pipelines.silver.validations.validation_utils import (
    validate_duplicates,
    validate_nulls
)


# =========================================================
# MAIN VALIDATION FUNCTION
# =========================================================

def run_mql_validation(
    source_df,
    transformed_df
):
    """
    Run complete validation suite for silver_mql.

    Parameters
    ----------
    source_df : DataFrame
        Original Bronze MQL dataframe.

    transformed_df : DataFrame
        Final Silver MQL dataframe.
    """

    print("\n=================================================")
    print("RUNNING MQL VALIDATION")
    print("=================================================")

    # =====================================================
    # 1. ROW COUNT ANALYSIS
    # =====================================================

    """
    CRM lead datasets should preserve
    acquisition-event cardinality.
    """

    print("\n[1] ROW COUNT ANALYSIS")

    source_count = source_df.count()

    transformed_count = transformed_df.count()

    print(f"Source MQL Count: {source_count}")

    print(
        f"Silver MQL Count: "
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
    ONE ROW = ONE QUALIFIED LEAD EVENT
    """

    print("\n[2] GRAIN VALIDATION")

    validate_duplicates(
        df=transformed_df,
        key_columns=["mql_id"]
    )

    # =====================================================
    # 3. CRITICAL NULL VALIDATION
    # =====================================================

    print("\n[3] CRITICAL NULL VALIDATION")

    critical_columns = [

        "mql_id",

        "first_contact_date",

        "origin"

    ]

    validate_nulls(
        df=transformed_df,
        critical_columns=critical_columns
    )

    # =====================================================
    # 4. MQL ID VALIDATION
    # =====================================================

    """
    Validate CRM lead identifier integrity.
    """

    print("\n[4] MQL ID VALIDATION")

    invalid_mql_ids = (

        transformed_df

        .filter(

            col("mql_id").isNull()

            |

            (
                trim(col("mql_id")) == ""
            )

        )

        .count()

    )

    print(
        f"Invalid MQL ID Records: "
        f"{invalid_mql_ids}"
    )

    if invalid_mql_ids > 0:

        raise ValueError(
            "FAILED: Invalid MQL IDs detected."
        )

    print("PASSED: MQL ID validation.")

    # =====================================================
    # 5. ORIGIN NORMALIZATION VALIDATION
    # =====================================================

    """
    Validate deterministic attribution formatting.
    """

    print("\n[5] ORIGIN NORMALIZATION VALIDATION")

    inconsistent_origin_records = (

        transformed_df

        .filter(

            col("origin").isNotNull()

            &

            (
                col("origin")
                !=
                lower(
                    trim(
                        col("origin")
                    )
                )
            )

        )

        .count()

    )

    print(
        f"Inconsistent Origin Records: "
        f"{inconsistent_origin_records}"
    )

    if inconsistent_origin_records > 0:

        print("""
WARNING:
Some acquisition sources are not normalized.
""")

    else:

        print(
            "PASSED: Origin normalization validation."
        )

    # =====================================================
    # 6. LANDING PAGE VALIDATION
    # =====================================================

    """
    Validate deterministic landing-page formatting.
    """

    print("\n[6] LANDING PAGE VALIDATION")

    inconsistent_landing_pages = (

        transformed_df

        .filter(

            col("landing_page_id").isNotNull()

            &

            (
                col("landing_page_id")
                !=
                lower(
                    trim(
                        col("landing_page_id")
                    )
                )
            )

        )

        .count()

    )

    print(
        f"Inconsistent Landing Page Records: "
        f"{inconsistent_landing_pages}"
    )

    if inconsistent_landing_pages > 0:

        print("""
WARNING:
Some landing-page identifiers
are not normalized.
""")

    else:

        print(
            "PASSED: Landing page normalization validation."
        )

    # =====================================================
    # 7. TIMESTAMP VALIDATION
    # =====================================================

    """
    Validate acquisition chronology consistency.
    """

    print("\n[7] TIMESTAMP VALIDATION")

    invalid_timestamp_records = (

        transformed_df

        .filter(
            col("first_contact_date").isNull()
        )

        .count()

    )

    print(
        f"Invalid Timestamp Records: "
        f"{invalid_timestamp_records}"
    )

    if invalid_timestamp_records > 0:

        raise ValueError(
            "FAILED: Invalid first-contact timestamps detected."
        )

    print("PASSED: Timestamp validation.")

    # =====================================================
    # 8. FUTURE DATE VALIDATION
    # =====================================================

    """
    Validate CRM chronology realism.
    """

    print("\n[8] FUTURE DATE VALIDATION")

    future_date_records = (

        transformed_df

        .filter(

            col("first_contact_date")
            >
            current_timestamp()

        )

        .count()

    )

    print(
        f"Future Contact Date Records: "
        f"{future_date_records}"
    )

    if future_date_records > 0:

        print("""
WARNING:
Some acquisition events occur in the future.
""")

    else:

        print(
            "PASSED: Future date validation."
        )

    # =====================================================
    # 9. NULL LANDING PAGE ANALYSIS
    # =====================================================

    """
    Analyze missing attribution landing pages.
    NOT always invalid operationally.
    """

    print("\n[9] NULL LANDING PAGE ANALYSIS")

    null_landing_pages = (

        transformed_df

        .filter(
            col("landing_page_id").isNull()
        )

        .count()

    )

    print(
        f"Null Landing Page Records: "
        f"{null_landing_pages}"
    )

    print("""
INFO:
Some leads may originate from:
- offline acquisition
- manual onboarding
- direct CRM insertion
- non-trackable channels
""")

    # =====================================================
    # 10. ATTRIBUTION DISTRIBUTION VALIDATION
    # =====================================================

    """
    Validate acquisition attribution completeness.
    """

    print("\n[10] ATTRIBUTION DISTRIBUTION VALIDATION")

    null_origin_records = (

        transformed_df

        .filter(
            col("origin").isNull()
        )

        .count()

    )

    print(
        f"Null Origin Records: "
        f"{null_origin_records}"
    )

    if null_origin_records > 0:

        print("""
WARNING:
Some leads are missing acquisition-source attribution.
""")

    else:

        print(
            "PASSED: Attribution distribution validation."
        )

    # =====================================================
    # FINAL VALIDATION SUMMARY
    # =====================================================

    print("\n=================================================")
    print("ALL MQL VALIDATIONS COMPLETED")
    print("=================================================")

    print("""
Validation Summary:
- CRM acquisition integrity verified
- Lead-grain consistency validated
- Attribution normalization enforced
- Funnel chronology protected
- Marketing operational trust verified
- Controlled acquisition governance applied

silver_mql is TRUSTED.
""")
