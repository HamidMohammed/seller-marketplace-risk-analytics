"""
validation_utils.py

Objective:
Reusable Silver-layer validation framework for the
Olist Seller Intelligence Platform.

This module provides generic validation functions used across:
- silver_orders
- silver_order_items
- silver_payments
- silver_reviews
- future Silver datasets

The framework follows:
- validation-driven engineering
- grain-preserving architecture
- enterprise ETL best practices
- KPI trust protection

Author: Hamid
Project: Olist Seller Intelligence Platform
Layer: Silver
"""

from pyspark.sql import DataFrame
from pyspark.sql.functions import col, count, when
from datetime import datetime
from typing import List, Dict, Any


# =========================================================
# HELPER FUNCTION
# =========================================================

def build_validation_result(
    validation_name: str,
    status: str,
    message: str,
    details: Dict[str, Any] = None
) -> Dict[str, Any]:
    """
    Standardized validation result structure.

    Parameters
    ----------
    validation_name : str
        Name of the validation.

    status : str
        PASSED / FAILED / WARNING

    message : str
        Human-readable explanation.

    details : dict
        Additional metrics or metadata.

    Returns
    -------
    dict
        Structured validation result.
    """

    return {
        "validation_name": validation_name,
        "status": status,
        "message": message,
        "details": details or {},
        "validated_at": datetime.utcnow().isoformat()
    }


# =========================================================
# 1. ROW COUNT VALIDATION
# =========================================================

def validate_row_count(
    source_df: DataFrame,
    transformed_df: DataFrame,
    allowed_difference: int = 0
) -> Dict[str, Any]:
    """
    Validates row-count consistency between source and transformed datasets.

    Purpose:
    - Detect accidental filtering
    - Detect failed joins
    - Detect unexpected row explosion

    Parameters
    ----------
    source_df : DataFrame
        Original dataset.

    transformed_df : DataFrame
        Transformed dataset.

    allowed_difference : int
        Acceptable row difference threshold.

    Returns
    -------
    dict
        Validation result dictionary.
    """

    source_count = source_df.count()
    transformed_count = transformed_df.count()

    difference = transformed_count - source_count

    if abs(difference) <= allowed_difference:
        status = "PASSED"
        message = "Row count validation passed."
    else:
        status = "FAILED"
        message = "Unexpected row-count difference detected."

    return build_validation_result(
        validation_name="row_count_validation",
        status=status,
        message=message,
        details={
            "source_count": source_count,
            "transformed_count": transformed_count,
            "difference": difference,
            "allowed_difference": allowed_difference
        }
    )


# =========================================================
# 2. DUPLICATE VALIDATION
# =========================================================

def validate_duplicates(
    df: DataFrame,
    key_columns: List[str]
) -> Dict[str, Any]:
    """
    Detect duplicate records based on dataset grain.

    Purpose:
    - Protect grain integrity
    - Prevent KPI corruption
    - Detect fan-out duplication

    Parameters
    ----------
    df : DataFrame
        Dataset to validate.

    key_columns : List[str]
        Columns defining dataset grain.

    Returns
    -------
    dict
        Validation result dictionary.
    """

    duplicate_count = (
        df.groupBy(key_columns)
          .count()
          .filter(col("count") > 1)
          .count()
    )

    if duplicate_count == 0:
        status = "PASSED"
        message = "No duplicate records detected."
    else:
        status = "FAILED"
        message = "Duplicate records detected."

    return build_validation_result(
        validation_name="duplicate_validation",
        status=status,
        message=message,
        details={
            "key_columns": key_columns,
            "duplicate_group_count": duplicate_count
        }
    )


# =========================================================
# 3. NULL VALIDATION
# =========================================================

