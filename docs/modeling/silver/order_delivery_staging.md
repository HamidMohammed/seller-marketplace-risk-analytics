# `order_delivery_staging`

## Objective

The `order_delivery_staging` dataset represents the trusted order-level delivery intelligence staging layer inside the Olist Seller Intelligence Platform.

This staging entity assembles:

# operational delivery lifecycle intelligence

by combining:

- trusted order lifecycle data
- seller fulfillment aggregations
- geographic enrichment
- logistics classification metrics

into:

# ONE ORDER-LEVEL DELIVERY STAGING ENTITY

used as the direct upstream source for:

```text
fct_order_delivery
```

The dataset acts as:

# the operational delivery intelligence bridge

between:

- Silver operational entities
  and:
- Gold delivery marts.

---

# Dataset Role in Architecture

```text
silver_orders
        +
silver_order_items
        +
silver_sellers
        +
silver_customers
                ↓
order_delivery_staging
                ↓
fct_order_delivery
                ↓
Delivery KPIs + Streaming Intelligence
```

This staging layer centralizes:

- delivery lifecycle metrics
- seller accountability enrichment
- freight aggregations
- geographic delivery intelligence

while preserving:

# order-level analytical integrity.

---

# Dataset Grain

# ONE ROW = ONE CUSTOMER ORDER

This grain is strictly preserved throughout all transformations.

This is CRITICAL because:

- delivery KPIs are order-level
- customer satisfaction analysis is order-level
- streaming delivery risk operates at order-level
- duplicate orders corrupt delivery analytics

---

# Source Datasets

| Source Dataset     | Layer  | Purpose                         |
| ------------------ | ------ | ------------------------------- |
| silver_orders      | Silver | Delivery lifecycle intelligence |
| silver_order_items | Silver | Seller fulfillment enrichment   |
| silver_sellers     | Silver | Seller geography                |
| silver_customers   | Silver | Customer geography              |

---

# Architectural Purpose

The purpose of this staging entity is:

# controlled operational enrichment

NOT:

# final dimensional modeling.

This layer intentionally:

- preserves modular architecture
- isolates delivery preparation logic
- prevents repeated enrichment logic
- protects Gold fact-table simplicity

---

# Transformations Applied

---

# 1. Order-Level Aggregation

## Transformation

```python
groupBy("order_id")
```

---

## Purpose

Transforms:

# seller-item grain

into:

# order-level operational enrichment

required for:

- delivery KPI calculations
- order-level accountability
- customer delivery analytics

---

# 2. Freight Aggregation

## Derived Column

```text
freight_total_value
```

---

## Formula

```python
sum(freight_value)
```

---

## Business Meaning

Measures:

# total freight charged across all order items

inside one customer order.

---

## Business Value

Supports:

- logistics burden analysis
- freight cost monitoring
- operational profitability analysis

---

# 3. Total Items Count

## Derived Column

```text
total_items_count
```

---

## Formula

```python
count(order_item_id)
```

---

## Business Meaning

Measures:

# number of purchased items inside order

---

## Business Value

Supports:

- fulfillment complexity analysis
- shipment workload investigation
- oversized-order segmentation

---

# 4. Seller Count

## Derived Column

```text
seller_count
```

---

## Formula

```python
countDistinct(seller_id)
```

---

## Business Meaning

Measures:

# number of sellers participating in order

---

## Business Importance

This is one of the MOST important operational governance metrics because:
multi-seller orders create:

# ambiguous accountability.

This metric protects:

- review attribution
- seller KPI integrity
- delivery accountability logic

---

# 5. Primary Seller Attribution

## Derived Column

```text
primary_seller_id
```

---

## Formula

```python
first(seller_id)
```

---

## Important Modeling Decision

This field is:

# analytically reliable ONLY for single-seller orders.

Gold marts may safely filter:

```text
seller_count = 1
```

to preserve:

- seller accountability
- KPI correctness
- review attribution integrity

---

# 6. Multi-Seller Flag

## Derived Column

```text
is_multi_seller_order
```

---

## Logic

```python
seller_count > 1
```

---

## Business Purpose

Provides:

# simplified accountability classification

Used for:

- operational filtering
- KPI governance
- seller attribution protection

---

# 7. Geographic Enrichment

## Seller Geography

Enriched Columns:

| Column       |
| ------------ |
| seller_state |
| seller_lat   |
| seller_lng   |

---

## Customer Geography

Enriched Columns:

| Column         |
| -------------- |
| customer_state |
| customer_lat   |
| customer_lng   |

---

## Purpose

Supports:

- logistics-distance analysis
- regional delivery monitoring
- operational geography intelligence

---

# 8. Distance Bucket Classification

## Derived Column

```text
distance_bucket
```

---

## Logic

