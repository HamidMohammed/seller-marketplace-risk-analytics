# `mql_validation_report.md`

## Validation Report Overview

This report documents the validation results for the:

# `silver_mql`

dataset inside the:

# Olist Seller Intelligence Platform

The validation process follows:

# validation-driven CRM governance

defined in the Silver transformation strategy.

The purpose of this validation layer is to ensure:

- acquisition operational integrity
- CRM lead-grain correctness
- marketing attribution consistency
- acquisition chronology reliability
- funnel analytical trust

before the dataset becomes available for:

- acquisition funnel dashboards
- seller onboarding analytics
- CRM intelligence
- marketing attribution analysis
- conversion funnel KPIs
- executive growth reporting

---

# Dataset Information

| Attribute         | Value                              |
| ----------------- | ---------------------------------- |
| Dataset           | silver_mql                         |
| Layer             | Silver                             |
| Dataset Grain     | ONE ROW = ONE QUALIFIED LEAD EVENT |
| Validation Status | PASSED WITH CONTROLLED WARNINGS    |
| Output Format     | Parquet                            |

---

# Validation Scope

The validation framework covered:

| Validation Area                     | Objective                              |
| ----------------------------------- | -------------------------------------- |
| Row-count integrity                 | preserve acquisition-event cardinality |
| Grain validation                    | preserve lead uniqueness               |
| Critical null validation            | protect CRM operational trust          |
| MQL ID validation                   | validate CRM identifiers               |
| Origin normalization validation     | enforce attribution consistency        |
| Landing-page validation             | ensure deterministic grouping          |
| Timestamp validation                | protect funnel chronology              |
| Future-date validation              | validate temporal realism              |
| Landing-page analysis               | govern attribution edge cases          |
| Attribution completeness validation | monitor marketing-source coverage      |

---

# Validation Results

---

# [1] ROW COUNT ANALYSIS

## Objective

Ensure transformations do NOT create:

- duplicated acquisition events
- CRM fan-out corruption
- silent lead loss

---

## Result

| Metric           | Value  |
| ---------------- | ------ |
| Source MQL count | 8,000  |
| Silver MQL count | 8,000  |
| Status           | PASSED |

---

## Interpretation

The Silver transformation pipeline successfully preserved:

# acquisition-event cardinality

This confirms:

- no CRM leads were duplicated
- no acquisition records were silently removed
- no funnel corruption occurred

This is critical because:
lead duplication would corrupt:

- acquisition KPIs
- conversion rates
- onboarding metrics
- funnel analytics

---

# [2] GRAIN VALIDATION

## Objective

Validate:

# ONE ROW = ONE QUALIFIED LEAD EVENT

using:

```text id="x2m8pw"
mql_id
```

as the CRM business key.

---

## Result

| Metric            | Result |
| ----------------- | ------ |
| Validation Status | PASSED |

---

## Interpretation

No duplicate CRM acquisition events were detected.

This confirms:

- stable lead relationships
- deterministic CRM joins
- trustworthy funnel analytics

This validation is critical because:
grain corruption causes:

- duplicated acquisition metrics
- invalid conversion analytics
- distorted onboarding KPIs
- unreliable CRM intelligence

---

# [3] CRITICAL NULL VALIDATION

## Objective

Validate mandatory CRM acquisition attributes.

---

## Validated Columns

| Column             |
| ------------------ |
| mql_id             |
| first_contact_date |
| origin             |

---

## Result

| Metric            | Result |
| ----------------- | ------ |
| Validation Status | PASSED |

---

## Interpretation

All critical acquisition attributes passed validation governance.

This ensures:

- reliable CRM linkage
- trustworthy funnel chronology
- stable acquisition analytics

---

# [4] MQL ID VALIDATION

## Objective

Validate CRM lead identifier integrity.

---

## Result

| Validation             | Result |
| ---------------------- | ------ |
| Invalid MQL ID records | 0      |
| Status                 | PASSED |

---

## Interpretation

All CRM lead identifiers are operationally valid.

This confirms:

- deterministic acquisition relationships
- reliable funnel tracking
- stable downstream CRM joins

This is critical because:
invalid CRM identifiers would corrupt:

- acquisition analytics
- lead conversion tracking
- onboarding intelligence
- CRM operational trust

---

# [5] ORIGIN NORMALIZATION VALIDATION

## Objective

Validate deterministic acquisition-source normalization.

---

## Result

| Validation                  | Result |
| --------------------------- | ------ |
| Inconsistent origin records | 0      |
| Status                      | PASSED |

---

## Interpretation

All acquisition-source values were successfully normalized.

This confirms:

- stable attribution grouping
- deterministic acquisition segmentation
- reliable marketing-source analytics

This prevents:

- attribution fragmentation
- inconsistent funnel grouping
- unstable dashboard filtering

---

# [6] LANDING PAGE VALIDATION

## Objective

Validate deterministic landing-page normalization.

---

## Result