def validate_nulls(
    df: DataFrame,
    critical_columns: List[str]
) -> Dict[str, Any]:
    """
    Validate null distribution across critical business columns.

    Purpose:
    - Detect missing business keys
    - Protect KPI calculations
    - Identify operational anomalies

    Parameters
    ----------
    df : DataFrame
        Dataset to validate.

    critical_columns : List[str]
        Columns requiring null analysis.

    Returns
    -------
    dict
        Validation result dictionary.
    """

    null_summary = {}

    total_rows = df.count()

    for column_name in critical_columns:
        null_count = df.filter(col(column_name).isNull()).count()

        null_percentage = (
            (null_count / total_rows) * 100
            if total_rows > 0 else 0
        )

        null_summary[column_name] = {
            "null_count": null_count,
            "null_percentage": round(null_percentage, 2)
        }

    failed_columns = [
        column_name
        for column_name, metrics in null_summary.items()
        if metrics["null_count"] > 0
    ]

    if len(failed_columns) == 0:
        status = "PASSED"
        message = "No nulls detected in critical columns."
    else:
        status = "WARNING"
        message = (
            "Null values detected in critical columns. "
            "Business review recommended."
        )

    return build_validation_result(
        validation_name="null_validation",
        status=status,
        message=message,
        details={
            "critical_columns": critical_columns,
            "null_summary": null_summary
        }
    )


# =========================================================
# 4. COLUMN EXISTENCE VALIDATION
# =========================================================

def validate_column_existence(
    df: DataFrame,
    expected_columns: List[str]
) -> Dict[str, Any]:
    """
    Validate required schema columns exist.

    Purpose:
    - Detect schema drift
    - Prevent downstream failures
    - Protect transformation dependencies

    Parameters
    ----------
    df : DataFrame
        Dataset to validate.

    expected_columns : List[str]
        Required columns.

    Returns
    -------
    dict
        Validation result dictionary.
    """

    actual_columns = df.columns

    missing_columns = [
        column_name
        for column_name in expected_columns
        if column_name not in actual_columns
    ]

    if len(missing_columns) == 0:
        status = "PASSED"
        message = "All required columns exist."
    else:
        status = "FAILED"
        message = "Missing required columns detected."

    return build_validation_result(
        validation_name="column_existence_validation",
        status=status,
        message=message,
        details={
            "expected_columns": expected_columns,
            "missing_columns": missing_columns
        }
    )


# =========================================================
# 5. VALUE RANGE VALIDATION
# =========================================================

def validate_numeric_range(
    df: DataFrame,
    column_name: str,
    min_value: float = None,
    max_value: float = None
) -> Dict[str, Any]:
    """
    Validate numeric values fall within expected range.

    Purpose:
    - Detect impossible metrics
    - Protect KPI calculations
    - Prevent corrupted analytics

    Example:
    - payment_value >= 0
    - review_score between 1 and 5

    Parameters
    ----------
    df : DataFrame
        Dataset to validate.

    column_name : str
        Numeric column.

    min_value : float
        Minimum allowed value.

    max_value : float
        Maximum allowed value.

    Returns
    -------
    dict
        Validation result dictionary.
    """

    invalid_df = df

    if min_value is not None:
        invalid_df = invalid_df.filter(col(column_name) < min_value)

    if max_value is not None:
        invalid_df = invalid_df.filter(col(column_name) > max_value)

    invalid_count = invalid_df.count()

    if invalid_count == 0:
        status = "PASSED"
        message = "Numeric range validation passed."
    else:
        status = "FAILED"
        message = "Out-of-range values detected."

    return build_validation_result(
        validation_name="numeric_range_validation",
        status=status,
        message=message,
        details={
            "column_name": column_name,
            "min_value": min_value,
            "max_value": max_value,
            "invalid_count": invalid_count
        }
    )


# =========================================================
# 6. TIMESTAMP LOGIC VALIDATION
# =========================================================

