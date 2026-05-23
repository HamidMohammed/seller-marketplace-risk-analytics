# `silver_sellers.md`

## Objective

The `silver_sellers` dataset represents the trusted seller dimensional enrichment layer inside the Olist Seller Intelligence Platform.

This dataset transforms:

# raw seller registry records

into:

# validated geography-aware seller intelligence

used by:

- seller performance analytics
- seller fulfillment intelligence
- seller-risk monitoring
- regional seller analytics
- marketplace operational monitoring
- dimensional modeling
- streaming enrichment

The dataset acts as:

# the seller dimensional backbone

across the analytical warehouse.

Unlike:

- `silver_orders`
- `silver_order_items`

which represent:

# operational transactional events

`silver_sellers`
represents:

# operational business entities.

This distinction is architecturally critical.

---

# Dataset Role in Architecture

```text id="u4l2j3"
Bronze Sellers
        +
silver_geolocation
        ↓
silver_sellers
        ↓
Seller Dimension + Seller Intelligence
```

This dataset powers:

- seller regional analytics
- seller operational segmentation
- seller performance KPIs
- fulfillment-region analysis
- logistics intelligence
- seller-risk monitoring
- marketplace governance

and acts as:

# the seller enrichment foundation

of the warehouse.

---

# Dataset Grain

# ONE ROW = ONE SELLER

This grain is strictly preserved throughout all transformations.

The dataset intentionally models:

# seller-level dimensional intelligence

NOT:

- order-level events
- fulfillment transactions
- delivery records

Maintaining this grain is critical because:
seller duplication would corrupt:

- seller KPIs
- fulfillment analytics
- regional seller segmentation
- downstream fact relationships

---

# Source Datasets

| Source Dataset     | Layer  | Purpose                       |
| ------------------ | ------ | ----------------------------- |
| bronze/sellers     | Bronze | Raw seller registry           |
| silver_geolocation | Silver | Trusted geographic enrichment |

---

# Source Columns

| Column                 | Meaning                    |
| ---------------------- | -------------------------- |
| seller_id              | Seller business identifier |
| seller_zip_code_prefix | Seller ZIP-prefix          |
| seller_city            | Seller city                |
| seller_state           | Seller state               |

---

# Important Seller Interpretation

Sellers represent:

# operational marketplace entities

rather than:

# passive dimensional consumers.

This means sellers later become central to:

- fulfillment analysis
- delivery performance
- operational risk scoring
- seller acquisition analytics
- logistics monitoring

This makes:
`silver_sellers`

one of the MOST strategically important dimensions
in the platform.

---

# Silver Responsibilities

The `silver_sellers` pipeline is responsible for:

| Responsibility             | Purpose                      |
| -------------------------- | ---------------------------- |
| Seller-key validation      | dimensional integrity        |
| ZIP-prefix standardization | geographic joins             |
| City normalization         | regional consistency         |
| State normalization        | KPI consistency              |
| Geographic enrichment      | seller regional intelligence |
| Metadata enrichment        | lineage                      |
| Validation governance      | analytical trust             |

---

# Geographic Enrichment Strategy

The dataset enriches sellers using:

# silver_geolocation

through:

```text id="0drk8z"
seller_zip_code_prefix
=
zip_code_prefix
```

This creates:

# trusted geography-aware seller intelligence

without rebuilding geographic transformation logic.

This follows:

# layered enrichment architecture

where trusted Silver datasets are reused across the platform.

---

# Why Reuse `silver_geolocation`?

The project intentionally avoids:

# duplicated geographic engineering

inside multiple pipelines.

Instead:
`silver_geolocation`
acts as:

# centralized geographic enrichment infrastructure.

This ensures:

- deterministic enrichment
- reusable analytical logic
- regional consistency
- scalable architecture

---

# Transformations Applied

---

# 1. ZIP Prefix Standardization

## Transformation

```python id="v8x4e9"
cast(seller_zip_code_prefix as integer)
```

---

## Purpose

Ensures:

- deterministic enrichment joins
- geographic compatibility
- dimensional consistency

---

# 2. City Normalization

## Transformation

```python id="bn1p0o"
lower(trim(seller_city))
```

---

## Purpose

Prevents:

- grouping fragmentation
- duplicate regional categories
- inconsistent dashboard filters

Supports:

- reliable seller segmentation
- regional KPI grouping
- analytical consistency

---

# 3. State Normalization

## Transformation

```python id="g8v4ri"
upper(trim(seller_state))
```

---

## Purpose

Standardizes:
Brazilian state abbreviations

for:

- regional analytics
- dashboard filtering
- geographic segmentation

---

# 4. Geographic Enrichment

## Enrichment Source

```text id="l9g2af"
silver_geolocation
```

---

## Added Attributes

