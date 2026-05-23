# `fct_customer_reviews.md`

## Objective

The `fct_customer_reviews` fact table captures customer satisfaction feedback events associated with completed orders and seller delivery performance.

This mart enables:

- customer satisfaction analysis
- seller reputation analysis
- delivery-impact investigation
- review sentiment analytics
- operational failure validation
- streaming feedback-loop analysis

The review mart acts as:

# the customer satisfaction layer of the warehouse

and connects operational delivery behavior with real customer outcomes.

---

# Business Process

Customer review submission event.

---

# Grain

# One Row = One Customer Review

Each row represents:

- one submitted review
- for one customer order
- at one point in time

This grain preserves:

- customer feedback integrity
- review timing accuracy
- satisfaction-event independence

---

# Why Reviews Require a Separate Fact

Reviews are:

# independent customer business events

They have:

- their own timestamps
- their own lifecycle
- their own behavioral meaning
- their own metrics

Reviews are NOT:

- delivery events
- fulfillment events
- payment events

Therefore:

# reviews must remain in a dedicated fact table

to avoid:

- mixed-grain corruption
- duplicated review metrics
- unreliable satisfaction KPIs

This follows Kimball dimensional modeling principles.

---

# Source Tables

| Source Table                  | Purpose              |
| ----------------------------- | -------------------- |
| `olist_order_reviews_dataset` | Customer review data |
| `olist_orders_dataset`        | Order linkage        |
| `olist_order_items_dataset`   | Seller linkage       |
| `olist_customers_dataset`     | Customer enrichment  |

---

# Table Name

```sql id="j8k2k7"
fct_customer_reviews
```

---

# Primary Key

```sql id="z2n8p1"
review_fact_sk
```

Warehouse-generated surrogate key.

---

# Recommended Schema

| Column Name               | Datatype  | Description                    |
| ------------------------- | --------- | ------------------------------ |
| review_fact_sk            | BIGINT    | Surrogate warehouse key        |
| review_id                 | VARCHAR   | Review business identifier     |
| order_id                  | VARCHAR   | Reviewed order identifier      |
| customer_sk_fk            | BIGINT    | Customer dimension foreign key |
| seller_sk_fk              | BIGINT    | Seller dimension foreign key   |
| review_creation_date_sk   | INT       | Review creation date FK        |
| review_answer_date_sk     | INT       | Review response date FK        |
| review_score              | SMALLINT  | Customer satisfaction score    |
| review_title              | TEXT      | Review title                   |
| review_message            | TEXT      | Review message                 |
| review_creation_timestamp | TIMESTAMP | Review creation timestamp      |
| review_answer_timestamp   | TIMESTAMP | Review response timestamp      |
| review_response_days      | INTEGER   | Time until review response     |
| negative_review_flag      | BOOLEAN   | Negative review indicator      |
| neutral_review_flag       | BOOLEAN   | Neutral review indicator       |
| positive_review_flag      | BOOLEAN   | Positive review indicator      |
| sentiment_category        | VARCHAR   | Satisfaction classification    |
| review_text_exists_flag   | BOOLEAN   | Indicates written feedback     |
| created_at                | TIMESTAMP | Warehouse load timestamp       |

---

# Recommended Sentiment Logic

| Review Score | Sentiment Category |
| ------------ | ------------------ |
| 1–2          | Negative           |
| 3            | Neutral            |
| 4–5          | Positive           |

---

# Recommended Flags

## Negative Review

```sql id="efgk3q"
review_score <= 2
```

---

## Neutral Review

```sql id="3x8l1u"
review_score = 3
```

---

## Positive Review

```sql id="nr9c2m"
review_score >= 4
```

---

# Review Response Days Logic

Measures:

# how quickly customer feedback receives platform response

Formula:

```sql id="0ff6n4"
review_answer_timestamp - review_creation_timestamp
```

Supports:

- customer support responsiveness
- complaint handling analysis
- satisfaction recovery tracking

---

# Text Review Logic

```sql id="1gx2fk"
review_text_exists_flag =
CASE
    WHEN review_message IS NOT NULL
         AND LENGTH(TRIM(review_message)) > 0
    THEN TRUE
    ELSE FALSE
END
```

