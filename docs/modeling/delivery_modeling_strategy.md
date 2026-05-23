# `delivery_modeling_strategy.md`

Based on the final warehouse architecture, two-fact delivery strategy, Kimball dimensional modeling approach, and streaming intelligence design

---

# Delivery Modeling Strategy

## Objective

This document explains the dimensional modeling strategy used to design the Delivery Intelligence Platform and clarifies the architectural decisions made during the modeling phase.

The objective of the delivery modeling layer is to:

- preserve analytical correctness
- prevent mixed-grain corruption
- support historical analytics
- support real-time streaming intelligence
- maintain scalable warehouse architecture
- align all marts with a single business narrative

The project follows:

# Kimball dimensional modeling principles

where:

- facts represent measurable business events
- dimensions provide descriptive business context

---

# 1. Core Business Narrative

The entire platform is designed around one operational problem:

> Olist cannot identify underperforming sellers before they damage customer experience and platform reputation.

The analytical objective is to investigate the following causal chain:

```text id="j7a8p9"
Bad Acquisition Channel
        ↓
Seller Operational Overload
        ↓
Delivery Failure
        ↓
Customer Dissatisfaction
        ↓
Revenue Loss
```

Every warehouse component exists to analyze, measure, or detect a specific part of this chain.

This ensures:

- business coherence
- architectural consistency
- streaming justification
- analytical focus

---

# 2. Major Dataset Discovery

During the exploratory analysis phase, a critical discovery was identified inside the Olist dataset.

The dataset tracks logistics at:

# two different operational levels

---

## Seller-Level Fulfillment

Inside:
`olist_order_items_dataset`

Each item contains:

- seller-level shipment responsibility
- seller-specific shipping deadlines
- shipment freight values

Example fields:

| Field               | Meaning                         |
| ------------------- | ------------------------------- |
| shipping_limit_date | Seller shipment deadline        |
| freight_value       | Item-level shipping fee         |
| seller_id           | Seller responsible for shipment |

This represents:

# operational shipment preparation behavior

---

## Customer-Level Delivery Outcome

Inside:
`olist_orders_dataset`

The delivery lifecycle is tracked for:

# the entire customer order

Example fields:

| Field                         | Meaning                 |
| ----------------------------- | ----------------------- |
| order_delivered_carrier_date  | First carrier pickup    |
| order_delivered_customer_date | Final customer delivery |
| order_estimated_delivery_date | Olist promised delivery |

This represents:

# final customer delivery outcome

---

# 3. Modeling Problem

Initially, a single delivery fact table was considered.

However, deeper analysis revealed that combining:

- seller-level shipment operations
- customer-level delivery outcomes

inside one fact table would create:

- mixed-grain corruption
- fan-out duplication
- ambiguous seller attribution
- incorrect KPI calculations
- unreliable delivery metrics

This is one of the most common mistakes in dimensional modeling projects.

---

# 4. Final Modeling Decision

To preserve grain integrity and analytical correctness, the architecture separates logistics into:

# two independent fact tables

Each fact table represents:

# a different business process

---

# 5. Fact Table 1 — `fct_order_delivery`

## Business Process

Final customer delivery outcome.

---

## Grain

# One Row = One Delivered Customer Order

---

## Purpose

This fact table measures:

- delivery performance
- late deliveries
- breached delivery promises
- customer delivery experience
- operational delivery risk

It acts as:

# the primary analytical and streaming fact table

for:

- Power BI dashboards
- delivery KPIs
- seller delivery analysis
- real-time risk scoring

---

## Main Metrics

| Metric                 | Purpose                             |
| ---------------------- | ----------------------------------- |
| delay_days             | Measures delivery lateness          |
| buffer_days            | Measures Olist delivery padding     |
| delivery_duration_days | Measures real delivery duration     |
| delivery_status        | Categorized delivery severity       |
| distance_bucket        | Geographic logistics classification |

---

## Important Business Rule

Operational seller-accountability analysis focuses primarily on:

# single-seller delivered orders

Reason:
multi-seller orders introduce ambiguous delivery responsibility because one final customer delivery timestamp may involve multiple seller shipments.

The project still preserves:

- seller_count
- is_multi_seller_order

for future advanced analysis.

---

# 6. Fact Table 2 — `fct_seller_fulfillment`

## Business Process

Seller operational fulfillment behavior.

---

## Grain

# One Row = One Seller Item Fulfillment Event

---

## Purpose

This fact table measures:

- seller preparation behavior
- operational shipment efficiency
- freight intensity
- seller workload pressure
- logistics complexity

This fact table acts primarily as:

# enrichment intelligence

for the streaming layer.

---

## Main Metrics

| Metric                         | Purpose                              |
| ------------------------------ | ------------------------------------ |
| seller_preparation_days        | Seller preparation duration          |
| shipping_deadline_gap_days     | Shipping deadline pressure           |
| freight_ratio                  | Shipping cost relative to item value |
| heavy_product_flag             | Logistics complexity indicator       |
| seller_to_customer_distance_km | Approximate shipment distance        |