| Column           | Purpose               |
| ---------------- | --------------------- |
| median_latitude  | geographic enrichment |
| median_longitude | regional intelligence |

---

## Business Meaning

Enables:

# geography-aware seller analytics

including:

- seller regional distribution
- fulfillment-region intelligence
- regional seller KPIs
- logistics-area analysis

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

```text id="jlwmm1"
silver_transformation_strategy.md
```

All dimensional transformations are validated BEFORE Silver output generation.

---

# Validation Rules

---

# 1. Grain Validation

## Rule

```text id="tpmr0s"
ONE ROW = ONE SELLER
```

---

## Validation

```python id="2gyr3x"
validate_duplicates(seller_id)
```

---

## Purpose

Protect:

- seller KPIs
- fulfillment analytics
- downstream joins
- operational attribution

---

# 2. Critical Null Validation

## Critical Columns

| Column                 | Reason                |
| ---------------------- | --------------------- |
| seller_id              | seller business key   |
| seller_zip_code_prefix | geographic linkage    |
| seller_city            | regional segmentation |
| seller_state           | regional analytics    |

---

## Purpose

Prevent:

- broken seller enrichment
- invalid geographic joins
- incomplete dimensional records

---

# 3. Geographic Enrichment Validation

## Validation

Validate:

- latitude availability
- longitude availability
- ZIP-prefix enrichment completeness

---

## Purpose

Ensure:

# trusted seller geographic intelligence

for downstream analytics.

---

# 4. State Validation

## Rule

State values must match:

# valid Brazilian state abbreviations

---

## Purpose

Protect:

- regional grouping consistency
- dashboard filtering
- seller KPI integrity

---

# 5. City Normalization Validation

## Purpose

Ensure:

- deterministic city representation
- reliable regional segmentation
- grouping consistency

---

# 6. ZIP Prefix Validation

## Rule

```text id="x6v7qz"
seller_zip_code_prefix > 0
```

---

## Purpose

Prevent:

- invalid geographic joins
- broken enrichment mappings
- unusable seller regions

---

# Important Architectural Decisions

---

# Sellers as Operational Dimensions

The project models sellers as:

# operational business dimensions

NOT:

# transactional fact events.

This is a critical dimensional-modeling decision.

Seller datasets should describe:

- who the seller is
- where the seller operates geographically

NOT:

- fulfillment transactions themselves

which belong inside:

- delivery facts
- fulfillment facts
- sales facts

---

# Layered Geographic Reuse

The pipeline intentionally reuses:

# silver_geolocation

instead of:

# rebuilding geographic intelligence.

This enforces:

- modular architecture
- enrichment consistency
- reusable analytical infrastructure

and follows:

# enterprise medallion principles.

---

# Controlled Dimensional Enrichment

The dataset intentionally avoids:

- sales enrichment
- payment enrichment
- review aggregation
- fulfillment aggregation

inside:
`silver_sellers`

because Silver dimensions should remain:

# focused and reusable

rather than:

# heavily denormalized marts.

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
- dimensional integrity
- analytical defensibility

---

# Downstream Dependencies

The following datasets depend on:

# silver_sellers

| Dataset                | Dependency Purpose           |
| ---------------------- | ---------------------------- |
| dim_seller             | dimensional modeling         |
| fct_seller_fulfillment | seller operational analytics |
| fct_order_sales        | seller revenue analytics     |
| fct_order_delivery     | seller delivery analysis     |
| fct_seller_acquisition | seller growth analytics      |

This makes:
`silver_sellers`

a:

# shared conformed seller dimension foundation

across the warehouse.

---

# Streaming Architecture Role

`silver_sellers`
supports:

# seller operational enrichment

for:

- seller-risk monitoring
- regional seller analysis
- fulfillment intelligence
- logistics-region monitoring

Streaming systems can use:

- seller region
- seller geography
- regional seller segmentation

for:

# real-time seller intelligence enrichment.

---

# Output Dataset Location

```text id="n5i1dx"
data/silver/sellers/
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

| Layer  | Purpose                                |
| ------ | -------------------------------------- |
| Bronze | raw seller registry                    |
| Silver | trusted seller enrichment              |
| Gold   | seller intelligence & analytical marts |

The Silver layer transforms:

# raw seller entities

into:

# trusted geography-aware seller intelligence.

---

# Final Architectural Value

The `silver_sellers` dataset transforms:

# raw seller registry records

into:

# trusted geographically enriched seller intelligence

through:

- dimensional standardization
- ZIP-prefix normalization
- geographic enrichment
- regional validation
- deterministic seller governance

This dataset establishes:

# trusted seller dimensional intelligence

for:

- seller analytics
- fulfillment intelligence
- seller-risk monitoring
- regional KPI reporting
- dimensional modeling
- streaming enrichment

and acts as:

# the seller intelligence backbone

of the Olist Seller Intelligence Platform.
