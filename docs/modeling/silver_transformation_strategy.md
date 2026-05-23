# Silver Transformation Strategy

## Objective

This document defines the transformation philosophy, validation methodology, and business-rule governance used inside the Silver Layer of the Olist Seller Intelligence Platform.

The Silver Layer acts as:

# the business-truth refinement layer

between:

- immutable raw Bronze ingestion
- trusted analytical Gold marts

The objective of the Silver layer is NOT simply data cleaning.

Instead, the Silver layer is responsible for:

- operational truth refinement
- controlled business transformations
- dimensional consistency
- trusted analytical preparation
- KPI integrity preservation
- streaming enrichment preparation

The project follows:

# validation-driven transformation engineering

where every transformation must be:

- explainable
- measurable
- validated
- documented
- business justified

This prevents:

- silent KPI corruption
- mixed-grain inconsistencies
- unreliable dashboards
- misleading operational insights

The Silver Layer transforms:

# raw operational data

into:

# trusted analytical staging datasets

used by:

- dimensional models
- fact marts
- Power BI dashboards
- streaming enrichment
- seller risk scoring

---

# 1. Silver Layer Philosophy

The Silver Layer is intentionally designed as:

# controlled transformation layer

NOT:

# uncontrolled cleaning layer

This distinction is critical.

The project avoids:

- arbitrary row deletion
- aggressive null replacement
- unexplained filtering
- undocumented transformations
- KPI-breaking enrichment

Every transformation must answer:

> “How does this improve business truth?”

NOT:

> “Can Spark perform this transformation?”

---

# 2. Core Silver Engineering Principles

The Silver Layer follows seven mandatory engineering principles.

---

## 2.1 Business-Driven Transformations

Every transformation must have:

# explicit business justification

Example:

| Bad Transformation                         | Why Wrong          |
| ------------------------------------------ | ------------------ |
| Remove canceled orders because nulls exist | Arbitrary cleaning |

Correct approach:

| Correct Transformation                              | Why Correct                               |
| --------------------------------------------------- | ----------------------------------------- |
| Exclude canceled orders from delivery KPI mart only | Delivery KPIs require completed lifecycle |

This preserves:

- business meaning
- KPI integrity
- analytical defensibility

---

## 2.2 Grain Preservation

Before every transformation:
the pipeline validates:

# dataset grain integrity

The most important question is:

```text
What does one row represent?
```

Examples:

| Dataset     | Grain                   |
| ----------- | ----------------------- |
| orders      | One customer order      |
| order_items | One seller item event   |
| payments    | One payment transaction |
| reviews     | One review event        |

Transformations must NEVER:

- merge incompatible grains
- create fan-out duplication
- duplicate operational events

This principle directly protects:

# fact table correctness

---

## 2.3 Controlled Information Loss

The Silver Layer follows:

# zero silent data loss policy

Meaning:
rows may only be removed when:

- explicitly documented
- business justified
- validated before and after

Example:

| Action                                         | Allowed? |
| ---------------------------------------------- | -------- |
| Remove corrupted duplicate geolocations        | Yes      |
| Remove null reviews silently                   | No       |
| Exclude canceled deliveries from delivery mart | Yes      |
| Delete late orders due to nulls                | No       |

---

## 2.4 Validation-Driven Engineering

Every transformation requires:

# before vs after validation

Validation categories:

| Validation Type         | Purpose                     |
| ----------------------- | --------------------------- |
| Row-count validation    | Detect lost records         |
| Distinct-key validation | Detect duplication          |
| Null analysis           | Detect new corruption       |
| KPI reconciliation      | Detect metric drift         |
| Distribution validation | Detect abnormal shifts      |
| Timestamp validation    | Preserve temporal integrity |

Transformations are considered:

# invalid

until validated.

---

## 2.5 Reproducibility

All Silver transformations must be:

# deterministic and reproducible

Meaning:
same input → same output.

The pipeline avoids:

- manual intervention
- notebook-only logic
- hidden business rules

This supports:

- Airflow orchestration
- pipeline replay
- auditability
- enterprise maintainability

---

## 2.6 Transformation Documentation

Every transformation must be documented with:

| Required Element       | Purpose                   |
| ---------------------- | ------------------------- |
| Source column meaning  | Operational understanding |
| Transformation logic   | Technical transparency    |
| Business justification | KPI trust                 |
| Validation strategy    | Engineering trust         |
| Risks/assumptions      | Analytical defensibility  |

Undocumented transformations are considered:

# invalid engineering practice

---

## 2.7 Operational Truth Preservation

The Silver Layer intentionally preserves:

# operational anomalies

when they represent:

- business failures
- seller issues
- logistics problems
- customer dissatisfaction signals

