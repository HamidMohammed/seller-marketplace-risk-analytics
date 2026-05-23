# Grain Definitions

## Objective

This document formally defines the grain of every fact table implemented during Phase 1 of the Olist Seller Intelligence Platform.

Grain definition is one of the most important parts of dimensional modeling because incorrect grain causes:

- duplicate metrics
- incorrect aggregations
- fan-out joins
- unreliable KPIs
- broken dashboards
- invalid business conclusions

Before any metric is added to a fact table, the grain must be explicitly declared.

This project follows:

# Kimball Dimensional Modeling Standards

where:

- each fact table represents exactly ONE business event
- every measure must describe that exact event
- dimensions provide descriptive context around that event

The Phase 1 Delivery Performance Mart contains two separate business processes:

1. Final customer delivery outcomes
2. Seller operational fulfillment behavior

Because these processes occur at different business levels, they require separate fact tables.

This separation is intentional and follows enterprise warehouse design principles.

---

# FACT TABLE 1 — `fct_order_delivery`

## Business Process

Final customer delivery outcome.

---

# OFFICIAL GRAIN

# ONE ROW = ONE DELIVERED CUSTOMER ORDER

---

## What This Means

Each row represents:

- one completed customer delivery
- one final delivery outcome
- one customer-facing logistics experience

The row answers:

> “What was the final delivery result for this customer order?”

---

## Why This Grain Was Chosen

The `olist_orders_dataset` stores delivery lifecycle timestamps at:

# order level

Examples:

- order_purchase_timestamp
- order_delivered_customer_date
- order_estimated_delivery_date

These timestamps describe:

# the ENTIRE order

NOT individual seller shipments.

Therefore:

- delay calculations belong at order grain
- customer experience belongs at order grain
- delivery promise analysis belongs at order grain

This grain supports:

- delivery KPI analysis
- late-delivery detection
- breached delivery promises
- customer delivery experience
- streaming risk scoring

---

## Measures Allowed In This Grain

The following metrics correctly describe ONE customer order:

| Metric                 | Why Valid                       |
| ---------------------- | ------------------------------- |
| delivery_duration_days | Entire order delivery duration  |
| delay_days             | Final order delay               |
| buffer_days            | Olist promised delivery padding |
| freight_total_value    | Total freight for the order     |
| total_items_count      | Number of items in order        |
| seller_count           | Number of sellers involved      |
| on_time_flag           | Delivery KPI for the order      |

---

## Measures NOT Allowed In This Grain

The following measures would violate the grain:

| Invalid Measure                   | Why Invalid                   |
| --------------------------------- | ----------------------------- |
| item-level preparation speed      | Exists at item/seller level   |
| seller shipment deadline per item | Item grain                    |
| product-specific shipment metrics | Product grain                 |
| one row per item                  | Would duplicate order metrics |

This is why:

# seller fulfillment behavior was separated into a second fact table

---

## Important Modeling Constraint

The dataset allows:

# multi-seller orders

Meaning:

- one customer order may contain multiple sellers
- one final delivery timestamp may involve multiple shipments

This creates:

# seller accountability ambiguity

To preserve analytical correctness:

Operational seller KPI calculations use:

```sql
WHERE seller_count = 1
```

while still preserving multi-seller orders for advanced analysis.

This is enterprise-grade modeling practice.

---

# FACT TABLE 2 --- `fct_seller_fulfillment`

## Business Process

Seller operational fulfillment behavior.

---

# OFFICIAL GRAIN

# ONE ROW = ONE SELLER ITEM FULFILLMENT EVENT

---

## What This Means

Each row represents:

\*   one seller

\*   preparing one item

\*   for shipment

\*   within one order

The row answers:

> "How did this seller operationally fulfill this specific item shipment?"

---

## Why This Grain Was Chosen

The `olist_order_items_dataset` stores logistics data at:

# item level

Examples:

\*   shipping_limit_date

\*   freight_value

\*   seller_id

\*   product_id

These attributes describe:

# individual seller shipment behavior

NOT the final customer delivery.

This grain supports:

\*   seller operational analysis

\*   shipment preparation analysis

\*   logistics workload analysis

\*   operational stress investigation

\*   streaming enrichment logic

---

## Measures Allowed In This Grain

Metric

Why Valid

seller_preparation_days

Seller shipment preparation duration

freight_ratio

Shipping cost relative to product value

shipping_deadline_gap_days

Time margin before shipment deadline

product_volume_cm3

Shipment size

item_price

Item-level revenue

freight_value

Item-level shipping fee

---

## Measures NOT Allowed In This Grain

Invalid Measure

Why Invalid

final customer delay

Exists at order level

order delivery duration

Entire order grain

customer delivery experience

Order-level business process

one row per completed order

Wrong grain

---

# WHY TWO FACT TABLES EXIST

The Olist dataset tracks logistics at:

Perspective

Dataset

Grain

Seller Fulfillment

olist_order_items

Item / Seller

Customer Delivery

olist_orders

Final Order

Combining both into one table would create:

\*   duplicate rows

\*   broken delivery KPIs

\*   fan-out aggregation errors

\*   ambiguous seller responsibility

\*   unreliable dashboards

Separating them provides:

\*   dimensional integrity

\*   accurate metrics

\*   scalable warehouse design

\*   streaming compatibility

\*   trustworthy analytics

---

# DIMENSION GRAIN ALIGNMENT

## `dim_date`

# ONE ROW = ONE CALENDAR DATE

Used as:

\*   purchase date

\*   estimated delivery date

\*   actual delivery date

\*   shipping limit date

This is a:

# role-playing dimension

---

## `dim_customer`

# ONE ROW = ONE UNIQUE CUSTOMER

Business entity represented:

\*   the customer identity

---

## `dim_seller`

# ONE ROW = ONE SELLER

Business entity represented:

\*   marketplace seller

This dimension is central to the project narrative.

---

## `dim_product`

# ONE ROW = ONE PRODUCT

Business entity represented:

\*   product logistics and category characteristics

---

# ENTERPRISE MODELING PRINCIPLES USED

This project intentionally follows professional warehouse standards:

| Principle                   | Implementation                  |
| --------------------------- | ------------------------------- |
| Explicit grain declaration  | Every fact formally defined     |
| Mixed-grain prevention      | Two separate logistics facts    |
| Conformed dimensions        | Shared dimensions across marts  |
| Role-playing dates          | Multiple date usages            |
| Surrogate keys              | Warehouse-managed identifiers   |
| Business-process separation | Fulfillment vs delivery outcome |
| Analytical integrity        | Prevents duplicate KPIs         |
