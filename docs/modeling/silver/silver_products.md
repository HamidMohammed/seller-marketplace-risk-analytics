# `silver_products.md`

## Objective

The `silver_products` dataset represents the trusted product dimensional intelligence layer inside the Olist Seller Intelligence Platform.

This dataset transforms:

# raw product registry records

into:

# validated operationally enriched product intelligence

used by:

- product analytics
- category performance analysis
- logistics intelligence
- freight analysis
- seller-product analytics
- marketplace monitoring
- dimensional modeling

The dataset acts as:

# the product intelligence foundation

across the analytical warehouse.

Unlike:

- customer dimensions
- seller dimensions

products contain:

# operational logistics attributes

which makes this dataset BOTH:

- analytical
- operationally significant

inside downstream marts.

---

# Dataset Role in Architecture

```text id="5k9u6d"
Bronze Products
        ↓
silver_products
        ↓
Product Dimension + Logistics Intelligence
```

This dataset powers:

- product-category analytics
- logistics complexity analysis
- freight investigation
- oversized shipment analysis
- seller-product intelligence
- review-category analytics
- marketplace product monitoring

and acts as:

# the product enrichment backbone

of the warehouse.

---

# Dataset Grain

# ONE ROW = ONE PRODUCT

This grain is strictly preserved throughout all transformations.

The dataset intentionally models:

# reusable product dimensional intelligence

NOT:

- sales transactions
- delivery events
- payment operations
- review aggregations

Maintaining this grain is critical because:
product duplication would corrupt:

- product KPIs
- category aggregations
- logistics analytics
- downstream fact joins

---

# Source Dataset

| Source Dataset  | Layer  | Purpose              |
| --------------- | ------ | -------------------- |
| bronze/products | Bronze | Raw product registry |

---

# Source Columns

| Column                     | Meaning                     |
| -------------------------- | --------------------------- |
| product_id                 | Product business identifier |
| product_category_name      | Product category            |
| product_name_length        | Product title length        |
| product_description_length | Product description length  |
| product_photos_qty         | Product image count         |
| product_weight_g           | Product weight              |
| product_length_cm          | Product length              |
| product_height_cm          | Product height              |
| product_width_cm           | Product width               |

---

# Important Product Data Challenges

The raw products dataset contains:

# significant missing values

especially for:

- product_category_name
- product_weight_g
- dimensional attributes

This creates:

# governance and dimensional-quality challenges

requiring:

- controlled validation
- documented anomaly handling
- operational truth preservation

rather than:

# aggressive record deletion.

---

# Silver Responsibilities

The `silver_products` pipeline is responsible for:

| Responsibility            | Purpose               |
| ------------------------- | --------------------- |
| Product-key validation    | dimensional integrity |
| Category normalization    | grouping consistency  |
| Logistics standardization | operational analytics |
| Product volume derivation | freight intelligence  |
| Metadata enrichment       | lineage               |
| Validation governance     | analytical trust      |

---

# Product Category Strategy

The dataset standardizes:

# product_category_name

to ensure:

- deterministic grouping
- dashboard consistency
- category KPI stability

---

# Category Normalization

## Transformation

```python id="7rwv6g"
lower(trim(product_category_name))
```

---

## Purpose

Prevents:

- category fragmentation
- inconsistent dashboard filters
- duplicated category groupings

Supports:

- stable category analytics
- trustworthy aggregations
- reliable segmentation

---

# Logistics Intelligence Strategy

Products contain:

# operational logistics attributes

including:

- weight
- dimensions
- physical size

This makes:
`silver_products`

foundational for:

# logistics intelligence.

---

# Product Volume Derivation

## Derived Metric

```text id="gkkb36"
product_volume_cm3
```

---

## Formula

product_volume_cm^3 = length\times width\times height

---

## Business Meaning

Represents:

# physical shipment volume

used for:

- freight analysis
- oversized shipment detection
- warehouse complexity analysis
- logistics intelligence

---

# Why Product Volume Matters

Product volume later becomes critical for:

- freight-cost analysis
- shipping optimization
- delivery complexity
- logistics inefficiency detection

This is one of the MOST valuable operational enrichments
inside the product dimension.

---

# Transformations Applied

---

# 1. Product Key Standardization

## Transformation

```python id="7a7p0d"
trim(product_id)
```

---

## Purpose

Ensures:

- stable joins
- dimensional consistency
- reliable downstream relationships

---

# 2. Category Normalization

## Transformation

```python id="3p3d0y"
lower(trim(product_category_name))
```

---

## Purpose

Supports:

- category consistency
- deterministic grouping
- analytical trust

---

# 3. Numeric Standardization

## Transformation

Cast logistics attributes into:

# controlled numeric types

including:

- weights
- dimensions
- product metrics

---

## Purpose

Ensures:

- KPI-safe calculations
- reliable aggregations
- logistics consistency

---

# 4. Product Volume Derivation

## Derived Attribute

```text id="tx4kk7"
product_volume_cm3
```

---

## Purpose

