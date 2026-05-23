# `dim_date.md`

## Objective

The `dim_date` dimension provides standardized calendar intelligence across all marts and analytical layers. It enables:

- time-series analytics
- trend analysis
- seasonality analysis
- delivery timeline tracking
- KPI aggregation by time periods

The warehouse follows Kimball dimensional modeling principles where:

- facts store measurable events
- dimensions provide descriptive business context

---

# Business Purpose

`dim_date` centralizes all calendar-related attributes into one reusable conformed dimension.

Used for:

- monthly delivery trends
- seller growth analysis
- operational KPI tracking
- review activity analysis
- streaming event enrichment
- Power BI time intelligence

Without a dedicated date dimension:

- dashboard filtering becomes inconsistent
- repeated date calculations appear everywhere
- fiscal and calendar grouping becomes difficult

Professional warehouses do not rely directly on raw timestamps for analytics.

---

# Grain

# One Row = One Calendar Date

Example:

| date_sk  | full_date  |
| -------- | ---------- |
| 20170115 | 2017-01-15 |
| 20170116 | 2017-01-16 |

---

# Table Name

```sql
dim_date
```

---

# Primary Key

```sql
date_sk
```

Format:

```text
YYYYMMDD
```

Example:

```text
20180325
```

---

# Schema Design

| Column Name    | Datatype | Description                   |
| -------------- | -------- | ----------------------------- |
| date_sk        | INT      | Surrogate date key (YYYYMMDD) |
| full_date      | DATE     | Full calendar date            |
| day_number     | SMALLINT | Day of month                  |
| day_name       | VARCHAR  | Monday, Tuesday, etc.         |
| week_number    | SMALLINT | Week of year                  |
| month_number   | SMALLINT | Month number                  |
| month_name     | VARCHAR  | January, February, etc.       |
| quarter_number | SMALLINT | Quarter number                |
| year_number    | SMALLINT | Calendar year                 |
| is_weekend     | BOOLEAN  | Weekend indicator             |
| is_month_start | BOOLEAN  | First day of month            |
| is_month_end   | BOOLEAN  | Last day of month             |

Schema aligned with the dimensional modeling strategy documentation.

---

# Example Record

| Column         | Example    |
| -------------- | ---------- |
| date_sk        | 20180115   |
| full_date      | 2018-01-15 |
| day_number     | 15         |
| day_name       | Monday     |
| week_number    | 3          |
| month_number   | 1          |
| month_name     | January    |
| quarter_number | 1          |
| year_number    | 2018       |
| is_weekend     | False      |
| is_month_start | False      |
| is_month_end   | False      |

---

# Role-Playing Dimension Strategy

The same `dim_date` table is reused multiple times across facts using:

# role-playing dimensions

Examples:

| Foreign Key                | Business Meaning         |
| -------------------------- | ------------------------ |
| purchase_date_sk           | Order purchase date      |
| estimated_delivery_date_sk | Promised delivery date   |
| actual_delivery_date_sk    | Final delivery date      |
| shipping_limit_date_sk     | Seller shipment deadline |
| review_creation_date_sk    | Customer review date     |

This avoids:

- duplicated date dimensions
- inconsistent calendar logic
- unnecessary storage overhead

This is a standard enterprise dimensional modeling pattern.

---

# Relationships

| Fact Table             | Foreign Key                |
| ---------------------- | -------------------------- |
| fct_order_delivery     | purchase_date_sk           |
| fct_order_delivery     | estimated_delivery_date_sk |
| fct_order_delivery     | actual_delivery_date_sk    |
| fct_seller_fulfillment | shipping_limit_date_sk     |
| fct_customer_review    | review_creation_date_sk    |

---

# Data Generation Strategy

The dimension is generated programmatically using Python during warehouse initialization.

Date range:

```text
2016-01-01 → 2019-12-31
```

This fully covers:

- historical Olist transactions
- future buffer dates
- streaming replay timelines

---

# ETL Logic

## Source

Generated internally — not sourced from raw Olist CSV files.

## Transformation Logic

Derived attributes:

- weekday names
- month names
- quarter calculations
- weekend flags
- month boundary indicators

## Load Frequency

```text
One-time initialization load
```

---

# Data Quality Rules

| Rule                 | Validation                 |
| -------------------- | -------------------------- |
| Unique dates         | No duplicate date_sk       |
| Valid calendar dates | No invalid generated dates |
| Non-null primary key | date_sk required           |
| Continuous timeline  | No missing calendar days   |

---

# Best Practices Applied

| Best Practice                    | Applied |
| -------------------------------- | ------- |
| Kimball conformed dimension      | Yes     |
| Role-playing dimension           | Yes     |
| Surrogate key strategy           | Yes     |
| Reusable across marts            | Yes     |
| Power BI optimization            | Yes     |
| Standardized calendar attributes | Yes     |

---

# Architectural Importance

`dim_date` acts as:

# the temporal backbone of the warehouse

It guarantees:

- consistent analytics
- reusable time intelligence
- scalable dashboard filtering
- clean star-schema joins
- enterprise-grade dimensional consistency

It is shared across:

- batch marts
- streaming enrichment
- Power BI dashboards
- operational KPIs
- seller intelligence analytics.
