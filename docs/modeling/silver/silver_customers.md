# `silver_customers.md`

## Objective

The `silver_customers` dataset represents the trusted customer dimensional enrichment layer inside the Olist Seller Intelligence Platform.

This dataset transforms:

# raw customer registry records

into:

# validated geography-aware customer intelligence

used by:

- customer analytics
- regional segmentation
- delivery-region analysis
- geographic KPI reporting
- customer distribution analytics
- dimensional modeling
- streaming enrichment

The dataset acts as:

# the conformed customer enrichment foundation

across the analytical warehouse.

Unlike:

- `silver_orders`
- `silver_order_items`

which represent:

# operational transactional truth

`silver_customers`
represents:

# customer dimensional intelligence.

---

# Dataset Role in Architecture

```text id="dcxf5k"
Bronze Customers
        +
silver_geolocation
        ↓
silver_customers
        ↓
Customer Dimension + Regional Analytics
```

This dataset powers:

- customer regional segmentation
- customer-state analytics
- regional delivery analysis
- customer distribution KPIs
- geographic dashboarding
- customer enrichment

and acts as:

# the customer dimensional backbone

of the warehouse.

---

# Dataset Grain

# ONE ROW = ONE CUSTOMER

This grain is strictly preserved throughout all transformations.

The dataset intentionally models:

# customer-level dimensional intelligence

NOT:

- order-level events
- delivery-level events
- seller-level operations

Maintaining this grain is critical because:
customer duplication would corrupt:

- customer KPIs
- segmentation analysis
- geographic distributions
- downstream dimensional joins

---

# Source Datasets

| Source Dataset     | Layer  | Purpose                       |
| ------------------ | ------ | ----------------------------- |
| bronze/customers   | Bronze | Raw customer registry         |
| silver_geolocation | Silver | Trusted geographic enrichment |

---

# Source Columns

| Column                   | Meaning                          |
| ------------------------ | -------------------------------- |
| customer_id              | Customer business identifier     |
| customer_unique_id       | Unique logical customer identity |
| customer_zip_code_prefix | Customer ZIP-prefix              |
| customer_city            | Customer city                    |
| customer_state           | Customer state                   |

---

# Important Customer Identity Interpretation

The dataset contains:

# two customer identifiers

---

# customer_id

Represents:

# transactional customer instance

Used operationally inside:

- orders
- delivery linkage
- transactional relationships

---

# customer_unique_id

Represents:

# logical real-world customer identity

Used analytically for:

- repeat-customer analysis
- customer retention
- customer behavior analytics

This distinction is architecturally important because:
one logical customer may appear across:

# multiple customer_id records

over time.

---

# Silver Responsibilities

The `silver_customers` pipeline is responsible for:

| Responsibility             | Purpose               |
| -------------------------- | --------------------- |
| Customer-key validation    | dimensional integrity |
| ZIP-prefix standardization | geographic joins      |
| City normalization         | grouping consistency  |
| State normalization        | KPI consistency       |
| Geographic enrichment      | regional intelligence |
| Metadata enrichment        | lineage               |
| Validation governance      | dimensional trust     |

---

# Geographic Enrichment Strategy

The dataset enriches customers using:

# silver_geolocation

through:

```text id="mkf0h7"
customer_zip_code_prefix
=
zip_code_prefix
```

This creates:

# trusted region-aware customer intelligence

without duplicating geographic transformation logic.

This follows:

# layered enrichment architecture

where trusted Silver datasets are reused across the platform.

---

# Why Reuse `silver_geolocation`?

The project intentionally avoids:

# rebuilding geographic intelligence

inside multiple pipelines.

Instead:
`silver_geolocation`
acts as:

# centralized geographic enrichment infrastructure.

This ensures:

- enrichment consistency
- deterministic regional mapping
- reusable analytical logic
- scalable architecture

---

# Transformations Applied

---

# 1. ZIP Prefix Standardization

## Transformation

```python id="i9g10s"
cast(customer_zip_code_prefix as integer)
```

---

## Purpose

Ensures:

- deterministic enrichment joins
- dimensional consistency
- geographic compatibility

---

# 2. City Normalization

## Transformation

```python id="b7m1rt"
lower(trim(customer_city))
```

