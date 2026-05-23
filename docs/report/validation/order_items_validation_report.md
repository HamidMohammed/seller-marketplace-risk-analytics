# `order_items_validation_report.md`

## Validation Report Overview

This report documents the validation results for the:

# `silver_order_items`

dataset inside the:

# Olist Seller Intelligence Platform

The validation process follows:

# validation-driven transformation governance

defined in the Silver transformation strategy.

The purpose of this validation layer is to ensure:

- grain integrity
- financial consistency
- logistics correctness
- seller accountability
- operational lifecycle validity
- KPI trustworthiness

before the dataset becomes available for:

- Gold marts
- dashboards
- streaming enrichment
- analytical consumption

---

# Dataset Information

| Attribute         | Value                                       |
| ----------------- | ------------------------------------------- |
| Dataset           | silver_order_items                          |
| Layer             | Silver                                      |
| Dataset Grain     | ONE ROW = ONE SELLER ITEM FULFILLMENT EVENT |
| Validation Status | PASSED WITH WARNINGS                        |
| Output Format     | Parquet                                     |

---

# Validation Scope

The validation framework covered:

| Validation Area                  | Objective                      |
| -------------------------------- | ------------------------------ |
| Row-count integrity              | prevent accidental row loss    |
| Grain validation                 | preserve dataset uniqueness    |
| Critical null validation         | protect operational joins      |
| Financial validation             | ensure KPI-safe values         |
| Freight validation               | protect logistics intelligence |
| Product volume validation        | prevent impossible dimensions  |
| Seller accountability validation | preserve seller attribution    |
| Shipping lifecycle validation    | ensure operational chronology  |
| Multi-seller analysis            | operational enrichment         |
| Product enrichment validation    | enrichment completeness        |

---

# Validation Results

---

# [1] ROW COUNT VALIDATION

## Objective

Ensure no unexpected row loss or row explosion occurred during transformations.

---

## Result

| Metric            | Result |
| ----------------- | ------ |
| Validation Status | PASSED |

---

## Interpretation

The Silver transformation pipeline successfully preserved:

# dataset cardinality integrity

This confirms:

- joins were controlled correctly
- no accidental filtering occurred
- no duplicate row explosion occurred during enrichment

This is critical because:
row-count instability can silently corrupt downstream KPIs.

---

# [2] GRAIN VALIDATION

## Objective

Validate:

# ONE ROW = ONE ORDER ITEM EVENT

using:

```text
(order_id, order_item_id)
```

as the composite business grain.

---

## Result

| Metric            | Result |
| ----------------- | ------ |
| Validation Status | PASSED |

---

## Interpretation

No duplicate fulfillment events were detected.

This confirms:

- seller accountability integrity
- logistics KPI consistency
- downstream fact-table reliability

This validation is one of the MOST important controls in the platform because grain corruption causes:

- fan-out duplication
- inflated metrics
- invalid aggregations
- broken seller attribution

---

# [3] CRITICAL NULL VALIDATION

## Objective

Validate critical business fields required for:

- fulfillment integrity
- logistics analysis
- seller accountability
- dimensional linkage

---

## Validated Columns

| Column        |
| ------------- |
| order_id      |
| order_item_id |
| product_id    |
| seller_id     |
| price         |
| freight_value |

---

## Result

| Metric            | Result |
| ----------------- | ------ |
| Validation Status | PASSED |

---

## Interpretation

Critical operational fields are present and complete.

This ensures:

- stable dimensional joins
- valid logistics calculations
- trustworthy downstream analytics

---

# [4] FINANCIAL VALIDATION

## Objective

Ensure financial metrics remain logically valid and non-negative.

---

# Price Validation

## Result

| Validation             | Result |
| ---------------------- | ------ |
| Negative price records | 0      |
| Status                 | PASSED |

---

## Interpretation

No invalid product pricing values were detected.

This protects:

- revenue calculations
- sales KPIs
- profitability metrics

---

# Freight Value Validation

## Result

| Validation               | Result |
| ------------------------ | ------ |
| Negative freight records | 0      |
| Status                   | PASSED |

---

## Interpretation

No invalid freight charges were detected.

This confirms:

- logistics calculations remain trustworthy
- shipping analytics remain operationally valid

---

# [5] FREIGHT RATIO VALIDATION

## Objective

Validate:

# freight_ratio >= 0

---

## Result

| Validation              | Result |
| ----------------------- | ------ |
| Negative freight ratios | 0      |
| Status                  | PASSED |

---

## Interpretation

All freight burden calculations are logically valid.

This confirms:

