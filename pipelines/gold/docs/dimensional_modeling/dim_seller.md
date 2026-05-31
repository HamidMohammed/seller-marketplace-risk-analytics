# Seller Dimension (`dim_seller`)

## Objective

The `dim_seller` table is the primary conformed seller dimension of the Olist Seller Intelligence Platform.

This dimension provides a unified Seller 360 view by combining:

- seller identity
- seller geography
- acquisition intelligence
- business segmentation
- location classification

into a single reusable analytical entity.

The dimension serves as the central seller reference across the entire warehouse and supports:

- delivery analytics
- fulfillment analytics
- sales analytics
- acquisition analytics
- customer review analytics
- seller performance analytics

---

# Architectural Role

The `dim_seller` table is a:

# Conformed Dimension

Meaning it is shared across multiple fact tables and provides consistent seller context throughout the warehouse.

---

# Facts Referencing dim_seller

| Fact Table             | Purpose                        |
| ---------------------- | ------------------------------ |
| fct_order_delivery     | Delivery performance analysis  |
| fct_seller_fulfillment | Operational workload analysis  |
| fct_order_sales        | Revenue attribution            |
| fct_order_payments     | Payment behavior analysis      |
| fct_customer_reviews   | Customer satisfaction analysis |
| fct_seller_acquisition | Acquisition effectiveness      |
| fct_seller_performance | Longitudinal seller analytics  |

This creates:

# Single Version of Seller Truth

across all analytical domains.

---

# Dataset Grain

# ONE ROW = ONE SELLER

Each record represents a unique seller within the Olist marketplace ecosystem.

The dimension preserves seller-level granularity and intentionally excludes transactional metrics.

Examples of metrics intentionally excluded:

- monthly_orders
- avg_review_score
- on_time_rate
- volume_growth_rate
- delayed_orders_count

These belong in fact tables.

---

# Source Dataset

## Primary Source

```text
silver_sellers
```

The Silver layer already contains:

- standardized seller identities
- geographic enrichment
- acquisition enrichment
- validated business attributes

The Gold layer therefore focuses on:

- dimensional modeling
- conformed classifications
- surrogate key generation
- SCD readiness

rather than additional operational transformations.

---

# Seller 360 Model

The dimension combines four major intelligence domains.

---

# 1. Seller Identity

Provides:

- seller identifier
- warehouse surrogate key

Columns:

| Column    |
| --------- |
| seller_sk |
| seller_id |

Purpose:

Provides stable warehouse relationships between dimensions and facts.

---

# 2. Geographic Intelligence

Provides:

- seller location
- regional segmentation
- spatial analysis capability

Columns:

| Column                 |
| ---------------------- |
| seller_zip_code_prefix |
| seller_city            |
| seller_state           |
| median_latitude        |
| median_longitude       |
| seller_region          |
| seller_location_type   |

Supports:

- geographic reporting
- regional benchmarking
- logistics analysis
- fulfillment intelligence

---

# Seller Region Classification

The Gold layer classifies Brazilian states into analytical regions.

## Distribution

| Region       | Sellers |
| ------------ | ------: |
| Southeast    |   2,287 |
| South        |     668 |
| Central-West |      79 |
| Northeast    |      56 |
| North        |       5 |

---

## Business Interpretation

The seller ecosystem is heavily concentrated in:

# Southeast Brazil

which aligns with known marketplace behavior where:

- São Paulo
- Rio de Janeiro
- Minas Gerais
- Espírito Santo

represent the largest commercial hubs.

This concentration becomes extremely important when analyzing:

- delivery efficiency
- shipping distance
- fulfillment performance
- marketplace expansion opportunities

---

# 3. Seller Location Classification

The Gold layer derives:

```text
seller_location_type
```

Categories:

| Type         |
| ------------ |
| Metropolitan |
| Urban        |
| Regional     |

---

## Distribution

| Location Type | Sellers |
| ------------- | ------: |
| Urban         |   1,403 |
| Metropolitan  |   1,061 |
| Regional      |     631 |

---

## Business Interpretation

This classification enables:

