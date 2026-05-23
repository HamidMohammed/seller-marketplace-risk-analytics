# `dim_seller.md`

## Objective

The `dim_seller` dimension stores seller identity, geographic attributes, and acquisition intelligence used across all marts and streaming enrichment layers.

This is:

# the most important dimension in the project

because the entire business narrative revolves around:

- seller performance
- seller operational overload
- delivery failure risk
- acquisition quality
- seller lifecycle behavior

---

# Business Purpose

`dim_seller` provides reusable seller context for:

- delivery analytics
- seller risk scoring
- streaming enrichment
- operational KPI analysis
- acquisition channel analysis
- seller segmentation
- geographic logistics analysis

Used by:

- `fct_order_delivery`
- `fct_seller_fulfillment`
- streaming risk scoring
- Power BI dashboards

---

# Grain

# One Row = One Seller

For SCD Type 2:

# One Row = One Seller Version

---

# Table Name

```sql
dim_seller
```

---

# Primary Key

```sql
seller_sk
```

Warehouse-generated surrogate key.

---

# Business Key

```sql
seller_id
```

Original Olist seller identifier.

---

# Schema Design

| Column Name            | Datatype      | Description                         |
| ---------------------- | ------------- | ----------------------------------- |
| seller_sk              | BIGINT        | Surrogate warehouse key             |
| seller_id              | VARCHAR       | Business seller identifier          |
| seller_zip_code_prefix | VARCHAR       | Seller ZIP prefix                   |
| seller_city            | VARCHAR       | Seller city                         |
| seller_state           | VARCHAR       | Seller state                        |
| seller_region          | VARCHAR       | Derived Brazilian macro region      |
| latitude               | DECIMAL(10,6) | Seller latitude                     |
| longitude              | DECIMAL(10,6) | Seller longitude                    |
| acquisition_source     | VARCHAR       | Seller acquisition channel          |
| business_segment       | VARCHAR       | Seller business segment             |
| lead_type              | VARCHAR       | Funnel lead classification          |
| lead_behavior_profile  | VARCHAR       | Seller acquisition behavior profile |
| effective_start_date   | DATE          | SCD Type 2 start date               |
| effective_end_date     | DATE          | SCD Type 2 end date                 |
| is_current             | BOOLEAN       | Current active seller record        |

Schema aligned with the dimensional modeling architecture.

---

# Source Tables

| Source Table                              | Purpose                           |
| ----------------------------------------- | --------------------------------- |
| `olist_sellers_dataset`                   | Seller identity and geography     |
| `olist_geolocation_dataset`               | Latitude and longitude enrichment |
| `olist_closed_deals_dataset`              | Acquisition and funnel attributes |
| `olist_marketing_qualified_leads_dataset` | Acquisition source tracking       |

Dataset structure based on Olist source tables.

---

# Example Record

| Column                | Example                          |
| --------------------- | -------------------------------- |
| seller_sk             | 101                              |
| seller_id             | 3442f8959a84dea7ee197c632cb2df15 |
| seller_city           | sao paulo                        |
| seller_state          | SP                               |
| seller_region         | Southeast                        |
| latitude              | -23.550520                       |
| longitude             | -46.633308                       |
| acquisition_source    | organic_search                   |
| business_segment      | electronics                      |
| lead_type             | online_medium                    |
| lead_behavior_profile | cat                              |
| is_current            | TRUE                             |

---

# Geographic Enrichment

Latitude and longitude are enriched from:

```sql
olist_geolocation_dataset
```

Using:

- ZIP prefix matching
- deduplicated median coordinates

This supports:

- seller-to-customer distance analysis
- logistics segmentation
- streaming delivery-risk enrichment
- regional seller clustering

---

# Why Funnel Attributes Belong Here

The project narrative connects:

# acquisition quality → seller failure

Therefore:
seller acquisition attributes naturally belong inside:

# `dim_seller`

instead of fact tables.

This enables:

- seller lifecycle analysis
- acquisition-source segmentation
- seller-risk clustering
- marketing ROI analysis

WITHOUT:

- duplicating acquisition attributes across facts

This is:

# proper Kimball dimensional modeling

---

# Slowly Changing Dimension Strategy

Recommended implementation:

# SCD Type 2

Why?

Seller attributes may evolve:

- business segment
- acquisition classification
- geographic information
- operational categorization

Even though Olist historical changes are limited, implementing SCD Type 2 demonstrates:

# enterprise warehouse capability

---

# SCD Type 2 Columns

| Column               | Purpose                    |
| -------------------- | -------------------------- |
| effective_start_date | Record validity start      |
| effective_end_date   | Record validity end        |
| is_current           | Current active record flag |

---

# Relationships

| Fact Table             | Foreign Key  |
| ---------------------- | ------------ |
| fct_order_delivery     | seller_sk_fk |
| fct_seller_fulfillment | seller_sk_fk |
| fct_reviews            | seller_sk_fk |
| fct_seller_performance | seller_sk_fk |

---

# Streaming Architecture Role

`dim_seller` is heavily used in:

# streaming enrichment

The streaming layer loads:

- seller historical performance
- seller geography
- seller operational behavior

during stream startup to create:

# seller baseline intelligence

Used for:

- real-time risk scoring
- overloaded seller detection
- seller-level alert aggregation

Architecture aligned with the streaming design.

---

# ETL Logic

## Source Extraction

- extract seller records
- standardize city/state formatting
- clean ZIP prefixes

## Geographic Enrichment

- join seller ZIP prefix with geolocation dataset
- calculate median latitude/longitude

## Funnel Enrichment

- left join acquisition funnel tables
- preserve sellers without acquisition records

## SCD Handling

- detect attribute changes
- expire old records
- insert new seller versions

---

# Data Quality Rules

| Rule                      | Validation                   |
| ------------------------- | ---------------------------- |
| Unique surrogate key      | seller_sk unique             |
| Non-null business key     | seller_id required           |
| Valid geographic data     | state/city standardized      |
| One active seller version | only one `is_current = TRUE` |
| Valid SCD dates           | start date < end date        |

---

# Important Modeling Decision

The funnel dataset only covers a subset of sellers.

Therefore:

```sql
LEFT JOIN
```

is required during enrichment to avoid:

- silent seller loss
- biased acquisition analysis
- incomplete dimensional coverage

Sellers without funnel records are assigned:

```text
acquisition_source = 'Unknown'
```

This preserves:

# full seller population integrity

---

# Best Practices Applied

| Best Practice               | Applied |
| --------------------------- | ------- |
| Kimball conformed dimension | Yes     |
| Surrogate keys              | Yes     |
| SCD Type 2                  | Yes     |
| Geographic enrichment       | Yes     |
| Funnel enrichment           | Yes     |
| Streaming compatibility     | Yes     |
| Reusable across marts       | Yes     |
| Business-driven modeling    | Yes     |

---

# Architectural Importance

`dim_seller` acts as:

# the central intelligence dimension of the warehouse

It connects:

- acquisition behavior
- operational fulfillment
- delivery outcomes
- customer satisfaction
- seller risk
- streaming alerts

This dimension powers:

- seller intelligence analytics
- delivery-risk investigation
- real-time operational monitoring
- acquisition quality analysis
- cross-mart seller scorecards

and forms the foundation of the:

# Seller Failure Detection & Prevention Platform

described in the project proposal.
