# DIMENSION — `dim_customer`

## Objective

The `dim_customer` dimension stores customer identity and geographic information used across analytical marts and streaming enrichment.

This dimension supports:

- customer delivery analysis
- geographic segmentation
- logistics investigation
- regional KPI analysis
- customer retention analysis
- cross-state delivery analysis

The dimension follows Kimball conformed dimension principles.

---

# Grain

# ONE ROW = ONE UNIQUE CUSTOMER

The warehouse uses:

# `customer_unique_id`

as the stable business identity.

This is a critical modeling decision because one real customer may appear under multiple operational `customer_id` values in Olist.

---

# Source Tables

| Source Table              | Purpose                           |
| ------------------------- | --------------------------------- |
| olist_customers_dataset   | Customer identity and geography   |
| olist_geolocation_dataset | Latitude and longitude enrichment |

---

# Schema Design

| Column Name              | Datatype      | Description                         |
| ------------------------ | ------------- | ----------------------------------- |
| customer_sk              | BIGINT        | Warehouse surrogate key             |
| customer_id              | VARCHAR       | Operational customer identifier     |
| customer_unique_id       | VARCHAR       | Stable anonymized customer identity |
| customer_zip_code_prefix | VARCHAR       | ZIP code prefix                     |
| customer_city            | VARCHAR       | Customer city                       |
| customer_state           | VARCHAR       | Customer state                      |
| customer_region          | VARCHAR       | Derived macro region                |
| latitude                 | DECIMAL(10,6) | Geographic latitude                 |
| longitude                | DECIMAL(10,6) | Geographic longitude                |

---

# Geographic Enrichment Strategy

Latitude and longitude are enriched using:

- ZIP prefix matching
- deduplicated geolocation records
- median coordinate resolution

Source:

`olist_geolocation_dataset`

This supports:

- logistics analysis
- distance bucketing
- regional segmentation
- streaming risk scoring

---

# Region Derivation Logic

Brazilian states are grouped into macro regions.

Example:

| State | Region    |
| ----- | --------- |
| SP    | Southeast |
| RJ    | Southeast |
| BA    | Northeast |
| PR    | South     |

This simplifies:

- dashboard storytelling
- geographic KPIs
- cross-region logistics analysis

---

# Relationships

| Fact Table                        | Relationship   |
| --------------------------------- | -------------- |
| fct_order_delivery                | customer_sk_fk |
| Future customer satisfaction mart | customer_sk_fk |
| Future retention mart             | customer_sk_fk |

---

# Business Use Cases

## Delivery Failure Heatmaps

Analyze:

- regions with high delay rates
- delivery bottlenecks
- logistics imbalance

---

## Customer Retention Analysis

Track:

- repeat customers
- customer lifetime patterns
- return purchase behavior

---

## Geographic Risk Segmentation

Measure:

- cross-region delivery risk
- rural vs urban logistics behavior
- high-risk delivery corridors

---

# Important Modeling Decision

## Why `customer_unique_id` Matters

Olist operationally anonymizes customers.

Meaning:

- one real customer may own multiple `customer_id` values
- direct operational IDs are unreliable for retention analysis

Using `customer_unique_id` enables:

- repeat purchase tracking
- lifetime value analysis
- accurate customer counting

Most beginner projects miss this critical issue.

---

# Best Practices Applied

- Surrogate warehouse keys
- Geographic enrichment
- Conformed dimension reuse
- Business-friendly regions
- Stable customer identity modeling

---

# Common Student Mistakes Avoided

## Mistake 1 — Using customer_id as permanent identity

Wrong:

- assuming operational IDs are stable

Correct:

- using customer_unique_id

---

## Mistake 2 — No Geographic Enrichment

Wrong:

- city/state only

Correct:

- adding coordinates and regions

---

## Mistake 3 — Embedding Customer Attributes Inside Facts

Wrong:

- duplicating customer columns in facts

Correct:

- normalized conformed dimensions

---

# Integration With Streaming Layer

This dimension enriches streaming events with:

- customer region
- delivery geography
- logistics distance calculations

Supports real-time risk scoring architecture.