- urban vs regional performance analysis
- geographic fulfillment benchmarking
- operational scalability analysis

The marketplace shows strong representation in:

# Urban and Metropolitan Areas

which reflects the concentration of Brazilian e-commerce operations.

---

# 4. Acquisition Intelligence

The dimension contains seller acquisition attributes.

Columns:

| Column                |
| --------------------- |
| acquisition_source    |
| business_segment      |
| lead_type             |
| lead_behavior_profile |

These attributes provide:

# Commercial Seller Context

and enable analysis such as:

- Which acquisition channels generate the best sellers?
- Which seller profiles perform best operationally?
- Which business segments drive marketplace growth?

---

# Seller Business Profile

The Gold layer derives:

```text
seller_business_profile
```

Categories:

| Profile      |
| ------------ |
| Enterprise   |
| Professional |
| Standard     |

---

## Distribution

| Profile      | Sellers |
| ------------ | ------: |
| Standard     |   2,882 |
| Professional |     172 |
| Enterprise   |      41 |

---

## Business Interpretation

The marketplace is dominated by:

# Standard Sellers

representing approximately:

```text
93%
```

of the seller base.

This indicates:

- a long-tail seller ecosystem
- many small-to-medium merchants
- relatively few enterprise-scale participants

This becomes valuable for:

- seller segmentation
- growth strategies
- acquisition optimization

---

# SCD Type 2 Readiness

The dimension includes enterprise-ready Slowly Changing Dimension columns.

Columns:

| Column               |
| -------------------- |
| effective_start_date |
| effective_end_date   |
| is_current           |

Current implementation:

- one active record per seller
- historical versioning framework prepared
- future SCD expansion supported

---

# Surrogate Key Strategy

Primary Key:

```text
seller_sk
```

Business Key:

```text
seller_id
```

The warehouse uses:

# Surrogate Key Modeling

to ensure:

- stable joins
- warehouse independence
- future SCD support
- improved analytical performance

---

# Validation Strategy

The dimension includes enterprise validation controls.

| Validation                             |
| -------------------------------------- |
| Surrogate key uniqueness               |
| Business key uniqueness                |
| Critical null validation               |
| SCD integrity validation               |
| Geography validation                   |
| Acquisition validation                 |
| Classification distribution validation |

---

# Final Schema

| Column                  |
| ----------------------- |
| seller_sk               |
| seller_id               |
| seller_zip_code_prefix  |
| seller_city             |
| seller_state            |
| seller_region           |
| median_latitude         |
| median_longitude        |
| seller_location_type    |
| acquisition_source      |
| business_segment        |
| lead_type               |
| lead_behavior_profile   |
| seller_business_profile |
| effective_start_date    |
| effective_end_date      |
| is_current              |
| source_system           |
| transformation_version  |
| gold_loaded_at          |

---

# Architectural Significance

The `dim_seller` dimension is the:

# Central Business Entity Dimension

within the Olist Seller Intelligence Platform.

Unlike fact tables that measure:

- deliveries
- sales
- reviews
- acquisitions

the seller dimension provides:

# Business Context

that enables those measurements to be analyzed consistently.

This follows:

# Kimball Conformed Dimension Principles

and establishes the seller entity as a reusable analytical asset across the entire warehouse.

---

# Business Value Enabled

The dimension supports:

| Capability                | Enabled |
| ------------------------- | ------- |
| Seller segmentation       | YES     |
| Geographic analytics      | YES     |
| Regional benchmarking     | YES     |
| Acquisition analysis      | YES     |
| Seller lifecycle analysis | YES     |
| Cross-fact analytics      | YES     |
| Executive dashboards      | YES     |

---

# Gold Layer Readiness

The dimension is fully prepared for:

- star-schema joins
- fact table integration
- dbt modeling
- Power BI dashboards
- seller performance analytics
- operational intelligence
- streaming enrichment

with:

# FULL CONFORMED DIMENSION GOVERNANCE

# SELLER 360 ANALYTICAL CONTEXT

# STAR-SCHEMA READINESS

# ENTERPRISE WAREHOUSE STANDARDS
