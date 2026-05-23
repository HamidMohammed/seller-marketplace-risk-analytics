# `fct_seller_acquisition.md`

## Objective

The `fct_seller_acquisition` fact table captures seller acquisition and conversion events occurring throughout the Olist marketing funnel lifecycle.

This mart enables:

- acquisition channel analysis
- seller conversion tracking
- lead-quality evaluation
- funnel performance analytics
- seller lifecycle investigation
- acquisition ROI analysis
- seller risk origin analysis

The acquisition mart acts as:

# the seller lifecycle intelligence layer

of the warehouse.

It connects:

- marketing acquisition
- seller onboarding
- seller operational behavior
- delivery performance
- customer satisfaction

inside one integrated analytical platform.

---

# Business Process

Seller acquisition and conversion event.

---

# Grain

# One Row = One Seller Acquisition Event

Each row represents:

- one seller lead
- entering the acquisition funnel
- through one acquisition process

This grain preserves:

- funnel-event integrity
- acquisition attribution
- conversion lifecycle accuracy

---

# Why Acquisition Requires a Separate Fact

Acquisition events are:

# marketing business events

NOT:

- delivery events
- fulfillment events
- sales events
- customer review events

Acquisition contains:

- lead qualification
- funnel conversion
- acquisition timing
- marketing attribution
- onboarding lifecycle

Therefore:

# acquisition must remain in a dedicated fact table

to avoid:

- mixed-grain corruption
- duplicated funnel metrics
- unreliable conversion KPIs
- commercial-operational confusion

This follows Kimball dimensional modeling principles.

---

# Source Tables

| Source Table                              | Purpose                      |
| ----------------------------------------- | ---------------------------- |
| `olist_marketing_qualified_leads_dataset` | Lead acquisition information |
| `olist_closed_deals_dataset`              | Seller conversion outcomes   |
| `olist_sellers_dataset`                   | Seller linkage               |

---

# Table Name

```sql id="a6v4fk"
fct_seller_acquisition
```

---

# Primary Key

```sql id="b7g5tr"
seller_acquisition_fact_sk
```

Warehouse-generated surrogate key.

---

# Recommended Schema

| Column Name                | Datatype      | Description                         |
| -------------------------- | ------------- | ----------------------------------- |
| seller_acquisition_fact_sk | BIGINT        | Surrogate warehouse key             |
| mql_id                     | VARCHAR       | Marketing-qualified lead identifier |
| seller_id                  | VARCHAR       | Converted seller identifier         |
| seller_sk_fk               | BIGINT        | Seller dimension FK                 |
| first_contact_date_sk      | INT           | First contact date FK               |
| lead_qualification_date_sk | INT           | Lead qualification date FK          |
| conversion_date_sk         | INT           | Seller conversion date FK           |
| acquisition_channel        | VARCHAR       | Marketing acquisition source        |
| lead_type                  | VARCHAR       | Lead classification                 |
| lead_behavior_profile      | VARCHAR       | Behavioral profile                  |
| business_segment           | VARCHAR       | Seller business segment             |
| declared_monthly_revenue   | DECIMAL(12,2) | Seller self-declared revenue        |
| expected_sales_volume      | VARCHAR       | Expected seller sales scale         |
| lead_conversion_status     | VARCHAR       | Funnel conversion result            |
| days_to_convert            | INTEGER       | Lead-to-seller conversion duration  |
| converted_flag             | BOOLEAN       | Seller conversion indicator         |
| high_value_seller_flag     | BOOLEAN       | Premium seller indicator            |
| acquisition_risk_category  | VARCHAR       | Predicted operational risk          |
| load_timestamp             | TIMESTAMP     | Warehouse load timestamp            |

---

# Recommended Metrics Logic

## Days to Convert

Measures:

# seller onboarding efficiency

Formula:

```sql id="j8w9zt"
conversion_date - first_contact_date
```

Supports:

- funnel efficiency analysis
- onboarding optimization
- acquisition bottleneck investigation

---

# Converted Flag

```sql id="t3r8xa"
CASE
    WHEN seller_id IS NOT NULL
    THEN 1
    ELSE 0
END
```

Measures:

# lead conversion success

---

# High Value Seller Flag

Example:

```sql id="uq1xrm"
CASE
    WHEN declared_monthly_revenue >= 100000
    THEN 1
    ELSE 0
END
```

Supports:

- premium seller segmentation
- strategic seller prioritization
- acquisition ROI analysis

---

# Acquisition Risk Category

Derived using:

- lead behavior profile
- business segment
- acquisition source
- historical seller outcomes

Example categories:

| Category      | Meaning                          |
| ------------- | -------------------------------- |
| Low Risk      | Stable acquisition profile       |
| Medium Risk   | Moderate operational uncertainty |
| High Risk     | Historically problematic profile |
| Critical Risk | High failure probability         |

