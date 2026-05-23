# `fct_order_payments.md`

## Objective

The `fct_order_payments` fact table captures customer payment transactions associated with Olist e-commerce orders.

This mart enables:

- payment behavior analysis
- installment behavior investigation
- financial transaction analytics
- payment method trends
- customer financing analysis
- seller commercial-risk analysis
- cross-domain operational intelligence

The payment mart acts as:

# the financial behavior intelligence layer

of the warehouse.

It complements:

- sales analytics
- delivery analytics
- customer satisfaction analytics
- seller performance analytics

inside one integrated enterprise analytical platform.

---

# Business Process

Customer payment transaction event.

---

# Grain

# One Row = One Order Payment Transaction

Each row represents:

- one payment transaction
- for one customer order
- at one point in time

This grain aligns directly with:

```sql
olist_order_payments_dataset
```

and preserves:

- payment transaction integrity
- installment behavior accuracy
- financial-event independence

---

# Why Payments Require a Separate Fact

Payments are:

# financial business events

NOT:

- sales events
- delivery events
- review events
- fulfillment events

Payments contain:

- payment methods
- installment behavior
- split-payment logic
- transaction value behavior

The dataset also contains:

```sql
payment_sequential
```

meaning:

# one order can contain multiple payment transactions

Therefore:
payment grain differs from:

- sales grain
- delivery grain

and must remain:

# an independent fact table

to avoid:

- mixed-grain corruption
- duplicated payment metrics
- invalid revenue calculations
- fan-out join problems

This follows:

# Kimball dimensional modeling principles

and demonstrates:

# enterprise-grade grain awareness

---

# Source Tables

| Source Table                   | Purpose                      |
| ------------------------------ | ---------------------------- |
| `olist_order_payments_dataset` | Payment transaction behavior |
| `olist_orders_dataset`         | Order lifecycle linkage      |
| `olist_customers_dataset`      | Customer enrichment          |
| `olist_order_items_dataset`    | Order commercial totals      |
| `olist_sellers_dataset`        | Seller linkage               |

---

# Table Name

```sql
fct_order_payments
```

---

# Primary Key

```sql
payment_fact_sk
```

Warehouse-generated surrogate key.

---

# Recommended Schema

| Column Name              | Datatype      | Description                     |
| ------------------------ | ------------- | ------------------------------- |
| payment_fact_sk          | BIGINT        | Surrogate warehouse key         |
| order_id                 | VARCHAR       | Business order identifier       |
| payment_sequential       | INTEGER       | Payment sequence inside order   |
| customer_sk_fk           | BIGINT        | Customer dimension FK           |
| seller_sk_fk             | BIGINT        | Seller dimension FK             |
| purchase_date_sk         | INT           | Purchase date FK                |
| approval_date_sk         | INT           | Payment approval date FK        |
| payment_type             | VARCHAR       | Payment method                  |
| payment_installments     | INTEGER       | Installment count               |
| payment_value            | DECIMAL(12,2) | Payment transaction value       |
| total_order_value        | DECIMAL(12,2) | Total order commercial value    |
| payment_ratio            | DECIMAL(10,4) | Payment relative to order value |
| is_installment_payment   | BOOLEAN       | Installment indicator           |
| high_installment_flag    | BOOLEAN       | High financing indicator        |
| split_payment_flag       | BOOLEAN       | Multiple payments indicator     |
| payment_value_bucket     | VARCHAR       | Payment size classification     |
| payment_behavior_segment | VARCHAR       | Financing behavior category     |
| created_at               | TIMESTAMP     | Warehouse load timestamp        |

---

# Recommended Derived Metrics

# Payment Ratio

Measures:

# payment contribution relative to full order value

Formula:

```sql
payment_value / total_order_value
```

Supports:

- split-payment analysis
- financial allocation investigation
- payment consistency checks

---

# Installment Payment Flag

```sql
CASE
    WHEN payment_installments > 1
    THEN TRUE
    ELSE FALSE
END
```

Measures:

# customer financing behavior

---

# High Installment Flag

Example logic:

```sql
CASE
    WHEN payment_installments >= 6
    THEN TRUE
    ELSE FALSE
END
```

Supports:

- financial-risk analysis
- premium-order financing analysis
- delayed-order prioritization

---

# Split Payment Flag

```sql
CASE
    WHEN COUNT(payment_sequential)
         OVER(PARTITION BY order_id) > 1
    THEN TRUE
    ELSE FALSE
END
```

Measures:

# multi-payment order behavior

This is one of the most important financial patterns in the dataset.

---

# Payment Value Bucket

Example classification:

| Condition                          | Bucket        |
| ---------------------------------- | ------------- |
| payment_value < 50                 | Low Value     |
| payment_value BETWEEN 50 AND 200   | Medium Value  |
| payment_value BETWEEN 201 AND 1000 | High Value    |
| payment_value > 1000               | Premium Value |

Supports:

- customer segmentation
- operational prioritization
- commercial risk analysis

---

