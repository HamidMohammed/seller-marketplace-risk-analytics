# `silver_mql.md`

## Objective

The `silver_mql` dataset represents the trusted marketing acquisition intelligence layer inside the Olist Seller Intelligence Platform.

This dataset transforms:

# raw marketing-qualified lead records

into:

# validated CRM acquisition intelligence

used by:

- lead conversion analytics
- acquisition funnel analysis
- marketing attribution
- seller onboarding intelligence
- business growth monitoring
- executive acquisition reporting

The dataset acts as:

# the marketing funnel operational truth layer

across the analytical warehouse.

Unlike:

- marketplace orders
- customer purchases
- operational logistics datasets

this dataset models:

# B2B acquisition operations

focused on:

- seller acquisition
- lead qualification
- marketing funnel progression
- commercial growth intelligence

which makes this dataset:

# strategically important for business analytics.

---

# Dataset Role in Architecture

```text id="z8r3mv"
Bronze Marketing Qualified Leads
                ↓
silver_mql
                ↓
Marketing Acquisition Intelligence
```

This dataset powers:

- acquisition funnel dashboards
- lead qualification analytics
- seller acquisition monitoring
- marketing channel analysis
- growth performance KPIs
- executive CRM intelligence

and acts as:

# the marketing intelligence foundation

of the warehouse.

---

# Business Process Context

The dataset models:

# Marketing Qualified Leads (MQLs)

inside the Olist acquisition funnel.

An MQL represents:

# a business lead considered ready for sales engagement.

This means the lead:

- demonstrated business interest
- matched qualification criteria
- entered the commercial acquisition pipeline

---

# Business Funnel Flow

```text id="x5n8pt"
Marketing Lead
      ↓
Marketing Qualified Lead (MQL)
      ↓
Sales Qualification
      ↓
Closed Commercial Deal
      ↓
Seller Onboarding
```

This represents:

# enterprise CRM funnel architecture.

---

# Dataset Grain

# ONE ROW = ONE QUALIFIED LEAD EVENT

This grain is strictly preserved throughout all transformations.

The dataset intentionally models:

# lead-level acquisition events

NOT:

- aggregated marketing summaries
- campaign rollups
- conversion KPIs

Maintaining this grain is critical because:
lead duplication would corrupt:

- conversion metrics
- funnel analytics
- acquisition KPIs
- onboarding intelligence

---

# Source Dataset

| Source Dataset | Layer  | Purpose                             |
| -------------- | ------ | ----------------------------------- |
| bronze/mql     | Bronze | Raw marketing-qualified lead events |

---

# Source Columns

| Column             | Meaning                             |
| ------------------ | ----------------------------------- |
| mql_id             | Marketing-qualified lead identifier |
| first_contact_date | Lead acquisition timestamp          |
| landing_page_id    | Marketing landing page              |
| origin             | Lead acquisition source             |

---

# Important Marketing Modeling Interpretation

The dataset models:

# seller acquisition marketing operations

NOT:

# consumer marketplace purchases.

This distinction is critical.

The dataset focuses on:

- lead generation
- acquisition channels
- funnel qualification
- B2B marketplace growth

This introduces:

# CRM analytical modeling

into the warehouse architecture.

---

# Silver Responsibilities

The `silver_mql` pipeline is responsible for:

| Responsibility                 | Purpose                      |
| ------------------------------ | ---------------------------- |
| Lead-grain validation          | acquisition integrity        |
| Timestamp standardization      | funnel chronology            |
| Marketing-source normalization | attribution consistency      |
| Landing-page normalization     | deterministic grouping       |
| Metadata enrichment            | lineage                      |
| Validation governance          | acquisition analytical trust |

---

# Marketing Attribution Strategy

The dataset standardizes:

# acquisition source semantics

to ensure:

- deterministic attribution grouping
- stable acquisition KPIs
- reliable funnel analytics
- executive reporting consistency

---

# Source Normalization Rules

## Transformations

```python id="v2q7rc"
lower(trim(origin))
```

```python id="p5n8wx"
lower(trim(landing_page_id))
```

---

## Purpose

Prevents:

- acquisition-source fragmentation
- inconsistent campaign grouping
- unstable attribution analytics
- unreliable dashboard filtering

while preserving:

# original marketing intent.

---

# Timestamp Governance Strategy

The dataset standardizes:

# first-contact timestamps

to support:

- funnel chronology
- acquisition trend analysis
- onboarding velocity analytics
- temporal growth intelligence

---

# Timestamp Standardization

## Standardized Columns

| Column             |
| ------------------ |
| first_contact_date |

---

## Purpose

Ensures:

- temporal consistency
- reliable acquisition analytics
- stable trend intelligence

---

# IMPORTANT GOVERNANCE RULE

The Silver layer intentionally DOES NOT:

- infer attribution logic
- generate campaign scoring
- apply lead scoring AI
- modify acquisition semantics

because Silver should preserve:

# trusted CRM operational truth.

Advanced marketing analytics belong later in:

# Gold business intelligence layers.

---

# Transformations Applied

---

# 1. Lead ID Standardization

## Transformation

```python id="f7m2qa"
trim(mql_id)
```

---

## Purpose

Ensures:

- stable CRM relationships
- deterministic acquisition joins
- reliable operational lineage

---

# 2. Acquisition Source Normalization

## Transformation

```python id="x9r4vn"
lower(trim(origin))
```

---

## Purpose