This supports:

# proactive seller-risk investigation

---

# Relationships

| Dimension  | Foreign Key                |
| ---------- | -------------------------- |
| dim_seller | seller_sk_fk               |
| dim_date   | first_contact_date_sk      |
| dim_date   | lead_qualification_date_sk |
| dim_date   | conversion_date_sk         |

---

# Important Modeling Decision

The marketing funnel datasets do NOT cover:

# all Olist sellers

Therefore:

- not every seller has acquisition records
- some sellers entered outside tracked funnel systems

This is expected behavior.

The warehouse intentionally preserves:

# partial funnel coverage

rather than artificially forcing complete attribution.

---

# Recommended Join Strategy

Use:

```sql id="7czgfw"
LEFT JOIN
```

when enriching seller dimensions or linking acquisition facts.

This avoids:

- seller loss
- biased conversion analytics
- incomplete operational population

---

# Business Questions Supported

This mart enables:

- Which acquisition channels produce best sellers?
- Which lead profiles generate operational failures?
- Do certain acquisition sources lead to poor delivery performance?
- Which seller segments convert fastest?
- Which acquisition types produce highest revenue?
- Can acquisition behavior predict future seller risk?

---

# Cross-Mart Analytical Value

This mart becomes extremely powerful when connected with:

| Fact Table             | Analytical Connection                |
| ---------------------- | ------------------------------------ |
| fct_seller_fulfillment | Acquisition vs operational behavior  |
| fct_order_delivery     | Acquisition vs delivery quality      |
| fct_customer_reviews   | Acquisition vs customer satisfaction |
| fct_order_sales        | Acquisition vs revenue generation    |

This creates:

# full seller lifecycle intelligence

from:

```text id="6pjxcs"
lead acquisition
        ↓
seller onboarding
        ↓
operational behavior
        ↓
delivery outcome
        ↓
customer satisfaction
        ↓
revenue generation
```

This is the strongest business narrative in the entire platform.

---

# Streaming Architecture Role

`fct_seller_acquisition`
primarily acts as:

# historical enrichment intelligence

for:

- seller baseline creation
- risk scoring initialization
- seller segmentation
- onboarding monitoring

Streaming systems can prioritize:

```text id="2pnm4y"
historically risky acquisition profiles
```

before:

```text id="84l31z"
delivery failures occur
```

This enables:

# proactive operational intelligence

rather than reactive reporting.

---

# ETL Logic

## Step 1 — Extract Leads

Load:

```sql id="dfnq0v"
olist_marketing_qualified_leads_dataset
```

---

## Step 2 — Extract Converted Sellers

Load:

```sql id="k0z53w"
olist_closed_deals_dataset
```

---

## Step 3 — Link Sellers

Match:

- leads
- converted sellers
- seller identifiers

---

## Step 4 — Generate Funnel Metrics

Derive:

- days_to_convert
- converted_flag
- acquisition_risk_category
- high_value_seller_flag

---

# Data Quality Rules

| Rule                             | Validation   |
| -------------------------------- | ------------ |
| Unique lead identifiers          | enforced     |
| Valid conversion dates           | enforced     |
| Non-negative conversion duration | enforced     |
| Valid FK relationships           | enforced     |
| Valid acquisition categories     | standardized |

---

# Recommended Constraints

| Constraint                   | Purpose                   |
| ---------------------------- | ------------------------- |
| days_to_convert >= 0         | Valid onboarding duration |
| valid acquisition categories | Controlled segmentation   |
| valid FK relationships       | Referential integrity     |
| converted_flag values        | Boolean consistency       |

---

# Recommended Indexes

| Index                   | Purpose             |
| ----------------------- | ------------------- |
| idx_acquisition_channel | Channel analysis    |
| idx_conversion_status   | Funnel filtering    |
| idx_business_segment    | Seller segmentation |
| idx_conversion_date     | Trend analysis      |
| idx_risk_category       | Risk investigation  |

---

# Best Practices Applied

| Best Practice                   | Applied |
| ------------------------------- | ------- |
| Kimball fact modeling           | Yes     |
| Dedicated business-process fact | Yes     |
| Funnel lifecycle separation     | Yes     |
| Conformed dimensions            | Yes     |
| Streaming enrichment support    | Yes     |
| Historical seller intelligence  | Yes     |
| Seller lifecycle analytics      | Yes     |
| Business-driven architecture    | Yes     |

---

# Architectural Importance

`fct_seller_acquisition`
acts as:

# the seller origin intelligence layer

of the platform.

It enables the warehouse to analyze:

- where sellers come from
- which acquisition strategies succeed
- which seller profiles become operational risks
- how acquisition quality affects delivery outcomes
- how onboarding behavior affects customer satisfaction

and transforms the platform from:

# operational analytics

into:

# full seller lifecycle intelligence and predictive business analytics platform.
