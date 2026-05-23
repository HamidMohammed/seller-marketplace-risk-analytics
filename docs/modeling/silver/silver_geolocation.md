# `silver_geolocation.md`

## Objective

The `silver_geolocation` dataset represents the trusted geographic enrichment foundation layer inside the Olist Seller Intelligence Platform.

This dataset transforms:

# noisy raw zip-prefix geographic records

into:

# stable validated geographic intelligence

used by:

- customer regional analytics
- seller regional analytics
- logistics intelligence
- freight analysis
- delivery-region analytics
- geographic dashboarding
- operational enrichment

The dataset acts as:

# the geographic reference foundation

for all downstream regional intelligence.

Unlike transactional datasets:
`silver_geolocation`
is:

# reference enrichment infrastructure

rather than:

# operational event data.

---

# Dataset Role in Architecture

```text id="0jcz6w"
Bronze Geolocation
        ↓
silver_geolocation
        ↓
Customer + Seller Enrichment
        ↓
Regional Analytics & Logistics Intelligence
```

This dataset powers:

- geographic enrichment
- regional KPI grouping
- freight investigation
- delivery-distance intelligence
- seller territory analysis
- customer distribution analysis

and acts as:

# the geographic intelligence backbone

of the warehouse.

---

# Geographic Data Interpretation

The Olist geolocation dataset does NOT represent:

# exact customer homes

or:

# exact seller locations

Instead:
the coordinates represent:

# Brazilian ZIP-code geographic areas

specifically:

```text id="3l8m8s"
geolocation_zip_code_prefix
```

This distinction is architecturally critical.

The platform therefore models:

# approximate regional intelligence

NOT:

# GPS-level precision.

This design decision prevents:

- false geographic precision
- misleading distance assumptions
- invalid operational interpretations

and aligns the warehouse with:

# realistic geographic governance.

---

# Dataset Grain

# ONE ROW = ONE ZIP CODE PREFIX AREA

This grain is strictly enforced throughout the Silver transformation process.

The dataset intentionally aggregates:
multiple noisy coordinate records

into:

# one stable geographic representation

per ZIP-prefix area.

This prevents:

- unstable joins
- geographic duplication
- inconsistent regional enrichment

---

# Source Dataset

| Source Dataset     | Layer  | Purpose                          |
| ------------------ | ------ | -------------------------------- |
| bronze/geolocation | Bronze | Raw geographic reference records |

---

# Source Columns

| Column                      | Meaning              |
| --------------------------- | -------------------- |
| geolocation_zip_code_prefix | Brazilian ZIP prefix |
| geolocation_lat             | Latitude             |
| geolocation_lng             | Longitude            |
| geolocation_city            | City                 |
| geolocation_state           | State                |

---

# Key Raw Dataset Problem

The raw dataset contains:

# multiple coordinate records

for the SAME:

```text id="ck3z2i"
zip_code_prefix
```

Example:

| ZIP Prefix | Multiple Coordinates |
| ---------- | -------------------- |
| 1046       | Yes                  |

This creates:

- geographic inconsistency
- unstable enrichment
- ambiguous regional mapping

Therefore:
Silver transformation is required to establish:

# deterministic geographic intelligence.

---

# Silver Responsibilities

The `silver_geolocation` pipeline is responsible for:

| Responsibility           | Purpose                    |
| ------------------------ | -------------------------- |
| ZIP-prefix deduplication | stable joins               |
| Coordinate aggregation   | geographic consistency     |
| City normalization       | regional grouping          |
| State normalization      | analytical standardization |
| Geographic validation    | spatial integrity          |
| Metadata enrichment      | lineage                    |
| Enrichment preparation   | downstream joins           |

---

# Geographic Aggregation Strategy

The Silver layer intentionally aggregates:
multiple coordinate records

into:

# one representative coordinate

per ZIP-prefix region.

---

# Chosen Aggregation Method

The platform uses:

# MEDIAN coordinate aggregation

for:

- latitude
- longitude

---

# Why MEDIAN Instead of AVERAGE?

Median aggregation is more robust against:

- noisy coordinates
- outlier records
- inconsistent regional mappings

This prevents:

# geographic distortion

caused by:

- anomalous coordinate entries
- data-entry inconsistencies
- extreme spatial outliers

---

# Why NOT First Record Selection?

Using:

```text id="4p2dtf"
first()
```

would create:

# non-deterministic enrichment

because:

- record order is not guaranteed
- geographic consistency becomes unstable

The project intentionally avoids:

# unstable enrichment logic.

---

# Transformations Applied

---

# 1. ZIP Prefix Standardization

## Transformation

```python id="3i9h8k"
cast(zip_code_prefix as integer)
```

---

## Purpose

Ensures:

- join consistency
- deterministic enrichment
- dimensional compatibility

---

# 2. City Normalization

## Transformation

```python id="x7z3ms"
lower(trim(city))
```

---

## Purpose

Prevents:

- casing inconsistencies
- grouping fragmentation
- duplicate regional values

Supports:

- reliable dashboards
- stable grouping logic
- regional KPI consistency

---

# 3. State Normalization

## Transformation

```python id="tn9oqk"
upper(trim(state))
```

---

## Purpose

Standardizes:
Brazilian state abbreviations

for:

- geographic consistency
- dashboard filtering
- regional aggregation

---