This enables:

- NLP sentiment analysis later
- complaint text mining
- review quality analysis

---

# Relationships

| Dimension    | Foreign Key             |
| ------------ | ----------------------- |
| dim_customer | customer_sk_fk          |
| dim_seller   | seller_sk_fk            |
| dim_date     | review_creation_date_sk |
| dim_date     | review_answer_date_sk   |

---

# Important Modeling Decision

The Olist review dataset is:

# order-level

NOT:

- item-level
- seller-item-level

Therefore:
seller linkage must be carefully derived.

---

# Recommended Seller Attribution Strategy

For MVP:

# use single-seller delivered orders only

Reason:
multi-seller orders create ambiguous review attribution because one review may relate to multiple seller shipments.

Recommended filter:

```sql id="t2z2ah"
seller_count = 1
```

This preserves:

- KPI correctness
- seller accountability integrity
- reliable satisfaction analysis

This is a deliberate modeling decision rather than a limitation.

---

# Business Questions Supported

This mart enables:

- Do delayed deliveries reduce customer satisfaction?
- Which sellers generate the worst reviews?
- Which regions receive more complaints?
- Do freight-heavy products create lower satisfaction?
- Does distance affect review scores?
- Which seller behaviors predict negative feedback?

---

# Streaming Architecture Role

`fct_customer_reviews`
acts as:

# the streaming feedback validation layer

The streaming system predicts:

```text id="gk7q4n"
high-risk deliveries
```

The review mart later validates:

```text id="s0k9lt"
whether customer dissatisfaction actually occurred
```

This creates:

# closed-loop operational intelligence

and enables:

- model evaluation
- seller-risk validation
- operational effectiveness analysis

---

# ETL Logic

## Step 1 — Extract Reviews

Load:

```sql id="phxjco"
olist_order_reviews_dataset
```

---

## Step 2 — Join Orders

Link reviews to:

- customers
- delivery outcomes
- timestamps

---

## Step 3 — Seller Attribution

Join:

```sql id="0dq0w7"
olist_order_items_dataset
```

and retain:

```sql id="4lmg8h"
single-seller orders
```

for reliable seller attribution.

---

## Step 4 — Derive Sentiment Metrics

Generate:

- sentiment_category
- satisfaction flags
- review_response_days
- text existence flags

---

# Data Quality Rules

| Rule                            | Validation             |
| ------------------------------- | ---------------------- |
| review_score between 1–5        | enforced               |
| non-null review_id              | required               |
| valid date keys                 | FK enforced            |
| one review row per review event | preserved              |
| no orphan orders                | enforced through joins |

---

# Recommended Constraints

| Constraint                   | Purpose                  |
| ---------------------------- | ------------------------ |
| review_score BETWEEN 1 AND 5 | valid satisfaction scale |
| FK to dim_customer           | referential integrity    |
| FK to dim_seller             | seller linkage integrity |
| FK to dim_date               | timeline consistency     |

---

# Recommended Indexes

| Index                    | Purpose                |
| ------------------------ | ---------------------- |
| idx_review_score         | satisfaction filtering |
| idx_review_seller        | seller analysis        |
| idx_review_creation_date | trend analysis         |
| idx_sentiment_category   | dashboard filtering    |

---

# Best Practices Applied

| Best Practice                      | Applied |
| ---------------------------------- | ------- |
| Kimball fact modeling              | Yes     |
| Dedicated business-process fact    | Yes     |
| Separate review grain              | Yes     |
| Role-playing dates                 | Yes     |
| Customer satisfaction segmentation | Yes     |
| Streaming feedback validation      | Yes     |
| Sentiment categorization           | Yes     |
| KPI-safe seller attribution        | Yes     |

---

# Architectural Importance

`fct_customer_reviews`
acts as:

# the customer satisfaction intelligence layer

of the platform.

It connects:

- delivery outcomes
- seller operational behavior
- customer satisfaction
- operational risk
- reputation impact

and enables the warehouse to evolve from:

# logistics analytics

into:

# full operational intelligence and customer experience analytics.
