# `fct_order_sales.md`

## Objective

The `fct_order_sales` fact table captures commercial sales transactions occurring within the Olist platform.

This mart enables:

- revenue analysis
- GMV tracking
- seller sales performance
- category sales analysis
- pricing analytics
- payment behavior investigation
- profitability analysis

The sales mart acts as:

# the commercial intelligence layer of the warehouse

and complements:

- delivery analytics
- fulfillment analytics
- customer satisfaction analytics

inside one integrated analytical platform.

---

# Business Process

Order item sales transaction.

---

# Grain

# One Row = One Sold Order Item

Each row represents:

- one purchased product
- from one seller
- inside one customer order

This grain aligns naturally with:

```text
olist_order_items_dataset
```

and preserves:

- commercial transaction integrity
- seller revenue attribution
- product-level sales analytics

---

# Why Sales Requires a Separate Fact

Sales transactions are:

# commercial business events

NOT:

- delivery events
- review events
- fulfillment preparation events

Sales contain:

- product pricing
- freight monetization
- payment allocation
- revenue metrics

Therefore:

# sales must remain in a dedicated fact table

to avoid:

- mixed-grain corruption
- duplicated revenue metrics
- unreliable GMV calculations
- operational/commercial metric confusion

This follows Kimball dimensional modeling principles.

---

# Source Tables

| Source Table                   | Purpose                       |
| ------------------------------ | ----------------------------- |
| `olist_order_items_dataset`    | Item-level sales transactions |
| `olist_orders_dataset`         | Order lifecycle               |
| `olist_order_payments_dataset` | Payment information           |
| `olist_products_dataset`       | Product enrichment            |
| `olist_customers_dataset`      | Customer enrichment           |

---

# Table Name

```sql id="2phdri"
fct_order_sales
```

---

# Primary Key

```sql id="u4cw98"
sales_fact_sk
```

Warehouse-generated surrogate key.

---

# Recommended Schema

| Column Name             | Datatype      | Description                    |
| ----------------------- | ------------- | ------------------------------ |
| sales_fact_sk           | BIGINT        | Surrogate warehouse key        |
| order_id                | VARCHAR       | Business order identifier      |
| order_item_id           | INTEGER       | Item identifier inside order   |
| customer_sk_fk          | BIGINT        | Customer dimension FK          |
| seller_sk_fk            | BIGINT        | Seller dimension FK            |
| product_sk_fk           | BIGINT        | Product dimension FK           |
| purchase_date_sk        | INT           | Purchase date FK               |
| approval_date_sk        | INT           | Order approval date FK         |
| delivered_date_sk       | INT           | Delivered date FK              |
| order_status            | VARCHAR       | Final order status             |
| item_price              | DECIMAL(12,2) | Product sales price            |
| freight_value           | DECIMAL(12,2) | Freight charge                 |
| total_sales_value       | DECIMAL(12,2) | item_price + freight_value     |
| payment_value_allocated | DECIMAL(12,2) | Allocated payment value        |
| installment_count       | INTEGER       | Payment installments           |
| payment_type            | VARCHAR       | Payment method                 |
| product_quantity        | INTEGER       | Quantity sold                  |
| gross_merchandise_value | DECIMAL(12,2) | GMV contribution               |
| high_value_order_flag   | BOOLEAN       | High-value sale indicator      |
| freight_ratio           | DECIMAL(10,4) | Freight relative to item price |
| load_timestamp          | TIMESTAMP     | Warehouse load timestamp       |

---

# Recommended Metrics Logic

## Total Sales Value

```sql id="e9ph7v"
item_price + freight_value
```

Measures:

# total commercial value charged to customer

---

# GMV (Gross Merchandise Value)

```sql id="v5cb9h"
gross_merchandise_value = item_price
```

GMV excludes:

- freight
- refunds
- taxes

This is standard e-commerce practice.

---

# Freight Ratio

```sql id="z9jx5z"
freight_value / item_price
```

Measures:

# shipping cost intensity

Supports:

- logistics profitability analysis
- category freight investigation
- distance-cost analysis

---

# High Value Order Flag

Example logic:

