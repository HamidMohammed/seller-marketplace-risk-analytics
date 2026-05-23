# `silver_order_items.md`

## Objective

The `silver_order_items` dataset represents the trusted seller fulfillment and logistics operational staging layer inside the Olist Seller Intelligence Platform.

This dataset transforms:

# raw seller item fulfillment events

into:

# validated logistics-aware analytical staging

used by:

- seller fulfillment marts
- delivery enrichment
- freight analysis
- logistics intelligence
- sales analytics
- streaming enrichment
- seller accountability analysis

The dataset acts as:

# the seller operational truth layer

within the Silver architecture.

Unlike:
`silver_orders`

which represents:

# customer delivery lifecycle truth

`silver_order_items`
represents:

# seller shipment preparation and logistics responsibility

This distinction is architecturally critical and follows the platform’s dual-fact delivery modeling strategy.

---

# Dataset Role in Architecture

```text
Bronze Order Items
        ↓
silver_order_items
        ↓
Delivery + Fulfillment + Sales Facts
        ↓
Dashboards & Streaming Intelligence
```

This dataset powers:

- seller operational intelligence
- freight burden analytics
- fulfillment workload analysis
- logistics difficulty analysis
- seller accountability metrics

and acts as:

# the operational enrichment backbone

for downstream analytical marts.

---

# Dataset Grain

# ONE ROW = ONE SELLER ITEM FULFILLMENT EVENT

Each row represents:

- one purchased item
- sold by one seller
- inside one customer order

This grain MUST remain preserved throughout all transformations.

This grain is DIFFERENT from:
`silver_orders`

which uses:

# ONE ROW = ONE CUSTOMER ORDER

Mixing these grains incorrectly would create:

- fan-out duplication
- incorrect KPIs
- duplicated delivery metrics
- unreliable seller attribution

This follows the modeling strategy defined in the delivery architecture documentation.

---

# Source Datasets

| Source Dataset     | Layer  | Purpose                       |
| ------------------ | ------ | ----------------------------- |
| bronze/order_items | Bronze | Seller fulfillment operations |
| bronze/products    | Bronze | Product logistics enrichment  |
| silver_orders      | Silver | Order lifecycle enrichment    |

---

# Source Columns

| Column              | Meaning                         |
| ------------------- | ------------------------------- |
| order_id            | Parent customer order           |
| order_item_id       | Item identifier inside order    |
| product_id          | Product identifier              |
| seller_id           | Seller responsible for shipment |
| shipping_limit_date | Seller shipment deadline        |
| price               | Product sales value             |
| freight_value       | Shipping fee charged            |

These fields represent:

# seller operational shipment behavior

NOT:

# final customer delivery outcome.

---

# Silver Responsibilities

The `silver_order_items` pipeline is responsible for:

| Responsibility                     | Purpose                 |
| ---------------------------------- | ----------------------- |
| Financial datatype standardization | analytical accuracy     |
| Shipping timestamp parsing         | lifecycle analysis      |
| Freight metric derivation          | logistics intelligence  |
| Product logistics enrichment       | shipment analysis       |
| Seller-count aggregation           | accountability analysis |
| Grain validation                   | KPI integrity           |
| Metadata enrichment                | lineage                 |
| Operational enrichment             | Gold readiness          |

---

# Transformations Applied

---

# 1. Financial Standardization

## Transformed Columns

| Column        |
| ------------- |
| price         |
| freight_value |

---

## Transformation

```python
cast(DecimalType(12,2))
```

---

## Purpose

Financial fields require:

# deterministic decimal precision

for:

- revenue analytics
- freight calculations
- profitability analysis
- seller KPI consistency

Without financial standardization:

- aggregation drift may occur
- Spark floating-point inconsistencies may appear
- downstream KPIs become unreliable

---

# 2. Shipping Timestamp Casting

## Transformed Column

| Column              |
| ------------------- |
| shipping_limit_date |