Improves:

- attribution consistency
- acquisition segmentation
- executive readability

without changing:

# business acquisition meaning.

---

# 3. Landing Page Normalization

## Transformation

```python id="r3v8yt"
lower(trim(landing_page_id))
```

---

## Purpose

Supports:

- landing-page analytics
- funnel attribution
- deterministic grouping

---

# 4. Timestamp Standardization

## Transformation

```python id="q6n1zc"
cast(first_contact_date as timestamp)
```

---

## Purpose

Supports:

- acquisition trend monitoring
- funnel velocity analysis
- temporal CRM intelligence

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

# validation-driven acquisition governance

defined in:

```text id="j4m7pw"
silver_transformation_strategy.md
```

All CRM transformations are validated BEFORE Silver output generation.

---

# Validation Rules

---

# 1. Grain Validation

## Rule

```text id="d8x1tr"
ONE ROW = ONE QUALIFIED LEAD EVENT
```

---

## Validation Key

```text id="n5q8za"
mql_id
```

---

## Purpose

Protect:

- acquisition integrity
- conversion analytics
- funnel KPIs
- onboarding intelligence

---

# 2. Critical Null Validation

## Critical Columns

| Column             | Reason                 |
| ------------------ | ---------------------- |
| mql_id             | CRM business key       |
| first_contact_date | acquisition chronology |
| origin             | marketing attribution  |

---

## Purpose

Prevent:

- broken CRM relationships
- unusable attribution analytics
- unreliable funnel intelligence

---

# 3. Timestamp Validation

## Purpose

Validate:

- acquisition chronology
- temporal consistency
- reliable funnel sequencing

---

# 4. Source Normalization Validation

## Purpose

Ensure:

- deterministic acquisition-source formatting
- stable attribution grouping
- consistent CRM semantics

---

# 5. Landing Page Validation

## Purpose

Validate:

- landing-page consistency
- attribution completeness
- analytical grouping stability

---

# Important Architectural Decisions

---

# CRM Intelligence as Silver Responsibility

The project models MQL standardization as:

# CRM operational enrichment

inside:

# Silver

because acquisition normalization belongs between:

- raw CRM ingestion
- executive business analytics

This is a critical warehouse-modeling distinction.

---

# Marketing Operational Truth

The dataset preserves:

# authentic acquisition events

instead of:

# inferred marketing intelligence.

This follows:

# operational truth preservation

defined in the Silver governance strategy.

---

# Controlled Acquisition Governance

The pipeline intentionally avoids:

- predictive lead scoring
- attribution AI
- conversion inference
- marketing reinterpretation

inside:
`silver_mql`

because Silver operational enrichment should remain:

# trusted CRM operational truth

rather than:

# analytical business reinterpretation.

---

# No Silent Record Deletion

The pipeline follows:

# zero silent data-loss policy

Meaning:
CRM records may only be removed when:

- documented
- validated
- business justified

This preserves:

- acquisition reproducibility
- auditability
- analytical defensibility

---

# Downstream Dependencies

The following datasets depend on:

# silver_mql

| Dataset                  | Dependency Purpose        |
| ------------------------ | ------------------------- |
| seller acquisition marts | funnel analytics          |
| CRM dashboards           | acquisition intelligence  |
| conversion KPIs          | lead tracking             |
| closed-deal enrichment   | sales conversion analysis |

This makes:
`silver_mql`

a:

# shared acquisition intelligence foundation

across the warehouse.

---

# Streaming Architecture Role

`silver_mql`
supports:

# real-time acquisition intelligence

for:

- live lead monitoring
- acquisition funnel tracking
- marketing attribution analysis
- seller onboarding intelligence

Streaming systems can use:

- lead sources
- acquisition timestamps
- funnel progression

for:

# operational CRM intelligence.

---

# Output Dataset Location

```text id="m2x7pv"
data/silver/mql/
```

Stored as:

# parquet

for:

- Spark optimization
- scalable CRM processing
- warehouse integration

---

# Relationship to Medallion Architecture

Within the Medallion Architecture:

| Layer  | Purpose                                      |
| ------ | -------------------------------------------- |
| Bronze | raw CRM lead events                          |
| Silver | trusted acquisition operational intelligence |
| Gold   | conversion analytics & growth dashboards     |

The Silver layer transforms:

# raw marketing-qualified lead records

into:

# trusted acquisition operational intelligence.

---

# Enterprise Engineering Insight

The:

# `silver_mql`

dataset introduces:

# CRM funnel engineering

into the warehouse architecture.

This demonstrates implementation of:

- acquisition intelligence modeling
- marketing attribution normalization
- CRM operational governance
- temporal funnel engineering
- business growth analytics foundations

This is an important enterprise capability because:
modern marketplaces rely heavily on:

- seller acquisition
- CRM pipelines
- growth intelligence
- funnel optimization

---

# Final Architectural Value

The `silver_mql` dataset transforms:

# raw CRM lead records

into:

# trusted acquisition operational intelligence

through:

- attribution normalization
- timestamp standardization
- CRM validation governance
- deterministic acquisition semantics
- operational truth preservation
- validation-driven engineering

This dataset establishes:

# trusted acquisition intelligence foundation

for:

- funnel analytics
- growth dashboards
- seller acquisition intelligence
- CRM operational reporting
- executive business analytics

and acts as:

# the CRM acquisition backbone

of the Olist Seller Intelligence Platform.
