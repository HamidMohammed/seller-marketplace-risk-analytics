# `customers_validation_report.md`

## Validation Report Overview

This report documents the validation results for the:

# `silver_customers`

dataset inside the:

# Olist Seller Intelligence Platform

The validation process follows:

# validation-driven dimensional governance

defined in the Silver transformation strategy.

The purpose of this validation layer is to ensure:

- customer dimensional integrity
- geographic enrichment reliability
- regional standardization
- ZIP-prefix consistency
- coordinate validity
- analytical trustworthiness

before the dataset becomes available for:

- dimensional modeling
- customer analytics
- regional segmentation
- delivery-region analysis
- geographic KPI reporting
- streaming enrichment

---

# Dataset Information

| Attribute         | Value                  |
| ----------------- | ---------------------- |
| Dataset           | silver_customers       |
| Layer             | Silver                 |
| Dataset Grain     | ONE ROW = ONE CUSTOMER |
| Validation Status | PASSED WITH WARNINGS   |
| Output Format     | Parquet                |

---

# Validation Scope

The validation framework covered:

| Validation Area                  | Objective                        |
| -------------------------------- | -------------------------------- |
| Row-count integrity              | prevent enrichment fan-out       |
| Grain validation                 | preserve customer uniqueness     |
| Critical null validation         | protect dimensional completeness |
| Customer ID validation           | ensure identity integrity        |
| ZIP-prefix validation            | validate geographic linkage      |
| State validation                 | preserve regional consistency    |
| City normalization validation    | ensure deterministic grouping    |
| Geographic enrichment validation | validate geo completeness        |
| Latitude validation              | ensure geographic correctness    |
| Longitude validation             | ensure spatial validity          |

---

# Validation Results

---

# [1] ROW COUNT ANALYSIS

## Objective

Ensure dimensional enrichment does NOT create:

- row duplication
- fan-out joins
- customer inflation

---

## Result

| Metric                | Value  |
| --------------------- | ------ |
| Source customer count | 99,441 |
| Silver customer count | 99,441 |
| Status                | PASSED |

---

## Interpretation

The Silver enrichment pipeline successfully preserved:

# customer dimensional cardinality

This confirms:

- geographic enrichment joins were controlled correctly
- no customer duplication occurred
- no accidental filtering occurred

This is critical because:
dimensional fan-out corruption would invalidate:

- customer KPIs
- segmentation analysis
- regional distributions
- downstream dimensional joins

---

# [2] GRAIN VALIDATION

## Objective

Validate:

# ONE ROW = ONE CUSTOMER

using:

```text id="n0p9ef"
customer_id
```

as the dimensional business key.

---

## Result

| Metric            | Result |
| ----------------- | ------ |
| Validation Status | PASSED |

---

## Interpretation

No duplicate customer records were detected.

This confirms:

- dimensional integrity
- customer uniqueness
- stable downstream joins

This validation is one of the MOST important controls in the dimensional layer because:
grain corruption causes:

- duplicated customers
- inflated segmentation counts
- incorrect KPI aggregation
- broken dimensional modeling

---

# [3] CRITICAL NULL VALIDATION

## Objective

Validate mandatory customer dimensional attributes.

---

## Validated Columns

| Column                   |
| ------------------------ |
| customer_id              |
| customer_unique_id       |
| customer_zip_code_prefix |
| customer_city            |
| customer_state           |

---

## Result

| Metric            | Result |
| ----------------- | ------ |
| Validation Status | PASSED |

---

## Interpretation

All critical customer attributes are complete.

This ensures:

- reliable dimensional joins
- stable regional enrichment
- trustworthy customer analytics

---

# [4] CUSTOMER ID VALIDATION

## Objective

Validate customer identity integrity.

---

## Result

| Validation           | Result |
| -------------------- | ------ |
| Invalid customer IDs | 0      |
| Status               | PASSED |

---

## Interpretation

All customer business identifiers are valid.

This protects:

- dimensional consistency
- order linkage integrity
- downstream fact relationships

---

# [5] ZIP PREFIX VALIDATION

## Objective

Validate customer geographic business keys.

---

## Result

| Validation                 | Result |
| -------------------------- | ------ |
| Invalid ZIP-prefix records | 0      |
| Status                     | PASSED |

---

## Interpretation

All customer ZIP-prefix values are valid and positive.

This confirms:

- reliable geographic joins
- stable enrichment mappings
- trustworthy regional segmentation

---