Enables:

# advanced logistics analytics

and:

# freight intelligence.

---

# 5. Metadata Enrichment

## Added Columns

| Column                 | Purpose          |
| ---------------------- | ---------------- |
| silver_loaded_at       | pipeline lineage |
| source_system          | traceability     |
| transformation_version | reproducibility  |

---

# Validation Framework

The dataset follows:

# validation-driven dimensional governance

defined in:

```text id="l14vxe"
silver_transformation_strategy.md
```

All dimensional transformations are validated BEFORE Silver output generation.

---

# Validation Rules

---

# 1. Grain Validation

## Rule

```text id="vlgp4j"
ONE ROW = ONE PRODUCT
```

---

## Validation

```python id="f1fr2u"
validate_duplicates(product_id)
```

---

## Purpose

Protect:

- product KPIs
- category analytics
- downstream joins
- logistics calculations

---

# 2. Critical Null Validation

## Critical Columns

| Column     | Reason                   |
| ---------- | ------------------------ |
| product_id | dimensional business key |

---

## Purpose

Prevent:

- broken fact relationships
- unusable product records
- invalid dimensional joins

---

# 3. Category Validation

## Purpose

Validate:

- category normalization
- category consistency
- deterministic grouping behavior

---

# 4. Product Weight Validation

## Rule

```text id="jlwmw2"
product_weight_g >= 0
```

---

## Purpose

Prevent:

- impossible logistics values
- invalid freight calculations
- broken operational analytics

---

# 5. Product Dimension Validation

## Validated Columns

| Column            |
| ----------------- |
| product_length_cm |
| product_height_cm |
| product_width_cm  |

---

## Purpose

Ensure:

- physically valid dimensions
- trustworthy shipment metrics
- reliable logistics intelligence

---

# 6. Product Volume Validation

## Rule

```text id="ljn5so"
product_volume_cm3 >= 0
```

---

## Purpose

Protect:

- logistics calculations
- freight analytics
- warehouse intelligence

---

# Important Architectural Decisions

---

# Products as Reusable Dimensions

The project models products as:

# conformed reusable dimensions

NOT:

# transactional events.

Products should describe:

- what the product is
- how large the product is
- what category it belongs to

NOT:

- how much it sold
- who bought it
- payment outcomes

Those belong in:

# facts and marts.

---

# Operational Truth Preservation

The project intentionally preserves:

# incomplete but operationally valid products

instead of:

# aggressively deleting records.

This follows:

# zero silent data-loss policy

defined in the Silver governance strategy.

This is especially important because:
real-world product catalogs commonly contain:

- incomplete dimensions
- missing categories
- inconsistent logistics metadata

---

# Controlled Null Governance

Missing logistics attributes are:

- documented
- validated
- reported

rather than:

# silently discarded.

This improves:

- auditability
- reproducibility
- analytical defensibility

---

# Controlled Dimensional Scope

The dataset intentionally avoids:

- seller enrichment
- sales metrics
- payment metrics
- review aggregations

inside:
`silver_products`

because Silver dimensions should remain:

# modular and reusable

rather than:

# heavily denormalized marts.

---

# Downstream Dependencies

The following datasets depend on:

# silver_products

| Dataset                | Dependency Purpose              |
| ---------------------- | ------------------------------- |
| dim_product            | dimensional modeling            |
| fct_order_sales        | product sales analytics         |
| fct_seller_fulfillment | logistics intelligence          |
| fct_customer_reviews   | review-category analytics       |
| delivery analytics     | freight & shipment intelligence |

This makes:
`silver_products`

a:

# shared conformed product dimension foundation

across the warehouse.

---

# Streaming Architecture Role

`silver_products`
supports:

# operational logistics enrichment

for:

- shipment intelligence
- freight monitoring
- oversized product detection
- category-level operational monitoring

Streaming systems can use:

- product category
- product dimensions
- shipment volume

for:

# real-time logistics intelligence.

---

# Output Dataset Location

```text id="u6k2u9"
data/silver/products/
```

Stored as:

# parquet

for:

- Spark optimization
- scalable dimensional processing
- warehouse integration

---

# Relationship to Medallion Architecture

Within the Medallion Architecture:

| Layer  | Purpose                             |
| ------ | ----------------------------------- |
| Bronze | raw product registry                |
| Silver | trusted product enrichment          |
| Gold   | product analytics & logistics marts |

The Silver layer transforms:

# raw product records

into:

# trusted operational product intelligence.

---

# Final Architectural Value

The `silver_products` dataset transforms:

# raw product registry records

into:

# trusted operationally enriched product intelligence

through:

- dimensional standardization
- category normalization
- logistics enrichment
- derived shipment metrics
- validation governance
- deterministic dimensional engineering

This dataset establishes:

# trusted product intelligence foundation

for:

- product analytics
- category KPIs
- logistics intelligence
- freight analysis
- seller-product analytics
- dimensional modeling

and acts as:

# the product intelligence backbone

of the Olist Seller Intelligence Platform.
