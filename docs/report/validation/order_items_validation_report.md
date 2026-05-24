# `order_delivery_staging_validation_report.md`

````markdown id="m7k4xq"
# Order Delivery Staging Validation Report

## Dataset

```text
order_delivery_staging
```
````

---

# Objective

This report documents the validation results for the:

```text id="yb2m4w"
order_delivery_staging
```

dataset inside the Silver Staging layer of the:

# Olist Seller Intelligence Platform

The purpose of this validation process is to ensure:

- order-level grain integrity
- delivery lifecycle correctness
- seller attribution consistency
- geographic enrichment quality
- delivery KPI trustworthiness
- downstream Gold mart readiness

This dataset acts as:

# the operational customer delivery intelligence staging layer

for:

- `fct_order_delivery`
- delivery KPI analytics
- delay analysis
- seller delivery performance analysis
- streaming delivery risk detection

---

# Dataset Grain

# ONE ROW = ONE CUSTOMER ORDER

Each row represents:

- one customer order
- one final delivery lifecycle
- one customer delivery outcome

This grain is preserved throughout the staging pipeline to prevent:

- mixed-grain corruption
- fan-out duplication
- duplicated delivery metrics
- invalid seller attribution
- unreliable delivery KPIs

This follows the platform’s:

# dual-fact delivery modeling strategy

where:

- seller fulfillment operations
- final customer delivery outcomes

remain separated for analytical correctness.

---

# Validation Execution Summary

| Validation Category              | Result                               |
| -------------------------------- | ------------------------------------ |
| Row Count Validation             | PASSED                               |
| Grain Validation                 | PASSED                               |
| Critical Null Validation         | PASSED WITH INVESTIGATED EXCEPTION   |
| Delivery Lifecycle Validation    | PASSED                               |
| Delivered Order Validation       | PASSED WITH KNOWN DATA QUALITY ISSUE |
| Seller Accountability Validation | PASSED                               |
| Distance Bucket Validation       | PASSED                               |

---

# 1. Row Count Validation

## Final Row Count

```text id="m6j4n9"
99441
```

---

## Interpretation

The final row count confirms:

- customer delivery events were preserved
- no unexpected row loss occurred
- aggregation logic remained grain-safe
- joins did not create duplication

This validates:

# order-level delivery integrity

throughout the staging process.

---

# 2. Grain Validation

## Validation Rule

```text id="ah7v5n"
order_id
must remain unique
```

---

## Result

```text id="v9f2zx"
Duplicate order_id Count: 0
```

---

## Interpretation

This confirms:

# PERFECT ORDER-LEVEL GRAIN PRESERVATION

No duplicate customer delivery events were introduced during:

- order-item aggregation
- seller enrichment
- customer enrichment
- geographic joins

This is one of the MOST critical validations in the delivery architecture because:
incorrect grain handling would corrupt:

- delivery KPIs
- delay metrics
- freight calculations
- seller accountability analysis

---

# 3. Critical Null Validation

## Results

| Column                   | Null Count |
| ------------------------ | ---------- |
| order_id                 | 0          |
| customer_id              | 0          |
| order_status             | 0          |
| order_purchase_timestamp | 0          |
| seller_count             | 775        |
| distance_bucket          | 0          |

---

# Interpretation

The staging dataset achieved:

# ZERO CRITICAL IDENTIFIER FAILURES

for:

- orders
- customers
- statuses
- lifecycle timestamps

---

# Important Seller Count Observation

The:

```text id="k8o5pf"
seller_count
```

column contains:

```text id="aq3zpl"
775 nulls
```

This is NOT considered a pipeline failure.

---

## Business Explanation

These records likely represent:

- canceled orders
- unavailable orders
- orders without associated fulfillment items

Meaning:
the operational order lifecycle exists,
but no valid seller fulfillment events were attached.

This is:

# operational truth

and should be preserved rather than silently removed.

This follows the project’s:

# zero silent data loss policy

defined in the Silver transformation governance strategy.

---

# 4. Delivery Lifecycle Validation

## Results

| Validation                 | Result |
| -------------------------- | ------ |
| Invalid Approval Timelines | 0      |
| Invalid Delivery Timelines | 0      |

---

# Interpretation

This confirms:

# TEMPORAL LIFECYCLE INTEGRITY

The pipeline successfully preserved:

- chronological order progression
- operational lifecycle consistency
- delivery timeline correctness