---

## Transformation

```python
to_timestamp(shipping_limit_date)
```

---

## Purpose

Enables:

- shipping lifecycle analytics
- seller deadline analysis
- fulfillment timing intelligence
- operational validation

---

# 3. Freight Ratio Metric

## Derived Column

```text
freight_ratio
```

---

## Formula

```python
freight_value / price
```

---

## Business Meaning

Measures:

# shipping cost intensity relative to product value

---

## Example

| Product Price | Freight | Ratio |
| ------------- | ------- | ----- |
| 20            | 18      | 0.90  |
| 1000          | 20      | 0.02  |

---

## Business Value

Supports:

- freight burden analysis
- logistics profitability investigation
- seller operational cost analysis
- oversized shipment detection

This metric transforms the platform from:

# simple e-commerce reporting

into:

# logistics-aware operational intelligence.

---

# 4. Product Volume Metric

## Derived Column

```text
product_volume_cm3
```

---

## Formula

```python
product_length_cm
*
product_height_cm
*
product_width_cm
```

---

## Source Dependency

Derived using:

```text
bronze/products
```

enrichment.

---

## Business Meaning

Measures:

# physical shipment volume

for each purchased product.

---

## Business Value

Supports:

- oversized product detection
- logistics complexity analysis
- freight-cost investigation
- warehouse difficulty segmentation

---

# 5. Seller Count per Order

## Derived Column

```text
seller_count
```

---

## Formula

```python
count(distinct seller_id)
over(partition by order_id)
```

---

## Business Meaning

Measures:

# number of sellers participating in one order

---

## Business Importance

This is one of the MOST important metrics in the platform because:
multi-seller orders create:

# ambiguous delivery accountability

This metric becomes central to:

- delivery mart filtering
- review attribution
- seller KPI protection
- operational responsibility analysis

As documented in the delivery modeling strategy.

---

# 6. Multi-Seller Order Flag

## Derived Column

```text
is_multi_seller_order
```

---

## Logic

```python
seller_count > 1
```

---

## Business Purpose

Provides:

# simplified seller-accountability indicator

Used for:

- operational filtering
- review attribution safety
- delivery KPI governance

---

# 7. Metadata Enrichment

## Added Columns

| Column                 | Purpose          |
| ---------------------- | ---------------- |
| silver_loaded_at       | pipeline lineage |
| source_system          | traceability     |
| transformation_version | reproducibility  |

---

# Validation Framework

The dataset follows:

# validation-driven transformation engineering

defined in:

```text
silver_transformation_strategy.md
```

All transformations are validated BEFORE Silver output generation.

---

# Validation Rules

---

# 1. Grain Validation

## Rule

```text
ONE ROW = ONE ORDER ITEM EVENT
```

---

## Validation

```python
validate_duplicates(
    ["order_id", "order_item_id"]
)
```

---

## Purpose

Protect:

- seller accountability
- logistics KPIs
- fulfillment integrity
- downstream fact correctness

---

# 2. Critical Null Validation

## Critical Columns

| Column        | Reason               |
| ------------- | -------------------- |
| order_id      | parent linkage       |
| order_item_id | grain preservation   |
| seller_id     | accountability       |
| product_id    | enrichment linkage   |
| price         | commercial integrity |
| freight_value | logistics integrity  |

---

## Purpose

Prevent:

- orphan fulfillment events
- invalid logistics metrics
- broken downstream joins

---

# 3. Financial Validation

## Validation Rules

| Rule               | Purpose                    |
| ------------------ | -------------------------- |
| price >= 0         | prevent invalid revenue    |
| freight_value >= 0 | prevent impossible freight |
| freight_ratio >= 0 | analytical consistency     |

---

## Business Importance

Protect:

- revenue KPIs
- logistics analytics
- profitability calculations

---

# 4. Shipping Deadline Validation

## Rule

```text
shipping_limit_date >= order_purchase_timestamp
```

---

