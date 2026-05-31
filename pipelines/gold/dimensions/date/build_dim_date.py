"""
build_dim_date.py

Gold Layer

Conformed Date Dimension

Objective:
Create a reusable enterprise-grade
date dimension used across all
fact tables.

Grain:
ONE ROW = ONE CALENDAR DATE
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

from datetime import (
    datetime,
    timedelta
)

from pyspark.sql import SparkSession

from pyspark.sql import Row

from pyspark.sql.types import (
    IntegerType
)

from pyspark.sql.functions import (
    current_timestamp,
    lit,
    col
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

# =========================================================
# METADATA
# =========================================================

SOURCE_SYSTEM = "OLIST"

TRANSFORMATION_VERSION = "1.0"

# =========================================================
# DATE RANGE
# =========================================================

START_DATE = datetime(
    2015,
    1,
    1
)

END_DATE = datetime(
    2020,
    12,
    31
)

# =========================================================
# BUILD DATE ROWS
# =========================================================

date_rows = []

current_date = START_DATE

while current_date <= END_DATE:

    date_sk = int(
        current_date.strftime(
            "%Y%m%d"
        )
    )

    year_value = current_date.year

    month_value = current_date.month

    quarter_value = (
        (month_value - 1) // 3
    ) + 1

    day_value = current_date.day

    day_name = current_date.strftime(
        "%A"
    )

    month_name = current_date.strftime(
        "%B"
    )

    week_of_year = int(
        current_date.strftime(
            "%U"
        )
    )

    day_of_year = int(
        current_date.strftime(
            "%j"
        )
    )

    is_weekend = day_name in [
        "Saturday",
        "Sunday"
    ]

    is_business_day = (
        not is_weekend
    )

    day_type = (
        "Weekend"
        if is_weekend
        else "Business Day"
    )

    is_month_start = (
        day_value == 1
    )

    next_day = (
        current_date
        +
        timedelta(days=1)
    )

    is_month_end = (
        next_day.month
        !=
        current_date.month
    )

    is_quarter_start = (
        month_value in [1, 4, 7, 10]
        and
        day_value == 1
    )

    is_quarter_end = (
        (
            month_value in [3, 6, 9, 12]
        )
        and
        is_month_end
    )

    is_year_start = (
        month_value == 1
        and
        day_value == 1
    )

    is_year_end = (
        month_value == 12
        and
        day_value == 31
    )

    year_month = (
        f"{year_value}"
        f"-"
        f"{month_value:02d}"
    )

    month_key = (
        f"{month_value:02d}"
    )

    date_rows.append(

        Row(

            date_sk=date_sk,

            full_date=current_date.date(),

            year=year_value,

            quarter=quarter_value,

            month=month_value,

            month_key=month_key,

            month_name=month_name,

            year_month=year_month,

            week_of_year=week_of_year,

            day=day_value,

            day_of_year=day_of_year,

            day_name=day_name,

            is_weekend=is_weekend,

            is_business_day=is_business_day,

            day_type=day_type,

            is_month_start=is_month_start,

            is_month_end=is_month_end,

            is_quarter_start=is_quarter_start,

            is_quarter_end=is_quarter_end,

            is_year_start=is_year_start,

            is_year_end=is_year_end

        )

    )

    current_date += timedelta(
        days=1
    )

# =========================================================
# CREATE DATAFRAME
# =========================================================

dim_date_df = spark.createDataFrame(
    date_rows
)

# =========================================================
# DATA TYPE OPTIMIZATION
# =========================================================

from pyspark.sql.types import IntegerType

dim_date_df = (

    dim_date_df

    .withColumn(
        "date_sk",
        col("date_sk").cast(IntegerType())
    )

    .withColumn(
        "year",
        col("year").cast(IntegerType())
    )

    .withColumn(
        "quarter",
        col("quarter").cast(IntegerType())
    )

    .withColumn(
        "month",
        col("month").cast(IntegerType())
    )

    .withColumn(
        "week_of_year",
        col("week_of_year").cast(IntegerType())
    )

    .withColumn(
        "day",
        col("day").cast(IntegerType())
    )

    .withColumn(
        "day_of_year",
        col("day_of_year").cast(IntegerType())
    )

)
# =========================================================
# METADATA ENRICHMENT
# =========================================================

dim_date_df = (

    dim_date_df

    .withColumn(
        "gold_loaded_at",
        current_timestamp()
    )

    .withColumn(
        "source_system",
        lit(
            SOURCE_SYSTEM
        )
    )

    .withColumn(
        "transformation_version",
        lit(
            TRANSFORMATION_VERSION
        )
    )

)

# =========================================================
# FINAL COLUMN ORDER
# =========================================================

dim_date_df = dim_date_df.select(

    "date_sk",

    "full_date",

    "year",

    "quarter",

    "month",

    "month_key",

    "month_name",

    "year_month",

    "week_of_year",

    "day",

    "day_of_year",

    "day_name",

    "day_type",

    "is_weekend",

    "is_business_day",

    "is_month_start",

    "is_month_end",

    "is_quarter_start",

    "is_quarter_end",

    "is_year_start",

    "is_year_end",

    "gold_loaded_at",

    "source_system",

    "transformation_version"

)

# =========================================================
# RUN VALIDATION
# =========================================================

run_dim_date_validation(
    dim_date_df
)

# =========================================================
# PREVIEW
# =========================================================

print("\n=================================================")
print("DIM DATE PREVIEW")
print("=================================================")

dim_date_df.show(
    10,
    truncate=False
)

dim_date_df.printSchema()
# =========================================================
# WRITE DIMENSION
# =========================================================

print("\n=================================================")
print("WRITING DIM DATE")
print("=================================================")

dim_date_df.write \
    .mode("overwrite") \
    .parquet(
        DIM_DATE_PATH
    )

print(
    f"Dim Date Written To: "
    f"{DIM_DATE_PATH}"
)

# =========================================================
# FINAL SUMMARY
# =========================================================

print("\n=================================================")
print("DIM DATE BUILD COMPLETED")
print("=================================================")

print(
    f"Total Rows: "
    f"{dim_date_df.count()}"
)

# =========================================================
# STOP SPARK
# =========================================================

spark.stop()

