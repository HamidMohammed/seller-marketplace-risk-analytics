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

print(f"Project Root Added: {project_root}")

# =========================================================
# ORDERS VALIDATION MODULE
# =========================================================

from pyspark.sql.functions import (
    col,
    count,
    when
)

from pipelines.silver.validations.validation_utils import (
    validate_row_count,
    validate_duplicates,
    validate_nulls
)



# =========================================================
# VALIDATE ORDER GRAIN
# =========================================================

def validate_order_grain(df):
    """
    Validate:
    One row = one unique order.
    """

    print("\n[VALIDATION] Order Grain Integrity")

    validate_duplicates(
        df=df,
        key_columns=["order_id"]
    )


# =========================================================
# VALIDATE CRITICAL NULLS
# =========================================================

def validate_critical_nulls(df):
    """
    Validate important lifecycle fields.
    """

    print("\n[VALIDATION] Critical Null Analysis")

    critical_columns = [
        "order_id",
        "customer_id",
        "order_status",
        "order_purchase_timestamp"
    ]

    validate_nulls(
        df=df,
        critical_columns=critical_columns
    )


# =========================================================
# VALIDATE ORDER STATUS VALUES
# =========================================================

def validate_order_status(df):
    """
    Validate allowed order statuses.
    """

    print("\n[VALIDATION] Order Status Categories")

    allowed_statuses = [
        "created",
        "approved",
        "invoiced",
        "processing",
        "shipped",
        "delivered",
        "unavailable",
        "canceled"
    ]

    invalid_status_df = df.filter(
        ~col("order_status").isin(allowed_statuses)
    )

    invalid_count = invalid_status_df.count()

    if invalid_count > 0:

        print(f"[FAILED] Invalid order statuses found: {invalid_count}")

        invalid_status_df.select("order_status").distinct().show(
            truncate=False
        )

    else:
        print("[PASSED] All order statuses are valid")


# =========================================================
# VALIDATE PURCHASE → APPROVAL LOGIC
# =========================================================

def validate_purchase_approval_sequence(df):
    """
    Validate:
    purchase_timestamp <= approval_timestamp
    """

    print("\n[VALIDATION] Purchase → Approval Sequence")

    invalid_df = df.filter(
        (
            col("order_approved_at").isNotNull()
        ) &
        (
            col("order_purchase_timestamp")
            > col("order_approved_at")
        )
    )

    invalid_count = invalid_df.count()

    if invalid_count > 0:

        print(
            f"[FAILED] Invalid purchase/approval sequence rows: "
            f"{invalid_count}"
        )

    else:
        print("[PASSED] Purchase/approval lifecycle valid")


# =========================================================
# VALIDATE APPROVAL → DELIVERY LOGIC
# =========================================================

def validate_approval_delivery_sequence(df):
    """
    Validate:
    approval_timestamp <= customer_delivery_timestamp
    """

    print("\n[VALIDATION] Approval → Delivery Sequence")

    invalid_df = df.filter(
        (
            col("order_delivered_customer_date").isNotNull()
        ) &
        (
            col("order_approved_at")
            > col("order_delivered_customer_date")
        )
    )

    invalid_count = invalid_df.count()

    if invalid_count > 0:

        print(
            f"[FAILED] Invalid approval/delivery sequence rows: "
            f"{invalid_count}"
        )

    else:
        print("[PASSED] Approval/delivery lifecycle valid")


# =========================================================
# VALIDATE DELIVERED ORDERS HAVE DELIVERY DATE
# =========================================================

def validate_delivered_orders(df):
    """
    Delivered orders must contain delivery timestamp.
    """

    print("\n[VALIDATION] Delivered Orders Integrity")

    invalid_df = df.filter(
        (
            col("order_status") == "delivered"
        ) &
        (
            col("order_delivered_customer_date").isNull()
        )
    )

    invalid_count = invalid_df.count()

    if invalid_count > 0:

        print(
            f"[FAILED] Delivered orders missing delivery date: "
            f"{invalid_count}"
        )

    else:
        print("[PASSED] Delivered orders contain delivery timestamps")


# =========================================================
# VALIDATE DELIVERY METRICS
# =========================================================

def validate_delivery_metrics(df):
    """
    Validate delivery metric logic.
    """

    print("\n[VALIDATION] Delivery Metrics")

    # Negative delivery duration
    negative_duration = df.filter(
        col("delivery_duration_days") < 0
    ).count()

    # Extreme delay values
    extreme_delay = df.filter(
        col("delay_days") > 365
    ).count()

    if negative_duration > 0:

        print(
            f"[FAILED] Negative delivery durations found: "
            f"{negative_duration}"
        )

    else:
        print("[PASSED] Delivery durations valid")

    if extreme_delay > 0:

        print(
            f"[WARNING] Extremely delayed deliveries found: "
            f"{extreme_delay}"
        )

    else:
        print("[PASSED] Delay distribution looks reasonable")


# =========================================================
# FULL VALIDATION PIPELINE
# =========================================================

def run_orders_validation(
    source_df,
    transformed_df
):
    """
    Run full validation suite for silver_orders.
    """

    print("\n=================================================")
    print("RUNNING SILVER ORDERS VALIDATION")
    print("=================================================")

    # -------------------------------------------------
    # Row Count Validation
    # -------------------------------------------------

    validate_row_count(
        source_df=source_df,
        transformed_df=transformed_df
    )

    # -------------------------------------------------
    # Grain Validation
    # -------------------------------------------------

    validate_order_grain(transformed_df)

    # -------------------------------------------------
    # Null Validation
    # -------------------------------------------------

    validate_critical_nulls(transformed_df)

    # -------------------------------------------------
    # Status Validation
    # -------------------------------------------------

    validate_order_status(transformed_df)

    # -------------------------------------------------
    # Lifecycle Validation
    # -------------------------------------------------

    validate_purchase_approval_sequence(transformed_df)

    validate_approval_delivery_sequence(transformed_df)

    validate_delivered_orders(transformed_df)

    # -------------------------------------------------
    # Metric Validation
    # -------------------------------------------------

    validate_delivery_metrics(transformed_df)

    print("\n=================================================")
    print("ORDERS VALIDATION COMPLETED")
    print("=================================================")