## Purpose

Prevent:

# impossible operational timelines

This validation ensures:

- valid seller shipment windows
- trustworthy fulfillment analytics
- accurate lifecycle calculations

---

# 5. Seller Accountability Validation

## Validation

```text
seller_count >= 1
```

---

## Purpose

Protect:

- seller attribution integrity
- operational ownership analysis
- downstream delivery filtering

---

# 6. Product Volume Validation

## Validation Rules

| Rule        | Purpose                       |
| ----------- | ----------------------------- |
| volume >= 0 | prevent impossible dimensions |
| weight >= 0 | logistics consistency         |

---

# Important Architectural Decisions

---

# Controlled Enrichment Strategy

The pipeline intentionally avoids:

# aggressive denormalization

inside Silver.

The dataset does NOT fully join:

- reviews
- payments
- customers
- seller dimensions

inside:
`silver_order_items`

because Silver is:

# trusted analytical staging

NOT:

# final mart construction.

This preserves:

- modularity
- maintainability
- grain integrity
- scalable warehouse design

---

# Operational Truth Preservation

The dataset intentionally preserves:

# operational logistics anomalies

when they represent:

- seller shipment issues
- logistics complexity
- freight abnormalities
- fulfillment bottlenecks

Example:

| Pattern                      | Meaning                |
| ---------------------------- | ---------------------- |
| extremely high freight ratio | logistics inefficiency |
| missing shipping deadline    | operational issue      |
| oversized product            | fulfillment complexity |

The project avoids:

# over-cleaning

because operational anomalies themselves contain:

# valuable business intelligence.

---

# No Silent Record Deletion

The pipeline follows:

# zero silent data-loss policy

Meaning:
records may only be removed when:

- documented
- validated
- business justified

This preserves:

- reproducibility
- KPI trust
- analytical defensibility

---

# Gold Layer Dependencies

The following marts consume:

# silver_order_items

| Gold Dataset           | Dependency Purpose     |
| ---------------------- | ---------------------- |
| fct_seller_fulfillment | seller operations      |
| fct_order_delivery     | freight aggregation    |
| fct_order_sales        | sales transactions     |
| fct_order_payments     | order-value enrichment |
| fct_customer_reviews   | seller attribution     |

This makes:
`silver_order_items`

a:

# core operational enrichment dataset

across the warehouse.

---

# Streaming Architecture Role

`silver_order_items`
acts as:

# seller operational enrichment intelligence

for:

- delivery-risk scoring
- logistics stress analysis
- seller operational baselines
- freight-risk monitoring

Streaming systems can use:

- freight intensity
- seller workload
- shipment complexity
- multi-seller indicators

to enrich:

# real-time operational risk scoring.

---

# Output Dataset Location

```text
data/silver/order_items/
```

Stored as:

# parquet

for:

- Spark optimization
- scalable analytical processing
- dimensional ingestion efficiency

---

# Relationship to Delivery Modeling Strategy

The dataset directly implements the platform’s:

# dual-fact delivery modeling strategy

where:

| Dataset            | Operational Meaning      |
| ------------------ | ------------------------ |
| silver_orders      | customer delivery truth  |
| silver_order_items | seller fulfillment truth |

This separation preserves:

- clean dimensional modeling
- seller accountability integrity
- KPI correctness
- streaming alignment

and follows Kimball best practices.

---

# Final Architectural Value

The `silver_order_items` dataset transforms:

# raw seller shipment events

into:

# trusted logistics-aware operational intelligence

through:

- financial standardization
- logistics enrichment
- freight intelligence
- seller accountability metrics
- grain-preserving transformations
- validation-driven governance

This dataset establishes:

# trusted seller operational truth

for:

- fulfillment analytics
- delivery enrichment
- freight intelligence
- logistics investigation
- sales analysis
- streaming operational monitoring

and acts as:

# the logistics operational backbone

of the Olist Seller Intelligence Platform.