def validate_timestamp_sequence(
    df: DataFrame,
    earlier_column: str,
    later_column: str
) -> Dict[str, Any]:
    """
    Validate chronological lifecycle order.

    Purpose:
    - Protect lifecycle integrity
    - Detect impossible event flows
    - Prevent invalid delivery metrics

    Example:
    purchase_timestamp <= approval_timestamp

    Parameters
    ----------
    df : DataFrame
        Dataset to validate.

    earlier_column : str
        Earlier lifecycle timestamp.

    later_column : str
        Later lifecycle timestamp.

    Returns
    -------
    dict
        Validation result dictionary.
    """

    invalid_count = (
        df.filter(
            (col(earlier_column).isNotNull()) &
            (col(later_column).isNotNull()) &
            (col(earlier_column) > col(later_column))
        )
        .count()
    )

    if invalid_count == 0:
        status = "PASSED"
        message = "Timestamp lifecycle validation passed."
    else:
        status = "FAILED"
        message = "Invalid timestamp lifecycle sequence detected."

    return build_validation_result(
        validation_name="timestamp_sequence_validation",
        status=status,
        message=message,
        details={
            "earlier_column": earlier_column,
            "later_column": later_column,
            "invalid_record_count": invalid_count
        }
    )

# =========================================================
# POSITIVE VALUE VALIDATION
# =========================================================

def validate_positive_values(
    df,
    column_name,
    dataset_name="dataset"
):
    """
    Validates that numeric column values are non-negative.

    Purpose:
    Protect financial, operational, and KPI integrity.

    Parameters
    ----------
    df : DataFrame
        Spark dataframe.

    column_name : str
        Numeric column to validate.

    dataset_name : str
        Dataset name for logging.
    """

    print(
        f"\nValidating positive values for: "
        f"{column_name}"
    )

    invalid_count = (

        df

        .filter(
            col(column_name) < 0
        )

        .count()

    )

    print(
        f"Negative {column_name} Records: "
        f"{invalid_count}"
    )

    if invalid_count > 0:

        raise ValueError(
            f"FAILED: Negative values found in "
            f"{column_name} "
            f"for dataset {dataset_name}"
        )

    print(
        f"PASSED: {column_name} positive value validation."
    )

# =========================================================
# 7. VALIDATION REPORT PRINTER
# =========================================================

def print_validation_result(result: Dict[str, Any]) -> None:
    """
    Pretty-print validation result.

    Purpose:
    - Easier debugging
    - Cleaner notebook output
    - Operational visibility

    Parameters
    ----------
    result : dict
        Validation result dictionary.
    """

    print("=" * 60)
    print(f"VALIDATION: {result['validation_name']}")
    print(f"STATUS: {result['status']}")
    print(f"MESSAGE: {result['message']}")
    print("DETAILS:")

    for key, value in result["details"].items():
        print(f"  - {key}: {value}")

    print(f"VALIDATED AT: {result['validated_at']}")
    print("=" * 60)


# =========================================================
# 8. VALIDATION SUMMARY
# =========================================================

def summarize_validations(
    validation_results: List[Dict[str, Any]]
) -> Dict[str, Any]:
    """
    Generate pipeline-level validation summary.

    Purpose:
    - Centralized validation reporting
    - Pipeline health visibility
    - Airflow-ready monitoring

    Parameters
    ----------
    validation_results : List[dict]
        List of validation outputs.

    Returns
    -------
    dict
        Validation summary.
    """

    total = len(validation_results)

    passed = sum(
        1 for result in validation_results
        if result["status"] == "PASSED"
    )

    failed = sum(
        1 for result in validation_results
        if result["status"] == "FAILED"
    )

    warnings = sum(
        1 for result in validation_results
        if result["status"] == "WARNING"
    )

    overall_status = (
        "FAILED"
        if failed > 0
        else "WARNING"
        if warnings > 0
        else "PASSED"
    )

    return {
        "overall_status": overall_status,
        "total_validations": total,
        "passed": passed,
        "failed": failed,
        "warnings": warnings,
        "validated_at": datetime.utcnow().isoformat()
    }