---

## Purpose

Prevents:

- grouping fragmentation
- inconsistent regional categories
- dashboard inconsistencies

Supports:

- reliable segmentation
- regional grouping
- analytical consistency

---

# 3. State Normalization

## Transformation

```python id="4t8lzk"
upper(trim(customer_state))
```

---

## Purpose

Standardizes:
Brazilian state abbreviations

for:

- regional filtering
- dashboard consistency
- KPI grouping

---

# 4. Geographic Enrichment

## Enrichment Source

```text id="gnbr1v"
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

# geography-aware customer analytics

including:

- regional distributions
- state-level KPIs
- geographic segmentation
- logistics-region analysis

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

```text id="b6ghlm"
silver_transformation_strategy.md
```

All dimensional transformations are validated BEFORE Silver output generation.

---

# Validation Rules

---

# 1. Grain Validation

## Rule

```text id="lj7n8x"
ONE ROW = ONE CUSTOMER
```

---

## Validation

```python id="7d2gye"
validate_duplicates(customer_id)
```

---

## Purpose

Protect:

- customer KPIs
- dimensional integrity
- downstream joins
- segmentation correctness

---

# 2. Critical Null Validation

## Critical Columns

| Column                   | Reason                    |
| ------------------------ | ------------------------- |
| customer_id              | dimensional business key  |
| customer_unique_id       | logical customer identity |
| customer_zip_code_prefix | geographic linkage        |
| customer_city            | regional segmentation     |
| customer_state           | regional analytics        |

---

## Purpose

Prevent:

- broken customer enrichment
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

# trusted customer geographic intelligence

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
- geographic KPI integrity

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

```text id="bnkp4i"
customer_zip_code_prefix > 0
```

---

## Purpose

Prevent:

- invalid geographic joins
- broken enrichment mappings
- unusable customer regions

---

# Important Architectural Decisions

---

# Customers as Dimensions

The project models customers as:

# conformed analytical dimensions

NOT:

# transactional facts.

This is a critical dimensional-modeling decision.

Customer datasets should describe:

- who the customer is
- where the customer belongs geographically

NOT:

- operational order events

---

# Layered Geographic Reuse

The pipeline intentionally reuses:

# silver_geolocation

instead of:

# recalculating geo intelligence.

This enforces:

- modular architecture
- enrichment consistency
- reusable analytical infrastructure

and follows:

# enterprise medallion principles.

---

# Controlled Dimensional Enrichment

The dataset intentionally avoids:

- payment enrichment
- review enrichment
- sales enrichment
- delivery aggregation

inside:
`silver_customers`

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

# silver_customers

| Dataset              | Dependency Purpose          |
| -------------------- | --------------------------- |
| dim_customer         | dimensional modeling        |
| fct_order_sales      | customer enrichment         |
| fct_order_delivery   | regional delivery analytics |
| fct_customer_reviews | customer segmentation       |
| marketing analytics  | regional targeting          |

This makes:
`silver_customers`

a:

# shared conformed customer dimension foundation

across the warehouse.

---

# Streaming Architecture Role

`silver_customers`
supports:

# customer enrichment intelligence

for:

- regional segmentation
- customer-state monitoring
- geographic targeting
- streaming customer analytics

Streaming systems can use:

- customer region
- geographic segmentation
- regional grouping

for:

# real-time enrichment pipelines.

---

# Output Dataset Location

```text id="0y4r8v"
data/silver/customers/
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
| Bronze | raw customer registry                  |
| Silver | trusted customer enrichment            |
| Gold   | customer analytics & dimensional marts |

The Silver layer transforms:

# raw customer entities

into:

# trusted geography-aware customer intelligence.

---

# Final Architectural Value

The `silver_customers` dataset transforms:

# raw customer registry records

into:

# trusted geographically enriched customer intelligence

through:

- dimensional standardization
- ZIP-prefix normalization
- geographic enrichment
- regional validation
- deterministic customer governance

This dataset establishes:

# trusted customer dimensional intelligence

for:

- customer analytics
- regional segmentation
- delivery-region analysis
- geographic KPI reporting
- dimensional modeling
- streaming enrichment

and acts as:

# the customer enrichment backbone

of the Olist Seller Intelligence Platform.
