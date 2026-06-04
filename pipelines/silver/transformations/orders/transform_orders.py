
"""
transform_orders.py

Objective:
Transform Bronze orders dataset into trusted Silver orders dataset.

Hardening Version:
- Lifecycle chronology validation
- Quarantine architecture
- Advanced delivery metrics
- Operational delivery intelligence
- Business-truth preservation

Dataset Grain:
ONE ROW = ONE CUSTOMER ORDER
"""

# =========================================================
# PROJECT ROOT SETUP
# =========================================================

import sys
import os

project_root = os.path.abspath(
    os.path.join(
        os.path.dirname(__file__),
        "../../../../"
    )
)

if project_root not in sys.path:
    sys.path.append(project_root)

print(f"Project Root Added: {project_root}")


# =========================================================
# IMPORTS
# =========================================================

from pyspark.sql import SparkSession

from pyspark.sql.functions import (

    col,
    lower,
    trim,
    to_timestamp,
    datediff,
    when,
    current_timestamp,
    lit,
    abs

)

from pipelines.silver.utils.config_loader import (
    load_config,
    resolve_path
)

from pipelines.silver.validations.orders_validation import (
    run_orders_validation
)

from pipelines.silver.utils.spark_session import (
    create_spark_session
)


# =========================================================
# CREATE SPARK SESSION
# =========================================================

spark = create_spark_session(
    "TransformSilverOrders"
)

# =========================================================
# LOAD CONFIGURATION
# =========================================================

config = load_config()

BRONZE_ORDERS_PATH = resolve_path(

    config["paths"]["bronze"]["orders"],
    config

)

SILVER_ORDERS_PATH = resolve_path(

    config["paths"]["silver"]["orders"],
    config

)

SILVER_ORDERS_QUARANTINE_PATH = resolve_path(

    config["paths"]["silver"]["orders_quarantine"],
    config

)

SOURCE_SYSTEM = (
    config["metadata"]["source_system"]
)

TRANSFORMATION_VERSION = (
    config["metadata"]["transformation_version"]
)


# =========================================================
# LOAD BRONZE DATA
# =========================================================

print("\n=================================================")
print("LOADING BRONZE ORDERS DATA")
print("=================================================")

bronze_orders_df = spark.read.parquet(
    BRONZE_ORDERS_PATH
)

print(
    f"Bronze Orders Count: "
    f"{bronze_orders_df.count()}"
)

silver_orders_df = bronze_orders_df


# =========================================================
# STANDARDIZE STATUS
# =========================================================

silver_orders_df = silver_orders_df.withColumn(

    "order_status",

    lower(
        trim(
            col("order_status")
        )
    )
)


# =========================================================
# CAST TIMESTAMPS
# =========================================================

timestamp_columns = [

    "order_purchase_timestamp",
    "order_approved_at",
    "order_delivered_carrier_date",
    "order_delivered_customer_date",
    "order_estimated_delivery_date"

]

for column_name in timestamp_columns:

    silver_orders_df = silver_orders_df.withColumn(

        column_name,

        to_timestamp(
            col(column_name)
        )
    )


# =========================================================
# DELIVERY METRICS
# =========================================================

silver_orders_df = silver_orders_df.withColumn(

    "delivery_duration_days",

    datediff(
        col(
            "order_delivered_customer_date"
        ),
        col(
            "order_purchase_timestamp"
        )
    )
)

silver_orders_df = silver_orders_df.withColumn(

    "delay_days",

    datediff(
        col(
            "order_delivered_customer_date"
        ),
        col(
            "order_estimated_delivery_date"
        )
    )
)

silver_orders_df = silver_orders_df.withColumn(

    "estimated_delivery_window_days",

    datediff(
        col(
            "order_estimated_delivery_date"
        ),
        col(
            "order_purchase_timestamp"
        )
    )
)


# =========================================================
# DELIVERY STATUS CATEGORY
# =========================================================

silver_orders_df = silver_orders_df.withColumn(

    "delivery_status_category",

    when(
        col("delay_days") > 0,
        "Late"
    )

    .when(
        col("delay_days") < 0,
        "Early"
    )

    .when(
        col("delay_days") == 0,
        "On Time"
    )

    .otherwise(
        "Unknown"
    )
)


# =========================================================
# DELIVERY STATUS DETAIL
# =========================================================

silver_orders_df = silver_orders_df.withColumn(

    "delivery_status_detail",

    when(
        col("delay_days") <= -7,
        "Very Early"
    )

    .when(
        col("delay_days") < 0,
        "Early"
    )

    .when(
        col("delay_days") == 0,
        "On Time"
    )

    .when(
        col("delay_days") <= 7,
        "Slightly Late"
    )

    .otherwise(
        "Severely Late"
    )
)