# Payment Behavior Segment

Example logic:

| Condition                    | Segment            |
| ---------------------------- | ------------------ |
| installments = 1             | Full Payment       |
| installments BETWEEN 2 AND 5 | Moderate Financing |
| installments >= 6            | Heavy Financing    |

This creates:

# customer financing intelligence

instead of simple payment reporting.

---

# Important Modeling Decision

The payment dataset is:

# order-level

while:

```sql
olist_order_items_dataset
```

is:

# item-level

Therefore:

# direct joins between payments and order items are dangerous

because they create:

# fan-out duplication

Example:

```text
1 order
    ↓
3 items

1 order
    ↓
2 payments

Result:
3 × 2 = 6 rows
```

This causes:

- duplicated revenue
- invalid GMV
- inflated payment metrics

---

# Correct Enterprise Strategy

Payments remain:

# independent financial events

linked through:

```sql
order_id
```

while sales remain:

# independent commercial events

This preserves:

- grain integrity
- KPI correctness
- warehouse reliability

---

# Relationships

| Dimension    | Foreign Key      |
| ------------ | ---------------- |
| dim_customer | customer_sk_fk   |
| dim_seller   | seller_sk_fk     |
| dim_date     | purchase_date_sk |
| dim_date     | approval_date_sk |

---

# Business Questions Supported

This mart enables:

- Which payment methods are most common?
- Which regions rely most on installments?
- Do delayed orders correlate with financing behavior?
- Which sellers generate heavily financed purchases?
- Are premium orders more likely to use installments?
- Do financing-heavy customers leave worse reviews?
- Which payment methods dominate high-value orders?

---

# Cross-Mart Intelligence Examples

This fact becomes VERY powerful when connected with:

- delivery mart
- review mart
- sales mart

Example:

```text
Heavy Installments
        +
Late Delivery
        +
Negative Review
        ↓
High Customer Dissatisfaction Risk
```

This is:

# operational + financial intelligence

NOT isolated analytics.

---

# Streaming Architecture Role

`fct_order_payments`
acts primarily as:

# commercial enrichment intelligence

for:

- high-value order prioritization
- financial-risk segmentation
- customer-value scoring

Example:

Streaming system can prioritize:

```text
Premium financed delayed orders
```

before:

```text
Low-value delayed orders
```

This improves:

- operational prioritization
- customer retention
- business impact awareness

---

# ETL Logic

## Step 1 — Extract Payments

Load:

```sql
olist_order_payments_dataset
```

---

## Step 2 — Join Orders

Retrieve:

- order lifecycle
- approval timestamps
- customer linkage

---

## Step 3 — Calculate Order Totals

Aggregate:

```sql
olist_order_items_dataset
```

to calculate:

- total order value
- seller attribution

---

## Step 4 — Derive Payment Metrics

Generate:

- installment flags
- payment buckets
- financing segments
- split-payment indicators

---

## Step 5 — Load Fact Table

Insert enriched payment transactions into:

```sql
fct_order_payments
```

---

# Data Quality Rules

| Rule                        | Validation |
| --------------------------- | ---------- |
| payment_value >= 0          | enforced   |
| payment_installments > 0    | enforced   |
| valid payment_type          | enforced   |
| no orphan orders            | enforced   |
| valid date FK relationships | enforced   |

---

# Recommended Constraints

| Constraint               | Purpose                      |
| ------------------------ | ---------------------------- |
| payment_value >= 0       | Prevent invalid transactions |
| payment_installments > 0 | Preserve financing integrity |
| FK to dim_customer       | Referential integrity        |
| FK to dim_date           | Timeline consistency         |

---

# Recommended Indexes

| Index                     | Purpose              |
| ------------------------- | -------------------- |
| idx_payment_type          | Payment analysis     |
| idx_payment_installments  | Financing analysis   |
| idx_payment_order         | Order lookup         |
| idx_payment_purchase_date | Trend analysis       |
| idx_payment_value         | High-value filtering |

---

# Best Practices Applied

| Best Practice                        | Applied |
| ------------------------------------ | ------- |
| Kimball fact modeling                | Yes     |
| Dedicated financial business process | Yes     |
| Proper payment grain isolation       | Yes     |
| Fan-out prevention strategy          | Yes     |
| Conformed dimensions                 | Yes     |
| Cross-domain analytical support      | Yes     |
| Financial segmentation               | Yes     |
| Streaming-aware enrichment           | Yes     |

---

# Architectural Importance

`fct_order_payments`
acts as:

# the financial intelligence foundation

of the platform.

It connects:

- customer financing behavior
- commercial transactions
- seller performance
- operational risk
- customer satisfaction
- revenue intelligence

and evolves the warehouse from:

# operational e-commerce analytics

into:

# full enterprise operational + commercial + financial intelligence platform.

This fact table strongly complements your:

- `fct_order_sales`
- `fct_order_delivery`
- `fct_customer_reviews`

while preserving:

- dimensional integrity
- grain correctness
- enterprise modeling quality.