---

# 7. Why Two Fact Tables Are Correct

Separating the facts provides:

| Benefit                      | Explanation                                    |
| ---------------------------- | ---------------------------------------------- |
| Clean grain integrity        | Each fact has one business grain               |
| Correct KPI calculations     | No duplicated delivery metrics                 |
| Better seller accountability | Fulfillment separated from customer delivery   |
| Streaming alignment          | Order delivery remains operational focus       |
| Easier debugging             | Clear event ownership                          |
| Better scalability           | Future marts can be added safely               |
| Kimball compliance           | Facts represent independent business processes |

---

# 8. Conformed Dimensions Strategy

The warehouse uses:

# conformed dimensions

shared across all marts.

---

## Shared Dimensions

| Dimension    | Used By             |
| ------------ | ------------------- |
| dim_date     | All marts           |
| dim_customer | Delivery + reviews  |
| dim_seller   | Both delivery facts |
| dim_product  | Fulfillment + sales |

This guarantees:

- consistent business logic
- stable joins
- reusable analytical entities
- scalable warehouse growth

---

# 9. Role-Playing Date Design

The warehouse uses:

# role-playing date dimensions

where the same `dim_date` table is reused multiple times with different business meanings.

---

## Examples

| Foreign Key                | Meaning                      |
| -------------------------- | ---------------------------- |
| purchase_date_sk           | Order purchase date          |
| estimated_delivery_date_sk | Promised delivery date       |
| actual_delivery_date_sk    | Final customer delivery date |
| shipping_limit_date_sk     | Seller shipment deadline     |

This is a professional dimensional modeling pattern widely used in enterprise warehouses.

---

# 10. Geographic Modeling Strategy

Initially, the architecture considered creating:

# `dim_location`

However, deeper analysis revealed that:

- Olist coordinates represent approximate ZIP-code regions
- location is not an independent business entity
- geography acts only as descriptive enrichment

Therefore:

# `dim_location` was intentionally removed

to avoid:

- unnecessary normalization
- additional joins
- redundant geographic abstraction

Instead:
geographic attributes remain directly inside:

- `dim_customer`
- `dim_seller`

following Kimball denormalized modeling principles.

---

# 11. Distance Intelligence

The project introduces:

# distance intelligence

through:

# `distance_bucket`

which categorizes seller-to-customer delivery distance into business-friendly logistics groups.

---

## Initial Distance Classification

| Condition              | distance_bucket |
| ---------------------- | --------------- |
| Same city              | Same City       |
| Same state             | Same State      |
| Same macro region      | Same Region     |
| Different macro region | Cross Region    |

This supports:

- delivery-risk analysis
- logistics segmentation
- seller overload investigation
- operational storytelling

without requiring advanced GIS calculations.

---

# 12. Streaming Architecture Relationship

The streaming layer was intentionally designed around:

# customer delivery risk

rather than shipment-level tracking.

---

## Why?

Because:

- customer delivery is the real business outcome
- customer reviews depend on final delivery
- operational intervention occurs at order level

---

# Streaming Flow

```text id="g0eq7u"
fct_seller_fulfillment
        ↓
seller operational signals
        ↓
stream enrichment layer
        ↓
fct_order_delivery events
        ↓
real-time delivery risk scoring
        ↓
late-order alerts
```

This design allows:

- historical seller intelligence
- real-time operational scoring
- proactive risk detection

inside one integrated platform.

---

# 13. Data Integrity Strategy

The warehouse enforces:

# referential integrity

through:

- surrogate keys
- foreign key constraints
- check constraints
- dimensional consistency rules

Examples:

- valid delivery status categories
- non-negative freight values
- foreign-key dimensional enforcement
- uniqueness constraints

This improves:

- warehouse reliability
- KPI trustworthiness
- analytical correctness

---

# 14. Architectural Best Practices Applied

| Best Practice                      | Applied |
| ---------------------------------- | ------- |
| Kimball dimensional modeling       | Yes     |
| Conformed dimensions               | Yes     |
| Role-playing dimensions            | Yes     |
| Surrogate keys                     | Yes     |
| Grain-first modeling               | Yes     |
| Streaming enrichment architecture  | Yes     |
| Controlled denormalization         | Yes     |
| Delivery intelligence segmentation | Yes     |
| Data quality constraints           | Yes     |
| Business-driven modeling           | Yes     |

---

# 15. Final Architectural Outcome

The final delivery modeling architecture provides:

- analytically correct fact separation
- scalable warehouse structure
- operational streaming intelligence
- delivery-risk analytics
- seller operational visibility
- strong dashboard storytelling
- enterprise-grade dimensional consistency

The final platform successfully transforms the Olist dataset into:

# a professionally architected seller intelligence and delivery-risk analytics platform

capable of supporting:

- historical business intelligence
- operational monitoring
- real-time alerting
- seller-risk detection
- logistics performance analysis

while preserving:

- grain integrity
- warehouse maintainability
- KPI correctness
- architectural defensibility.
