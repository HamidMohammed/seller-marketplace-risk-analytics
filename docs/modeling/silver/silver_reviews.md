# `silver_reviews.md`

## Objective

The `silver_reviews` dataset represents the trusted behavioral intelligence layer inside the Olist Seller Intelligence Platform.

This dataset transforms:

# raw customer review records

into:

# validated behavioral operational intelligence

used by:

- customer satisfaction analytics
- seller quality analysis
- delivery experience monitoring
- review sentiment exploration
- marketplace trust analytics
- operational quality intelligence

The dataset acts as:

# the customer behavioral truth layer

across the analytical warehouse.

Unlike:

- customer dimensions
- seller dimensions
- product dimensions

reviews represent:

# behavioral operational events

capturing:

- customer feedback
- satisfaction outcomes
- post-purchase experiences

which makes this dataset:

# analytically strategic.

---

# Dataset Role in Architecture

```text id="x8r2pq"
Bronze Reviews
        ↓
silver_reviews
        ↓
Behavioral Operational Intelligence
```

This dataset powers:

- customer satisfaction dashboards
- seller quality monitoring
- delivery experience analysis
- review-score analytics
- operational quality KPIs
- behavioral marketplace intelligence

and acts as:

# the behavioral intelligence foundation

of the warehouse.

---

# Dataset Grain

# ONE ROW = ONE REVIEW EVENT

This grain is strictly preserved throughout all transformations.

The dataset intentionally models:

# review-level behavioral events

NOT:

- aggregated sentiment summaries
- seller rating rollups
- NLP predictions
- AI-generated sentiment classifications

Maintaining this grain is critical because:
review duplication would corrupt:

- satisfaction KPIs
- seller-quality metrics
- review-score distributions
- operational trust analytics

---

# Source Dataset

| Source Dataset       | Layer  | Purpose                    |
| -------------------- | ------ | -------------------------- |
| bronze/order_reviews | Bronze | Raw customer review events |

---

# Source Columns

| Column                  | Meaning                     |
| ----------------------- | --------------------------- |
| review_id               | Review business identifier  |
| order_id                | Related order identifier    |
| review_score            | Customer satisfaction score |
| review_comment_title    | Review title                |
| review_comment_message  | Review message              |
| review_creation_date    | Review creation timestamp   |
| review_answer_timestamp | Review response timestamp   |

---

# Important Review Modeling Interpretation

The Olist review dataset models:

# customer post-purchase feedback behavior

through:

- review scores
- review text
- review timestamps

This means:
reviews represent:

# operational customer experience signals

across:

- sellers
- products
- delivery experiences
- marketplace trust

---

# Silver Responsibilities

The `silver_reviews` pipeline is responsible for:

| Responsibility            | Purpose                     |
| ------------------------- | --------------------------- |
| Review-grain validation   | behavioral integrity        |
| Review-score validation   | analytical trust            |
| Text normalization        | consistency                 |
| Timestamp standardization | temporal analytics          |
| Metadata enrichment       | lineage                     |
| Validation governance     | behavioral analytical trust |

---

# Review Score Strategy

The dataset validates:

# customer satisfaction scores

to ensure:

- business correctness
- analytical reliability
- KPI trustworthiness

---

# Review Score Interpretation

Review scores follow:

# marketplace satisfaction scoring

where:

| Score | Meaning           |
| ----- | ----------------- |
| 1     | Very dissatisfied |
| 2     | Dissatisfied      |
| 3     | Neutral           |
| 4     | Satisfied         |
| 5     | Very satisfied    |

This creates:

# operational customer satisfaction intelligence

for downstream analytics.

---

# Text Governance Strategy

The Silver layer applies:

# controlled text normalization

to:

- preserve operational truth
- improve consistency
- avoid analytical fragmentation

---

# Text Normalization Rules

## Transformations

```python id="k6f9zt"
trim(review_comment_title)
```

```python id="d1g4pa"
trim(review_comment_message)
```

---

## Purpose

Prevents:

- inconsistent spacing
- malformed textual records
- unstable text grouping

while preserving:

# original customer intent.

---

# IMPORTANT GOVERNANCE RULE

The Silver layer intentionally DOES NOT:

- rewrite customer language
- perform sentiment AI
- aggressively clean text
- remove behavioral anomalies

because Silver should preserve:

# operational behavioral truth.

Advanced NLP belongs later in:

# Gold analytics or ML pipelines.

---

# Temporal Intelligence Strategy

The dataset standardizes:

# review timestamps

to support:

- temporal satisfaction analytics
- response-time analysis
- operational quality monitoring
- review trend intelligence

---

# Timestamp Standardization

## Standardized Columns

| Column                  |
| ----------------------- |
| review_creation_date    |
| review_answer_timestamp |

---

## Purpose

Ensures:

- temporal consistency
- reliable time-based KPIs
- stable trend analysis

---

# Transformations Applied

---

# 1. Review ID Standardization

## Transformation

```python id="7q4s8x"
trim(review_id)
```

---

## Purpose

Ensures:

- stable joins
- behavioral consistency
- reliable downstream relationships

