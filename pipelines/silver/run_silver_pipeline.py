"""
run_silver_pipeline.py

Objective:
Configuration-driven Silver Layer Orchestration

Responsibilities:
- Read execution plan from silver_config.yaml
- Execute transformations in dependency order
- Support future Airflow migration
- Support future MinIO migration
- Support future environment abstraction
- Stop on failure
- Execution monitoring

Project:
Olist Seller Intelligence Platform

Layer:
Silver Orchestration
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

from pipelines.silver.utils.config_loader import (
    load_config
)

config = load_config()


# =========================================================
# ORCHESTRATION CONFIGURATION
# =========================================================

PIPELINE_CONFIG = config["silver_pipeline"]

ORCHESTRATION_CONFIG = config["orchestration"]

STOP_ON_FAILURE = ORCHESTRATION_CONFIG.get(
    "stop_on_failure",
    True
)

RUN_MARKETING_LAYER = ORCHESTRATION_CONFIG.get(
    "run_marketing_layer",
    True
)

RUN_PERFORMANCE_LAYER = ORCHESTRATION_CONFIG.get(
    "run_performance_layer",
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
        "silver",
        "transformations",
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
                f"Pipeline failed at: {script_path}"
            )

    if LOG_EXECUTION_TIME:

        print(
            f"Execution Time: "
            f"{execution_time} seconds"
        )

    print("SUCCESS")


# =========================================================
# EXECUTION GROUP HELPER
# =========================================================

def run_group(
    group_name,
    transformations
):

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
print("STARTING SILVER PIPELINE")
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
# CORE LAYER
# =========================================================

run_group(
    "Core Silver Layer",
    PIPELINE_CONFIG["core"]
)


# =========================================================
# MARKETING LAYER
# =========================================================

if RUN_MARKETING_LAYER:

    run_group(
        "Marketing Layer",
        PIPELINE_CONFIG["marketing"]
    )


# =========================================================
# STAGING LAYER
# =========================================================

run_group(
    "Analytical Staging Layer",
    PIPELINE_CONFIG["staging"]
)


# =========================================================
# PERFORMANCE LAYER
# =========================================================

if RUN_PERFORMANCE_LAYER:

    run_group(
        "Performance Intelligence Layer",
        PIPELINE_CONFIG["performance"]
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
print("SILVER PIPELINE COMPLETED")
print("=" * 70)

print(
    f"Total Runtime: "
    f"{total_runtime} seconds"
)

print("=" * 70)
