# `seller_acquisition_staging.md`

````markdown id="z7m4qk"
# Seller Acquisition Staging

## Objective

The `seller_acquisition_staging` dataset represents the unified seller acquisition intelligence layer inside the Olist Seller Intelligence Platform.

This staging dataset combines:

- marketing-qualified lead intelligence
- seller conversion lifecycle data
- seller operational enrichment

to create:

# end-to-end seller acquisition intelligence

used by:

- acquisition analytics
- seller onboarding analysis
- funnel conversion KPIs
- seller quality segmentation
- acquisition-risk analytics
- seller lifecycle intelligence
- downstream acquisition marts

The staging layer acts as:

# the commercial intelligence bridge

between:

- marketing acquisition
- seller onboarding
- operational seller ecosystem performance

inside one integrated analytical platform.

---

# Dataset Role in Architecture

```text
silver_mql
        +
silver_closed_deals
        +
silver_sellers
        ↓
seller_acquisition_staging
        ↓
fct_seller_acquisition
        ↓
Seller Lifecycle Analytics
```
````

This staging dataset enables:

# seller lifecycle causality analysis

connecting:

- acquisition source
- conversion quality
- operational seller profile
- future operational outcomes

inside one analytical flow.

---

# Business Process

# Seller acquisition and conversion lifecycle

This process tracks:

- marketing-qualified lead generation
- seller conversion
- onboarding speed
- seller commercial profile
- acquisition quality

Unlike:

- delivery operations
- fulfillment operations
- customer satisfaction

this dataset models:

# commercial acquisition intelligence

which is a completely different business process.

---

# Dataset Grain

# ONE ROW = ONE SELLER ACQUISITION EVENT

Each row represents:

- one marketing-qualified lead
- one acquisition journey
- one seller conversion outcome

This grain is strictly preserved throughout all transformations.

This is architecturally critical because:
acquisition intelligence operates at:

# funnel-event grain

NOT:

- order grain
- review grain
- fulfillment grain
- delivery grain

Breaking this grain would corrupt:

- conversion metrics
- funnel analytics
- acquisition attribution
- seller lifecycle intelligence

---

# Source Datasets

| Source Dataset      | Layer  | Purpose                               |
| ------------------- | ------ | ------------------------------------- |
| silver_mql          | Silver | Marketing-qualified lead intelligence |
| silver_closed_deals | Silver | Seller conversion outcomes            |
| silver_sellers      | Silver | Seller operational enrichment         |

---

# Source Dataset Responsibilities

---

# 1. `silver_mql`

Provides:

# acquisition-origin intelligence

Including:

- lead identifiers
- acquisition channels
- landing pages
- first-contact timing

This dataset represents:

# marketing funnel entry

---

# 2. `silver_closed_deals`

Provides:

# conversion lifecycle intelligence

Including:

- seller linkage
- conversion outcomes
- business segmentation
- declared revenue
- seller commercial profile

This dataset represents:

# acquisition funnel conversion

---

# 3. `silver_sellers`

Provides:

# operational seller enrichment

Including:

- seller geography
- acquisition source normalization
- seller operational identity

This enables:

# operational-commercial linkage

between:

- acquisition intelligence
- future seller operations

---

# Silver Responsibilities

The `seller_acquisition_staging` pipeline is responsible for:

| Responsibility                | Purpose                          |
| ----------------------------- | -------------------------------- |
| Funnel lifecycle integration  | unified acquisition intelligence |
| Seller enrichment             | operational-commercial linkage   |
| Conversion metric derivation  | onboarding analytics             |
| Acquisition risk segmentation | predictive intelligence          |
| Metadata enrichment           | lineage                          |
| Grain preservation            | KPI integrity                    |
| Analytical preparation        | Gold readiness                   |

---

# Transformations Applied

---

# 1. Acquisition Dataset Integration

## Transformation

The pipeline integrates:

```text
silver_mql
        +
silver_closed_deals
        +
silver_sellers
```

using:

- `mql_id`
- `seller_id`

as controlled business linkage keys.

---

## Purpose

This creates:

# unified seller acquisition lifecycle intelligence

allowing:

- acquisition tracking
- seller onboarding analysis
- operational-commercial correlation

inside one analytical entity.

---

# 2. Days to Convert Metric

## Derived Column

```text
days_to_convert
```

---

## Formula

```python
datediff(
    won_date,
    first_contact_date
)
```

---

## Business Meaning

Measures:

# seller onboarding efficiency

from:

- first acquisition contact
  to:
- successful seller conversion

---

## Business Value

Supports:

- funnel optimization
- onboarding performance analysis
- acquisition bottleneck investigation
- sales-process efficiency analysis

---

# 3. Converted Flag

## Derived Column

```text
converted_flag
```

---

## Logic

```python
seller_id IS NOT NULL
```

---

## Business Meaning

Identifies:

# successful acquisition conversion

---

## Business Value

Supports:

- conversion-rate KPIs
- acquisition-source performance analysis
- marketing efficiency analytics

---

# 4. High Value Seller Flag

## Derived Column

```text
high_value_seller_flag
```

---

## Logic

```python
declared_monthly_revenue >= 100000
```

---

## Business Meaning

Identifies:

# commercially valuable sellers

based on:

- self-declared monthly revenue

---

## Business Value

Supports:

- premium seller segmentation
- acquisition prioritization
- seller portfolio optimization

---

# 5. Acquisition Risk Category

## Derived Column

```text
acquisition_risk_category
```

---

## Logic

| Condition                      | Category  |
| ------------------------------ | --------- |
| low revenue + long conversion  | High Risk |
| high revenue + fast conversion | Premium   |
| unknown revenue                | Unknown   |
| otherwise                      | Standard  |

---

## Business Meaning

Provides:

# early seller quality estimation

before:

- operational fulfillment
- delivery performance
- customer satisfaction outcomes

---

## Business Value

Supports:

- seller risk intelligence
- acquisition-quality analysis
- commercial strategy optimization
- predictive seller segmentation

This is one of the MOST strategically valuable enrichments in the entire platform architecture.

---

# Final Dataset Schema

| Column                    | Datatype  | Description                          |
| ------------------------- | --------- | ------------------------------------ |
| mql_id                    | string    | Marketing-qualified lead identifier  |
| seller_id                 | string    | Converted seller identifier          |
| first_contact_date        | timestamp | Initial lead contact date            |
| won_date                  | timestamp | Seller conversion timestamp          |
| landing_page_id           | string    | Acquisition landing page             |
| marketing_origin          | string    | Marketing acquisition channel        |
| acquisition_source        | string    | Normalized seller acquisition source |
| business_segment          | string    | Seller business segment              |
| lead_type                 | string    | Seller lead classification           |
| lead_behaviour_profile    | string    | Seller behavioral profile            |
| declared_monthly_revenue  | decimal   | Seller-declared revenue              |
| seller_city               | string    | Seller city                          |
| seller_state              | string    | Seller state                         |
| days_to_convert           | integer   | Funnel conversion duration           |
| converted_flag            | boolean   | Conversion success indicator         |
| high_value_seller_flag    | boolean   | Premium seller indicator             |
| acquisition_risk_category | string    | Seller acquisition risk class        |
| silver_loaded_at          | timestamp | Pipeline load timestamp              |
| source_system             | string    | Source system metadata               |
| transformation_version    | string    | Transformation version metadata      |

---

# Grain Integrity Protection

The pipeline explicitly preserves:

# ONE ROW = ONE SELLER ACQUISITION EVENT

This protection prevents:

- duplicate conversion events
- inflated funnel KPIs
- acquisition attribution corruption
- seller lifecycle distortion

The validation layer enforces:

# strict acquisition-grain governance

through:

- duplicate MQL validation
- conversion consistency validation
- lifecycle integrity validation

---

# Validation Strategy

The staging dataset includes enterprise-style validation checks:

| Validation Type                     | Purpose                       |
| ----------------------------------- | ----------------------------- |
| MQL grain validation                | duplicate prevention          |
| Critical null validation            | analytical trust              |
| Conversion timeline validation      | lifecycle integrity           |
| Revenue quality validation          | commercial metric correctness |
| Acquisition distribution validation | anomaly detection             |
| Risk-category validation            | segmentation integrity        |

This follows the project’s:

# validation-driven transformation engineering strategy

used throughout the Silver architecture.

---

# Architectural Significance

The `seller_acquisition_staging` dataset represents:

# commercial seller lifecycle intelligence

inside the warehouse architecture.

Unlike:

```text
order_delivery_staging
```

which measures:

# customer delivery outcomes

and:

```text
seller_fulfillment_staging
```

which measures:

# seller operational workload

this staging layer measures:

# seller acquisition quality and conversion intelligence

This distinction is architecturally critical because:

- acquisition is a commercial process
- operations are fulfillment processes
- customer reviews are behavioral processes

Keeping these processes separated while analytically connected preserves:

- business-process integrity
- KPI correctness
- dimensional consistency
- analytical trustworthiness

This follows:

# Kimball dimensional modeling principles

and:

# enterprise analytical engineering practices.

---

# Operational Intelligence Enabled

This staging layer now supports:

| Capability                      | Enabled |
| ------------------------------- | ------- |
| seller acquisition analytics    | YES     |
| conversion funnel analysis      | YES     |
| onboarding performance analysis | YES     |
| seller quality segmentation     | YES     |
| acquisition-risk analysis       | YES     |
| acquisition-source benchmarking | YES     |
| seller lifecycle analytics      | YES     |

---

# Business Narrative Contribution

This staging dataset completes the platform’s:

# full seller lifecycle intelligence narrative

```text
Seller Acquisition
        ↓
Seller Quality
        ↓
Operational Fulfillment
        ↓
Delivery Outcome
        ↓
Customer Satisfaction
```

This is one of the MOST strategically valuable aspects of the entire platform architecture because it enables:

# cross-process business causality analytics

rather than isolated dashboard reporting.

---

# Gold Layer Readiness

The dataset is specifically designed to support:

```text
fct_seller_acquisition
```

inside the Gold analytical layer.

The staging structure ensures:

- clean acquisition grain
- trusted seller linkage
- validated conversion metrics
- dimensional modeling readiness
- KPI-safe analytical enrichment

for downstream:

- dbt modeling
- Power BI dashboards
- seller intelligence analytics
- strategic commercial reporting.

```

```
