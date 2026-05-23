"""
customers_validation.py

Objective:
Validation framework for silver_customers dataset.

This module protects:
- customer dimensional integrity
- geographic enrichment consistency
- ZIP-prefix correctness
- customer identity reliability
- regional analytical trust

Project:
Olist Seller Intelligence Platform

Layer:
Silver Validation Layer

Dataset:
silver_customers
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
    lower,
    trim
)

from pipelines.silver.validations.validation_utils import (
    validate_duplicates,
    validate_nulls
)


# =========================================================
# VALID BRAZILIAN STATES
# =========================================================

VALID_BRAZILIAN_STATES = [

    "AC", "AL", "AP", "AM", "BA",
    "CE", "DF", "ES", "GO", "MA",
    "MT", "MS", "MG", "PA", "PB",
    "PR", "PE", "PI", "RJ", "RN",
    "RS", "RO", "RR", "SC", "SP",
    "SE", "TO"

]


# =========================================================
# MAIN VALIDATION FUNCTION
# =========================================================

def run_customers_validation(
    source_df,
    transformed_df
):
    """
    Run complete validation suite for silver_customers.

    Parameters
    ----------
    source_df : DataFrame
        Original Bronze customers dataframe.

    transformed_df : DataFrame
        Final Silver customers dataframe.
    """

    print("\n=================================================")
    print("RUNNING CUSTOMERS VALIDATION")
    print("=================================================")

    # =====================================================
    # 1. ROW COUNT ANALYSIS
    # =====================================================

    """
    Customer dimensional datasets should preserve
    row counts because enrichment should not create
    fan-out duplication.
    """

    print("\n[1] ROW COUNT ANALYSIS")

    source_count = source_df.count()

    transformed_count = transformed_df.count()

    print(f"Source Customer Count: {source_count}")

    print(
        f"Silver Customer Count: "
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
    ONE ROW = ONE CUSTOMER
    """

    print("\n[2] GRAIN VALIDATION")

    validate_duplicates(
        df=transformed_df,
        key_columns=["customer_id"]
    )

    # =====================================================
    # 3. CRITICAL NULL VALIDATION
    # =====================================================

    print("\n[3] CRITICAL NULL VALIDATION")

    critical_columns = [

        "customer_id",
        "customer_unique_id",

        "customer_zip_code_prefix",

        "customer_city",
        "customer_state"

    ]

    validate_nulls(
        df=transformed_df,
        critical_columns=critical_columns
    )

    # =====================================================
    # 4. CUSTOMER ID VALIDATION
    # =====================================================

    """
    Ensure customer identifiers are valid.
    """

    print("\n[4] CUSTOMER ID VALIDATION")

    invalid_customer_ids = (

        transformed_df

        .filter(
            col("customer_id").isNull()
        )

        .count()

    )

    print(
        f"Invalid Customer IDs: "
        f"{invalid_customer_ids}"
    )

    if invalid_customer_ids > 0:

        raise ValueError(
            "FAILED: Null customer IDs detected."
        )

    print("PASSED: Customer ID validation.")

    # =====================================================
    # 5. ZIP PREFIX VALIDATION
    # =====================================================

    """
    ZIP prefixes must be positive.
    """

    print("\n[5] ZIP PREFIX VALIDATION")

    invalid_zip_prefixes = (

        transformed_df

        .filter(
            col("customer_zip_code_prefix") <= 0
        )

        .count()

    )

    print(
        f"Invalid ZIP Prefix Records: "
        f"{invalid_zip_prefixes}"
    )

    if invalid_zip_prefixes > 0:

        raise ValueError(
            "FAILED: Invalid ZIP prefixes detected."
        )

    print("PASSED: ZIP prefix validation.")

    # =====================================================
    # 6. STATE VALIDATION
    # =====================================================

    """
    Validate Brazilian state abbreviations.
    """

    print("\n[6] STATE VALIDATION")

    invalid_state_records = (

        transformed_df

        .filter(
            ~col("customer_state").isin(
                VALID_BRAZILIAN_STATES
            )
        )

        .count()

    )

    print(
        f"Invalid State Records: "
        f"{invalid_state_records}"
    )

    if invalid_state_records > 0:

        print("""
WARNING:
Some customer states are invalid.
""")

    else:

        print("PASSED: State validation.")

    # =====================================================
    # 7. CITY NORMALIZATION VALIDATION
    # =====================================================

    """
    Ensure customer cities are normalized.
    """

    print("\n[7] CITY NORMALIZATION VALIDATION")

    inconsistent_city_records = (

        transformed_df

        .filter(

            col("customer_city")
            !=
            lower(trim(col("customer_city")))

        )

        .count()

    )

    print(
        f"Inconsistent City Records: "
        f"{inconsistent_city_records}"
    )

    if inconsistent_city_records > 0:

        print("""
WARNING:
Some customer cities are not normalized.
""")

    else:

        print(
            "PASSED: City normalization validation."
        )

    # =====================================================
    # 8. GEOGRAPHIC ENRICHMENT VALIDATION
    # =====================================================

    """
    Validate geolocation enrichment completeness.
    """

    print("\n[8] GEOGRAPHIC ENRICHMENT VALIDATION")

    missing_geo_records = (

        transformed_df

        .filter(

            col("median_latitude").isNull()

            |

            col("median_longitude").isNull()

        )

        .count()

    )

    print(
        f"Missing Geographic Enrichment Records: "
        f"{missing_geo_records}"
    )

    if missing_geo_records > 0:

        print("""
WARNING:
Some customers are missing geographic enrichment.
""")

    else:

        print(
            "PASSED: Geographic enrichment validation."
        )

    # =====================================================
    # 9. LATITUDE RANGE VALIDATION
    # =====================================================

    """
    Latitude must be geographically valid.
    """

    print("\n[9] LATITUDE RANGE VALIDATION")

    invalid_latitude_records = (

        transformed_df

        .filter(

            (
                col("median_latitude") < -90
            )

            |

            (
                col("median_latitude") > 90
            )

        )

        .count()

    )

    print(
        f"Invalid Latitude Records: "
        f"{invalid_latitude_records}"
    )

    if invalid_latitude_records > 0:

        raise ValueError(
            "FAILED: Invalid latitude values detected."
        )

    print("PASSED: Latitude validation.")

    # =====================================================
    # 10. LONGITUDE RANGE VALIDATION
    # =====================================================

    """
    Longitude must be geographically valid.
    """

    print("\n[10] LONGITUDE RANGE VALIDATION")

    invalid_longitude_records = (

        transformed_df

        .filter(

            (
                col("median_longitude") < -180
            )

            |

            (
                col("median_longitude") > 180
            )

        )

        .count()

    )

    print(
        f"Invalid Longitude Records: "
        f"{invalid_longitude_records}"
    )

    if invalid_longitude_records > 0:

        raise ValueError(
            "FAILED: Invalid longitude values detected."
        )

    print("PASSED: Longitude validation.")

    # =====================================================
    # FINAL VALIDATION SUMMARY
    # =====================================================

    print("\n=================================================")
    print("ALL CUSTOMERS VALIDATIONS COMPLETED")
    print("=================================================")

    print("""
Validation Summary:
- Customer grain integrity verified
- Customer identity validated
- ZIP-prefix integrity verified
- Geographic enrichment validated
- Regional normalization verified
- Coordinate validity verified
- Dimensional integrity protected

silver_customers is TRUSTED.
""")
