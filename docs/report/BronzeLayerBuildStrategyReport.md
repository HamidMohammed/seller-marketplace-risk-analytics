# Bronze Layer Build Strategy Report

## Objective

This document defines the recommended implementation strategy for building the Bronze Layer of the Olist Seller Intelligence Platform and clarifies the correct project progression order for a scalable enterprise-style data engineering architecture.

The primary architectural question addressed is:

> Should the project be built mart-by-mart end-to-end, or should the engineering layers be completed first across all datasets?

The final decision is:

# foundation-first architecture development

where shared ingestion and transformation layers are completed before fully implementing individual business marts.

This approach aligns with:

- Medallion Architecture
- Kimball dimensional modeling
- enterprise data platform engineering
- scalable warehouse design

and prevents duplicated logic, inconsistent transformations, and unstable analytical outputs.

---

# 1. Strategic Engineering Decision

## Incorrect Approach

A common beginner approach is:

```text id="0xj1u1"
Delivery Mart
    ↓
Dashboard
    ↓
Seller Mart
    ↓
Dashboard
```

This creates:

- duplicated ingestion logic
- repeated cleaning pipelines
- inconsistent dimensions
- fragmented business rules
- unstable KPIs

Each mart effectively becomes:

# a separate mini-project

instead of one unified analytical platform.

---

## Correct Professional Approach

The project follows:

# foundation-first engineering

Meaning:

```text id="2wrf6m"
Bronze Layer
        ↓
Silver Layer
        ↓
Conformed Dimensions
        ↓
Business Fact Marts
        ↓
Dashboards & Streaming
```

This creates:

- reusable data foundations
- shared business entities
- centralized transformations
- scalable architecture
- consistent analytical logic

---

# 2. Why Foundation-First Is Correct

The project is designed as:

# one integrated seller intelligence platform

not multiple isolated marts.

All marts share:

- customers
- sellers
- products
- orders
- geolocation
- date intelligence

For example:

| Shared Entity | Used By                     |
| ------------- | --------------------------- |
| dim_seller    | Delivery + Reviews + Funnel |
| dim_customer  | Delivery + Revenue          |
| dim_product   | Fulfillment + Revenue       |
| dim_date      | All marts                   |

This conformed-dimension strategy requires:

# centralized foundational layers

before mart implementation begins.

---

# 3. Bronze Layer Role

The Bronze Layer acts as:

# immutable raw ingestion storage

inside the Medallion Architecture.

---

## Bronze Responsibilities

The Bronze layer performs:

| Responsibility     | Included |
| ------------------ | -------- |
| Raw CSV ingestion  | Yes      |
| Schema inference   | Yes      |
| Parquet conversion | Yes      |
| Ingestion metadata | Yes      |
| Raw preservation   | Yes      |

---

## Bronze Does NOT Perform

| Responsibility   | Excluded |
| ---------------- | -------- |
| Cleansing        | No       |
| Deduplication    | No       |
| KPI calculations | No       |
| Business rules   | No       |
| Aggregations     | No       |

Those belong to:

# the Silver Layer

---

# 4. Bronze Layer Build Scope

The Bronze Layer should ingest:

# ALL core datasets first

before any mart implementation begins.

---

## Required Bronze Datasets

| Dataset                      | Purpose                  |
| ---------------------------- | ------------------------ |
| olist_orders_dataset         | Delivery lifecycle       |
| olist_order_items_dataset    | Seller fulfillment       |
| olist_customers_dataset      | Customer geography       |
| olist_sellers_dataset        | Seller geography         |
| olist_products_dataset       | Product logistics        |
| olist_order_reviews_dataset  | Satisfaction analysis    |
| olist_order_payments_dataset | Revenue analysis         |
| olist_geolocation_dataset    | Geographic enrichment    |
| Funnel datasets              | Acquisition intelligence |

These datasets support the complete business narrative:

```text id="gptm49"
Acquisition
    ↓
Seller Performance
    ↓
Delivery Failure
    ↓
Customer Dissatisfaction
    ↓
Revenue Impact
```

which is the central architecture principle of the platform.

---

# 5. Recommended Build Order

## PHASE 1 — Bronze Layer

Build ingestion pipelines for:

