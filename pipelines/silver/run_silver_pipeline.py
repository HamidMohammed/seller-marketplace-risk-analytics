"""
run_silver_pipeline.py

Objective:
Central orchestration pipeline for the complete Silver Layer.

This orchestrator executes all Silver transformations
in dependency-safe order and acts as the lightweight
workflow engine before enterprise orchestration tools
like Airflow are introduced.

Project:
Olist Seller Intelligence Platform

Architecture:
Medallion Architecture

Layer:
Silver

Responsibilities:
- Execute Silver transformations sequentially
- Preserve dependency order
- Stop execution on failures
- Provide centralized execution logging
- Measure execution runtime
- Support scalable orchestration architecture

Author:
Olist Seller Intelligence Platform
"""

# =========================================================
# PROJECT ROOT SETUP
# =========================================================

import sys
import os

project_root = os.path.abspath(
    os.path.join(os.path.dirname(__file__), "../../")
)

if project_root not in sys.path:
    sys.path.append(project_root)

print(f"Project Root Added: {project_root}")


# =========================================================
# IMPORTS
# =========================================================

import subprocess
import time
from datetime import datetime


# =========================================================
# PIPELINE CONFIGURATION
# =========================================================

print("\n=================================================")
print("INITIALIZING SILVER PIPELINE")
print("=================================================")

PIPELINE_START_TIME = time.time()

PIPELINE_START_TIMESTAMP = datetime.now()

print(
    f"Pipeline Start Time: "
    f"{PIPELINE_START_TIMESTAMP}"
)


# =========================================================
# SILVER PIPELINE EXECUTION ORDER
# =========================================================

"""
IMPORTANT:
Execution order preserves dataset dependencies.

Do NOT reorder casually.

Dependency Flow:

silver_orders
    ↓
silver_order_items
    ↓
silver_geolocation
    ↓
silver_customers
    ↓
silver_sellers
    ↓
silver_products
    ↓
silver_payments
    ↓
silver_reviews
    ↓
staging datasets
"""

silver_pipeline = [

    # =====================================================
    # CORE OPERATIONAL FOUNDATIONS
    # =====================================================

    {
        "name": "silver_orders",
        "path": (
            "pipelines/silver/transformations/"
            "orders/transform_orders.py"
        )
    },

    {
        "name": "silver_order_items",
        "path": (
            "pipelines/silver/transformations/"
            "order_items/transform_order_items.py"
        )
    },

    {
        "name": "silver_geolocation",
        "path": (
            "pipelines/silver/transformations/"
            "geolocation/transform_geolocation.py"
        )
    },

    {
        "name": "silver_customers",
        "path": (
            "pipelines/silver/transformations/"
            "customers/transform_customers.py"
        )
    },

    {
        "name": "silver_sellers",
        "path": (
            "pipelines/silver/transformations/"
            "sellers/transform_sellers.py"
        )
    },

    {
        "name": "silver_products",
        "path": (
            "pipelines/silver/transformations/"
            "products/transform_products.py"
        )
    },

    # =====================================================
    # ANALYTICAL SUPPORT DATASETS
    # =====================================================

    {
        "name": "silver_payments",
        "path": (
            "pipelines/silver/transformations/"
            "payments/transform_payments.py"
        )
    },

    {
        "name": "silver_reviews",
        "path": (
            "pipelines/silver/transformations/"
            "reviews/transform_reviews.py"
        )
    },

    {
        "name": "silver_category_translation",
        "path": (
            "pipelines/silver/transformations/"
            "category_translation/"
            "transform_category_translation.py"
        )
    },

    # =====================================================
    # MARKETING / ACQUISITION DATASETS
    # =====================================================

    {
        "name": "silver_mql",
        "path": (
            "pipelines/silver/transformations/"
            "mql/"
            "transform_mql.py"
        )
    },

    {
        "name": "silver_closed_deals",
        "path": (
            "pipelines/silver/transformations/"
            "closed_deals/"
            "transform_closed_deals.py"
        )
    },

    # {
    #     "name": "silver_seller_acquisition",
    #     "path": (
    #         "pipelines/silver/transformations/"
    #         "seller_acquisition/"
    #         "transform_seller_acquisition.py"
    #     )
    # },

    # =====================================================
    # STAGING LAYER
    # =====================================================

    {
        "name": "order_delivery_staging",
        "path": (
            "pipelines/silver/transformations/"
            "staging/"
            "transform_order_delivery_staging.py"
        )
    },

    {
        "name": "seller_fulfillment_staging",
        "path": (
            "pipelines/silver/transformations/"
            "staging/"
            "transform_seller_fulfillment_staging.py"
        )
    },
    
        {
        "name": "reviews_staging",
        "path": (
            "pipelines/silver/transformations/"
            "staging/"
            "transform_reviews_staging.py"
        )
    }
]