```sql id="40b6vc"
CASE
    WHEN total_sales_value >= 1000
    THEN 1
    ELSE 0
END
```

Supports:

- premium customer analysis
- seller segmentation
- risk prioritization

---

# Important Modeling Decision — Payments

The payment dataset:

```text
olist_order_payments_dataset
```

is:

# order-level

while sales are:

# order-item-level

Therefore:
payment allocation must be handled carefully.

---

# Recommended MVP Strategy

Allocate:

```text
payment_value
```

proportionally across order items.

Example:

```sql id="7m2pk8"
allocated_payment =
item_price / total_order_price
* payment_value
```

This preserves:

- item-level commercial analysis
- seller revenue attribution
- payment consistency

---

# Relationships

| Dimension    | Foreign Key       |
| ------------ | ----------------- |
| dim_customer | customer_sk_fk    |
| dim_seller   | seller_sk_fk      |
| dim_product  | product_sk_fk     |
| dim_date     | purchase_date_sk  |
| dim_date     | approval_date_sk  |
| dim_date     | delivered_date_sk |

---

# Business Questions Supported

This mart enables:

- Which sellers generate highest revenue?
- Which categories produce highest GMV?
- Which products create highest freight burden?
- Which regions generate strongest sales?
- Do delayed orders reduce high-value purchasing?
- Which sellers balance revenue and delivery quality best?

---

# Streaming Architecture Role

`fct_order_sales`
acts primarily as:

# analytical enrichment

for:

- seller prioritization
- revenue-aware risk scoring
- commercial segmentation

Example:
streaming can prioritize:

```text
high-value delayed orders
```

before:

```text
low-value delayed orders
```

This improves:

- operational prioritization
- customer retention focus
- business impact awareness

---

# ETL Logic

## Step 1 — Extract Order Items

Load:

```sql id="5xy0eu"
olist_order_items_dataset
```

---

## Step 2 — Join Orders

Retrieve:

- order lifecycle
- approval timestamps
- delivery status

---

## Step 3 — Join Products

Retrieve:

- category
- logistics attributes
- product metadata

---

## Step 4 — Join Payments

Allocate:

- payment value
- installment information
- payment methods

---

## Step 5 — Derive Commercial Metrics

Generate:

- total_sales_value
- freight_ratio
- GMV
- high_value_order_flag

---

# Data Quality Rules

| Rule                         | Validation |
| ---------------------------- | ---------- |
| Non-negative sales values    | enforced   |
| Valid freight values         | enforced   |
| Valid payment allocation     | enforced   |
| No duplicate order item rows | enforced   |
| Valid foreign keys           | enforced   |

---

# Recommended Constraints

| Constraint             | Purpose                          |
| ---------------------- | -------------------------------- |
| item_price >= 0        | Prevent invalid revenue          |
| freight_value >= 0     | Prevent invalid logistics values |
| product_quantity > 0   | Preserve sales integrity         |
| valid FK relationships | Referential integrity            |

---

# Recommended Indexes

| Index                   | Purpose               |
| ----------------------- | --------------------- |
| idx_sales_seller        | Seller analysis       |
| idx_sales_product       | Product analysis      |
| idx_sales_purchase_date | Time-series analysis  |
| idx_sales_order_status  | Operational filtering |
| idx_sales_payment_type  | Payment analytics     |

---

# Best Practices Applied

| Best Practice                    | Applied |
| -------------------------------- | ------- |
| Kimball fact modeling            | Yes     |
| Dedicated sales business process | Yes     |
| Item-level commercial grain      | Yes     |
| Payment allocation strategy      | Yes     |
| Revenue metric isolation         | Yes     |
| Conformed dimensions             | Yes     |
| Commercial enrichment            | Yes     |
| Streaming-aware prioritization   | Yes     |

---

# Architectural Importance

`fct_order_sales`
acts as:

# the commercial intelligence foundation

of the platform.

It connects:

- sellers
- products
- customers
- payments
- logistics costs
- delivery outcomes

and enables the warehouse to evolve from:

# operational logistics analytics

into:

# full e-commerce business intelligence and revenue analytics platform.
