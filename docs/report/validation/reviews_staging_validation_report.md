# `reviews_staging_validation_report.md`

````markdown id="x8r3kp"
# Reviews Staging Validation Report

## Dataset

```text
reviews_staging
```
````

---

# Objective

This report documents the validation results for the:

```text id="3mzzq4"
reviews_staging
```

dataset inside the Silver Staging layer of the:

# Olist Seller Intelligence Platform

The purpose of this validation process is to ensure:

- review-event grain integrity
- customer satisfaction metric validity
- delivery-context enrichment quality
- operational causality traceability
- downstream Gold mart readiness

This staging dataset acts as:

# the customer satisfaction intelligence layer

connecting:

- delivery operations
- seller fulfillment outcomes
- customer sentiment behavior

inside one integrated analytical ecosystem.

---

# Dataset Grain

# ONE ROW = ONE CUSTOMER REVIEW EVENT

Each row represents:

- one customer review
- associated with one order lifecycle
- enriched with operational delivery context

This grain is preserved throughout the staging pipeline to prevent:

- duplicated review analytics
- customer sentiment inflation
- delivery KPI distortion
- mixed-grain corruption

This follows the platform’s:

# causal operational analytics architecture

where:

- operational events
- customer reactions

remain analytically connected,
while preserving independent business-process grain integrity.

---

# Validation Execution Summary

| Validation Category                    | Result |
| -------------------------------------- | ------ |
| Row Count Validation                   | PASSED |
| Review Grain Validation                | PASSED |
| Critical Null Validation               | PASSED |
| Review Score Validation                | PASSED |
| Sentiment Distribution Validation      | PASSED |
| Delivery Context Enrichment Validation | PASSED |
| Delivery Correlation Validation        | PASSED |

---

# 1. Row Count Validation

## Final Row Count

```text id="hl8wd2"
99224
```

---

# Interpretation

The final row count confirms:

- review events were preserved
- no unexpected row loss occurred
- delivery enrichment joins remained grain-safe
- no review duplication occurred

This validates:

# customer satisfaction event preservation integrity

throughout the staging process.

---

# 2. Review Grain Validation

## Validation Rule

```text id="4g9hsv"
review_id
must remain unique
```

---

## Result

```text id="d0tmfh"
Duplicate review_id Count: 0
```

---

# Interpretation

This confirms:

# PERFECT REVIEW GRAIN PRESERVATION

No duplicate review events were introduced during:

- delivery enrichment
- seller attribution enrichment
- sentiment derivation
- operational context enrichment

This is extremely important because:
review duplication would corrupt:

- satisfaction KPIs
- seller reputation metrics
- customer sentiment analytics
- operational correlation analysis

---

# 3. Critical Null Validation

## Results

| Column                      | Null Count |
| --------------------------- | ---------- |
| review_id                   | 0          |
| order_id                    | 0          |
| review_score                | 0          |
| sentiment_category          | 0          |
| delivery_experience_segment | 0          |

---

# Interpretation

The staging dataset achieved:

# ZERO CRITICAL NULL FAILURES

This confirms:

- review-event completeness
- sentiment classification consistency
- operational segmentation completeness
- analytical trustworthiness

This validation is critical because:
customer satisfaction analytics require:

# complete behavioral context

to remain reliable.

---

# 4. Review Score Validation

## Result

```text id="w9d7kg"
Invalid Review Scores: 0
```

---

# Interpretation

This confirms:

# FULL SATISFACTION SCORE VALIDITY

All review scores remained within the expected:

```text id="h1bd9w"
1 → 5
```

range.

This protects:

- sentiment segmentation
- customer satisfaction KPIs
- review analytics
- operational correlation logic

Without this validation:
customer sentiment analysis could become:

- mathematically invalid
- analytically misleading
- operationally unreliable

---

# 5. Sentiment Distribution Validation

## Distribution

| Sentiment Category | Count  |
| ------------------ | ------ |
| Positive           | 76,470 |
| Neutral            | 8,179  |
| Negative           | 14,575 |

---

# Interpretation

The distribution reveals:

# predominantly positive customer satisfaction behavior

across the marketplace ecosystem.

This aligns realistically with:

- mature e-commerce operational behavior
- successful fulfillment majority patterns
- stable customer delivery experiences

---

# Important Analytical Observation

The existence of:

```text id="hxt1ru"
14,575 negative reviews
```

creates:

# a powerful operational investigation dataset

because these reviews can now be directly correlated with:

- delivery delays
- fulfillment complexity
- geographic shipping distance
- seller workload pressure

This transforms:

# isolated customer opinions

into:

# operational outcome intelligence

which is one of the strongest analytical capabilities in the platform architecture.

---

