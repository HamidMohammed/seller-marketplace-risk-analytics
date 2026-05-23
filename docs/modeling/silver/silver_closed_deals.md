# `silver_closed_deals.md`

## Objective

The `silver_closed_deals` dataset represents the trusted commercial conversion intelligence layer inside the Olist Seller Intelligence Platform.

This dataset transforms:

# raw closed commercial deal records

into:

# validated sales conversion operational intelligence

used by:

- sales performance analytics
- acquisition conversion analysis
- seller onboarding intelligence
- commercial funnel monitoring
- growth-performance reporting
- executive CRM dashboards

The dataset acts as:

# the commercial conversion operational truth layer

across the analytical warehouse.

Unlike:

- marketplace transactions
- customer purchases
- logistics operations

this dataset models:

# B2B commercial acquisition operations

focused on:

- seller conversion
- commercial negotiations
- acquisition success
- sales-funnel completion
- marketplace growth intelligence

which makes this dataset:

# strategically critical for executive analytics.

---

# Dataset Role in Architecture

```text id="t4m8qx"
Bronze Closed Deals
          ↓
silver_closed_deals
          ↓
Commercial Conversion Intelligence
```

This dataset powers:

- sales conversion dashboards
- seller onboarding analytics
- acquisition efficiency KPIs
- commercial funnel analysis
- CRM operational intelligence
- executive growth reporting

and acts as:

# the commercial acquisition intelligence foundation

of the warehouse.

---

# Business Process Context

The dataset models:

# successfully converted seller acquisition events.

A closed deal represents:

# a completed commercial agreement

between:

- Olist
- a prospective marketplace seller

after:

- lead qualification
- commercial engagement
- sales negotiation

This dataset therefore models:

# successful funnel conversion milestones.

---

# Business Funnel Flow

