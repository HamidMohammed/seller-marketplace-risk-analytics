# Fact Table — fct_order_delivery

## Objective

The `fct_order_delivery` fact table is the core analytical table of the Delivery Performance Mart.

It is designed to measure the final customer delivery outcome for each order and provide the foundation for:

- delivery KPI analysis
- seller delivery performance tracking
- late-delivery detection
- operational reporting
- streaming risk scoring
- customer delivery experience analysis

This fact table represents the final stage of the logistics lifecycle from the customer perspective.

The table is intentionally modeled separately from seller fulfillment behavior to preserve grain integrity and avoid fan-out duplication. :contentReference[oaicite:0]{index=0}

---

# Business Process

Final customer delivery outcome.

This process answers:

- Was the order delivered on time?
- How late was the order?
- Did the seller breach Olist’s padded delivery promise?
- Which sellers generate the highest delivery risk?
- Which regions suffer the worst delivery performance?

---

# Grain Definition

# ONE ROW = ONE DELIVERED CUSTOMER ORDER

This is the MOST important modeling decision.

The table does NOT store:

- item-level shipments
- seller shipment preparation
- per-product logistics

Those belong to:

# `fct_seller_fulfillment`

because seller shipment behavior operates at a different business grain. :contentReference[oaicite:1]{index=1}

Keeping a strict grain prevents:

- duplicated metrics
- broken aggregations
- inaccurate seller KPIs
- incorrect delivery calculations

This follows Kimball dimensional modeling best practices. :contentReference[oaicite:2]{index=2}

---

# Source Tables

| Source Table                | Purpose                             |
| --------------------------- | ----------------------------------- |
| `olist_orders_dataset`      | Delivery lifecycle timestamps       |
| `olist_order_items_dataset` | Freight aggregation + seller counts |
| `olist_customers_dataset`   | Customer geography                  |
| `olist_sellers_dataset`     | Seller geography                    |
| `dim_customer`              | Customer surrogate keys             |
| `dim_seller`                | Seller surrogate keys               |
| `dim_date`                  | Calendar intelligence               |

Dataset structure derived from Olist official schema. :contentReference[oaicite:3]{index=3}

---

# Fact Table Schema

| Column Name                | Datatype      | Description                        |
| -------------------------- | ------------- | ---------------------------------- |
| delivery_sk                | BIGINT        | Surrogate warehouse key            |
| order_id                   | VARCHAR       | Business order identifier          |
| customer_sk_fk             | BIGINT        | FK to dim_customer                 |
| seller_sk_fk               | BIGINT        | FK to dim_seller                   |
| purchase_date_sk           | INT           | FK to dim_date                     |
| estimated_delivery_date_sk | INT           | FK to dim_date                     |
| actual_delivery_date_sk    | INT           | FK to dim_date                     |
| order_status               | VARCHAR       | Final order status                 |
| purchase_timestamp         | TIMESTAMP     | Order creation timestamp           |
| estimated_delivery_date    | TIMESTAMP     | Olist promised delivery date       |
| actual_delivery_date       | TIMESTAMP     | Final customer delivery timestamp  |
| carrier_handoff_date       | TIMESTAMP     | Handoff to logistics carrier       |
| delivery_duration_days     | INTEGER       | End-to-end delivery duration       |
| buffer_days                | INTEGER       | Olist delivery padding duration    |
| delay_days                 | INTEGER       | Delivery delay vs estimate         |
| delivery_status            | VARCHAR       | Categorized delivery outcome       |
| distance_bucket            | VARCHAR       | Geographic delivery classification |
| freight_total_value        | DECIMAL(10,2) | Total freight cost                 |
| total_items_count          | INTEGER       | Total items in order               |
| seller_count               | INTEGER       | Number of sellers in order         |
| is_multi_seller_order      | BOOLEAN       | Multi-seller indicator             |
| on_time_flag               | BOOLEAN       | Simplified KPI flag                |

Schema derived from finalized mart design. :contentReference[oaicite:4]{index=4}

---

# Key Derived Metrics

## 1. Delay Days

Measures customer delivery lateness.

Formula:

```sql
DATEDIFF(
    day,
    estimated_delivery_date,
    actual_delivery_date
)

Interpretation:

ValueMeaningNegativeDelivered earlyZeroDelivered on timePositiveDelivered late

This becomes the central operational KPI.

2\. Buffer Days
---------------

Measures how much Olist padded the promised delivery date.

Formula:

`   DATEDIFF(
            day,
            purchase_timestamp,
            estimated_delivery_date
        )   `

This metric is extremely important to the project narrative because prior analysis suggests Olist artificially padded delivery estimates by approximately 12 days.

This helps explain why:

*   aggregate on-time rate appears high

*   true operational performance is hidden

*   breached deliveries are rare but serious


3\. Delivery Duration Days
--------------------------

Measures the true end-to-end delivery lifecycle.

Formula:

`   DATEDIFF(    day,    purchase_timestamp,    actual_delivery_date)   `

Used for:

*   operational benchmarking

*   logistics trend analysis

*   regional delivery comparisons


Delivery Status Logic
=====================

The project standardizes delivery outcomes into business-friendly operational categories.

ConditionStatusdelay\_days < 0Earlydelay\_days = 0On-Timedelay\_days BETWEEN 1 AND 3Slight Delaydelay\_days BETWEEN 4 AND 7Latedelay\_days > 7Breached Buffer

This classification powers:

*   Power BI storytelling

*   seller segmentation

*   operational alerting

*   streaming thresholds

*   executive reporting


Geographic Logic
================

The distance\_bucket field classifies logistics difficulty.

Example categories:

ScenarioBucketSame citySame CitySame stateSame StateDifferent stateCross StateDifferent macro-regionCross Region

Purpose:

*   isolate geography impact

*   distinguish seller failure from distance difficulty

*   support risk scoring in streaming


Important Business Rules
========================

Rule 1 — Delivered Orders Only
------------------------------

Phase 1 delivery analysis includes only:

`   WHERE order_status = 'delivered'   `

Reason:

*   non-delivered orders contain incomplete timestamps

*   delay calculations become invalid

*   KPI accuracy degrades


This preserves analytical correctness.

Rule 2 — Single-Seller Accountability
-------------------------------------

Seller operational KPIs use:

`   WHERE seller_count = 1   `

Reason:

Multi-seller orders create ambiguous responsibility because:

*   multiple sellers contribute to one final delivery timestamp

*   one seller may delay the entire order

*   attribution becomes analytically unsafe


The project still preserves:

*   seller\_count

*   is\_multi\_seller\_order


for advanced future analysis.

This is enterprise-grade modeling discipline.

Why This Fact Table Matters
===========================

This table is the operational heart of the project.

It directly supports:

Business AreaUsagePower BIDelivery KPI dashboardsStreamingLate-order risk scoringSeller AnalysisWorst-performing sellersOperationsDelivery breach monitoringExecutive ReportingPlatform health metrics

Without this fact table:

*   the streaming pipeline loses its scoring foundation

*   seller risk cannot be measured

*   delivery intelligence becomes unreliable


Relationship to Streaming Layer
===============================

This fact table feeds the streaming system.

The streaming layer uses:

*   historical seller on-time rates

*   historical delay distributions

*   geography behavior

*   delivery thresholds


to calculate:

*   live delivery risk

*   seller overload alerts

*   breached estimate predictions
```
