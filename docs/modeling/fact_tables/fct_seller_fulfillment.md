---

# `fct_seller_fulfillment.md`

```md
# Fact Table — fct_seller_fulfillment

## Objective

The `fct_seller_fulfillment` fact table measures seller-side operational fulfillment behavior at the item shipment level.

It exists to analyze:

- seller operational efficiency
- shipment preparation behavior
- seller workload stress
- shipping deadlines
- fulfillment bottlenecks
- operational overload indicators

Unlike `fct_order_delivery`, which measures final customer delivery outcomes, this fact table focuses on the seller’s internal logistics responsibility before the order reaches the customer. :contentReference[oaicite:10]{index=10}

---

# Business Process

Seller operational fulfillment behavior.

This process answers:

- How quickly do sellers prepare shipments?
- Which sellers consistently approach shipping deadlines?
- Which product categories create operational pressure?
- Which sellers may become overloaded?
- Which fulfillment patterns predict future delivery failure?

---

# Grain Definition

# ONE ROW = ONE SELLER ITEM FULFILLMENT EVENT

This means:

Every row represents:

- one product item
- from one seller
- inside one order

This is fundamentally different from:

# `fct_order_delivery`

because:

- orders may contain multiple items
- items may come from multiple sellers
- each seller has independent shipment obligations

Olist tracks seller logistics separately using:

- `shipping_limit_date`
- `freight_value`
- item-level shipment data

:contentReference[oaicite:11]{index=11}

This strict grain separation prevents:

- fan-out duplication
- mixed-grain modeling
- broken seller metrics
- invalid operational KPIs

---

# Source Tables

| Source Table                | Purpose                           |
| --------------------------- | --------------------------------- |
| `olist_order_items_dataset` | Seller shipment behavior          |
| `olist_orders_dataset`      | Purchase timestamps               |
| `olist_products_dataset`    | Product logistics characteristics |
| `olist_sellers_dataset`     | Seller information                |
| `dim_product`               | Product surrogate keys            |
| `dim_seller`                | Seller surrogate keys             |
| `dim_customer`              | Customer surrogate keys           |
| `dim_date`                  | Calendar intelligence             |

Dataset structure derived from official Olist schema. :contentReference[oaicite:12]{index=12}

---

# Fact Table Schema

| Column Name            | Datatype      | Description                           |
| ---------------------- | ------------- | ------------------------------------- |
| fulfillment_sk         | BIGINT        | Surrogate warehouse key               |
| order_id               | VARCHAR       | Parent order identifier               |
| order_item_id          | INTEGER       | Item identifier within order          |
| seller_sk_fk           | BIGINT        | FK to dim_seller                      |
| product_sk_fk          | BIGINT        | FK to dim_product                     |
| customer_sk_fk         | BIGINT        | FK to dim_customer                    |
| purchase_date_sk       | INT           | FK to dim_date                        |
| shipping_limit_date_sk | INT           | FK to dim_date                        |
| purchase_timestamp     | TIMESTAMP     | Original order purchase timestamp     |
| shipping_limit_date    | TIMESTAMP     | Seller shipment deadline              |
| item_price             | DECIMAL(10,2) | Product price                         |
| freight_value          | DECIMAL(10,2) | Shipping fee                          |
| product_weight_g       | DECIMAL(10,2) | Product weight                        |
| product_volume_cm3     | DECIMAL(12,2) | Derived package volume                |
| shipping_deadline_days | INTEGER       | Days allowed before shipment deadline |
| freight_ratio          | DECIMAL(10,4) | Freight relative to product price     |
| workload_bucket        | VARCHAR       | Seller operational load category      |
| shipping_pressure_flag | BOOLEAN       | Near-deadline shipment indicator      |

Derived from finalized fulfillment mart strategy. :contentReference[oaicite:13]{index=13}

---

# Key Derived Metrics

## 1. Shipping Deadline Days

Measures how much preparation time the seller received before shipment deadline.

Formula:

```sql
DATEDIFF(
    day,
    purchase_timestamp,
    shipping_limit_date
)
```

Purpose:

- seller operational pressure analysis
- workload stress investigation
- fulfillment efficiency tracking

## 2\. Product Volume

Measures physical shipment complexity.

Formula:

`   product_length_cm* product_height_cm* product_width_cm   `

Purpose:

- logistics complexity analysis
- heavy-product operational segmentation
- shipping risk investigation

## 3\. Freight Ratio

Measures shipping cost relative to product value.

Formula:

`   freight_value / item_price   `

Purpose:

- identify operational inefficiency
- analyze expensive shipping patterns
- detect problematic product categories

# Workload Classification Logic

Seller workload is categorized into operational buckets.

Seller Monthly OrdersWorkload Bucket1–20Low Volume21–100Medium Volume101–500High Volume>500Overloaded

Purpose:

- identify seller operational stress
- detect scaling problems
- support streaming risk enrichment

# Shipping Pressure Logic

The shipping_pressure_flag identifies shipments approaching operational deadlines.

Example logic:

`   CASE    WHEN shipping_deadline_days <= 2 THEN TRUE    ELSE FALSEEND   `

Purpose:

- operational alerting
- overload investigation
- streaming enrichment logic

# Why This Fact Table Exists Separately

This is one of the most important architectural decisions in the project.

The Olist dataset contains:

PerspectiveGrainFinal customer deliveryOrder levelSeller shipment preparationItem level

Combining both into one fact table would create:

- duplicated delivery rows
- incorrect freight aggregation
- broken seller KPIs
- invalid delivery calculations

Therefore:

Fact TableResponsibilityfct_order_deliveryCustomer outcomefct_seller_fulfillmentSeller operational behavior

This is proper Kimball modeling.

# Relationship to Streaming Pipeline

This fact table acts as:

# enrichment intelligence

for the streaming system.

The streaming layer uses fulfillment behavior to detect:

- seller overload
- shipment stress
- risky operational patterns
- abnormal shipping behavior

Examples:

- rapidly increasing workload
- sellers consistently near shipping deadline
- heavy-product operational bottlenecks

Architecture reference:

# Business Value

This table allows Olist to move from:

# reactive analytics

to:

# operational diagnostics

Instead of only seeing:

- late deliveries

the company can investigate:

- WHY sellers became late
- WHICH sellers are operationally overloaded
- WHICH product categories create pressure
- WHEN seller stress begins increasing

This directly supports the project narrative:

Bad Acquisition→ Seller Overload→ Delivery Failure→ Bad Reviews→ Revenue Loss
