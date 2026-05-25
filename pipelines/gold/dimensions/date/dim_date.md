# `dim_date.md`

````markdown id="v8m2pk"
# Date Dimension (`dim_date`)

## Objective

The `dim_date` table is the conformed temporal dimension of the Olist Seller Intelligence Platform.

This dimension provides:

- standardized calendar intelligence
- reusable time hierarchies
- temporal analytical consistency
- shared date semantics across all fact tables

It acts as:

# the central temporal reference layer

for:

- operational analytics
- sales analytics
- delivery analytics
- customer behavior analytics
- seller performance analytics
- streaming trend analysis

inside the Gold warehouse architecture.

---

# Architectural Role

The `dim_date` table is:

# a conformed dimension

meaning:
it is reused consistently across multiple fact tables.

---

# Fact Tables Using `dim_date`

| Fact Table             | Date Usage                     |
| ---------------------- | ------------------------------ |
| fct_order_delivery     | purchase / delivery dates      |
| fct_order_sales        | sales transaction dates        |
| fct_order_payments     | payment lifecycle dates        |
| fct_customer_reviews   | review creation dates          |
| fct_seller_acquisition | conversion lifecycle dates     |
| fct_seller_fulfillment | fulfillment event dates        |
| fct_seller_performance | monthly behavioral aggregation |

This creates:

# temporal analytical consistency

across the entire warehouse.

---

# Dataset Grain

# ONE ROW = ONE CALENDAR DATE

Each row represents:

- one unique calendar day
- enriched with temporal attributes
- optimized for analytical grouping and filtering

This grain is strictly preserved.

---

# Why `dim_date` Exists

Fact tables should NOT repeatedly calculate:

- month names
- quarters
- weekends
- temporal hierarchies
- calendar logic

Instead:
the warehouse centralizes:

# reusable calendar intelligence

inside:

```text id="x4z9tp"
dim_date
```
````

This improves:

- performance
- consistency
- semantic clarity
- BI usability
- analytical governance

---

# Gold Layer Role

Inside the Gold architecture:

```text
Silver Staging
        ↓
Conformed Dimensions
        ↓
Fact Tables
        ↓
Business KPIs
        ↓
Dashboards & Analytics
```

`dim_date` is one of the MOST important conformed dimensions because:

# every business process is time-dependent

---

# Dimension Type

# Static Conformed Dimension

Characteristics:

- low volatility
- deterministic generation
- reusable across all marts
- no dependency on transactional data

Unlike:

- seller dimensions
- customer dimensions

the date dimension is:

# system-generated intelligence

rather than business-entity enrichment.

---

# Date Range

## Configured Range

| Start Date | End Date   |
| ---------- | ---------- |
| 2015-01-01 | 2020-12-31 |

---

# Why This Range Was Selected

The range was chosen to:

- fully cover the Olist operational timeline
- support historical trend analysis
- support future-safe analytical windows
- avoid temporal gaps in fact relationships

This ensures:

# complete warehouse temporal coverage

for all:

- facts
- KPIs
- dashboards
- streaming baselines

---

# Key Responsibilities

The `dim_date` dimension is responsible for:

| Responsibility                | Purpose                       |
| ----------------------------- | ----------------------------- |
| Calendar standardization      | shared temporal semantics     |
| Time hierarchy support        | drill-down analytics          |
| Weekend classification        | operational behavior analysis |
| Quarter aggregation           | executive reporting           |
| Monthly grouping              | trend analysis                |
| Temporal filtering            | dashboard slicing             |
| Surrogate key standardization | warehouse joins               |

---

# Surrogate Key Strategy

## Primary Key

```text id="t2m8vw"
date_sk
```

---

# Surrogate Key Format

```text id="u6x9qp"
YYYYMMDD
```

Example:

| Date       | date_sk  |
| ---------- | -------- |
| 2018-01-05 | 20180105 |
| 2019-12-31 | 20191231 |

---

# Why This Strategy Was Chosen

This approach:

- improves join performance
- simplifies partitioning
- supports BI tools efficiently
- follows warehouse best practices

It also creates:

# human-readable surrogate keys

which improves:

- debugging
- auditing
- warehouse transparency

---

# Temporal Attributes

The dimension contains multiple temporal intelligence attributes.

---

# 1. Year Intelligence

| Column | Purpose         |
| ------ | --------------- |
| year   | annual analysis |

Supports:

- yearly trends
- YoY comparisons
- executive reporting

---

# 2. Quarter Intelligence

| Column        | Purpose                   |
| ------------- | ------------------------- |
| quarter       | quarterly aggregation     |
| quarter_label | business-friendly display |

Supports:

- quarterly KPIs
- executive dashboards
- trend segmentation

---

# 3. Month Intelligence

| Column     | Purpose          |
| ---------- | ---------------- |
| month      | numeric month    |
| month_name | readable month   |
| year_month | monthly grouping |

Supports:

- monthly analytics
- seasonal analysis
- trend reporting

---

# 4. Weekly Intelligence

