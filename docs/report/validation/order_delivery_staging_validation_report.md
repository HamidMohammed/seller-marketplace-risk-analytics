# `order_delivery_staging_validation_report`

## Objective

This report documents the validation results for:

# order_delivery_staging

inside the Olist Seller Intelligence Platform.

The validation framework ensures:

- order-level grain integrity
- delivery lifecycle correctness
- seller accountability consistency
- geographic enrichment quality
- delivery KPI trustworthiness

The dataset follows:

# validation-driven transformation engineering

where transformations are NOT trusted blindly and must be continuously validated.

---

# Dataset Information

| Property            | Value                        |
| ------------------- | ---------------------------- |
| Dataset             | order_delivery_staging       |
| Layer               | Silver Staging               |
| Grain               | ONE ROW = ONE CUSTOMER ORDER |
| Downstream Consumer | fct_order_delivery           |

---

# Validation Categories

The validation process includes:

| Validation Category              | Purpose                 |
| -------------------------------- | ----------------------- |
| Row-count validation             | detect unexpected loss  |
| Duplicate validation             | preserve grain          |
| Null validation                  | protect critical fields |
| Lifecycle validation             | operational correctness |
| Seller accountability validation | attribution integrity   |
| Geographic validation            | enrichment quality      |
| Delivery metrics validation      | KPI correctness         |

---

# Validation Execution Summary

| Validation Metric                     | Result |
| ------------------------------------- | ------ |
| Final Row Count                       | 99,441 |
| Duplicate order_id values             | 0      |
| Distance Bucket Categories            | 4      |
| Multi-Seller Orders                   | 1,278  |
| Single-Seller Orders                  | 97,388 |
| Orders With Missing Seller Enrichment | 775    |

---

# 1. Row Count Validation

## Objective

Ensure:

# no unexpected row loss

during staging enrichment.

---

## Validation Logic

```python
validate_row_count(df)
```

---

## Validation Result

```text
Final Row Count: 99,441
```

---

## Result Interpretation

The staging pipeline successfully preserved:

# operational order coverage

while enriching:

- seller accountability
- freight aggregations
- geographic intelligence

No unexpected row-loss behavior was detected.

---

# 2. Grain Validation

## Rule

```text
ONE ROW = ONE CUSTOMER ORDER
```

---

## Validation Logic

```python
validate_duplicates(["order_id"])
```

---

## Validation Result

```text
0 duplicate order_id values detected
```

---

## Business Importance

This validation protects:

- delivery KPIs
- streaming risk scoring
- operational analytics
- downstream Gold fact integrity

This confirms:

# order-level grain integrity preserved successfully.

---

# 3. Critical Null Validation

## Validated Columns

| Column                   | Purpose                  |
| ------------------------ | ------------------------ |
| order_id                 | business key             |
| customer_id              | customer linkage         |
| order_status             | lifecycle classification |
| order_purchase_timestamp | lifecycle origin         |
| delivery_duration_days   | delivery intelligence    |
| delay_days               | KPI calculation          |
| seller_count             | accountability           |
| distance_bucket          | logistics segmentation   |

---

## Validation Goal

Critical analytical fields should maintain:

# minimal unexpected null distribution

after enrichment and aggregation.

---

## Result Interpretation

Most critical business fields preserved:

# high enrichment quality

with only limited operational enrichment gaps
documented separately in:

- seller enrichment analysis
- geographic enrichment analysis

---

# 4. Delivery Lifecycle Validation

## Rules

| Rule                 | Purpose                  |
| -------------------- | ------------------------ |
| purchase <= approval | valid payment lifecycle  |
| purchase <= delivery | valid delivery lifecycle |

---

## Validation Logic

```python
order_approved_at >= order_purchase_timestamp
```

```python
order_delivered_customer_date >= order_purchase_timestamp
```

---

## Business Importance

These validations prevent:

- impossible operational timelines
- corrupted delivery analytics
- invalid KPI calculations
- negative lifecycle metrics

---

## Result Interpretation

Lifecycle chronology was successfully preserved across the dataset.

No major operational timeline corruption was detected.

---

# 5. Delivered Orders Validation

## Rule

```text
Delivered orders must contain delivery timestamp
```

---

## Validation Logic

```python
order_status = 'delivered'
AND order_delivered_customer_date IS NULL
```

---

## Expected Result

```text
0 invalid delivered orders
```

---

## Business Importance

Protects:

- delivery duration metrics
- delay calculations
- delivery intelligence correctness

---

## Result Interpretation

Delivered orders maintained:

# reliable delivery timestamp integrity

required for:

- delivery KPIs
- seller performance analysis
- customer satisfaction analytics

---

# 6. Delivery Metrics Validation

## Validations

| Validation                 | Purpose                        |
| -------------------------- | ------------------------------ |
| negative delivery duration | impossible lifecycle detection |
| extreme delay monitoring   | anomaly awareness              |
| negative buffer_days       | invalid logistics promises     |

---

## Validation Logic

```python
delivery_duration_days < 0
```

```python
delay_days > 100
```

```python
buffer_days < 0
```

---

## Result Interpretation

No impossible operational delivery metrics were identified.

Extreme delays are intentionally preserved because:
they represent:

# valuable operational intelligence

rather than invalid data.

---

# 7. Seller Accountability Validation

## Rules

| Rule                                        | Purpose                 |
| ------------------------------------------- | ----------------------- |
| seller_count >= 1                           | seller integrity        |
| single-seller orders require primary seller | attribution correctness |

---

## Validation Results

| Metric                        | Count  |
| ----------------------------- | ------ |
| Multi-Seller Orders           | 1,278  |
| Single-Seller Orders          | 97,388 |
| Missing Seller Accountability | 775    |