- all source datasets
- parquet storage
- metadata enrichment
- validation checks

Output:

```text id="6j0p0k"
data/bronze/
```

This creates:

# replayable raw analytical storage

---

## PHASE 2 — Silver Layer

After Bronze stabilizes:
build:

- cleaned datasets
- standardized timestamps
- null handling
- deduplicated geolocation
- derived operational fields

Output:

```text id="7bhm5x"
data/silver/
```

This becomes:

# trusted analytical staging

---

## PHASE 3 — Conformed Dimensions

Build shared dimensions:

- dim_date
- dim_customer
- dim_seller
- dim_product

These dimensions become reusable across:

- delivery mart
- review mart
- revenue mart
- funnel mart
- streaming enrichment

---

## PHASE 4 — Business Fact Marts

Only after shared foundations are trusted:
begin implementing marts individually.

Recommended order:

| Order | Mart                  |
| ----- | --------------------- |
| 1     | Delivery Performance  |
| 2     | Seller Performance    |
| 3     | Customer Satisfaction |
| 4     | Revenue               |
| 5     | Funnel                |

This sequence follows the project narrative progression.

---

# 6. Why Delivery Mart Is Built First

The Delivery Performance Mart is:

# the operational foundation of the platform

because:

- streaming risk scoring depends on delivery metrics
- seller performance depends on delivery outcomes
- customer reviews depend on delivery quality

The project proposal explicitly defines it as:

# NON-NEGOTIABLE PHASE 1

because all later intelligence builds on delivery behavior.

---

# 7. Relationship Between Bronze and Streaming

The streaming layer does NOT directly consume raw CSV files.

Instead:

```text id="5jxq1g"
RAW
    ↓
Bronze
    ↓
Silver
    ↓
Gold Marts
    ↓
Streaming Enrichment
```

The batch layer first calculates:

- seller historical baselines
- operational thresholds
- delivery risk patterns

Then:
the streaming layer consumes those outputs for:

# real-time operational intelligence

This ensures:

- statistically grounded streaming alerts
- explainable thresholds
- operational consistency

instead of arbitrary hardcoded logic.

---

# 8. Enterprise Benefits of This Strategy

## Benefit 1 — Reusability

Shared transformations are built once and reused everywhere.

---

## Benefit 2 — KPI Consistency

All marts calculate metrics from:

# one trusted transformation layer

instead of duplicated logic.

---

## Benefit 3 — Easier Debugging

Problems can be isolated by layer:

- Bronze ingestion
- Silver cleansing
- Gold marts

instead of debugging entire pipelines simultaneously.

---

## Benefit 4 — Better Scalability

New marts can be added later without redesigning ingestion.

---

## Benefit 5 — Stronger Academic Defensibility

The architecture demonstrates:

- separation of concerns
- layered engineering
- dimensional consistency
- professional ETL lifecycle management

---

# 9. Important Exception

Although foundational layers are built first:
after:

- Bronze
- Silver
- dimensions

are stable,

the project should then complete:

# one mart end-to-end at a time

Meaning:

```text id="dk6g20"
Fact Table
    ↓
Validation
    ↓
KPIs
    ↓
Dashboard
    ↓
Documentation
```

before moving to the next mart.

This creates:

- visible milestones
- demonstrable business value
- stable incremental delivery

without losing architectural consistency.

---

# 10. Final Engineering Recommendation

The final recommended engineering strategy is:

---

## Step 1

Build:

# Bronze Layer for ALL datasets

---

## Step 2

Build:

# Silver Layer for ALL shared entities

---

## Step 3

Build:

# shared conformed dimensions

---

## Step 4

Complete:

# Delivery Mart end-to-end

---

## Step 5

Build remaining marts incrementally.

---

# 11. Final Architectural Outcome

This strategy transforms the project from:

# a collection of disconnected ETL scripts

into:

# a unified enterprise-style analytical platform

with:

- scalable ingestion
- reusable transformations
- conformed dimensions
- stable marts
- streaming integration
- maintainable warehouse architecture

The final architecture aligns with:

- Kimball best practices
- Medallion architecture
- enterprise data engineering principles
- scalable lakehouse design

while preserving:

- business coherence
- dimensional integrity
- KPI trustworthiness
- future extensibility.
