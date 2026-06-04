"""
verify_postgres_load.py

Objective:
Validate PostgreSQL warehouse loads
against Gold Layer datasets stored
in MinIO.

Validation Rules:

1. Table Exists
2. Row Count Match
3. Load Completeness

Project:
Olist Seller Intelligence Platform
"""

# =========================================================
# PROJECT ROOT
# =========================================================

import os
import sys

project_root = os.path.abspath(
    os.path.join(
        os.path.dirname(__file__),
        "../../"
    )
)

if project_root not in sys.path:
    sys.path.append(project_root)

# =========================================================
# IMPORTS
# =========================================================

from pyspark.sql.functions import count

from pipelines.silver.utils.spark_session import (
    create_spark_session
)

# =========================================================
# SPARK SESSION
# =========================================================

spark = create_spark_session(
    "VerifyPostgresLoad"
)

# =========================================================
# POSTGRES CONFIG
# =========================================================

POSTGRES_URL = (
    "jdbc:postgresql://localhost:5432/olist_dw"
)

POSTGRES_PROPERTIES = {

    "user": "olist",

    "password": "olist123",

    "driver": "org.postgresql.Driver"
}

# =========================================================
# DATASETS
# =========================================================

DATASETS = {

    "dim_date":
        "s3a://gold/dim_date/",

    "dim_customer":
        "s3a://gold/dim_customer/",

    "dim_seller":
        "s3a://gold/dim_seller/",

    "dim_product":
        "s3a://gold/dim_product/",

    "fct_order_delivery":
        "s3a://gold/fct_order_delivery/",

    "fct_seller_fulfillment":
        "s3a://gold/fct_seller_fulfillment/",

    "fct_customer_reviews":
        "s3a://gold/fct_customer_reviews/",

    "fct_order_sales":
        "s3a://gold/fct_order_sales/",

    "seller_performance_mart":
        "s3a://gold/marts/seller_performance_mart/"
}

# =========================================================
# VALIDATION
# =========================================================

print("\n=================================================")
print("POSTGRES LOAD VALIDATION")
print("=================================================")

validation_results = []

for table_name, gold_path in DATASETS.items():

    print("\n-------------------------------------------------")
    print(f"Validating: {table_name}")
    print("-------------------------------------------------")

    try:

        # =============================================
        # GOLD COUNT
        # =============================================

        gold_df = spark.read.parquet(
            gold_path
        )

        gold_count = gold_df.count()

        # =============================================
        # POSTGRES COUNT
        # =============================================

        postgres_df = spark.read.jdbc(

            url=POSTGRES_URL,

            table=table_name,

            properties=POSTGRES_PROPERTIES
        )

        postgres_count = postgres_df.count()

        counts_match = (
            gold_count == postgres_count
        )

        validation_results.append({

            "table": table_name,

            "gold_count": gold_count,

            "postgres_count": postgres_count,

            "status":
                "PASS"
                if counts_match
                else "FAIL"
        })

        print(
            f"Gold Rows: {gold_count:,}"
        )

        print(
            f"Postgres Rows: {postgres_count:,}"
        )

        print(
            f"Status: "
            f"{'PASS' if counts_match else 'FAIL'}"
        )

    except Exception as e:

        validation_results.append({

            "table": table_name,

            "gold_count": 0,

            "postgres_count": 0,

            "status": "ERROR"
        })

        print(
            f"ERROR: {str(e)}"
        )

# =========================================================
# SUMMARY
# =========================================================

print("\n=================================================")
print("VALIDATION SUMMARY")
print("=================================================")

pass_count = 0
fail_count = 0

for result in validation_results:

    print(

        f"{result['table']:30} | "
        f"{result['status']}"
    )

    if result["status"] == "PASS":
        pass_count += 1
    else:
        fail_count += 1

print("\n=================================================")

print(
    f"PASS: {pass_count}"
)

print(
    f"FAIL: {fail_count}"
)

print("=================================================")

if fail_count == 0:

    print(
        "\nPOSTGRES LOAD VALIDATION PASSED"
    )

else:

    print(
        "\nPOSTGRES LOAD VALIDATION FAILED"
    )

spark.stop()