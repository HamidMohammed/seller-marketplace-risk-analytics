# Orders Hardening Sprint Report

## Dataset

```text
silver_orders
```

---

# Objective

This sprint introduced the first major Silver Layer hardening initiative for the Olist Seller Intelligence Platform.

The objective was to transform the existing Silver Orders dataset from a standard transformation layer into a business-truth-preserving analytical foundation by:

- identifying operational inconsistencies
- quarantining invalid business events
- enriching lifecycle analytics
- protecting downstream facts and marts

This sprint represents the transition from:

```text
Silver Transformation
```

to

```text
Silver Data Quality Governance
```

inside the warehouse architecture.

---

# Why This Sprint Was Necessary

During exploratory data analysis (EDA), several order lifecycle anomalies were identified.

The original Silver pipeline correctly transformed orders but did not isolate business-invalid records.

This created the risk of:

- corrupted delivery KPIs
- inaccurate seller performance metrics
- misleading operational analytics
- unreliable streaming baselines

The hardening sprint addressed these risks.

---

# Architecture Before Hardening

```text
Bronze Orders
      ↓
Silver Orders
      ↓
Delivery Mart
      ↓
Seller Performance
```

All records flowed downstream regardless of lifecycle validity.

---

# Architecture After Hardening

```text
Bronze Orders
      ↓
Business Rule Validation
      ↓
 ┌───────────────┬───────────────┐
 │               │
 ↓               ↓
Silver Orders    Orders Quarantine
(Clean)          (Invalid)
```

This architecture preserves:

- analytical trust
- auditability
- lineage
- operational transparency

without silently deleting data.

---

# Hardening Components Implemented

## 1. Chronology Validation

### Business Rule

Order lifecycle events must occur in chronological order.

Valid sequence:

```text
Purchase
    ↓
Approval
    ↓
Carrier Pickup
    ↓
Customer Delivery
```

Invalid sequences indicate operational contradictions.

Examples:

```text
Approval before purchase
Carrier pickup before approval
Customer delivery before carrier pickup
```

---

## Result

```text
Chronology Violations: 1382
```

These records were quarantined.

---

## Business Impact

Without this validation:

- delivery duration becomes unreliable
- delay calculations become misleading
- seller performance metrics become distorted

This is one of the highest-value data quality checks in the platform.

---

# 2. Delivered Orders Missing Delivery Timestamp

### Business Rule

If:

```text
order_status = delivered
```

then:

```text
order_delivered_customer_date
```

must exist.

---

## Validation Results

EDA initially found:

```text
2965 orders
with missing delivery timestamps
```

However, business-rule analysis showed:

| Status      | Count |
| ----------- | ----- |
| shipped     | 1107  |
| canceled    | 619   |
| unavailable | 609   |
| invoiced    | 314   |
| processing  | 301   |
| created     | 5     |
| approved    | 2     |
| delivered   | 8     |

Only:

```text
8 delivered orders
```

were true business inconsistencies.

---

## Result

```text
Delivered Missing Delivery Date: 8
```

These records were quarantined.

---

## Business Impact

This validation prevents:

- false delivery completion
- inaccurate SLA calculations
- incorrect delivery success reporting

---

# Quarantine Architecture

A dedicated quarantine dataset was introduced.

## Dataset

```text
silver/quarantine/orders/
```

---

## Quarantine Categories

| Reason                          | Count |
| ------------------------------- | ----- |
| CHRONOLOGY_VIOLATION            | 1382  |
| DELIVERED_WITHOUT_DELIVERY_DATE | 8     |

---

## Total Quarantined

```text
1390
```

---

# Why Quarantine Instead of Delete

The project follows:

# Zero Silent Data Loss Policy

Meaning:

- invalid records remain available
- auditability is preserved
- business investigations remain possible
- lineage remains intact

This follows enterprise data engineering practices.

---

# New Lifecycle Metrics Added

Several operational metrics were introduced.

---

## handling_days

Measures:

```text
Approval → Carrier Pickup
```

Represents seller processing time.

---

## shipping_days

Measures:

```text
Carrier Pickup → Customer Delivery
```

Represents logistics performance.

---

## total_lead_time

Measures:

```text
Purchase → Delivery
```

Represents full customer wait time.

---

## days_diff_estimated

Measures:

```text
Actual Delivery
vs
Estimated Delivery
```

Represents delivery accuracy.

---

## estimated_buffer

Measures:

```text
Built-in estimation safety margin
```

used by Olist.

---

## abs_days_diff

Measures:

```text
Absolute delivery variance
```

regardless of early or late status.

---

## delivery_status_detail

Extended delivery classification:

| Category      |
| ------------- |
| Very Early    |
| Early         |
| On Time       |
| Slightly Late |
| Severely Late |

This provides richer operational analytics than the original:

```text
Early
Late
On Time
```

classification.

---

# Validation Results

## Quarantine Summary

```text
Total Quarantined Orders: 1390
```

| Reason                          | Count |
| ------------------------------- | ----- |
| CHRONOLOGY_VIOLATION            | 1382  |
| DELIVERED_WITHOUT_DELIVERY_DATE | 8     |

---

## Business Rule Correctness

Validation confirmed:

```text
Only 8 delivered orders
were missing delivery timestamps.
```

All other missing timestamps belonged to non-delivered statuses where null delivery dates are expected.

Therefore:

```text
Hardening Logic = Correct
```

---

# Dataset Impact

Before Hardening:

```text
99,441 orders
```

After Hardening:

```text
98,051 clean orders
```

Quarantined:

```text
1,390 orders
```

---

# Downstream Benefits

This hardening improves:

## Delivery Analytics

- delivery duration accuracy
- delay analysis
- SLA reporting

---

## Seller Performance Analytics

- reliable on-time rates
- cleaner seller benchmarking
- improved risk scoring

---

## Customer Experience Analytics

- trustworthy delivery outcomes
- improved review correlation

---

## Streaming Architecture

The streaming baseline now starts from:

```text
business-valid orders
```

instead of:

```text
raw operational events
```

This significantly improves anomaly detection quality.

---

# Architectural Significance

This sprint marks the introduction of:

# Data Quality Governance

inside the Silver layer.

The Silver layer is no longer only responsible for transformation.

It is now responsible for:

- business-rule enforcement
- operational consistency validation
- quarantine management
- analytical trust preservation

This is a major step toward enterprise-grade data engineering practices.

---

# Final Status

## Sprint 1 — Orders Hardening

Status:

```text
COMPLETED SUCCESSFULLY
```

Results:

- Chronology validation implemented
- Delivery completion validation implemented
- Quarantine architecture implemented
- Lifecycle metrics implemented
- Advanced delivery classifications implemented
- Validation framework upgraded

The Silver Orders dataset is now considered:

```text
Gold-Ready Foundation Data
```

for downstream:

- delivery analytics
- seller performance analytics
- customer satisfaction analytics
- streaming intelligence systems.

```

```
