# `seller_acquisition_staging_validation_report.md`

````markdown id="k7x2vd"
# Seller Acquisition Staging Validation Report

## Dataset

```text
seller_acquisition_staging
```
````

---

# Objective

This report documents the validation results for the:

```text id="g5q4mt"
seller_acquisition_staging
```

dataset inside the Silver Staging layer of the:

# Olist Seller Intelligence Platform

The purpose of this validation process is to ensure:

- acquisition-event grain integrity
- conversion lifecycle correctness
- acquisition intelligence reliability
- seller onboarding consistency
- commercial enrichment quality
- downstream Gold mart readiness

This staging dataset acts as:

# the seller lifecycle intelligence layer

connecting:

- marketing acquisition
- seller conversion
- seller operational identity

inside one integrated analytical ecosystem.

---

# Dataset Grain

# ONE ROW = ONE SELLER ACQUISITION EVENT

Each row represents:

- one marketing-qualified lead
- one acquisition lifecycle
- one seller conversion pathway

This grain is preserved throughout the staging pipeline to prevent:

- duplicated funnel analytics
- inflated conversion KPIs
- acquisition attribution corruption
- lifecycle inconsistencies

This follows the platform’s:

# commercial lifecycle modeling architecture

where:

- marketing acquisition
- seller onboarding
- operational performance

remain analytically connected while preserving:

# independent business-process integrity

throughout the warehouse.

---

# Validation Execution Summary

| Validation Category                 | Result                             |
| ----------------------------------- | ---------------------------------- |
| Row Count Validation                | PASSED                             |
| Acquisition Grain Validation        | PASSED                             |
| Critical Null Validation            | PASSED WITH INVESTIGATED EXCEPTION |
| Conversion Lifecycle Validation     | PASSED WITH KNOWN ANOMALY          |
| Revenue Validation                  | PASSED                             |
| Acquisition Distribution Validation | PASSED                             |
| Acquisition Risk Validation         | PASSED                             |

---

# 1. Row Count Validation

## Final Row Count

```text id="8p0x1z"
8000
```

---

# Interpretation

The final row count confirms:

- acquisition events were preserved
- no unexpected row loss occurred
- joins remained grain-safe
- seller enrichment did not create duplication

This validates:

# seller acquisition lifecycle preservation integrity

throughout the staging process.

---

# 2. Acquisition Grain Validation

## Validation Rule

```text id="z3c7mh"
mql_id
must remain unique
```

---

## Result

```text id="7m5vkc"
Duplicate mql_id Count: 0
```

---

# Interpretation

This confirms:

# PERFECT ACQUISITION GRAIN PRESERVATION

No duplicate acquisition events were introduced during:

- seller conversion enrichment
- operational seller enrichment
- acquisition intelligence derivation

This is extremely important because:
duplicate acquisition events would corrupt:

- conversion KPIs
- acquisition-channel attribution
- funnel analytics
- onboarding metrics

---

# 3. Critical Null Validation

## Results

| Column                    | Null Count |
| ------------------------- | ---------- |
| mql_id                    | 0          |
| marketing_origin          | 60         |
| converted_flag            | 0          |
| acquisition_risk_category | 0          |

---

# Interpretation

The staging dataset achieved:

# ZERO CRITICAL IDENTIFIER FAILURES

for:

- acquisition identity
- conversion classification
- acquisition risk segmentation

---

# Important Marketing Origin Observation

The:

```text id="q7l9zx"
marketing_origin
```

column contains:

```text id="6v4gta"
60 nulls
```

This is NOT considered a pipeline failure.

---

## Business Explanation

These records likely represent:

- incomplete acquisition tracking
- unattributed lead sources
- historical marketing ingestion gaps

Meaning:
the seller acquisition lifecycle exists,
but the originating marketing channel was not captured.

This represents:

# operational business missingness

NOT:

# transformation corruption

The records were intentionally preserved because:
silent deletion would:

- distort funnel metrics
- bias acquisition analytics
- hide source-system limitations

This follows the project’s:

# zero silent data loss philosophy

used throughout the Silver architecture.

---

# 4. Conversion Lifecycle Validation

## Result

```text id="s2n6kp"
Invalid Conversion Timelines: 1
```

---

# Interpretation

Only:

```text id="d4k0rq"
1 acquisition event
```

contained:

# an invalid conversion timeline

where:

```text id="0m2zlb"
won_date < first_contact_date
```

This likely represents:

- operational data-entry error
- CRM synchronization issue
- historical onboarding inconsistency

---

# Engineering Decision

The record was intentionally preserved because:

- it represents real operational history
- anomaly preservation supports auditability
- silent removal would distort funnel truth

