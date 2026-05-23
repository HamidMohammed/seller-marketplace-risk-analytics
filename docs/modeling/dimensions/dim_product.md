# DIMENSION — `dim_product`

## Objective

The `dim_product` dimension stores product identity, category, and physical characteristics.

This dimension supports:

- logistics analysis
- delivery risk analysis
- product category KPIs
- freight cost investigation
- operational bottleneck analysis

---

# Grain

# ONE ROW = ONE PRODUCT

Each row represents one unique product sold on the platform.

---

# Source Tables

| Source Table                 | Purpose                      |
| ---------------------------- | ---------------------------- |
| olist_products_dataset       | Product attributes           |
| product_category_translation | English category translation |

---

# Schema Design

| Column Name                | Datatype      | Description                   |
| -------------------------- | ------------- | ----------------------------- |
| product_sk                 | BIGINT        | Warehouse surrogate key       |
| product_id                 | VARCHAR       | Business product identifier   |
| product_category_name      | VARCHAR       | Portuguese category           |
| product_category_english   | VARCHAR       | English translated category   |
| product_name_length        | INTEGER       | Product title character count |
| product_description_length | INTEGER       | Description character count   |
| product_photos_qty         | INTEGER       | Number of product photos      |
| product_weight_g           | DECIMAL(10,2) | Product weight in grams       |
| product_length_cm          | DECIMAL(10,2) | Product length                |
| product_height_cm          | DECIMAL(10,2) | Product height                |
| product_width_cm           | DECIMAL(10,2) | Product width                 |
| product_volume_cm3         | DECIMAL(12,2) | Derived cubic volume          |
| product_size_bucket        | VARCHAR       | Small / Medium / Large        |

---

# Derived Logic

## Product Volume

Calculated as:

```sql
product_length_cm * product_height_cm * product_width_cm
```

## Product Size Bucket

Derived from volume thresholds.

Example:

VolumeBucketSmall<= thresholdMediummoderate sizeLargeoversized

Supports logistics segmentation.

# Why This Dimension Matters

Product characteristics strongly affect:

- shipping difficulty
- freight cost
- delivery duration
- carrier complexity

Heavy or oversized products often correlate with:

- higher freight cost
- delayed deliveries
- increased logistics risk

# Relationships

Fact TableRelationshipfct_seller_fulfillmentproduct_sk_fkFuture sales martproduct_sk_fkFuture review martproduct_sk_fk

# Business Use Cases

## Freight Cost Analysis

Analyze:

- which categories generate highest shipping cost
- oversized product logistics burden

## Delay Segmentation

Measure:

- delay rates by category
- heavy-product delivery risk
- fragile category performance

## Operational Efficiency

Track:

- seller specialization
- category-level fulfillment performance
- operational bottlenecks

# Best Practices Applied

- Translation normalization
- Derived logistics metrics
- Category standardization
- Reusable conformed dimension

# Common Student Mistakes Avoided

## Mistake 1 — No Category Translation

Wrong:

- Portuguese-only categories

Correct:

- translated analytical categories

## Mistake 2 — Ignoring Product Size

Wrong:

- treating all products equally

Correct:

- modeling logistics impact

## Mistake 3 — Embedding Product Fields Inside Facts

Wrong:

- duplicated product attributes

Correct:

- reusable dimension modeling

# Integration With Project Narrative

Products influence:

- freight cost
- delivery duration
- seller operational load
- logistics complexity

This dimension supports deeper operational analysis rather than surface-level sales reporting.