```text id="x8q2mv"
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

# enterprise CRM + sales-funnel architecture.

---

# Dataset Grain

# ONE ROW = ONE CLOSED COMMERCIAL DEAL

This grain is strictly preserved throughout all transformations.

The dataset intentionally models:

# deal-level commercial conversion events

NOT:

- aggregated sales summaries
- seller-level rollups
- executive KPIs

Maintaining this grain is critical because:
deal duplication would corrupt:

- conversion metrics
- acquisition analytics
- sales performance KPIs
- onboarding intelligence

---

# Source Dataset

| Source Dataset      | Layer  | Purpose                           |
| ------------------- | ------ | --------------------------------- |
| bronze/closed_deals | Bronze | Raw commercial conversion records |

---

# Important Commercial Modeling Interpretation

The dataset models:

# marketplace seller acquisition operations

NOT:

# consumer e-commerce transactions.

This distinction is critical.

The dataset focuses on:

- commercial conversion
- seller onboarding
- CRM acquisition operations
- sales-funnel success
- business growth intelligence

This introduces:

# enterprise sales analytics

into the warehouse architecture.

---

# Silver Responsibilities

The `silver_closed_deals` pipeline is responsible for:

| Responsibility                  | Purpose                 |
| ------------------------------- | ----------------------- |
| Deal-grain validation           | conversion integrity    |
| Sales timestamp standardization | funnel chronology       |
| Business-segment normalization  | deterministic grouping  |
| Sales-channel normalization     | attribution consistency |
| Seller-type normalization       | commercial readability  |
| Metadata enrichment             | lineage                 |
| Validation governance           | sales analytical trust  |

---

# Commercial Attribution Strategy

The dataset standardizes:

# commercial acquisition semantics

to ensure:

- deterministic sales grouping
- stable conversion analytics
- reliable funnel KPIs
- executive reporting consistency

---

# Normalization Strategy

The dataset normalizes:

- business segments
- lead channels
- seller categories
- acquisition metadata

to support:

# deterministic commercial intelligence.

---

# Timestamp Governance Strategy

The dataset standardizes:

# commercial funnel chronology

to support:

- acquisition velocity analysis
- onboarding trend monitoring
- sales performance analytics
- temporal CRM intelligence

---

# IMPORTANT GOVERNANCE RULE

The Silver layer intentionally DOES NOT:

- infer conversion scoring
- generate predictive analytics
- calculate sales KPIs
- reinterpret acquisition logic

because Silver should preserve:

# trusted commercial operational truth.

Advanced business intelligence belongs later in:

# Gold analytical marts.

---

# Transformations Applied

---

# 1. Deal Identifier Standardization

## Transformation

```python id="j7n2vx"
trim(mql_id)
```

---

## Purpose

Ensures:

- stable CRM relationships
- deterministic commercial joins
- reliable operational lineage

---

# 2. Business Segment Normalization

## Transformation

```python id="r5m8pt"
lower(trim(business_segment))
```

---

## Purpose

Improves:

- sales segmentation consistency
- executive readability
- deterministic grouping

without changing:

# business semantic meaning.

---

# 3. Lead Channel Normalization

## Transformation

```python id="f2x7qw"
lower(trim(lead_channel))
```

---

## Purpose

Supports:

- acquisition attribution analytics
- funnel segmentation
- stable sales-channel grouping

---

# 4. Seller Type Normalization

## Transformation

```python id="m4v1zk"
lower(trim(seller_type))
```

---

## Purpose

Improves:

- seller segmentation consistency
- onboarding analytics
- deterministic commercial grouping

---

# 5. Timestamp Standardization

## Standardized Columns

| Column                |
| --------------------- |
| won_date              |
| business_closure_date |

---

## Purpose

Supports:

- sales velocity analytics
- acquisition chronology
- temporal funnel intelligence

---

# 6. Metadata Enrichment

## Added Columns

| Column                 | Purpose          |
| ---------------------- | ---------------- |
| silver_loaded_at       | pipeline lineage |
| source_system          | traceability     |
| transformation_version | reproducibility  |

---

# Validation Framework

The dataset follows:

# validation-driven commercial governance

defined in:

```text id="v9q2mx"
silver_transformation_strategy.md
```

All commercial transformations are validated BEFORE Silver output generation.

---

# Validation Rules

---

# 1. Grain Validation

## Rule

```text id="k2r7vz"
ONE ROW = ONE CLOSED COMMERCIAL DEAL
```

---

## Validation Key

```text id="t8x1qp"
mql_id
```

---

## Purpose

Protect:

- conversion integrity
- sales analytics
- onboarding intelligence
- commercial funnel trust

---

# 2. Critical Null Validation

## Critical Columns

| Column           | Reason                |
| ---------------- | --------------------- |
| mql_id           | CRM business key      |
| won_date         | conversion chronology |
| business_segment | sales segmentation    |

---

## Purpose

Prevent:

- broken CRM relationships
- unusable conversion analytics
- unreliable funnel intelligence

---

# 3. Timestamp Validation

## Purpose

Validate:

- commercial chronology
- temporal consistency
- reliable conversion sequencing

---

# 4. Segment Normalization Validation

## Purpose

Ensure:

- deterministic business segmentation
- stable funnel grouping
- consistent CRM semantics

---

# 5. Commercial Completeness Validation

## Purpose

Validate:

- sales operational completeness
- onboarding traceability
- acquisition coverage

---

# Important Architectural Decisions

---

# Commercial Intelligence as Silver Responsibility

The project models closed-deal standardization as:

# commercial operational enrichment

inside:

# Silver

because sales normalization belongs between:

- raw CRM ingestion
- executive business analytics

This is a critical warehouse-modeling distinction.

---

# Commercial Operational Truth

The dataset preserves:

# authentic commercial conversion events

instead of:

# inferred business intelligence.

This follows:

# operational truth preservation

defined in the Silver governance strategy.

---

# Controlled Commercial Governance

The pipeline intentionally avoids:

- predictive sales scoring
- AI conversion prediction
- inferred onboarding logic
- commercial reinterpretation

inside:
`silver_closed_deals`

because Silver operational enrichment should remain:

# trusted commercial operational truth

rather than:

# business reinterpretation.

---

# No Silent Record Deletion

The pipeline follows:

# zero silent data-loss policy

Meaning:
commercial records may only be removed when:

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

# silver_closed_deals

| Dataset                     | Dependency Purpose      |
| --------------------------- | ----------------------- |
| seller acquisition marts    | conversion analytics    |
| CRM dashboards              | sales intelligence      |
| onboarding KPIs             | acquisition performance |
| executive growth dashboards | commercial reporting    |

This makes:
`silver_closed_deals`

a:

# shared commercial intelligence foundation

across the warehouse.

---

# Streaming Architecture Role

`silver_closed_deals`
supports:

# real-time commercial intelligence

for:

- live conversion monitoring
- onboarding tracking
- acquisition analytics
- executive growth intelligence

Streaming systems can use:

- conversion timestamps
- seller segments
- acquisition channels
- sales-funnel events

for:

# operational CRM intelligence.

---

# Output Dataset Location

```text id="p5x8mr"
data/silver/closed_deals/
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

| Layer  | Purpose                                     |
| ------ | ------------------------------------------- |
| Bronze | raw commercial conversion records           |
| Silver | trusted sales operational intelligence      |
| Gold   | conversion analytics & executive dashboards |

The Silver layer transforms:

# raw commercial deal records

into:

# trusted commercial operational intelligence.

---

# Enterprise Engineering Insight

The:

# `silver_closed_deals`

dataset introduces:

# enterprise sales-funnel engineering

into the warehouse architecture.

This demonstrates implementation of:

- commercial operational governance
- conversion intelligence modeling
- acquisition funnel engineering
- sales attribution normalization
- business-growth analytical foundations

This is an important enterprise capability because:
modern marketplaces rely heavily on:

- seller acquisition
- CRM operations
- sales conversion
- onboarding efficiency
- growth intelligence

---

# Final Architectural Value

The `silver_closed_deals` dataset transforms:

# raw commercial conversion records

into:

# trusted commercial operational intelligence

through:

- business-segment normalization
- timestamp standardization
- CRM validation governance
- deterministic acquisition semantics
- operational truth preservation
- validation-driven engineering

This dataset establishes:

# trusted commercial intelligence foundation

for:

- conversion analytics
- growth dashboards
- seller onboarding intelligence
- CRM operational reporting
- executive business analytics

and acts as:

# the commercial conversion backbone

of the Olist Seller Intelligence Platform.