Example:

| Data Pattern          | Interpretation               |
| --------------------- | ---------------------------- |
| Missing delivery date | Potential failed fulfillment |
| Delayed approval      | Operational payment issue    |
| High freight ratio    | Logistics burden             |
| Multi-payment orders  | Financing behavior           |

The pipeline avoids:

# over-cleaning

because dirty operational data often contains:

# the most valuable intelligence

---

# 3. Silver Layer Responsibilities

The Silver Layer performs:

# analytical refinement transformations

---

## Included Responsibilities

| Responsibility                  | Included |
| ------------------------------- | -------- |
| Type standardization            | Yes      |
| Timestamp parsing               | Yes      |
| Controlled deduplication        | Yes      |
| Null handling                   | Yes      |
| Business-rule filtering         | Yes      |
| Derived operational metrics     | Yes      |
| Geographic enrichment           | Yes      |
| Standardized categorical values | Yes      |
| Distance classification         | Yes      |
| Seller operational enrichment   | Yes      |

---

## Excluded Responsibilities

| Responsibility             | Excluded |
| -------------------------- | -------- |
| Final star schema modeling | No       |
| Dashboard calculations     | No       |
| Final KPI aggregation      | No       |
| Visualization logic        | No       |
| ML scoring                 | No       |

Those belong to:

# Gold marts and analytical layers

---

# 4. Silver Layer Dataset Strategy

The Silver layer transforms:

# Bronze datasets into trusted staging entities

---

## Core Silver Datasets

| Silver Dataset     | Purpose                            |
| ------------------ | ---------------------------------- |
| silver_orders      | Trusted order lifecycle            |
| silver_order_items | Trusted seller fulfillment         |
| silver_customers   | Geographic customer entity         |
| silver_sellers     | Seller operational entity          |
| silver_products    | Product logistics enrichment       |
| silver_reviews     | Customer satisfaction staging      |
| silver_payments    | Financial behavior staging         |
| silver_geolocation | Deduplicated geographic enrichment |

---

# 5. Transformation Categories

The Silver layer organizes transformations into:

# five transformation domains

---

## 5.1 Structural Transformations

Purpose:

# schema consistency

Examples:

- type casting
- timestamp conversion
- decimal normalization
- column renaming

---

## 5.2 Quality Transformations

Purpose:

# controlled data integrity

Examples:

- duplicate handling
- invalid ZIP removal
- corrupted timestamp filtering

---

## 5.3 Standardization Transformations

Purpose:

# analytical consistency

Examples:

- lowercase city names
- trimmed categorical fields
- standardized order statuses

---

## 5.4 Enrichment Transformations

Purpose:

# business intelligence enhancement

Examples:

- geographic region derivation
- product volume calculation
- distance bucket generation
- seller operational metrics

---

## 5.5 Business Rule Transformations

Purpose:

# KPI-safe analytical preparation

Examples:

- delivered-order filtering
- single-seller operational isolation
- delivery severity categorization

---

# 6. Dataset-Level Transformation Governance

---

# 6.1 `silver_orders`

## Purpose

Trusted operational order lifecycle dataset.

---

## Key Transformations

| Column                   | Transformation      | Business Reason              |
| ------------------------ | ------------------- | ---------------------------- |
| order_purchase_timestamp | cast to timestamp   | temporal analytics           |
| order_status             | standardized casing | KPI consistency              |
| delivery timestamps      | temporal validation | prevent impossible timelines |
| delay_days               | derived metric      | delivery intelligence        |
| buffer_days              | derived metric      | delivery padding analysis    |

---

## Important Validation Rules

| Validation                                       | Rule               |
| ------------------------------------------------ | ------------------ |
| purchase <= approval                             | must hold          |
| approval <= delivery                             | expected lifecycle |
| estimated_delivery not null for delivered orders | required           |
| duplicate order_id                               | prohibited         |

---

# 6.2 `silver_order_items`

## Purpose

Trusted seller fulfillment staging.

---

## Key Transformations

| Column                 | Transformation          | Business Reason          |
| ---------------------- | ----------------------- | ------------------------ |
| freight_value          | decimal standardization | financial accuracy       |
| product volume         | derived metric          | logistics intelligence   |
| freight_ratio          | derived metric          | shipping burden analysis |
| seller_count per order | aggregation             | seller accountability    |

---

## Important Validation Rules

| Validation           | Rule       |
| -------------------- | ---------- |
| freight_value >= 0   | required   |
| item_price >= 0      | required   |
| duplicate item grain | prohibited |
| orphan product_id    | monitored  |

---

# 6.3 `silver_reviews`

## Purpose

Trusted customer satisfaction staging.

---

