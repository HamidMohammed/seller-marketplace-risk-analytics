# `docs/modeling/silver/seller_fulfillment_staging.md`

````markdown id="f8m2vr"
# `seller_fulfillment_staging.md`

## Objective

The `seller_fulfillment_staging` dataset represents the trusted operational fulfillment intelligence staging layer inside the Olist Seller Intelligence Platform.

This dataset transforms:

# trusted seller item fulfillment events

into:

# workload-aware operational logistics intelligence

used by:

- `fct_seller_fulfillment`
- seller operational analytics
- workload segmentation
- logistics burden analysis
- freight intelligence
- seller risk scoring
- streaming enrichment

The staging dataset acts as:

# the seller operational fulfillment foundation

inside the warehouse architecture.

Unlike:

```text
order_delivery_staging
```
````

which represents:

# final customer delivery outcomes

this dataset represents:

# seller-side operational shipment responsibility

This distinction is architecturally critical and follows the platform’s:

# dual-fact logistics modeling strategy

where:

- customer delivery outcomes
- seller operational fulfillment

remain separated for analytical correctness and grain integrity.

---

# Dataset Role in Architecture

```text
Bronze Order Items
        ↓
silver_order_items
        ↓
seller_fulfillment_staging
        ↓
fct_seller_fulfillment
        ↓
Operational Dashboards & Streaming Intelligence
```

This dataset acts as:

# the operational enrichment bridge

between:

- Silver fulfillment events
- Gold seller fulfillment analytics

It introduces:

- seller geography enrichment
- workload intelligence
- operational pressure segmentation
- acquisition enrichment

without violating:

# seller-item grain integrity.

---

# Dataset Grain

# ONE ROW = ONE SELLER ITEM FULFILLMENT EVENT

Each row represents:

- one purchased item
- fulfilled by one seller
- inside one customer order

This grain is inherited directly from:

```text
silver_order_items
```

and remains strictly preserved throughout all transformations.

---

# Why Grain Preservation Matters

This dataset powers:

- seller workload analytics
- fulfillment pressure metrics
- freight intelligence
- seller accountability KPIs

If the grain were incorrectly aggregated:
the warehouse would suffer:

- duplicated fulfillment metrics
- invalid seller KPIs
- unreliable workload analysis
- incorrect logistics intelligence

This follows:

# Kimball dimensional modeling principles

and preserves:

# operational truth integrity.

---

# Source Datasets

| Source Dataset       | Layer  | Purpose                               |
| -------------------- | ------ | ------------------------------------- |
| `silver_order_items` | Silver | Seller fulfillment operational events |
| `silver_sellers`     | Silver | Seller enrichment and geography       |

---

# Core Business Purpose

The objective of this staging layer is to answer:

```text
How operationally overloaded are sellers,
and how does workload pressure affect
fulfillment performance?
```

This directly supports the platform’s core business narrative:

```text
Seller Operational Overload
        ↓
Fulfillment Pressure
        ↓
Delivery Failure
        ↓
Customer Dissatisfaction
```

The dataset therefore acts as:

# operational seller intelligence infrastructure

for downstream analytical marts and streaming systems.

---

# Seller Fulfillment vs Customer Delivery

One of the most important architectural discoveries in the project was:

# seller fulfillment

IS NOT

# customer delivery outcome

---

## Seller Fulfillment

Tracked in:

```text
olist_order_items_dataset
```

Represents:

- seller shipment preparation
- logistics responsibility
- shipping deadlines
- freight burden

Grain:

# item-level operational responsibility

---

## Customer Delivery Outcome

Tracked in:

```text
olist_orders_dataset
```

Represents:

- final customer delivery
- delivery promises
- actual delivery outcome
- customer delivery experience

Grain:

# order-level customer outcome

---

# Why This Separation Matters

Combining:

- fulfillment operations
- customer delivery outcomes

inside one fact table would create:

- mixed-grain corruption
- duplicated delivery metrics
- invalid seller attribution
- unreliable KPIs

To prevent this:
the architecture intentionally separates:

# fulfillment intelligence

from:

# customer delivery intelligence.

This is one of the strongest modeling decisions in the entire platform architecture.

---

# Silver Responsibilities

The `seller_fulfillment_staging` pipeline is responsible for:

| Responsibility                   | Purpose                       |
| -------------------------------- | ----------------------------- |
| seller geography enrichment      | logistics analysis            |
| workload intelligence derivation | operational pressure analysis |
| acquisition enrichment           | seller lifecycle intelligence |
| workload segmentation            | seller classification         |
| metadata enrichment              | lineage                       |
| grain preservation               | KPI integrity                 |
| staging preparation              | Gold fact readiness           |

---

# Transformations Applied

---

# 1. Seller Geography Enrichment

## Joined Dataset

```text
silver_sellers
```

---

## Added Attributes

| Column             | Purpose                         |
| ------------------ | ------------------------------- |
| seller_state       | geographic segmentation         |
| seller_lat         | logistics mapping               |
| seller_lng         | route analysis                  |
| acquisition_source | seller acquisition intelligence |

---

## Business Purpose

Enables:

- regional workload analysis
- logistics heatmaps
- seller clustering
- acquisition-performance analysis

This transformation also demonstrates:

# conformed dimension reuse

across multiple analytical domains.

---

# 2. Seller Monthly Workload Metric

## Derived Column

```text
seller_monthly_orders
```

---

## Logic

Monthly seller order volume is calculated using:

# window functions

partitioned by:

- seller_id
- purchase month
- purchase year

---

## Business Meaning

Measures:

# seller operational fulfillment pressure

inside a specific monthly operational window.

---

## Why This Metric Matters

This becomes one of the MOST important operational metrics in the platform because it enables:

- seller overload detection
- operational capacity analysis
- fulfillment pressure investigation
- risk scoring enrichment
- workload-performance correlation

This metric later supports:

# predictive operational intelligence.

---

# 3. Workload Bucket Classification

## Derived Column

```text
workload_bucket
```

---

## Classification Logic

| Monthly Orders | Bucket        |
| -------------- | ------------- |
| 0–20           | Low Volume    |
| 21–100         | Medium Volume |
| 101–500        | High Volume   |
| 500+           | Overloaded    |

---

## Business Purpose

Transforms:

# raw operational counts

into:

# interpretable operational segments

This allows:

- seller benchmarking
- workload comparisons
- dashboard segmentation
- operational pressure analysis

without requiring:

- repeated downstream calculations

---

# 4. Metadata Enrichment

## Added Columns

| Column                 | Purpose             |
| ---------------------- | ------------------- |
| silver_loaded_at       | load traceability   |
| source_system          | lineage tracking    |
| transformation_version | pipeline governance |

---

## Business Purpose

Supports:

- auditability
- pipeline traceability
- reproducibility
- operational governance

This follows:

# enterprise lineage engineering principles.

---

# Final Schema

| Column                     | Description                      |
| -------------------------- | -------------------------------- |
| order_id                   | Parent customer order            |
| order_item_id              | Item identifier                  |
| product_id                 | Purchased product                |
| seller_id                  | Responsible seller               |
| order_purchase_timestamp   | Customer purchase timestamp      |
| shipping_limit_date        | Seller shipping deadline         |
| price                      | Product sales value              |
| freight_value              | Shipping cost                    |
| freight_ratio              | Freight relative to item price   |
| product_volume_cm3         | Product logistics size           |
| seller_item_count_in_order | Seller contribution inside order |
| seller_state               | Seller geography                 |
| seller_lat                 | Seller latitude                  |
| seller_lng                 | Seller longitude                 |
| acquisition_source         | Seller acquisition origin        |
| seller_monthly_orders      | Seller workload volume           |
| workload_bucket            | Seller workload segment          |
| silver_loaded_at           | Load timestamp                   |
| source_system              | Source lineage                   |
| transformation_version     | Pipeline version                 |

---

# Validation Strategy

The dataset follows:

# validation-driven transformation engineering

Every transformation is validated using:

| Validation Type      | Purpose                     |
| -------------------- | --------------------------- |
| grain validation     | prevent duplication         |
| null validation      | preserve completeness       |
| workload validation  | verify segmentation         |
| geography validation | validate enrichment         |
| freight validation   | protect financial integrity |

Validation results are documented separately in:

```text
seller_fulfillment_staging_validation_report.md
```

---

# Important Engineering Decision

The workload classification logic intentionally remains:

# inside staging

instead of:

# Gold marts

Why?

Because workload segmentation represents:

# reusable operational business logic

used across:

- fulfillment marts
- dashboards
- streaming enrichment
- seller risk scoring

Centralizing this logic prevents:

- duplicated calculations
- inconsistent workload definitions
- KPI drift

This is:

# enterprise semantic consistency engineering.

---

# Architectural Significance

The `seller_fulfillment_staging` dataset represents:

# seller operational truth

inside the warehouse architecture.

This dataset is one of the MOST important operational enrichment layers because it connects:

- seller workload
- logistics burden
- acquisition intelligence
- fulfillment pressure

into:

# one unified operational seller view.

It acts as:

# the analytical foundation

for:

- seller operational monitoring
- fulfillment intelligence
- workload analytics
- seller risk scoring
- operational streaming systems

---

# Operational Intelligence Enabled

This staging layer enables:

| Capability                       | Enabled |
| -------------------------------- | ------- |
| seller workload analysis         | YES     |
| fulfillment burden analytics     | YES     |
| freight intensity analysis       | YES     |
| seller segmentation              | YES     |
| operational overload analysis    | YES     |
| acquisition-performance analysis | YES     |
| streaming enrichment support     | YES     |

---

# Engineering Strengths Demonstrated

This dataset demonstrates:

✅ grain-aware engineering
✅ workload intelligence modeling
✅ operational enrichment strategy
✅ conformed dimension reuse
✅ validation-driven transformation
✅ enterprise staging architecture
✅ business-truth preservation
✅ reusable semantic modeling

---

# Final Architectural Status

# APPROVED AS CORE OPERATIONAL STAGING ENTITY

The:

```text
seller_fulfillment_staging
```

dataset is officially designated as:

# the operational fulfillment intelligence staging layer

for:

- `fct_seller_fulfillment`
- seller operational analytics
- logistics intelligence
- workload segmentation
- streaming enrichment architecture

inside the:

# Olist Seller Intelligence Platform

```

```