| Condition                     | Bucket       |
| ----------------------------- | ------------ |
| seller_state = customer_state | Same State   |
| both inside Southeast region  | Same Region  |
| missing geography             | Unknown      |
| otherwise                     | Cross Region |

---

## Business Meaning

Provides:

# explainable delivery-distance classification

without:

- expensive geospatial processing
- unrealistic routing assumptions

---

## Business Value

Supports:

- delivery delay analysis
- regional logistics monitoring
- freight burden investigation
- operational segmentation

---

# 9. Buffer Days Metric

## Derived Column

```text
buffer_days
```

---

## Formula

```python
estimated_delivery_date
-
purchase_timestamp
```

---

## Business Meaning

Measures:

# promised delivery window size

defined by Olist logistics planning.

---

## Business Value

Supports:

- unrealistic promise detection
- logistics benchmarking
- delivery-padding analysis

---

# 10. Metadata Enrichment

## Added Columns

| Column                 | Purpose         |
| ---------------------- | --------------- |
| silver_loaded_at       | lineage         |
| source_system          | traceability    |
| transformation_version | reproducibility |

---

# Validation Framework

The dataset follows:

# validation-driven transformation engineering

Every transformation is validated BEFORE Gold consumption.

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

```python
validate_duplicates(["order_id"])
```

---

## Purpose

Protect:

- delivery KPIs
- streaming logic
- downstream fact integrity

---

# 2. Lifecycle Validation

## Rules

| Rule                  | Meaning                  |
| --------------------- | ------------------------ |
| purchase <= approval  | valid payment lifecycle  |
| purchase <= delivered | valid delivery lifecycle |

---

## Business Importance

Prevents:

- impossible operational timelines
- corrupted delivery metrics
- invalid delay calculations

---

# 3. Delivered Order Validation

## Rule

```text
Delivered orders must contain delivery timestamp
```

---

## Purpose

Protect:

- delivery duration metrics
- delay intelligence
- operational correctness

---

# 4. Delivery Metrics Validation

## Validations

| Validation                  | Purpose                    |
| --------------------------- | -------------------------- |
| delivery_duration_days >= 0 | lifecycle correctness      |
| extreme delays monitored    | anomaly detection          |
| buffer_days >= 0            | promise-window correctness |

---

# 5. Seller Accountability Validation

## Rules

| Rule                                        | Purpose                  |
| ------------------------------------------- | ------------------------ |
| seller_count >= 1                           | accountability integrity |
| single-seller orders require primary seller | attribution correctness  |

---

# 6. Geographic Validation

## Validations

| Validation                   | Purpose                      |
| ---------------------------- | ---------------------------- |
| seller_state availability    | logistics enrichment quality |
| customer_state availability  | delivery-region analysis     |
| valid distance_bucket values | KPI consistency              |

---

# Important Architectural Decisions

---

# Controlled Operational Enrichment

This staging layer intentionally centralizes:

- order-level delivery metrics
- seller enrichment
- geography enrichment

BEFORE:
Gold fact modeling.

This prevents:

- duplicated enrichment logic
- repeated aggregation logic
- inconsistent delivery KPIs

---

# No Silent Data Loss

The pipeline follows:

# zero silent data-loss policy

Records may only be excluded when:

- explicitly documented
- business justified
- validation verified

---

# Operational Truth Preservation

The dataset intentionally preserves:

# operational anomalies

when they represent:

- logistics failures
- delayed deliveries
- geographic complexity
- seller accountability ambiguity

Examples:

| Pattern             | Meaning                  |
| ------------------- | ------------------------ |
| extreme delays      | operational bottlenecks  |
| multi-seller orders | accountability ambiguity |
| missing geography   | enrichment limitation    |
| large buffer_days   | logistics padding        |

The project avoids:

# over-cleaning operational truth

because operational anomalies themselves contain:

# business intelligence.

---

# Gold Layer Dependencies

This dataset directly feeds:

| Gold Entity          | Purpose                  |
| -------------------- | ------------------------ |
| fct_order_delivery   | delivery KPIs            |
| seller risk scoring  | operational intelligence |
| streaming enrichment | alert prioritization     |
| Power BI dashboards  | delivery storytelling    |

---

# Business Questions Supported

This staging entity enables:

- Which regions experience worst delivery delays?
- Do multi-seller orders delay deliveries?
- Which sellers create highest freight burden?
- Does geographic distance increase delivery risk?
- Are unrealistic delivery promises causing delays?
- Which delivery patterns predict dissatisfaction?

---

# Strategic Architectural Value

This dataset demonstrates:

# enterprise-grade operational staging design

through:

- controlled enrichment
- grain preservation
- accountability governance
- delivery intelligence preparation
- validation-driven engineering

It acts as:

# the operational foundation

for:

- delivery intelligence
- seller performance monitoring
- customer experience analytics
- streaming operational alerting