# 4. Median Latitude Aggregation

## Derived Column

```text id="jlwm5v"
median_latitude
```

---

## Business Meaning

Represents:

# stable approximate latitude

for a ZIP-prefix geographic area.

---

# 5. Median Longitude Aggregation

## Derived Column

```text id="5o5n4t"
median_longitude
```

---

## Business Meaning

Represents:

# stable approximate longitude

for a ZIP-prefix geographic area.

---

# 6. Geographic Record Deduplication

## Transformation Goal

Convert:

# multiple noisy geo records

into:

# one deterministic geo reference

per ZIP-prefix area.

---

# Business Importance

This transformation is critical because:
downstream datasets require:

# stable geographic enrichment.

Without deduplication:

- customer enrichment becomes inconsistent
- seller enrichment becomes unstable
- logistics analytics become unreliable

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

# validation-driven geographic governance

defined in:

```text id="h5l6yk"
silver_transformation_strategy.md
```

All geographic transformations are validated BEFORE Silver output generation.

---

# Validation Rules

---

# 1. Grain Validation

## Rule

```text id="4tvg5v"
ONE ROW = ONE ZIP PREFIX
```

---

## Validation

```python id="84e4vv"
validate_duplicates(zip_code_prefix)
```

---

## Purpose

Protect:

- stable enrichment joins
- regional consistency
- geographic dimensional integrity

---

# 2. Null Coordinate Validation

## Validated Columns

| Column           |
| ---------------- |
| median_latitude  |
| median_longitude |

---

## Purpose

Prevent:

- invalid geographic enrichment
- broken regional intelligence
- unusable spatial analytics

---

# 3. Latitude Range Validation

## Rule

```text id="e2mff0"
-90 <= latitude <= 90
```

---

## Purpose

Ensure:

# geographically valid coordinates

---

# 4. Longitude Range Validation

## Rule

```text id="yk0hyj"
-180 <= longitude <= 180
```

---

## Purpose

Prevent:

# impossible spatial locations

---

# 5. City Normalization Validation

## Purpose

Ensure:

- consistent regional grouping
- deterministic city representation
- dashboard filter reliability

---

# 6. State Validation

## Purpose

Ensure:
valid Brazilian state abbreviations are preserved.

Supports:

- regional filtering
- geographic segmentation
- operational territory analytics

---

# Important Architectural Decisions

---

# Approximate Geographic Intelligence

The platform intentionally models:

# approximate regional intelligence

NOT:

# exact physical coordinates.

This is an intentional governance decision because:
the raw dataset itself represents:

# ZIP-prefix regions

rather than:

# exact locations.

---

# Geographic Truth Preservation

The project intentionally preserves:

# realistic geographic ambiguity

instead of:

# artificial GPS precision.

This prevents:

- misleading analytics
- false operational assumptions
- invalid delivery-distance conclusions

---

# Controlled Geographic Enrichment

The dataset acts as:

# enrichment infrastructure

and intentionally avoids:

- transactional denormalization
- operational fact modeling
- delivery event duplication

This preserves:

- modular architecture
- enrichment consistency
- dimensional governance

---

# No Silent Geographic Record Deletion

The pipeline follows:

# zero silent data-loss policy

Meaning:
records may only be removed when:

- documented
- validated
- operationally justified

This preserves:

- reproducibility
- auditability
- analytical defensibility

---

# Downstream Dependencies

The following datasets depend on:

# silver_geolocation

| Dataset                | Dependency Purpose          |
| ---------------------- | --------------------------- |
| silver_customers       | customer enrichment         |
| silver_sellers         | seller enrichment           |
| fct_order_delivery     | regional delivery analytics |
| fct_seller_fulfillment | seller regional KPIs        |
| fct_order_sales        | regional sales analytics    |

This makes:
`silver_geolocation`

a:

# shared conformed enrichment dataset

across the warehouse.

---

# Streaming Architecture Role

`silver_geolocation`
supports:

# regional operational enrichment

for:

- regional delivery monitoring
- geographic risk analysis
- freight-region investigation
- seller territory analytics

Streaming systems can use:

- regional grouping
- geographic segmentation
- territory intelligence

for:

# real-time operational monitoring.

---

# Output Dataset Location

```text id="yvrygr"
data/silver/geolocation/
```

Stored as:

# parquet

for:

- scalable enrichment
- Spark optimization
- dimensional integration

---

# Relationship to Medallion Architecture

Within the Medallion Architecture:

| Layer  | Purpose                          |
| ------ | -------------------------------- |
| Bronze | raw noisy geographic records     |
| Silver | trusted geographic enrichment    |
| Gold   | regional analytical intelligence |

The Silver layer transforms:

# noisy geographic reference data

into:

# trusted reusable geographic intelligence.

---

# Final Architectural Value

The `silver_geolocation` dataset transforms:

# duplicated noisy geographic records

into:

# trusted regional enrichment intelligence

through:

- ZIP-prefix deduplication
- coordinate aggregation
- city normalization
- geographic validation
- deterministic enrichment engineering

This dataset establishes:

# trusted geographic foundation intelligence

for:

- customer enrichment
- seller enrichment
- logistics analytics
- freight investigation
- regional KPI analysis
- streaming geographic monitoring

and acts as:

# the geographic enrichment backbone

of the Olist Seller Intelligence Platform.