# =========================================================
# DELIVERY FLAG
# =========================================================

silver_orders_df = silver_orders_df.withColumn(

    "is_successfully_delivered",

    when(
        col("order_status")
        == "delivered",
        1
    ).otherwise(0)
)


# =========================================================
# ADVANCED LIFECYCLE METRICS
# =========================================================

silver_orders_df = silver_orders_df.withColumn(

    "handling_days",

    datediff(
        col(
            "order_delivered_carrier_date"
        ),
        col(
            "order_approved_at"
        )
    )
)

silver_orders_df = silver_orders_df.withColumn(

    "shipping_days",

    datediff(
        col(
            "order_delivered_customer_date"
        ),
        col(
            "order_delivered_carrier_date"
        )
    )
)

silver_orders_df = silver_orders_df.withColumn(

    "total_lead_time",

    datediff(
        col(
            "order_delivered_customer_date"
        ),
        col(
            "order_purchase_timestamp"
        )
    )
)

silver_orders_df = silver_orders_df.withColumn(

    "days_diff_estimated",

    datediff(
        col(
            "order_delivered_customer_date"
        ),
        col(
            "order_estimated_delivery_date"
        )
    )
)

silver_orders_df = silver_orders_df.withColumn(

    "estimated_buffer",

    datediff(
        col(
            "order_estimated_delivery_date"
        ),
        col(
            "order_purchase_timestamp"
        )
    )

    -

    datediff(
        col(
            "order_delivered_customer_date"
        ),
        col(
            "order_purchase_timestamp"
        )
    )
)

silver_orders_df = silver_orders_df.withColumn(

    "abs_days_diff",

    abs(
        col("days_diff_estimated")
    )
)


# =========================================================
# QUARANTINE
# =========================================================

chronology_violation_df = silver_orders_df.filter(

    (

        col("order_approved_at").isNotNull()

        &

        (
            col(
                "order_purchase_timestamp"
            )
            >
            col(
                "order_approved_at"
            )
        )

    )

    |

    (

        col(
            "order_delivered_carrier_date"
        ).isNotNull()

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

        col(
            "order_delivered_customer_date"
        ).isNotNull()

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

).withColumn(

    "quarantine_reason",

    lit(
        "CHRONOLOGY_VIOLATION"
    )
)

missing_delivery_df = silver_orders_df.filter(

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

).withColumn(

    "quarantine_reason",

    lit(
        "DELIVERED_WITHOUT_DELIVERY_DATE"
    )
)

orders_quarantine_df = (

    chronology_violation_df

    .unionByName(
        missing_delivery_df
    )
)


# =========================================================
# CLEAN DATASET
# =========================================================

clean_orders_df = silver_orders_df.join(

    orders_quarantine_df.select(
        "order_id"
    ),

    on="order_id",

    how="left_anti"
)


# =========================================================
# METADATA
# =========================================================

clean_orders_df = clean_orders_df.withColumn(

    "silver_loaded_at",

    current_timestamp()
)

clean_orders_df = clean_orders_df.withColumn(

    "source_system",

    lit(
        SOURCE_SYSTEM
    )
)

clean_orders_df = clean_orders_df.withColumn(

    "transformation_version",

    lit(
        TRANSFORMATION_VERSION
    )
)


# =========================================================
# VALIDATIONS
# =========================================================

run_orders_validation(

    source_df=bronze_orders_df,

    transformed_df=clean_orders_df,

    quarantine_df=orders_quarantine_df

)


# =========================================================
# WRITE QUARANTINE
# =========================================================

orders_quarantine_df.write \
    .mode("overwrite") \
    .parquet(
        SILVER_ORDERS_QUARANTINE_PATH
    )


# =========================================================
# WRITE CLEAN SILVER
# =========================================================

clean_orders_df.write \
    .mode("overwrite") \
    .parquet(
        SILVER_ORDERS_PATH
    )


# =========================================================
# FINAL SUMMARY
# =========================================================

print("\n=================================================")
print("ORDERS HARDENING COMPLETED")
print("=================================================")

print(
    f"Clean Orders: "
    f"{clean_orders_df.count()}"
)

print(
    f"Quarantined Orders: "
    f"{orders_quarantine_df.count()}"
)

silver_orders_df.filter(
    col("order_delivered_customer_date").isNull()
).groupBy(
    "order_status"
).count().show(truncate=False)

spark.stop()

