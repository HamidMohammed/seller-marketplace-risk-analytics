# `silver_orders.md`

## Objective

The `silver_orders` dataset represents the trusted operational lifecycle layer for customer orders inside the Olist Seller Intelligence Platform.

This dataset transforms:

# raw operational order events

into:

# validated analytical lifecycle intelligence

used by:

- delivery marts
- seller fulfillment analytics
- customer review analytics
- sales intelligence
- streaming enrichment
- KPI reporting

The Silver dataset acts as:

# the operational truth foundation

for all downstream analytical processes.

---

# Dataset Role in Architecture

```text
Bronze Orders
        ↓
silver_orders
        ↓
Gold Fact Tables
        ↓
Dashboards & Streaming Intelligence
```

This dataset is one of the MOST important entities in the entire warehouse because it governs:

- order lifecycle truth
- delivery timing intelligence
- delivery KPI consistency
- operational process validation

---

# Dataset Grain

# ONE ROW = ONE CUSTOMER ORDER

This grain is strictly preserved throughout all transformations.

Grain preservation is critical because:

- delivery KPIs depend on unique orders
- duplicate orders corrupt business metrics
- downstream marts assume order-level integrity

---

# Source Dataset

| Source Dataset | Layer  | Purpose                         |
| -------------- | ------ | ------------------------------- |
| bronze/orders  | Bronze | Raw operational order lifecycle |

---

# Source Columns

| Column                        | Meaning                            |
| ----------------------------- | ---------------------------------- |
| order_id                      | Unique customer order identifier   |
| customer_id                   | Customer business identifier       |
| order_status                  | Operational order lifecycle status |
| order_purchase_timestamp      | Customer purchase timestamp        |
| order_approved_at             | Payment approval timestamp         |
| order_delivered_carrier_date  | Carrier pickup timestamp           |
| order_delivered_customer_date | Customer delivery timestamp        |
| order_estimated_delivery_date | Promised delivery date             |

---

# Silver Responsibilities

The `silver_orders` pipeline is responsible for:

| Responsibility             | Purpose                    |
| -------------------------- | -------------------------- |
| Timestamp standardization  | Lifecycle analytics        |
| Status normalization       | KPI consistency            |
| Delivery metric derivation | Operational intelligence   |
| Lifecycle validation       | Business-process integrity |
| Metadata enrichment        | Traceability               |
| Analytical preparation     | Gold-layer readiness       |

---

# Transformations Applied

---

# 1. Order Status Standardization

## Transformation

```python id="r2xw4p"
lower(trim(order_status))
```

---

## Purpose

Operational datasets may contain:

- casing inconsistencies
- whitespace inconsistencies

Standardization ensures:

- reliable grouping
- KPI consistency
- dashboard stability

---

# 2. Timestamp Casting

## Transformed Columns

| Column                        |
| ----------------------------- |
| order_purchase_timestamp      |
| order_approved_at             |
| order_delivered_carrier_date  |
| order_delivered_customer_date |
| order_estimated_delivery_date |

---

## Transformation

```python id="v8px5q"
to_timestamp(column)
```

---

## Purpose

Timestamp casting enables:

- lifecycle validation
- duration calculations
- delivery intelligence
- streaming event processing

Without timestamp standardization:
delivery KPIs become unreliable.

---

# 3. Delivery Duration Metric

## Derived Column

```text
delivery_duration_days
```

---

## Formula

```python id="wz7m8n"
datediff(
    order_delivered_customer_date,
    order_purchase_timestamp
)
```

---

## Business Meaning

Measures:

# full customer delivery duration

from:

- purchase event
  to:
- final customer delivery

---

## Business Value

Supports:

- delivery efficiency analysis
- seller operational benchmarking
- logistics performance monitoring

---

# 4. Delay Days Metric

## Derived Column

```text
delay_days
```

---

## Formula

```python id="mx9p3r"
datediff(
    order_delivered_customer_date,
    order_estimated_delivery_date
)
```

---

## Interpretation

| Value    | Meaning          |
| -------- | ---------------- |
| Positive | Late delivery    |
| Zero     | On-time delivery |
| Negative | Early delivery   |

---

## Business Value

This is one of the MOST important operational KPIs in the entire platform.

Used for:

- seller risk analysis
- delivery performance analytics
- customer satisfaction analysis
- operational alerting

---

# 5. Estimated Delivery Window

## Derived Column

```text
estimated_delivery_window_days
```

---

## Formula

```python id="py3m7s"
datediff(
    order_estimated_delivery_date,
    order_purchase_timestamp
)
```

---

## Business Meaning

Measures:

# promised delivery window length

defined by:

- Olist logistics expectations
- operational delivery commitments

---

## Business Value

Supports:

- logistics planning analysis
- unrealistic promise detection
- operational benchmarking

---

# 6. Delivery Status Classification

## Derived Column

```text
delivery_status_category
```

---

## Logic

| Condition      | Category |
| -------------- | -------- |
| delay_days > 0 | Late     |
| delay_days = 0 | On Time  |
| delay_days < 0 | Early    |
| otherwise      | Unknown  |