| Column       | Purpose            |
| ------------ | ------------------ |
| week_of_year | weekly aggregation |

Supports:

- operational monitoring
- short-term trend analysis
- weekly KPI tracking

---

# 5. Day Intelligence

| Column      | Purpose          |
| ----------- | ---------------- |
| day         | day-of-month     |
| day_of_week | weekday number   |
| day_name    | readable weekday |

Supports:

- weekday behavior analysis
- operational workload trends
- customer behavioral analysis

---

# 6. Weekend Intelligence

| Column     | Purpose                  |
| ---------- | ------------------------ |
| is_weekend | operational segmentation |

Supports:

- weekend sales analysis
- logistics behavior analysis
- customer shopping pattern analysis

---

# 7. Month Boundary Intelligence

| Column         | Purpose                |
| -------------- | ---------------------- |
| is_month_start | financial period logic |
| is_month_end   | reporting cutoff logic |

Supports:

- financial closing analysis
- monthly KPI calculations
- reporting automation

---

# Final Schema

| Column                 | Datatype  | Description         |
| ---------------------- | --------- | ------------------- |
| date_sk                | integer   | Surrogate date key  |
| full_date              | date      | Full calendar date  |
| year                   | integer   | Calendar year       |
| quarter                | integer   | Calendar quarter    |
| quarter_label          | string    | Quarter label       |
| month                  | integer   | Calendar month      |
| month_name             | string    | Month name          |
| year_month             | string    | YYYY-MM format      |
| week_of_year           | integer   | Week number         |
| day                    | integer   | Day of month        |
| day_of_week            | integer   | ISO weekday number  |
| day_name               | string    | Weekday name        |
| is_weekend             | boolean   | Weekend indicator   |
| is_month_start         | boolean   | Month-start flag    |
| is_month_end           | boolean   | Month-end flag      |
| source_system          | string    | Source metadata     |
| transformation_version | string    | Pipeline version    |
| gold_loaded_at         | timestamp | Gold load timestamp |

---

# Validation Strategy

The dimension includes enterprise-style validation checks.

| Validation Type          | Purpose                  |
| ------------------------ | ------------------------ |
| Primary key validation   | duplicate prevention     |
| Critical null validation | dimensional completeness |
| Date-range validation    | temporal coverage        |
| Weekend validation       | calendar correctness     |
| Month validation         | hierarchy correctness    |

This follows the platform’s:

# validation-driven warehouse engineering strategy

used across:

- Silver
- Gold
- marts
- streaming baselines

---

# Weekend Logic

Weekend classification uses:

| Day           | Weekend |
| ------------- | ------- |
| Saturday      | TRUE    |
| Sunday        | TRUE    |
| Monday–Friday | FALSE   |

This enables:

# operational time segmentation

for:

- logistics analysis
- workload analysis
- customer shopping behavior

---

# Month-End Logic

Month-end detection is calculated dynamically.

Example:

| Date       | is_month_end |
| ---------- | ------------ |
| 2018-01-31 | TRUE         |
| 2018-02-15 | FALSE        |

This supports:

# financial and operational period analysis

---

# Conformed Dimension Significance

The `dim_date` table is:

# shared across all analytical domains

This means:

- delivery analytics
- sales analytics
- reviews analytics
- acquisition analytics
- streaming analytics

all interpret time:

# consistently

This is one of the MOST important principles in:

# Kimball dimensional modeling.

---

# Architectural Significance

The `dim_date` dimension represents:

# centralized temporal intelligence

inside the warehouse architecture.

Unlike:

- transactional facts
- operational staging datasets

this dimension provides:

# reusable semantic calendar context

used throughout the analytical ecosystem.

This separation is architecturally critical because:

- facts measure events
- dimensions provide context

This follows:

# star-schema modeling principles

and:

# enterprise data warehouse architecture practices.

---

# Operational Intelligence Enabled

This dimension supports:

| Capability                 | Enabled |
| -------------------------- | ------- |
| time-series analytics      | YES     |
| trend analysis             | YES     |
| executive reporting        | YES     |
| quarterly KPIs             | YES     |
| operational monitoring     | YES     |
| seasonal analysis          | YES     |
| streaming trend comparison | YES     |

---

# Business Narrative Contribution

The `dim_date` dimension enables:

# time-aware business intelligence

across the platform.

Without:

```text id="z3v9qt"
dim_date
```

the warehouse would lack:

- temporal consistency
- reusable hierarchies
- unified calendar semantics
- enterprise analytical governance

This dimension therefore acts as:

# the temporal backbone of the warehouse.

---

# Gold Layer Readiness

The dimension is fully prepared for:

- star-schema joins
- surrogate-key lookups
- BI semantic modeling
- dbt lineage
- Power BI dashboards
- streaming trend analysis
- executive KPI reporting

with:

# FULL TEMPORAL CONSISTENCY

# CONFORMED DIMENSION GOVERNANCE

# STAR-SCHEMA READINESS

# ENTERPRISE CALENDAR INTELLIGENCE

```

```