# =========================================================
# PIPELINE EXECUTION ENGINE
# =========================================================

successful_jobs = []

failed_jobs = []

print("\n=================================================")
print("STARTING SILVER TRANSFORMATIONS")
print("=================================================")

for step in silver_pipeline:

    dataset_name = step["name"]

    script_path = step["path"]

    print("\n-------------------------------------------------")
    print(f"STARTING: {dataset_name}")
    print("-------------------------------------------------")

    start_time = time.time()

    try:

        # =================================================
        # EXECUTE TRANSFORMATION SCRIPT
        # =================================================

        result = subprocess.run(

            ["python", script_path],

            check=True,

            capture_output=False,

            text=True
        )

        end_time = time.time()

        runtime_seconds = round(
            end_time - start_time,
            2
        )

        print("\nSUCCESS")
        print(
            f"{dataset_name} completed successfully"
        )

        print(
            f"Runtime: {runtime_seconds} seconds"
        )

        successful_jobs.append(dataset_name)

    except subprocess.CalledProcessError as error:

        end_time = time.time()

        runtime_seconds = round(
            end_time - start_time,
            2
        )

        print("\nFAILED")
        print(
            f"{dataset_name} failed"
        )

        print(
            f"Runtime Before Failure: "
            f"{runtime_seconds} seconds"
        )

        print(f"Error: {error}")

        failed_jobs.append(dataset_name)

        # ================================================
        # FAIL FAST STRATEGY
        # ================================================

        print("\n=================================================")
        print("PIPELINE TERMINATED")
        print("=================================================")

        print(
            "Stopping execution due to dependency-safe "
            "fail-fast strategy."
        )

        sys.exit(1)


# =========================================================
# FINAL PIPELINE SUMMARY
# =========================================================

PIPELINE_END_TIME = time.time()

PIPELINE_TOTAL_RUNTIME = round(
    PIPELINE_END_TIME - PIPELINE_START_TIME,
    2
)

PIPELINE_END_TIMESTAMP = datetime.now()

print("\n=================================================")
print("SILVER PIPELINE COMPLETED")
print("=================================================")

print(
    f"Pipeline End Time: "
    f"{PIPELINE_END_TIMESTAMP}"
)

print(
    f"Total Runtime: "
    f"{PIPELINE_TOTAL_RUNTIME} seconds"
)

print("\n=================================================")
print("SUCCESSFUL DATASETS")
print("=================================================")

for dataset in successful_jobs:

    print(f"SUCCESS -> {dataset}")

print("\n=================================================")
print("FAILED DATASETS")
print("=================================================")

if len(failed_jobs) == 0:

    print("NO FAILURES DETECTED")

else:

    for dataset in failed_jobs:

        print(f"FAILED -> {dataset}")


# =========================================================
# FINAL EXECUTION STATUS
# =========================================================

print("\n=================================================")
print("FINAL PIPELINE STATUS")
print("=================================================")

if len(failed_jobs) == 0:

    print(
        "ALL SILVER TRANSFORMATIONS "
        "COMPLETED SUCCESSFULLY"
    )

else:

    print(
        "PIPELINE COMPLETED WITH FAILURES"
    )

print("\n=================================================")
print("SILVER ORCHESTRATION FINISHED")
print("=================================================")