---

## Business Importance

This validation protects:

- seller attribution
- review attribution logic
- delivery accountability
- operational KPI integrity

---

## Result Interpretation

Most orders maintained:

# reliable seller accountability enrichment.

A limited subset of records contained:

- missing seller attribution
- missing seller aggregation coverage

These records were intentionally preserved for:

# operational anomaly visibility.

---

# 8. Geographic Validation

## Validations

| Validation                  | Purpose                      |
| --------------------------- | ---------------------------- |
| seller_state availability   | logistics enrichment quality |
| customer_state availability | delivery-region analytics    |
| distance_bucket validity    | segmentation consistency     |

---

## Distance Bucket Distribution

| Distance Bucket | Count  |
| --------------- | ------ |
| Same State      | 35,479 |
| Same Region     | 23,666 |
| Cross Region    | 39,521 |
| Unknown         | 775    |

---

## Business Importance

Supports:

- regional delivery analysis
- freight burden investigation
- logistics intelligence
- operational segmentation

---

## Result Interpretation

The majority of orders successfully received:

# geographic logistics classification.

Only:

```text
775 records
```

remained:

```text
distance_bucket = Unknown
```

which aligned exactly with:

- missing seller accountability enrichment
- missing geographic enrichment coverage

This consistency strongly suggests:

# incomplete fulfillment enrichment

rather than:

# random corruption.

---

# 9. Multi-Seller Distribution Analysis

## Validation Output

| Multi-Seller Classification | Count  |
| --------------------------- | ------ |
| FALSE                       | 97,388 |
| TRUE                        | 1,278  |
| NULL                        | 775    |

---

## Interpretation

The platform primarily consists of:

# single-seller orders

which simplifies:

- seller accountability
- review attribution
- delivery KPI governance

However:

```text
1,278 orders
```

contained:

# multi-seller operational complexity.

These records are analytically important because:
multi-seller orders create:

- ambiguous delivery accountability
- more complex logistics coordination
- more difficult review attribution

---

# 10. Geographic & Seller Enrichment Coverage Analysis

## Observed Pattern

Validation identified:

| Condition                    | Count |
| ---------------------------- | ----- |
| distance_bucket = Unknown    | 775   |
| is_multi_seller_order = NULL | 775   |

These counts matched exactly.

---

## Root Cause Analysis

This pattern indicates:

# missing order-item enrichment coverage

for a subset of orders.

Most likely causes include:

- canceled operational lifecycle
- incomplete fulfillment events
- missing seller attribution
- orders existing without item-level shipment records

Because:

```text
seller_count
```

depends on:

```text
silver_order_items
```

missing enrichment propagates into:

- seller_count
- primary_seller_id
- is_multi_seller_order
- seller geography
- distance classification

---

## Important Architectural Decision

The project intentionally preserves these records.

The pipeline does NOT:

- silently delete records
- force artificial seller attribution
- fabricate geographic enrichment

This follows the platform philosophy of:

# operational truth preservation

and:

# zero silent data-loss governance.

---

## Business Interpretation

These records may represent:

- incomplete operational fulfillment
- failed logistics preparation
- canceled order flows
- enrichment coverage limitations

Such anomalies themselves contain:

# valuable operational intelligence.

---

## Gold Layer Strategy

Gold marts may:

- exclude these records selectively
- segment them separately
- monitor them as operational anomalies

depending on:

- KPI requirements
- business use-case
- analytical objective

This preserves:

# analytical flexibility

WITHOUT:

# corrupting operational truth.

---

# 11. Operational Anomaly Preservation

The validation framework intentionally preserves:

# operational anomalies

when they represent:

- logistics failures
- geographic complexity
- seller ambiguity
- delivery bottlenecks

Examples:

| Pattern                    | Interpretation             |
| -------------------------- | -------------------------- |
| extreme delays             | operational bottlenecks    |
| multi-seller orders        | accountability ambiguity   |
| missing geography          | enrichment limitation      |
| missing seller attribution | fulfillment incompleteness |

---

## Important Governance Principle

The project avoids:

# aggressive over-cleaning

because operational anomalies themselves contain:

# valuable business intelligence.

This aligns with:

- enterprise governance philosophy
- Silver-layer business-truth engineering
- explainable analytical design

---

# Validation Philosophy

The dataset follows:

# enterprise validation governance principles

including:

- grain preservation
- lifecycle correctness
- accountability integrity
- explainable enrichment
- KPI-safe transformations

This ensures:

# trusted downstream delivery intelligence.

---

# Strategic Architectural Value

This validation framework demonstrates:

# enterprise-grade analytical governance

through:

- validation-driven engineering
- operational truth preservation
- controlled enrichment validation
- delivery KPI protection
- seller accountability governance

The dataset is therefore considered:

# trusted for Gold-layer delivery modeling.

---

# Final Engineering Assessment

The `order_delivery_staging` dataset successfully achieved:

| Capability                       | Status                         |
| -------------------------------- | ------------------------------ |
| Order grain preservation         | PASS                           |
| Delivery lifecycle integrity     | PASS                           |
| Geographic enrichment coverage   | PASS with documented anomalies |
| Seller accountability enrichment | PASS with documented anomalies |
| Delivery KPI safety              | PASS                           |
| Controlled anomaly preservation  | PASS                           |
| Gold-layer readiness             | PASS                           |

The dataset is therefore approved as:

# trusted operational delivery staging

for:

- `fct_order_delivery`
- delivery intelligence dashboards
- seller performance monitoring
- streaming enrichment workflows
- operational analytics
