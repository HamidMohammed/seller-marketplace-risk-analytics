
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
# IMPORTS
# =========================================================

from pyspark.sql.functions import (
    col
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

    print("\n[VALIDATION] Order Grain Integrity")

    validate_duplicates(
        df=df,
        key_columns=["order_id"]
    )


# =========================================================
# VALIDATE CRITICAL NULLS
# =========================================================

def validate_critical_nulls(df):

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
# VALIDATE ORDER STATUS
# =========================================================

def validate_order_status(df):

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

        ~col("order_status").isin(
            allowed_statuses
        )

    )

    invalid_count = invalid_status_df.count()

    if invalid_count > 0:

        print(
            f"[FAILED] Invalid statuses found: "
            f"{invalid_count}"
        )

        invalid_status_df.select(
            "order_status"
        ).distinct().show(
            truncate=False
        )

    else:

        print(
            "[PASSED] All order statuses valid"
        )


# =========================================================
# PURCHASE → APPROVAL
# =========================================================

def validate_purchase_approval_sequence(df):

    print(
        "\n[VALIDATION] Purchase → Approval"
    )

    invalid_count = df.filter(

        (
            col("order_approved_at").isNotNull()
        )

        &

        (
            col("order_purchase_timestamp")
            >
            col("order_approved_at")
        )

    ).count()

    print(
        f"Invalid Purchase/Approval: "
        f"{invalid_count}"
    )


# =========================================================
# APPROVAL → CARRIER
# =========================================================

def validate_approval_carrier_sequence(df):

    print(
        "\n[VALIDATION] Approval → Carrier"
    )

    invalid_count = df.filter(

        (
            col(
                "order_delivered_carrier_date"
            ).isNotNull()
        )

        &

        (
            col("order_approved_at")
            >
            col(
                "order_delivered_carrier_date"
            )
        )

    ).count()

    print(
        f"Invalid Approval/Carrier: "
        f"{invalid_count}"
    )


# =========================================================
# CARRIER → CUSTOMER
# =========================================================

def validate_carrier_customer_sequence(df):

    print(
        "\n[VALIDATION] Carrier → Customer"
    )

    invalid_count = df.filter(

        (
            col(
                "order_delivered_customer_date"
            ).isNotNull()
        )

        &

        (
            col(
                "order_delivered_carrier_date"
            )
            >
            col(
                "order_delivered_customer_date"
            )
        )

    ).count()

    print(
        f"Invalid Carrier/Customer: "
        f"{invalid_count}"
    )


# =========================================================
# CHRONOLOGY SUMMARY
# =========================================================

def validate_chronology_violations(df):

    print(
        "\n[VALIDATION] Chronology Integrity"
    )

    chronology_count = df.filter(

        (
            (
                col("order_approved_at").isNotNull()
            )

            &

            (
                col("order_purchase_timestamp")
                >
                col("order_approved_at")
            )
        )

        |

        (
            (
                col(
                    "order_delivered_carrier_date"
                ).isNotNull()
            )

            &

            (
                col("order_approved_at")
                >
                col(
                    "order_delivered_carrier_date"
                )
            )
        )

        |

        (
            (
                col(
                    "order_delivered_customer_date"
                ).isNotNull()
            )

            &

            (
                col(
                    "order_delivered_carrier_date"
                )
                >
                col(
                    "order_delivered_customer_date"
                )
            )
        )

    ).count()

    print(
        f"Chronology Violations: "
        f"{chronology_count}"
    )


# =========================================================
# DELIVERED ORDERS
# =========================================================

def validate_delivered_orders(df):

    print(
        "\n[VALIDATION] Delivered Orders"
    )

    invalid_count = df.filter(

        (
            col("order_status")
            == "delivered"
        )

        &

        (
            col(
                "order_delivered_customer_date"
            ).isNull()
        )

    ).count()

    print(
        f"Delivered Orders Missing Date: "
        f"{invalid_count}"
    )


# =========================================================
# DELIVERY METRICS
# =========================================================

def validate_delivery_metrics(df):

    print(
        "\n[VALIDATION] Delivery Metrics"
    )

    negative_duration = df.filter(
        col("delivery_duration_days") < 0
    ).count()

    extreme_delay = df.filter(
        col("delay_days") > 365
    ).count()

    print(
        f"Negative Delivery Duration: "
        f"{negative_duration}"
    )

    print(
        f"Extreme Delay Orders: "
        f"{extreme_delay}"
    )


# =========================================================
# NEW METRICS VALIDATION
# =========================================================

def validate_new_metrics(df):

    print(
        "\n[VALIDATION] Derived Metrics"
    )

    negative_handling = df.filter(
        col("handling_days") < 0
    ).count()

    negative_shipping = df.filter(
        col("shipping_days") < 0
    ).count()

    negative_lead_time = df.filter(
        col("total_lead_time") < 0
    ).count()

    print(
        f"Negative Handling Days: "
        f"{negative_handling}"
    )

    print(
        f"Negative Shipping Days: "
        f"{negative_shipping}"
    )

    print(
        f"Negative Lead Time: "
        f"{negative_lead_time}"
    )


# =========================================================
# QUARANTINE VALIDATION
# =========================================================

def validate_quarantine_counts(
    quarantine_df
):

    print(
        "\n[VALIDATION] Quarantine Summary"
    )

    total_quarantined = (
        quarantine_df.count()
    )

    print(
        f"Total Quarantined Orders: "
        f"{total_quarantined}"
    )

    quarantine_df.groupBy(
        "quarantine_reason"
    ).count().show(
        truncate=False
    )


# =========================================================
# FULL VALIDATION PIPELINE
# =========================================================

def run_orders_validation(

    source_df,
    transformed_df,
    quarantine_df

):

    print(
        "\n================================================="
    )

    print(
        "RUNNING SILVER ORDERS VALIDATION"
    )

    print(
        "================================================="
    )

    validate_row_count(
        source_df=source_df,
        transformed_df=transformed_df
    )

    validate_order_grain(
        transformed_df
    )

    validate_critical_nulls(
        transformed_df
    )

    validate_order_status(
        transformed_df
    )

    validate_purchase_approval_sequence(
        transformed_df
    )

    validate_approval_carrier_sequence(
        transformed_df
    )

    validate_carrier_customer_sequence(
        transformed_df
    )

    validate_chronology_violations(
        transformed_df
    )

    validate_delivered_orders(
        transformed_df
    )

    validate_delivery_metrics(
        transformed_df
    )

    validate_new_metrics(
        transformed_df
    )

    validate_quarantine_counts(
        quarantine_df
    )

    print(
        "\n================================================="
    )

    print(
        "ORDERS VALIDATION COMPLETED"
    )

    print(
        "================================================="
    )