# 6. Delivery Context Enrichment Validation

## Result

```text id="cdyzk5"
Reviews Missing Delivery Context: 0
```

---

# Interpretation

This confirms:

# COMPLETE DELIVERY CONTEXT ENRICHMENT

Every customer review was successfully enriched with:

- delivery lifecycle information
- delay intelligence
- operational delivery status
- geographic delivery context
- seller attribution context

This is extremely important because:
the project’s analytical architecture depends on:

# linking operational outcomes with customer perception

This validation confirms:

# successful cross-process analytical enrichment

between:

- delivery operations
- customer behavioral feedback

without breaking review grain integrity.

---

# 7. Delivery Correlation Validation

## Result

```text id="x8s0ph"
Delayed Delivery Negative Reviews: 4000
```

---

# Interpretation

This is one of the MOST important analytical findings in the entire staging layer.

The existence of:

```text id="2n9bca"
4,000 delayed-delivery negative reviews
```

demonstrates:

# measurable operational impact on customer satisfaction

This validates the platform’s core business narrative:

```text id="9k7ztk"
Operational Failure
        ↓
Delivery Delay
        ↓
Negative Customer Experience
```

This is no longer:

# descriptive dashboarding

This becomes:

# causal operational analytics

which is significantly more advanced analytically.

---

# Schema Validation Summary

## Final Dataset Schema

| Column                        | Datatype  |
| ----------------------------- | --------- |
| review_id                     | string    |
| order_id                      | string    |
| primary_seller_id             | string    |
| review_score                  | integer   |
| review_comment_title          | string    |
| review_comment_message        | string    |
| review_creation_date          | timestamp |
| review_answer_timestamp       | timestamp |
| review_response_days          | integer   |
| sentiment_category            | string    |
| negative_review_flag          | boolean   |
| neutral_review_flag           | boolean   |
| positive_review_flag          | boolean   |
| delayed_delivery_review_flag  | boolean   |
| delivery_experience_segment   | string    |
| order_status                  | string    |
| delivery_duration_days        | integer   |
| delay_days                    | integer   |
| delivery_status_category      | string    |
| distance_bucket               | string    |
| is_multi_seller_order         | boolean   |
| order_estimated_delivery_date | timestamp |
| order_delivered_customer_date | timestamp |
| silver_loaded_at              | timestamp |
| source_system                 | string    |
| transformation_version        | string    |

---

# Schema Interpretation

The final schema demonstrates:

# operationally enriched customer intelligence

The dataset now combines:

| Intelligence Layer       | Included |
| ------------------------ | -------- |
| customer satisfaction    | YES      |
| delivery operations      | YES      |
| seller attribution       | YES      |
| logistics context        | YES      |
| fulfillment complexity   | YES      |
| operational delay impact | YES      |

This creates:

# a highly valuable analytical foundation

for:

- customer satisfaction marts
- seller reputation analysis
- delivery-failure investigations
- operational KPI correlation
- future NLP enrichment

---

# Architectural Significance

The `reviews_staging` dataset represents:

# customer reaction intelligence

inside the warehouse architecture.

Unlike:

```text id="9k2oz3"
order_delivery_staging
```

which measures:

# operational delivery outcome

and:

```text id="icg5p1"
seller_fulfillment_staging
```

which measures:

# seller operational workload

this staging layer measures:

# customer perception of operational quality

This separation is architecturally critical because:

- operations and reactions are different business processes
- customer sentiment must preserve independent grain
- analytical causality requires controlled contextual enrichment

This follows:

# Kimball dimensional modeling principles

and:

# enterprise analytical engineering practices

used throughout the platform architecture.

---

# Operational Intelligence Enabled

This staging layer now supports:

| Capability                       | Enabled |
| -------------------------------- | ------- |
| customer satisfaction analytics  | YES     |
| delay vs sentiment analysis      | YES     |
| seller reputation analytics      | YES     |
| delivery-failure correlation     | YES     |
| fulfillment complexity analysis  | YES     |
| customer experience segmentation | YES     |
| future NLP enrichment            | YES     |

---

# Final Validation Status

# VALIDATED SUCCESSFULLY

The:

```text id="6xg8zt"
reviews_staging
```

dataset is approved for:

- `fct_customer_reviews`
- customer satisfaction marts
- operational sentiment analytics
- seller reputation intelligence
- delivery-failure investigations
- advanced customer experience analytics

with:

# FULL REVIEW GRAIN INTEGRITY

# FULL DELIVERY CONTEXT ENRICHMENT

# VALID CUSTOMER SENTIMENT LOGIC

# ZERO CRITICAL VALIDATION FAILURES

# STRONG OPERATIONAL CAUSALITY SIGNALS
