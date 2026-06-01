"""
run_gold_pipeline.py

Objective:
Configuration-driven Gold Layer Orchestration

Responsibilities:
- Build Dimensions
- Build Facts
- Build Business Marts
- Build Scoring Layer
- Stop on Failure
- Support Future Airflow Migration
- Support Future MinIO Migration

Project:
Olist Seller Intelligence Platform

Layer:
Gold Orchestration
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
        "../../"
    )
)

if project_root not in sys.path:
    sys.path.append(project_root)


# =========================================================
# CONFIG LOADER
# =========================================================

from pipelines.gold.utils.config_loader import (
    load_config
)

config = load_config()


# =========================================================
# ORCHESTRATION CONFIGURATION
# =========================================================

PIPELINE_CONFIG = config["gold_pipeline"]

ORCHESTRATION_CONFIG = config["orchestration"]

STOP_ON_FAILURE = ORCHESTRATION_CONFIG.get(
    "stop_on_failure",
    True
)

RUN_MARTS = ORCHESTRATION_CONFIG.get(
    "run_marts",
    True
)

RUN_SCORING = ORCHESTRATION_CONFIG.get(
    "run_scoring",
    True
)

LOG_EXECUTION_TIME = ORCHESTRATION_CONFIG.get(
    "log_execution_time",
    True
)


# =========================================================
# EXECUTION HELPER
# =========================================================

def run_transformation(relative_script_path):

    script_path = os.path.join(
        project_root,
        "pipelines",
        "gold",
        relative_script_path
    )

    print("\n" + "=" * 70)
    print(
        f"RUNNING: "
        f"{os.path.basename(script_path)}"
    )
    print("=" * 70)

    start_time = time.time()

    result = subprocess.run(
        [sys.executable, script_path],
        cwd=project_root
    )

    execution_time = round(
        time.time() - start_time,
        2
    )

    if result.returncode != 0:

        print("\n" + "=" * 70)
        print("TRANSFORMATION FAILED")
        print(script_path)
        print("=" * 70)

        if STOP_ON_FAILURE:

            raise RuntimeError(
                f"Gold Pipeline Failed: {script_path}"
            )

    if LOG_EXECUTION_TIME:

        print(
            f"Execution Time: "
            f"{execution_time} seconds"
        )

    print("SUCCESS")


# =========================================================
# GROUP EXECUTION
# =========================================================

def run_group(
    group_name,
    transformations
):

    if not transformations:
        return

    print("\n")
    print("=" * 70)
    print(
        f"STARTING {group_name.upper()}"
    )
    print("=" * 70)

    for transformation in transformations:

        run_transformation(
            transformation
        )


# =========================================================
# PIPELINE START
# =========================================================

pipeline_start = time.time()

print("\n")
print("=" * 70)
print("STARTING GOLD PIPELINE")
print("=" * 70)

print(
    f"Environment: "
    f"{config.get('environment', 'unknown')}"
)

print(
    f"Project Root: "
    f"{project_root}"
)


# =========================================================
# DIMENSIONS
# =========================================================

run_group(
    "Dimensions",
    PIPELINE_CONFIG["dimensions"]
)


# =========================================================
# FACTS
# =========================================================

run_group(
    "Facts",
    PIPELINE_CONFIG["facts"]
)


# =========================================================
# BUSINESS MARTS
# =========================================================

if RUN_MARTS:

    run_group(
        "Business Marts",
        PIPELINE_CONFIG.get(
            "marts",
            []
        )
    )


# =========================================================
# SCORING LAYER
# =========================================================

if RUN_SCORING:

    run_group(
        "Scoring Layer",
        PIPELINE_CONFIG.get(
            "scoring",
            []
        )
    )


# =========================================================
# PIPELINE SUMMARY
# =========================================================

total_runtime = round(
    time.time() - pipeline_start,
    2
)

print("\n")
print("=" * 70)
print("GOLD PIPELINE COMPLETED")
print("=" * 70)

print(
    f"Total Runtime: "
    f"{total_runtime} seconds"
)

print("=" * 70)