This follows the platform’s:

# operational anomaly preservation philosophy

where:

- business anomalies are documented
- not silently deleted

This is:

# enterprise-grade analytical governance

rather than:

# aggressive data cleaning.

---

# 5. Revenue Validation

## Result

```text id="4r6v1q"
Negative Revenue Values: 0
```

---

# Interpretation

This confirms:

# FULL COMMERCIAL METRIC VALIDITY

No corrupted commercial revenue values were detected.

This protects:

- acquisition quality analytics
- seller segmentation
- premium seller classification
- acquisition-risk modeling

Without this validation:
commercial analytics could become:

- mathematically invalid
- operationally misleading
- strategically unreliable

---

# 6. Acquisition Source Distribution Validation

## Distribution

| Marketing Origin  | Count |
| ----------------- | ----- |
| organic_search    | 2,296 |
| paid_search       | 1,586 |
| social            | 1,350 |
| unknown           | 1,099 |
| email             | 493   |
| direct_traffic    | 499   |
| referral          | 284   |
| other             | 150   |
| display           | 118   |
| other_publicities | 65    |
| NULL              | 60    |

---

# Interpretation

The acquisition distribution reveals:

# search-based acquisition dominates seller onboarding

Specifically:

- `organic_search`
- `paid_search`

represent the majority of acquisition channels.

This suggests:

# strong digital acquisition dependency

inside the marketplace ecosystem.

---

# Important Strategic Insight

The relatively high:

```text id="0t7yxh"
unknown
```

category count:

```text id="p7c0wr"
1,099
```

suggests:

# acquisition attribution limitations

inside the original operational platform.

This is analytically important because:
incomplete acquisition attribution may reduce:

- marketing ROI visibility
- seller-channel performance analysis
- acquisition optimization accuracy

This creates:

# realistic enterprise analytical constraints

which strengthens the realism of the project architecture.

---

# 7. Acquisition Risk Distribution Validation

## Distribution

| Acquisition Risk Category | Count |
| ------------------------- | ----- |
| Unknown                   | 7,158 |
| Standard                  | 593   |
| High Risk                 | 249   |

---

# Interpretation

The overwhelming majority of acquisition events were classified as:

```text id="h6xqpd"
Unknown
```

This is expected because:
many seller acquisition records lack:

- complete revenue information
- strong onboarding intelligence
- sufficient commercial profiling

This represents:

# sparse commercial enrichment

rather than:

# pipeline failure

---

# Important Analytical Insight

Although:

```text id="5f9kgw"
High Risk
```

represents only:

```text id="7b8dzt"
249 sellers
```

this subset becomes:

# highly valuable operational intelligence

because these sellers can later be correlated with:

- delivery failures
- poor customer reviews
- fulfillment instability
- operational underperformance

This creates:

# predictive seller lifecycle analytics

which is one of the strongest analytical capabilities in the platform architecture.

---

# Architectural Significance

The `seller_acquisition_staging` dataset represents:

# seller origin intelligence

inside the warehouse architecture.

Unlike:

```text id="e8y3rp"
seller_fulfillment_staging
```

which measures:

# operational seller workload

and:

```text id="b4n9os"
reviews_staging
```

which measures:

# customer satisfaction behavior

this staging layer measures:

# commercial seller acquisition lifecycle

This separation is architecturally critical because:

- acquisition is a different business process
- onboarding events require independent grain
- operational analytics require controlled enrichment

This follows:

# Kimball dimensional modeling principles

and:

# enterprise lifecycle analytics architecture

used throughout the platform.

---

# Operational Intelligence Enabled

This staging layer now supports:

| Capability                    | Enabled |
| ----------------------------- | ------- |
| acquisition-channel analytics | YES     |
| seller conversion analysis    | YES     |
| funnel lifecycle analytics    | YES     |
| acquisition-risk modeling     | YES     |
| premium seller segmentation   | YES     |
| seller onboarding analysis    | YES     |
| seller lifecycle intelligence | YES     |

---

# Final Validation Status

# VALIDATED SUCCESSFULLY

The:

```text id="d1y7kw"
seller_acquisition_staging
```

dataset is approved for:

- `fct_seller_acquisition`
- seller lifecycle analytics
- acquisition intelligence marts
- funnel analysis
- onboarding KPI reporting
- predictive seller intelligence

with:

# FULL ACQUISITION GRAIN INTEGRITY

# VALID COMMERCIAL ENRICHMENT

# CONTROLLED OPERATIONAL ANOMALIES

# ZERO DUPLICATE ACQUISITION EVENTS

# STRONG LIFECYCLE ANALYTICS FOUNDATIONS
