# Sprint 3 — Reviews Hardening Report

## Dataset

```text
silver_reviews
```

---

# Objective

The purpose of Sprint 3 was to transform customer reviews from a raw feedback dataset into a trusted analytical asset.

This sprint introduced:

- review governance
- referential integrity validation
- quarantine architecture
- review enrichment
- sentiment classification
- customer experience intelligence

The objective was to ensure that every review can be traced to a valid customer order and can be safely used in downstream analytics.

---

# Business Problem

Customer reviews are one of the most important datasets in the Olist platform.

Reviews influence:

- seller reputation
- customer satisfaction analysis
- delivery performance analysis
- seller performance scoring
- executive dashboards

However, raw review data may contain:

- invalid references
- duplicate records
- incomplete business context

Without validation, these issues can distort business insights.

---

# Architecture Before Hardening

```text
Bronze Reviews
        ↓
Silver Reviews
```

All reviews flowed directly into analytics.

No governance layer existed.

---

# Architecture After Hardening

```text
Bronze Reviews
        ↓

Review Governance
        ↓

 ┌─────────────────┬─────────────────┐
 │                 │
 ↓                 ↓

Silver Reviews     Reviews Quarantine
(Clean)            (Invalid)
```

This introduces enterprise-grade review governance.

---

# Hardening Components Implemented

## 1. Review Deduplication

Reviews are deduplicated using:

```text
review_id
```

When duplicates exist:

```text
Latest review_answer_timestamp
```

is retained.

This ensures:

- one business review
- one analytical record

---

# 2. Referential Integrity Validation

Every review must belong to a valid order.

Relationship:

```text
review
      ↓
order_id
      ↓
silver_orders
```

If the parent order does not exist:

```text
ORPHAN_REVIEW
```

is assigned.

These reviews are quarantined.

---

# 3. Missing Business Context Validation

The following rule was implemented:

```text
review_creation_date IS NULL
AND
review_answer_timestamp IS NULL
```

Records matching this condition are quarantined.

These reviews lack temporal business context.

---

# 4. Null Order Validation

The following rule was implemented:

```text
order_id IS NULL
```

Reviews without an associated order are quarantined.

These records cannot be linked to a transaction.

---

# Review Enrichment

The Silver layer now derives additional business attributes.

---

## review_label

Customer sentiment classification:

| Review Score | Label    |
| ------------ | -------- |
| 1–2          | Negative |
| 3            | Neutral  |
| 4–5          | Positive |

This creates a reusable sentiment dimension.

---

## review_response_days

Measures:

```text
Review Creation
        ↓
Review Response
```

Used to evaluate customer service responsiveness.

---

## review_context

Customer feedback is categorized as:

| Context            |
| ------------------ |
| Delivery Related   |
| Product Related    |
| General Experience |

Classification uses:

- review sentiment
- delivery delay behavior

This creates actionable customer experience intelligence.

---

# Delivery Context Integration

Reviews are enriched using:

```text
silver_orders
```

Additional delivery attributes added:

- delivery_duration_days
- delay_days
- delivery_status_category

This enables:

```text
Customer Feedback
        +
Delivery Performance
```

analysis.

---

# Validation Results

## Quarantine Summary

```text
Total Quarantined Reviews: 1380
```

| Reason        | Count |
| ------------- | ----- |
| ORPHAN_REVIEW | 1380  |

---

# Observations

No records were found for:

```text
NULL_ORDER_ID
```

and

```text
MISSING_REVIEW_TIMESTAMPS
```

This indicates the source review dataset has stronger quality than originally expected.

---

# Relationship Analysis

Sprint 1 quarantined:

```text
1390 orders
```

Sprint 3 quarantined:

```text
1380 reviews
```

This strongly suggests that nearly all quarantined reviews were associated with orders removed during Orders Hardening.

This validates the referential integrity framework implemented across the Silver layer.

---

# Business Impact

## Customer Satisfaction Analytics

Improves:

- sentiment reporting
- customer experience analysis
- review trend analysis

---

## Seller Performance Analytics

Improves:

- seller reputation scoring
- customer feedback attribution
- seller benchmarking

---

## Delivery Analytics

Enables:

```text
Review Sentiment
        +
Delivery Outcomes
```

correlation analysis.

---

## Power BI Reporting

Creates trusted metrics for:

- sentiment KPIs
- customer satisfaction dashboards
- seller scorecards

---

# Architectural Significance

This sprint introduces:

# Customer Experience Governance

within the Silver layer.

The Silver layer now guarantees:

```text
Valid Review
        ↓
Valid Order
```

before records enter:

- staging datasets
- Gold facts
- Power BI dashboards
- streaming intelligence systems

---

# Final Status

## Sprint 3 — Reviews Hardening

Status:

```text
COMPLETED SUCCESSFULLY
```

Results:

- Review governance implemented
- Referential integrity restored
- Quarantine architecture implemented
- Sentiment classification added
- Delivery context enrichment added
- Customer experience intelligence introduced

The `silver_reviews` dataset is now considered:

```text
TRUSTED CUSTOMER EXPERIENCE DATA
```

for downstream analytical processing.