---

# 2. Text Normalization

## Transformation

```python id="4m8s0v"
trim(review_comment_message)
```

---

## Purpose

Improves:

- text consistency
- analytical cleanliness
- operational readability

without changing:

# customer behavioral meaning.

---

# 3. Review Score Standardization

## Transformation

```python id="9f6j2r"
cast(review_score as integer)
```

---

## Purpose

Ensures:

- analytical correctness
- stable KPI calculations
- deterministic score distributions

---

# 4. Timestamp Standardization

## Transformation

```python id="y2w6lt"
cast(review timestamps as timestamp)
```

---

## Purpose

Supports:

- time-series analysis
- operational trend monitoring
- behavioral intelligence

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

# validation-driven behavioral governance

defined in:

```text id="1c7h2v"
silver_transformation_strategy.md
```

All review transformations are validated BEFORE Silver output generation.

---

# Validation Rules

---

# 1. Grain Validation

## Rule

```text id="y6m3zn"
ONE ROW = ONE REVIEW EVENT
```

---

## Validation Key

```text id="m8z2ja"
review_id
```

---

## Purpose

Protect:

- satisfaction analytics
- seller-quality KPIs
- review distributions
- behavioral trust

---

# 2. Critical Null Validation

## Critical Columns

| Column       | Reason                    |
| ------------ | ------------------------- |
| review_id    | review business key       |
| order_id     | operational linkage       |
| review_score | satisfaction intelligence |

---

## Purpose

Prevent:

- broken behavioral relationships
- invalid review analytics
- unusable satisfaction metrics

---

# 3. Review Score Validation

## Rule

1 \leq review_score \leq 5

---

## Purpose

Ensure:

- valid customer satisfaction scoring
- trustworthy KPI distributions
- reliable operational analytics

---

# 4. Timestamp Validation

## Purpose

Validate:

- valid review timestamps
- temporal consistency
- operational chronology

---

# 5. Text Normalization Validation

## Purpose

Ensure:

- deterministic text formatting
- stable review consistency
- controlled operational cleanliness

---

# Important Architectural Decisions

---

# Reviews as Behavioral Facts

The project models reviews as:

# behavioral operational facts

NOT:

# dimensions.

Reviews represent:

- customer experience signals
- post-purchase behavior
- operational satisfaction outcomes

This is a critical warehouse-modeling distinction.

---

# Behavioral Operational Truth

The dataset preserves:

# authentic customer behavioral records

instead of:

# aggressively rewriting customer feedback.

This follows:

# operational truth preservation

defined in the Silver governance strategy.

This is important because:
real-world review systems commonly contain:

- imperfect language
- incomplete text
- behavioral anomalies
- inconsistent formatting

---

# Controlled Text Governance

The pipeline intentionally avoids:

- NLP sentiment scoring
- AI classification
- semantic rewriting
- language filtering

inside:
`silver_reviews`

because Silver operational facts should remain:

# raw-but-governed behavioral truth.

Advanced sentiment analytics belong later in:

# Gold analytical layers or ML systems.

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

- behavioral reproducibility
- auditability
- analytical defensibility

---

# Downstream Dependencies

The following datasets depend on:

# silver_reviews

| Dataset               | Dependency Purpose         |
| --------------------- | -------------------------- |
| fct_customer_reviews  | satisfaction analytics     |
| seller-quality marts  | operational trust analysis |
| review dashboards     | behavioral intelligence    |
| sentiment exploration | review analysis            |

This makes:
`silver_reviews`

a:

# shared behavioral intelligence foundation

across the warehouse.

---

# Streaming Architecture Role

`silver_reviews`
supports:

# operational behavioral monitoring

for:

- customer satisfaction tracking
- seller-quality monitoring
- delivery-experience analysis
- review-score intelligence

Streaming systems can use:

- review scores
- review timestamps
- behavioral feedback

for:

# real-time operational quality intelligence.

---

# Output Dataset Location

```text id="f8k4vt"
data/silver/reviews/
```

Stored as:

# parquet

for:

- Spark optimization
- scalable behavioral processing
- warehouse integration

---

# Relationship to Medallion Architecture

Within the Medallion Architecture:

| Layer  | Purpose                                     |
| ------ | ------------------------------------------- |
| Bronze | raw review events                           |
| Silver | trusted behavioral operational intelligence |
| Gold   | satisfaction marts & review analytics       |

The Silver layer transforms:

# raw customer feedback records

into:

# trusted behavioral operational intelligence.

---

# Final Architectural Value

The `silver_reviews` dataset transforms:

# raw customer review records

into:

# trusted behavioral operational intelligence

through:

- review-score governance
- text normalization
- timestamp standardization
- behavioral validation
- operational truth preservation
- validation-driven engineering

This dataset establishes:

# trusted behavioral intelligence foundation

for:

- customer satisfaction analytics
- seller-quality monitoring
- review intelligence
- operational quality KPIs
- behavioral warehouse analytics

and acts as:

# the behavioral intelligence backbone

of the Olist Seller Intelligence Platform.