# [6] STATE VALIDATION

## Objective

Validate Brazilian state standardization.

---

## Result

| Validation            | Result |
| --------------------- | ------ |
| Invalid state records | 0      |
| Status                | PASSED |

---

## Interpretation

All customer states match valid Brazilian state abbreviations.

This ensures:

- reliable regional filtering
- dashboard consistency
- trustworthy KPI grouping

This validation protects:

# regional analytical consistency

across the warehouse.

---

# [7] CITY NORMALIZATION VALIDATION

## Objective

Validate deterministic customer city normalization.

---

## Result

| Validation                | Result |
| ------------------------- | ------ |
| Inconsistent city records | 0      |
| Status                    | PASSED |

---

## Interpretation

All customer city names were successfully normalized.

This confirms:

- deterministic grouping behavior
- stable regional segmentation
- reliable dashboard filtering

This prevents:

- fragmented city analytics
- duplicate categories
- inconsistent geographic reporting

---

# [8] GEOGRAPHIC ENRICHMENT VALIDATION

## Objective

Validate completeness of customer geographic enrichment.

---

## Result

| Validation                            | Result  |
| ------------------------------------- | ------- |
| Missing geographic enrichment records | 278     |
| Status                                | WARNING |

---

## Interpretation

278 customer records are missing:

- representative latitude
- representative longitude

from:

# `silver_geolocation`

enrichment.

These missing enrichments may affect:

- geographic segmentation
- regional distance analysis
- map visualizations
- regional KPI completeness

However:
the customer dimensional records themselves remain:

# operationally valid

because:
customer identity and regional business attributes still exist.

---

# Architectural Interpretation of Warning

The warning demonstrates:

# governed enrichment transparency

instead of:

# silent customer record deletion.

The project intentionally follows:

# operational truth preservation

and:

# zero silent data-loss policy

defined in the Silver governance strategy.

This means:
records are preserved unless removal is:

- documented
- validated
- business justified

This is an intentional enterprise engineering decision.

---

# Likely Cause of Missing Enrichment

The missing enrichment records likely originate from:

- ZIP-prefixes absent in the original geolocation dataset
- unmatched geographic regions
- incomplete source geographic coverage

This is common in:

# real-world geographic enrichment systems.

---

# [9] LATITUDE RANGE VALIDATION

## Objective

Validate:

# -90 <= latitude <= 90

---

## Result

| Validation               | Result |
| ------------------------ | ------ |
| Invalid latitude records | 0      |
| Status                   | PASSED |

---

## Interpretation

All available customer geographic coordinates are geographically valid.

This confirms:

- trustworthy regional mapping
- spatial consistency
- reliable enrichment quality

---

# [10] LONGITUDE RANGE VALIDATION

## Objective

Validate:

# -180 <= longitude <= 180

---

## Result

| Validation                | Result |
| ------------------------- | ------ |
| Invalid longitude records | 0      |
| Status                    | PASSED |

---

## Interpretation

All available customer longitude values are geographically valid.

This confirms:

- spatial reliability
- coordinate integrity
- trustworthy geographic enrichment

---

# Overall Validation Assessment

| Area                               | Result                |
| ---------------------------------- | --------------------- |
| Customer Grain Integrity           | PASSED                |
| Customer Identity Integrity        | PASSED                |
| Regional Standardization           | PASSED                |
| Geographic Coordinate Validity     | PASSED                |
| ZIP-prefix Integrity               | PASSED                |
| Geographic Enrichment Completeness | WARNING               |
| Overall Dataset Status             | TRUSTED WITH WARNINGS |

---

# Final Engineering Assessment

The:

# `silver_customers`

dataset successfully passed all critical dimensional validation controls.

The dataset is considered:

# analytically trusted

for:

- customer dimensional modeling
- regional segmentation
- delivery-region analysis
- geographic KPI reporting
- streaming enrichment
- downstream Gold marts

The detected enrichment warning is:

- documented
- explainable
- operationally acceptable
- governance-compliant

and does NOT compromise:

- customer dimensional integrity
- regional standardization
- customer identity consistency
- downstream analytical usability

---

# Governance Alignment

This validation process demonstrates implementation of:

- validation-driven dimensional governance
- layered enrichment architecture
- controlled geographic enrichment
- operational truth preservation
- reusable Silver enrichment engineering
- enterprise-grade dimensional quality standards

as defined in:

# `silver_transformation_strategy.md`

and:

# `silver_customers.md`