- shipping intensity metrics remain trustworthy
- freight-to-product-value analytics are stable

This metric is foundational for:

- logistics profitability analysis
- oversized shipment detection
- operational cost investigation

---

# [6] PRODUCT VOLUME VALIDATION

## Objective

Ensure derived product shipment volume remains physically valid.

---

## Result

| Validation               | Result |
| ------------------------ | ------ |
| Negative product volumes | 0      |
| Status                   | PASSED |

---

## Interpretation

No impossible shipment dimensions were detected.

This confirms:

- logistics enrichment integrity
- reliable shipment-volume analysis
- trustworthy warehouse complexity metrics

---

# [7] SELLER ACCOUNTABILITY VALIDATION

## Objective

Validate:

# seller_count >= 1

for all order-item events.

---

## Result

| Validation                   | Result |
| ---------------------------- | ------ |
| Invalid seller count records | 0      |
| Status                       | PASSED |

---

## Interpretation

Every fulfillment event is successfully associated with at least one seller.

This protects:

- seller operational attribution
- fulfillment accountability
- downstream review linkage

---

# [8] SHIPPING DEADLINE VALIDATION

## Objective

Validate operational chronology:

```text
shipping_limit_date >= order_purchase_timestamp
```

---

## Result

| Validation                        | Result |
| --------------------------------- | ------ |
| Invalid shipping timeline records | 0      |
| Status                            | PASSED |

---

## Interpretation

No impossible seller fulfillment timelines were detected.

This confirms:

- operational lifecycle consistency
- trustworthy fulfillment timing analytics
- reliable logistics SLA analysis

This validation is critical because:
invalid shipment timelines corrupt:

- seller KPIs
- delay metrics
- operational monitoring

---

# [9] MULTI-SELLER ORDER ANALYSIS

## Objective

Measure operational complexity caused by:

# multi-seller orders

---

## Result

| Metric              | Value |
| ------------------- | ----- |
| Multi-seller orders | 1278  |

---

## Interpretation

The platform contains:

# 1278 multi-seller orders

This is operationally significant because:
multi-seller orders introduce:

- delivery accountability ambiguity
- review attribution complexity
- logistics coordination overhead

This metric becomes important for:

- seller-risk analytics
- delivery attribution governance
- customer experience analysis

This result validates the architectural importance of:

# dual-fact delivery modeling

implemented across the warehouse.

---

# [10] ORPHAN ENRICHMENT VALIDATION

## Objective

Validate completeness of:

# product logistics enrichment

from:

```text
bronze/products
```

---

## Result

| Validation                         | Result  |
| ---------------------------------- | ------- |
| Missing product enrichment records | 18      |
| Status                             | WARNING |

---

## Interpretation

18 order-item records are missing product logistics enrichment attributes.

Missing enrichment may impact:

- volume calculations
- logistics complexity analysis
- freight investigation

However:
this does NOT invalidate the operational fulfillment events themselves.

Therefore:
the records were intentionally preserved according to:

# operational truth preservation policy

defined in the Silver governance strategy.

---

# Architectural Interpretation of Warning

The warning demonstrates:

# governed anomaly preservation

instead of:

# aggressive record deletion

This is an intentional enterprise engineering decision.

The pipeline prioritizes:

- operational truth retention
- analytical transparency
- reproducibility
- KPI defensibility

over:

- silent over-cleaning

This aligns with the platform’s:

# zero silent data-loss policy.

---

# Overall Validation Assessment

| Area                   | Result                |
| ---------------------- | --------------------- |
| Grain Integrity        | PASSED                |
| Financial Integrity    | PASSED                |
| Logistics Integrity    | PASSED                |
| Lifecycle Integrity    | PASSED                |
| Seller Accountability  | PASSED                |
| Product Enrichment     | WARNING               |
| Overall Dataset Status | TRUSTED WITH WARNINGS |

---

# Final Engineering Assessment

The:

# `silver_order_items`

dataset successfully passed all critical operational validations.

The dataset is considered:

# analytically trusted

for:

- Gold fact construction
- seller fulfillment marts
- delivery enrichment
- logistics intelligence
- streaming operational analytics

The detected enrichment warning is:

- documented
- explainable
- operationally acceptable
- governance-compliant

and does NOT compromise:

- dataset grain
- KPI correctness
- seller accountability
- lifecycle integrity

---

# Governance Alignment

This validation process demonstrates implementation of:

- validation-driven engineering
- operational truth preservation
- modular ETL governance
- scalable analytical quality controls
- enterprise-grade Silver transformation standards

as defined in:

# `silver_transformation_strategy.md`

and:

# `silver_order_items.md`
