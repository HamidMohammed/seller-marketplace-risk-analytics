"""
build_dim_date.py

Objective:
Build the conformed calendar dimension
used across all Gold fact tables.

This dimension provides:
- temporal analytics
- calendar hierarchies
- fiscal-style reporting support
- time intelligence

Project:
Olist Seller Intelligence Platform

Layer:
Gold

Dimension:
dim_date

Grain:
ONE ROW = ONE CALENDAR DATE
"""

# =========================================================
# PROJECT ROOT SETUP
# =========================================================

import sys
import os

project_root = os.path.abspath(
    os.path.join(os.path.dirname(__file__), "../../../../")
)

if project_root not in sys.path:
    sys.path.append(project_root)

print(f"Project Root Added: {project_root}")


# =========================================================
# IMPORTS
# =========================================================

from datetime import datetime, timedelta

from pyspark.sql import Row

from pyspark.sql.functions import (
    current_timestamp,
    lit
)

from pipelines.silver.utils.spark_session import (
    create_spark_session
)

from pipelines.silver.utils.config_loader import (
    load_config
)

from pipelines.gold.dimensions.date.dim_date_validation import (
    run_dim_date_validation
)


# =========================================================
# CREATE SPARK SESSION
# =========================================================

spark = create_spark_session(
    "BuildDimDate"
)


# =========================================================
# LOAD CONFIGURATION
# =========================================================

config = load_config()

# ---------------------------------------------------------
# Output Path
# ---------------------------------------------------------

DIM_DATE_PATH = (
    config["paths"]["gold"]["dim_date"]
)

# ---------------------------------------------------------
# Metadata
# ---------------------------------------------------------

SOURCE_SYSTEM = (
    config["metadata"]["source_system"]
)

TRANSFORMATION_VERSION = (
    config["metadata"]["transformation_version"]
)


# =========================================================
# DATE RANGE CONFIGURATION
# =========================================================

START_DATE = datetime(2016, 1, 1)

END_DATE = datetime(2019, 12, 31)

print("\n=================================================")
print("DATE RANGE CONFIGURATION")
print("=================================================")

print(f"Start Date: {START_DATE}")
print(f"End Date: {END_DATE}")


# =========================================================
# GENERATE DATE ROWS
# =========================================================

print("\n=================================================")
print("GENERATING DATE DIMENSION")
print("=================================================")

date_rows = []

current_date = START_DATE

while current_date <= END_DATE:

    date_sk = int(
        current_date.strftime("%Y%m%d")
    )

    year_value = current_date.year

    month_value = current_date.month

    day_value = current_date.day

    quarter_value = (
        (month_value - 1) // 3
    ) + 1

    week_of_year = int(
        current_date.strftime("%U")
    )

    day_of_week = current_date.isoweekday()

    day_name = current_date.strftime("%A")

    month_name = current_date.strftime("%B")

    is_weekend = (
        day_of_week in [6, 7]
    )

    is_month_start = (
        day_value == 1
    )

    next_day = current_date + timedelta(days=1)

    is_month_end = (
        next_day.month != month_value
    )

    date_rows.append(

        Row(

            date_sk=date_sk,

            full_date=current_date,

            year=year_value,

            quarter=quarter_value,

            month=month_value,

            month_name=month_name,

            week_of_year=week_of_year,

            day=day_value,

            day_of_week=day_of_week,

            day_name=day_name,

            is_weekend=is_weekend,

            is_month_start=is_month_start,

            is_month_end=is_month_end,

            year_month=f"{year_value}-{month_value:02d}",

            quarter_label=f"Q{quarter_value}",

            source_system=SOURCE_SYSTEM,

            transformation_version=TRANSFORMATION_VERSION
        )
    )

    current_date += timedelta(days=1)


# =========================================================
# CREATE DATAFRAME
# =========================================================

dim_date_df = spark.createDataFrame(
    date_rows
)

print(
    f"Generated Date Rows: "
    f"{dim_date_df.count()}"
)


# =========================================================
# ADD AUDIT METADATA
# =========================================================

dim_date_df = dim_date_df.withColumn(
    "gold_loaded_at",
    current_timestamp()
)


# =========================================================
# FINAL COLUMN ORDER
# =========================================================

dim_date_df = dim_date_df.select(

    "date_sk",

    "full_date",

    "year",

    "quarter",

    "quarter_label",

    "month",

    "month_name",

    "year_month",

    "week_of_year",

    "day",

    "day_of_week",

    "day_name",

    "is_weekend",

    "is_month_start",

    "is_month_end",

    "source_system",

    "transformation_version",

    "gold_loaded_at"
)


# =========================================================
# RUN VALIDATIONS
# =========================================================

print("\n=================================================")
print("RUNNING DIM DATE VALIDATIONS")
print("=================================================")

run_dim_date_validation(
    dim_date_df
)


# =========================================================
# WRITE DIMENSION
# =========================================================

print("\n=================================================")
print("WRITING DIM DATE")
print("=================================================")

dim_date_df.coalesce(1).write.mode(
    "overwrite"
).parquet(
    DIM_DATE_PATH
)

print("dim_date Written Successfully")


# =========================================================
# FINAL SUMMARY
# =========================================================

print("\n=================================================")
print("DIM DATE BUILD COMPLETED")
print("=================================================")

print(f"Final Row Count: {dim_date_df.count()}")

dim_date_df.printSchema()

spark.stop()