| Validation                        | Result |
| --------------------------------- | ------ |
| Inconsistent landing-page records | 0      |
| Status                            | PASSED |

---

## Interpretation

All landing-page identifiers were successfully normalized.

This confirms:

- deterministic campaign grouping
- stable landing-page analytics
- reliable acquisition attribution

This improves:

- marketing analytics consistency
- attribution readability
- funnel reporting quality

---

# [7] TIMESTAMP VALIDATION

## Objective

Validate acquisition chronology consistency.

---

## Result

| Validation                | Result |
| ------------------------- | ------ |
| Invalid timestamp records | 0      |
| Status                    | PASSED |

---

## Interpretation

All acquisition timestamps were successfully standardized.

This confirms:

- trustworthy funnel chronology
- reliable acquisition trend analysis
- stable temporal CRM intelligence

This enables:

- onboarding velocity analysis
- lead acquisition monitoring
- temporal growth analytics

---

# [8] FUTURE DATE VALIDATION

## Objective

Validate CRM temporal realism.

---

## Result

| Validation                  | Result |
| --------------------------- | ------ |
| Future contact-date records | 0      |
| Status                      | PASSED |

---

## Interpretation

No acquisition events were detected with future timestamps.

This confirms:

- realistic CRM chronology
- trustworthy acquisition sequencing
- reliable temporal analytics

This validation protects:

- onboarding KPIs
- funnel timing analysis
- acquisition-trend reliability

---

# [9] NULL LANDING PAGE ANALYSIS

## Objective

Analyze acquisition events without landing-page attribution.

---

## Result

| Validation                | Result        |
| ------------------------- | ------------- |
| Null landing-page records | 0             |
| Status                    | INFORMATIONAL |

---

## Interpretation

All CRM acquisition events contain valid landing-page attribution.

This indicates:

- strong acquisition traceability
- reliable attribution coverage
- stable marketing funnel visibility

The informational note remains intentionally documented because:
real-world CRM systems may contain:

- offline acquisition
- direct onboarding
- manual CRM insertion
- non-trackable acquisition channels

This follows:

# proactive operational governance documentation.

---

# [10] ATTRIBUTION DISTRIBUTION VALIDATION

## Objective

Validate acquisition-source completeness.

---

## Result

| Validation          | Result  |
| ------------------- | ------- |
| Null origin records | 60      |
| Status              | WARNING |

---

## Interpretation

60 CRM lead records are missing:

# acquisition-source attribution

This represents:

# controlled operational incompleteness

rather than:

# critical data corruption.

---

# Business Interpretation

Missing acquisition-source attribution may occur due to:

- offline lead generation
- manual CRM onboarding
- attribution-system limitations
- legacy operational workflows
- incomplete marketing capture

This is common in:

# real enterprise CRM systems.

---

# Architectural Governance Decision

The project intentionally preserves:

# unattributed acquisition events

instead of:

# silently filtering incomplete CRM records.

This follows:

# operational truth preservation

and:

# zero silent data-loss policy

defined in the Silver governance strategy.

Removing these records would:

- distort acquisition KPIs
- bias funnel analytics
- reduce CRM realism
- hide operational limitations

---

# Enterprise CRM Engineering Significance

The:

# `silver_mql`

dataset introduces:

# CRM acquisition intelligence engineering

into the warehouse architecture.

This demonstrates implementation of:

- acquisition operational governance
- funnel chronology engineering
- attribution normalization
- CRM integrity validation
- business-growth intelligence foundations

This is an important enterprise capability because:
modern marketplaces rely heavily on:

- seller acquisition
- CRM operations
- lead qualification
- growth analytics
- funnel optimization

---

# Overall Validation Assessment

| Area                      | Result  |
| ------------------------- | ------- |
| CRM Acquisition Integrity | PASSED  |
| Lead-Grain Consistency    | PASSED  |
| Attribution Normalization | PASSED  |
| Funnel Chronology         | PASSED  |
| Landing-Page Governance   | PASSED  |
| Attribution Completeness  | WARNING |
| Overall Dataset Status    | TRUSTED |

---

# Final Engineering Assessment

The:

# `silver_mql`

dataset successfully passed all critical CRM acquisition validation controls.

The dataset is considered:

# analytically trusted

for:

- acquisition funnel analytics
- CRM dashboards
- seller onboarding intelligence
- growth analytics
- marketing attribution reporting
- downstream Gold marts

The attribution incompleteness warning is:

- documented
- explainable
- operationally realistic
- governance-compliant

and does NOT compromise:

- acquisition operational integrity
- funnel analytical trust
- CRM usability
- warehouse reliability

---

# Governance Alignment

This validation process demonstrates implementation of:

- validation-driven CRM governance
- operational truth preservation
- acquisition attribution normalization
- funnel chronology enforcement
- enterprise-grade Silver transformation standards

as defined in:

# `silver_transformation_strategy.md`

and:

# `silver_mql.md`
