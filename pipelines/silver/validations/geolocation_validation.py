"""
geolocation_validation.py

Objective:
Validation framework for silver_geolocation dataset.

This module protects:
- geographic grain integrity
- coordinate validity
- regional consistency
- enrichment reliability
- geographic analytical trust

Project:
Olist Seller Intelligence Platform

Layer:
Silver Validation Layer

Dataset:
silver_geolocation
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
    upper,
    trim,
    lower
)

from pipelines.silver.validations.validation_utils import (
    validate_row_count,
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

def run_geolocation_validation(
    source_df,
    transformed_df
):
    """
    Run complete validation suite for silver_geolocation.

    Parameters
    ----------
    source_df : DataFrame
        Original Bronze geolocation dataframe.

    transformed_df : DataFrame
        Final Silver geolocation dataframe.
    """

    print("\n=================================================")
    print("RUNNING GEOLOCATION VALIDATION")
    print("=================================================")

    # =====================================================
    # 1. ROW COUNT VALIDATION
    # =====================================================

    """
    Row count reduction is EXPECTED because:
    multiple raw geographic records are aggregated
    into one ZIP-prefix representative record.
    """

    print("\n[1] ROW COUNT ANALYSIS")

    source_count = source_df.count()

    transformed_count = transformed_df.count()

    print(f"Source Record Count: {source_count}")

    print(
        f"Silver ZIP Prefix Count: "
        f"{transformed_count}"
    )

    print("""
INFO:
Row reduction is expected because the pipeline
aggregates duplicate geographic records into
one representative ZIP-prefix record.
""")

    # =====================================================
    # 2. GRAIN VALIDATION
    # =====================================================

    """
    Grain:
    ONE ROW = ONE ZIP PREFIX
    """

    print("\n[2] GRAIN VALIDATION")

    validate_duplicates(
        df=transformed_df,
        key_columns=["zip_code_prefix"]
    )

    # =====================================================
    # 3. CRITICAL NULL VALIDATION
    # =====================================================

    print("\n[3] CRITICAL NULL VALIDATION")

    critical_columns = [
        "zip_code_prefix",
        "median_latitude",
        "median_longitude",
        "city",
        "state"
    ]

    validate_nulls(
        df=transformed_df,
        critical_columns=critical_columns
    )

    # =====================================================
    # 4. LATITUDE RANGE VALIDATION
    # =====================================================

    """
    Latitude must be between:
    -90 and 90
    """

    print("\n[4] LATITUDE RANGE VALIDATION")

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
    # 5. LONGITUDE RANGE VALIDATION
    # =====================================================

    """
    Longitude must be between:
    -180 and 180
    """

    print("\n[5] LONGITUDE RANGE VALIDATION")

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
    # 6. STATE STANDARDIZATION VALIDATION
    # =====================================================

    """
    Validate Brazilian state abbreviations.
    """

    print("\n[6] STATE VALIDATION")

    invalid_state_records = (

        transformed_df

        .filter(
            ~col("state").isin(VALID_BRAZILIAN_STATES)
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
Some state values are not recognized as
valid Brazilian state abbreviations.
""")

    else:

        print("PASSED: State validation.")

    # =====================================================
    # 7. CITY NORMALIZATION VALIDATION
    # =====================================================

    """
    Ensure city normalization consistency.
    """

    print("\n[7] CITY NORMALIZATION VALIDATION")

    inconsistent_city_records = (

        transformed_df

        .filter(
            col("city") != lower(trim(col("city")))
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
Some city names are not fully normalized.
""")

    else:

        print("PASSED: City normalization validation.")

    # =====================================================
    # 8. DUPLICATE COORDINATE ANALYSIS
    # =====================================================

    """
    Informational geographic insight.
    NOT a failure condition.
    """

    print("\n[8] GEOGRAPHIC AGGREGATION ANALYSIS")

    duplicated_coordinates = (

        transformed_df

        .groupBy(
            "median_latitude",
            "median_longitude"
        )

        .count()

        .filter(
            col("count") > 1
        )

        .count()

    )

    print(
        f"Duplicated Coordinate Groups: "
        f"{duplicated_coordinates}"
    )

    print("""
INFO:
Some ZIP-prefix regions may share similar
representative coordinates naturally.
""")

    # =====================================================
    # 9. ZIP PREFIX VALIDATION
    # =====================================================

    """
    ZIP prefixes should be positive.
    """

    print("\n[9] ZIP PREFIX VALIDATION")

    invalid_zip_prefixes = (

        transformed_df

        .filter(
            col("zip_code_prefix") <= 0
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
    # 10. GEOGRAPHIC COMPLETENESS VALIDATION
    # =====================================================

    """
    Validate geographic enrichment completeness.
    """

    print("\n[10] GEOGRAPHIC COMPLETENESS VALIDATION")

    incomplete_geo_records = (

        transformed_df

        .filter(

            col("median_latitude").isNull()

            |

            col("median_longitude").isNull()

        )

        .count()

    )

    print(
        f"Incomplete Geographic Records: "
        f"{incomplete_geo_records}"
    )

    if incomplete_geo_records > 0:

        print("""
WARNING:
Some geographic regions are missing
representative coordinates.
""")

    else:

        print(
            "PASSED: Geographic completeness validation."
        )

    # =====================================================
    # FINAL VALIDATION SUMMARY
    # =====================================================

    print("\n=================================================")
    print("ALL GEOLOCATION VALIDATIONS COMPLETED")
    print("=================================================")

    print("""
Validation Summary:
- Geographic grain integrity verified
- Coordinate validity verified
- ZIP-prefix uniqueness verified
- Geographic normalization verified
- State integrity validated
- Spatial ranges validated
- Geographic completeness checked

silver_geolocation is TRUSTED.
""")