## Key Transformations

| Column             | Transformation         | Business Reason        |
| ------------------ | ---------------------- | ---------------------- |
| review_score       | integer validation     | sentiment correctness  |
| sentiment_category | derived classification | dashboard storytelling |
| text_exists_flag   | derived indicator      | NLP readiness          |

---

## Important Validation Rules

| Validation                | Rule       |
| ------------------------- | ---------- |
| review_score between 1–5  | required   |
| duplicate review_id       | prohibited |
| review timestamp validity | required   |

---

# 6.4 `silver_payments`

## Purpose

Trusted financial transaction staging.

---

## Key Transformations

| Column             | Transformation     | Business Reason        |
| ------------------ | ------------------ | ---------------------- |
| payment_type       | standardization    | payment analytics      |
| installment flags  | derived metrics    | financing intelligence |
| split payment flag | window calculation | financial behavior     |

---

## Important Validation Rules

| Validation         | Rule       |
| ------------------ | ---------- |
| payment_value >= 0 | required   |
| installments > 0   | required   |
| orphan order_id    | prohibited |

---

# 6.5 `silver_geolocation`

## Purpose

Trusted geographic enrichment staging.

---

## Major Architectural Challenge

The Olist geolocation dataset contains:

- duplicate ZIP prefixes
- inconsistent coordinates
- noisy geographic records

---

## Final Strategy

The project uses:

# median coordinate aggregation

per ZIP prefix.

Reason:
this creates:

- stable geographic enrichment
- reduced noise
- consistent distance analysis

WITHOUT:

- pretending coordinates are exact addresses

This is:

# responsible geographic modeling

---

# 7. Transformation Validation Framework

Every Silver pipeline stage produces:

# validation reports

---

## Mandatory Validation Metrics

| Metric             | Purpose                  |
| ------------------ | ------------------------ |
| source_row_count   | ingestion integrity      |
| output_row_count   | transformation integrity |
| duplicate_count    | grain protection         |
| null_distribution  | data quality             |
| rejected_records   | controlled filtering     |
| KPI reconciliation | analytical consistency   |

---

# 8. Business Rule Registry

All business rules must exist inside:

# centralized documented registry

Recommended file:

```text
docs/modeling/business_rules.md
```

Example:

| Rule ID | Rule                                           |
| ------- | ---------------------------------------------- |
| BR-001  | Delivered orders required for delivery KPIs    |
| BR-002  | Single-seller orders for seller accountability |
| BR-003  | Review scores restricted to 1–5                |

This prevents:

- hidden logic
- inconsistent KPIs
- undocumented assumptions

---

# 9. Relationship to Gold Layer

The Silver Layer feeds:

# dimensional models and fact marts

Silver outputs become:

- conformed dimensions
- operational metrics
- delivery intelligence
- seller enrichment
- streaming baselines

The Gold layer should NEVER:

# re-clean Silver logic

because Silver becomes:

# trusted transformation foundation

---

# 10. Common Silver Layer Mistakes Avoided

---

## Mistake 1 — Aggressive Null Removal

Wrong:
removing operational anomalies blindly.

Correct:
understand WHY null exists.

---

## Mistake 2 — Mixed-Grain Joins

Wrong:
joining payments directly to order items without grain awareness.

Correct:
preserve independent business processes.

---

## Mistake 3 — KPI Derivation Without Validation

Wrong:
calculating metrics before lifecycle validation.

Correct:
validate timestamps first.

---

## Mistake 4 — Undocumented Transformations

Wrong:
hidden business logic.

Correct:
centralized rule registry.

---

## Mistake 5 — Dashboard-Driven Cleaning

Wrong:
cleaning data to “look nicer.”

Correct:
preserve operational truth.

---

# 11. Recommended Silver Folder Structure

```text
data/silver/

├── orders/
├── order_items/
├── customers/
├── sellers/
├── products/
├── payments/
├── reviews/
└── geolocation/
```

---

# 12. Recommended Documentation Structure

```text
docs/modeling/

├── silver_transformation_strategy.md
├── business_rules.md
├── null_handling_rules.md
├── transformation_validation.md
└── grain_definitions.md
```

---

# 13. Final Architectural Outcome

The Silver Layer transforms:

# raw operational Olist data

into:

# trusted analytical staging datasets

through:

- validation-driven engineering
- business-governed transformations
- grain-preserving logic
- controlled enrichment
- operational truth refinement

The final Silver architecture provides:

- KPI trustworthiness
- scalable dimensional foundations
- streaming enrichment readiness
- enterprise-grade transformation governance
- analytically defensible business intelligence

while preserving:

- operational truth
- grain integrity
- reproducibility
- maintainability
- business coherence