---

## Business Value

This transformation enables:

- business-friendly dashboards
- executive KPI reporting
- delivery segmentation

without recalculating logic repeatedly downstream.

---

# 7. Delivery Success Flag

## Derived Column

```text
is_successfully_delivered
```

---

## Logic

```python id="e3pz2f"
order_status == "delivered"
```

---

## Business Purpose

Provides:

# simplified operational completion indicator

Used for:

- filtering delivery marts
- KPI calculations
- streaming prioritization

---

# 8. Metadata Enrichment

## Added Columns

| Column                 | Purpose          |
| ---------------------- | ---------------- |
| silver_loaded_at       | pipeline lineage |
| source_system          | traceability     |
| transformation_version | reproducibility  |

---

# Validation Framework

The dataset follows:

# validation-driven engineering

All transformations are validated BEFORE Silver output generation.

---

# Validation Rules

---

# 1. Grain Validation

## Rule

```text
ONE ROW = ONE ORDER
```

---

## Validation

```python id="a5n2pw"
validate_duplicates(order_id)
```

---

## Purpose

Protect:

- delivery KPIs
- lifecycle metrics
- downstream fact integrity

---

# 2. Critical Null Validation

## Critical Columns

| Column                   | Reason           |
| ------------------------ | ---------------- |
| order_id                 | business key     |
| customer_id              | customer linkage |
| order_purchase_timestamp | lifecycle start  |
| order_status             | KPI grouping     |

---

## Purpose

Protect:

- operational integrity
- analytical consistency
- downstream joins

---

# 3. Lifecycle Validation

The pipeline validates:

# chronological business-process correctness

---

## Validation Rules

| Rule                 | Meaning                  |
| -------------------- | ------------------------ |
| purchase <= approval | valid payment lifecycle  |
| approval <= delivery | valid delivery lifecycle |

---

## Business Importance

Prevents:

- impossible delivery timelines
- corrupted KPIs
- negative lifecycle calculations

This is:

# operational truth validation

NOT simple data cleaning.

---

# 4. Delivered Orders Validation

## Rule

```text
Delivered orders must contain delivery timestamp
```

---

## Purpose

Protect:

- delivery duration metrics
- delay calculations
- customer delivery intelligence

---

# 5. Delivery Metrics Validation

## Validations

| Validation                 | Purpose              |
| -------------------------- | -------------------- |
| negative delivery duration | impossible lifecycle |
| extreme delays             | anomaly monitoring   |

---

# Important Architectural Decisions

---

# Operational Truth Preservation

The pipeline intentionally preserves:

# operational anomalies

when they represent:

- logistics failures
- seller delays
- customer-impacting issues

Example:

| Data Pattern          | Interpretation          |
| --------------------- | ----------------------- |
| missing delivery date | incomplete fulfillment  |
| long delays           | operational bottleneck  |
| missing approval      | payment lifecycle issue |

The project avoids:

# aggressive over-cleaning

because operational anomalies themselves contain:

# business intelligence.

---

# No Silent Record Deletion

The pipeline follows:

# zero silent data-loss policy

Meaning:
records may only be excluded when:

- documented
- validated
- business justified

---

# Gold Layer Dependencies

The following marts consume:

# silver_orders

| Gold Dataset           | Dependency Purpose        |
| ---------------------- | ------------------------- |
| fct_order_delivery     | delivery lifecycle        |
| fct_order_sales        | order enrichment          |
| fct_customer_reviews   | review linkage            |
| fct_order_payments     | payment lifecycle         |
| fct_seller_fulfillment | seller operational timing |

This makes:
`silver_orders`
a:

# conformed operational foundation dataset

across the warehouse.

---

# Streaming Architecture Role

`silver_orders`
acts as:

# operational event intelligence layer

for streaming systems.

Streaming systems can monitor:

- delayed deliveries
- lifecycle bottlenecks
- seller operational failures
- delivery-risk escalation

using trusted Silver-derived metrics.

---

# Data Quality Governance

The dataset follows:

# validation-driven transformation governance

defined in:

```text
silver_transformation_strategy.md
```

The pipeline guarantees:

- grain preservation
- lifecycle integrity
- reproducibility
- KPI trustworthiness
- controlled transformations

---

# Output Dataset Location

```text
data/silver/orders/
```

Stored as:

# parquet

for:

- efficient analytics
- Spark optimization
- scalable warehouse ingestion

---

# Final Architectural Value

The `silver_orders` dataset transforms:

# raw operational order events

into:

# validated operational lifecycle intelligence

through:

- timestamp engineering
- lifecycle validation
- business-rule enforcement
- KPI-safe metric derivation
- operational anomaly preservation

This dataset establishes:

# trusted analytical order truth

for:

- dimensional modeling
- fact mart construction
- delivery intelligence
- seller-risk analytics
- streaming operational monitoring

and acts as:

# the operational backbone

of the Olist Seller Intelligence Platform.