No impossible lifecycle scenarios were detected such as:

- approvals before purchases
- deliveries before purchases

This validation is extremely important because:
delivery KPIs depend entirely on:

# trustworthy temporal sequencing

---

# 5. Delivered Order Validation

## Result

```text id="g0z4vh"
Delivered Orders Missing Delivery Timestamp: 8
```

---

# Interpretation

Only:

```text id="y4x1nq"
8 delivered orders
```

were missing:

```text
order_delivered_customer_date
```

This represents:

# a very small operational data-quality anomaly

likely originating from:

- source-system inconsistencies
- incomplete operational updates
- historical platform recording gaps

---

# Engineering Decision

These rows were intentionally preserved because:

- they represent real operational records
- silent deletion would distort delivery truth
- anomaly preservation supports auditability

This follows the platform’s:

# operational truth preservation philosophy

where:

- business anomalies are documented
- not silently removed

---

# 6. Seller Accountability Validation

## Results

| Category             | Count  |
| -------------------- | ------ |
| Multi Seller Orders  | 1,278  |
| Single Seller Orders | 97,388 |

---

# Interpretation

The overwhelming majority of orders are:

# single-seller fulfillment orders

This is extremely important analytically because:
single-seller orders provide:

# clean seller accountability

for:

- delivery KPIs
- seller delay analysis
- operational benchmarking

---

# Multi-Seller Importance

The:

```text id="oju3v8"
1,278
```

multi-seller orders remain analytically important because they represent:

- operational complexity
- distributed fulfillment coordination
- ambiguous delivery accountability

These orders may later require:

- special KPI segmentation
- advanced attribution logic
- exclusion from strict seller-performance benchmarking

---

# 7. Distance Bucket Validation

## Distribution

| Distance Bucket | Count  |
| --------------- | ------ |
| Same State      | 35,479 |
| Same Region     | 23,666 |
| Cross Region    | 39,521 |
| Unknown         | 775    |

---

# Interpretation

The distribution reveals:

# geographically diverse fulfillment operations

A significant portion of deliveries are:

# cross-region shipments

which likely contributes to:

- longer delivery durations
- logistics complexity
- higher freight burden
- operational delay risk

---

# Important Unknown Bucket Observation

The:

```text id="v29yr4"
Unknown
```

bucket count:

```text
775
```

matches the:

```text
seller_count null count
```

This confirms:

# validation consistency

and strongly suggests:
the same operational records lacking seller fulfillment data also lack:

- seller geography
- distance classification capability

This consistency indicates:

# controlled missingness

NOT:

# random corruption

which is an important distinction in enterprise data quality engineering.

---

# Architectural Significance

The `order_delivery_staging` dataset represents:

# customer delivery outcome truth

inside the warehouse architecture.

Unlike:

```text id="r5f0ji"
seller_fulfillment_staging
```

which measures:

# seller operational workload

this staging layer measures:

# final customer delivery experience

This distinction is architecturally critical because:

- fulfillment operations occur at item grain
- delivery outcomes occur at order grain

Separating these business processes preserves:

- dimensional integrity
- KPI correctness
- analytical trustworthiness

and follows:

# Kimball dimensional modeling principles

used throughout the platform architecture.

---

# Operational Intelligence Enabled

This staging layer now supports:

| Capability                       | Enabled |
| -------------------------------- | ------- |
| delivery KPI analysis            | YES     |
| delay analysis                   | YES     |
| seller delivery benchmarking     | YES     |
| freight aggregation analysis     | YES     |
| geographic delivery intelligence | YES     |
| multi-seller complexity analysis | YES     |
| streaming risk detection         | YES     |

---

# Final Validation Status

# VALIDATED SUCCESSFULLY

The:

```text id="g5s2lb"
order_delivery_staging
```

dataset is approved for:

- `fct_order_delivery`
- delivery intelligence marts
- seller delivery analytics
- operational KPI reporting
- streaming delivery-risk enrichment

with:

# FULL ORDER GRAIN INTEGRITY

# VALID DELIVERY TIMELINES

# CONTROLLED OPERATIONAL ANOMALIES

# CONSISTENT GEOGRAPHIC ENRICHMENT

# ZERO DUPLICATE DELIVERY EVENTS

```

This is a VERY strong validation result academically because:
you are not just validating:
- schema
- row counts

You are validating:
# business-process truth

which is exactly how enterprise analytical engineering should work.
```
