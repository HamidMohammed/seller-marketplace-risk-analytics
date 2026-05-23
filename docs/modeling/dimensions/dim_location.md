---

# `dim_location.md`

```markdown
# DIMENSION — `dim_location`

## Objective

The `dim_location` dimension standardizes geographic entities used across the warehouse.

This dimension supports:

- regional analytics
- logistics routing analysis
- distance bucketing
- cross-region KPI reporting
- streaming geographic enrichment

---

# Grain

# ONE ROW = ONE UNIQUE GEOGRAPHIC LOCATION

A location is defined by:

- ZIP prefix
- city
- state

---

# Source Table

| Source Table              | Purpose                |
| ------------------------- | ---------------------- |
| olist_geolocation_dataset | Geographic coordinates |

---

# Schema Design

| Column Name     | Datatype      | Description             |
| --------------- | ------------- | ----------------------- |
| location_sk     | BIGINT        | Warehouse surrogate key |
| zip_code_prefix | VARCHAR       | Geographic ZIP prefix   |
| city            | VARCHAR       | City name               |
| state           | VARCHAR       | State abbreviation      |
| region          | VARCHAR       | Brazilian macro region  |
| latitude        | DECIMAL(10,6) | Latitude                |
| longitude       | DECIMAL(10,6) | Longitude               |

---

# Geographic Standardization Strategy

The raw geolocation dataset contains:

- duplicate ZIP entries
- inconsistent spellings
- repeated coordinates

The warehouse standardizes location data using:

- deduplication
- median coordinate resolution
- normalized city names

This improves:

- analytical consistency
- distance calculations
- streaming enrichment quality

---

# Region Mapping

States are grouped into:

- North
- Northeast
- Central-West
- Southeast
- South

Supports executive-level regional storytelling.

---

# Relationships

| Fact Table             | Relationship          |
| ---------------------- | --------------------- |
| fct_order_delivery     | geographic enrichment |
| fct_seller_fulfillment | shipment geography    |
| Streaming pipeline     | distance calculation  |

---

# Business Use Cases

## Distance Bucket Calculation

Used for:

- Same City
- Same State
- Cross State
- Cross Region

classification logic inside `fct_order_delivery`.

---

## Regional Delivery Analysis

Analyze:

- regional delay concentration
- underserved logistics areas
- cross-region shipping pressure

---

## Streaming Risk Enrichment

Streaming jobs enrich live events with:

- seller region
- customer region
- shipment distance category

Supports operational risk scoring.

---

# Why Separate Location Dimension Exists

Even though customer and seller dimensions contain geography:

`dim_location` centralizes:

- reusable geographic logic
- coordinate standardization
- regional grouping

This avoids duplicated geographic transformations across dimensions.

---

# Best Practices Applied

- Geographic normalization
- Coordinate standardization
- Conformed regional logic
- Streaming compatibility

---

# Common Student Mistakes Avoided

## Mistake 1 — Raw Geolocation Usage

Wrong:

- directly using dirty ZIP records

Correct:

- standardized geographic dimension

---

## Mistake 2 — Repeating Geography Logic Everywhere

Wrong:

- duplicated region derivation

Correct:

- centralized location modeling

---

## Mistake 3 — No Distance Intelligence

Wrong:

- city/state only

Correct:

- logistics-aware geographic modeling

---

# Integration With Architecture

This dimension supports:

- Power BI regional dashboards
- Spark logistics analysis
- streaming enrichment
- delivery risk segmentation

Aligned with the warehouse geographic enrichment strategy and streaming architecture.
