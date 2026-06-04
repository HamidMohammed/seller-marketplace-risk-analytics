"""
run_pipeline.py

Objective:
Master Orchestration Layer

Responsibilities:
- Execute Bronze Pipeline
- Execute Silver Pipeline
- Execute Gold Pipeline
- Stop on Failure
- Execution Monitoring
- Future Airflow Blueprint

Project:
Olist Seller Intelligence Platform

Layer:
Master Orchestration
"""

# =========================================================
# PROJECT ROOT SETUP
# =========================================================

import os
import sys
import time
import subprocess

project_root = os.path.abspath(
    os.path.join(
        os.path.dirname(__file__),
        "../"
    )
)

if project_root not in sys.path:
    sys.path.append(project_root)


IS_DOCKER = (
    os.getenv(
        "SPARK_DOCKER",
        "false"
    ).lower() == "true"
)
# =========================================================
# PIPELINE EXECUTION HELPER
# =========================================================

def run_pipeline_component(
    pipeline_name,
    script_path
):

    print("\n")
    print("=" * 80)
    print(
        f"STARTING {pipeline_name.upper()}"
    )
    print("=" * 80)

    start_time = time.time()

    command = (
    [
        "/opt/spark/bin/spark-submit",
        script_path
    ]
    if IS_DOCKER
    else
    [
        sys.executable,
        script_path
    ]
    )

    result = subprocess.run(
        command,
        cwd=project_root
    )

    duration = round(
        time.time() - start_time,
        2
    )

    if result.returncode != 0:

        print("\n")
        print("=" * 80)
        print(
            f"{pipeline_name.upper()} FAILED"
        )
        print("=" * 80)

        raise RuntimeError(
            f"{pipeline_name} failed"
        )

    print(
        f"{pipeline_name} completed "
        f"successfully "
        f"({duration} sec)"
    )


# =========================================================
# PIPELINE PATHS
# =========================================================

BRONZE_PIPELINE = os.path.join(
    project_root,
    "pipelines",
    "bronze",
    "run_bronze_pipeline.py"
)

SILVER_PIPELINE = os.path.join(
    project_root,
    "pipelines",
    "silver",
    "run_silver_pipeline.py"
)

GOLD_PIPELINE = os.path.join(
    project_root,
    "pipelines",
    "gold",
    "run_gold_pipeline.py"
)

WAREHOUSE_LOAD = os.path.join(
    project_root,
    "infrastructure",
    "postgres",
    "load_gold_to_postgres.py"
)

# =========================================================
# MASTER PIPELINE
# =========================================================

master_start = time.time()

print("\n")
print("=" * 80)
print("OLIST SELLER INTELLIGENCE PLATFORM")
print("MASTER PIPELINE STARTED")
print("=" * 80)

try:

    # -----------------------------------------------------
    # BRONZE
    # -----------------------------------------------------

    run_pipeline_component(
        "Bronze Pipeline",
        BRONZE_PIPELINE
    )

    # -----------------------------------------------------
    # SILVER
    # -----------------------------------------------------

    run_pipeline_component(
        "Silver Pipeline",
        SILVER_PIPELINE
    )

    # -----------------------------------------------------
    # GOLD
    # -----------------------------------------------------

    run_pipeline_component(
        "Gold Pipeline",
        GOLD_PIPELINE
    )
    
    run_pipeline_component(
    "Warehouse Load",
    WAREHOUSE_LOAD
    )

except Exception as e:

    print("\n")
    print("=" * 80)
    print("MASTER PIPELINE FAILED")
    print("=" * 80)

    print(str(e))

    sys.exit(1)


# =========================================================
# FINAL SUMMARY
# =========================================================

total_runtime = round(
    time.time() - master_start,
    2
)

print("\n")
print("=" * 80)
print("MASTER PIPELINE COMPLETED")
print("=" * 80)

print(
    f"Total Runtime: "
    f"{total_runtime} seconds"
)

print("=" * 80)