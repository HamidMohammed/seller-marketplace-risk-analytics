# `seller_performance_monthly_staging.md`

````markdown id="m7q2vk"
# Seller Performance Monthly Staging

## Objective

The `seller_performance_monthly_staging` dataset represents the temporal seller behavioral intelligence layer inside the Olist Seller Intelligence Platform.

This staging dataset aggregates:

- delivery performance
- customer satisfaction behavior
- operational workload intelligence

into:

# longitudinal seller performance analytics

used by:

- seller performance scoring
- operational risk detection
- trend analysis
- streaming baseline initialization
- seller benchmarking
- downstream Gold marts

This staging layer acts as:

# the unified seller behavioral baseline

connecting:

- operational fulfillment
- delivery outcomes
- customer satisfaction
- temporal seller trends

inside one integrated analytical architecture.

---

# Dataset Role in Architecture

```text
order_delivery_staging
            +
reviews_staging
            +
seller_fulfillment_staging
            ↓
seller_performance_monthly_staging
            ↓
fct_seller_performance
            ↓
Seller Risk & Performance Intelligence
```
````

This staging dataset enables:

# seller lifecycle behavioral analysis

across:

- time
- operational quality
- customer satisfaction
- workload pressure

inside one unified seller-centric analytical model.

---

# Business Process

# Seller longitudinal performance monitoring

This process tracks:

- seller operational consistency
- delivery reliability
- customer satisfaction trends
- workload pressure evolution
- seller behavioral trajectory

Unlike:

- order events
- review events
- fulfillment events

this dataset models:

# aggregated seller behavioral performance over time

which is a completely different analytical process.

---

# Dataset Grain

# ONE ROW = ONE SELLER PER MONTH

Each row represents:

- one seller
- during one calendar month
- with aggregated operational and behavioral KPIs

This grain is strictly preserved throughout the pipeline.

This is architecturally critical because:
seller-performance intelligence operates at:

# temporal behavioral grain

NOT:

- order grain
- item grain
- review grain
- payment grain

Breaking this grain would corrupt:

- seller trend analysis
- behavioral trajectories
- streaming baselines
- performance KPIs
- risk scoring

---

# Source Datasets

| Source Dataset             | Layer          | Purpose                            |
| -------------------------- | -------------- | ---------------------------------- |
| order_delivery_staging     | Silver Staging | Delivery performance intelligence  |
| reviews_staging            | Silver Staging | Customer satisfaction intelligence |
| seller_fulfillment_staging | Silver Staging | Operational workload intelligence  |

---

# Source Dataset Responsibilities

---

# 1. `order_delivery_staging`

Provides:

# delivery operational intelligence

Including:

- shipping duration
- delay behavior
- delivery outcomes
- on-time performance

This dataset represents:

# operational delivery quality

---

# 2. `reviews_staging`

Provides:

# customer satisfaction intelligence

Including:

- review scores
- customer sentiment
- negative-review behavior
- delivery-experience reactions

This dataset represents:

# customer behavioral feedback

---

# 3. `seller_fulfillment_staging`

Provides:

# workload and fulfillment intelligence

Including:

- seller operational volume
- workload pressure
- freight characteristics
- fulfillment complexity

This dataset represents:

# operational seller workload

---

# Silver Responsibilities

The `seller_performance_monthly_staging` pipeline is responsible for:

| Responsibility                 | Purpose                          |
| ------------------------------ | -------------------------------- |
| Temporal seller aggregation    | seller-month behavioral baseline |
| KPI derivation                 | operational intelligence         |
| Trend metric calculation       | seller trajectory analytics      |
| Cross-process enrichment       | unified seller intelligence      |
| Performance segmentation       | risk classification              |
| Metadata enrichment            | lineage                          |
| Grain preservation             | KPI integrity                    |
| Streaming baseline preparation | real-time readiness              |

---

# Transformations Applied

---

# 1. Delivery Performance Aggregation

## Aggregated Metrics

| Metric               | Purpose                  |
| -------------------- | ------------------------ |
| monthly_orders       | seller operational scale |
| avg_shipping_days    | delivery efficiency      |
| on_time_rate         | operational reliability  |
| avg_delay_days       | delay severity           |
| delayed_orders_count | delivery risk            |

---

## Business Meaning

These metrics measure:

# seller delivery operational quality

over time.

---

## Business Value

Supports:

- operational benchmarking
- delivery reliability analysis
- seller SLA monitoring
- delay-risk investigation

---

# 2. Review Performance Aggregation

## Aggregated Metrics

| Metric               | Purpose                 |
| -------------------- | ----------------------- |
| avg_review_score     | customer satisfaction   |
| negative_review_rate | dissatisfaction signal  |
| monthly_review_count | review confidence level |

---

## Business Meaning

These metrics measure:

# customer perception of seller quality

over time.

---

## Business Value

Supports:

- seller reputation analysis
- customer experience analytics
- satisfaction trend monitoring
- behavioral anomaly detection

---

# 3. Workload Performance Aggregation

## Aggregated Metrics

| Metric                 | Purpose              |
| ---------------------- | -------------------- |
| avg_monthly_workload   | operational pressure |
| avg_freight_ratio      | logistics burden     |
| avg_product_volume_cm3 | shipping complexity  |

---

## Business Meaning

These metrics measure:

# seller operational burden

over time.

---

## Business Value

Supports:

- workload-risk analysis
- logistics pressure investigation
- fulfillment scalability analysis
- operational-capacity monitoring

---

# 4. Volume Growth Rate

## Derived Column

```text id="a7w9ml"
volume_growth_rate
```

---

## Formula

```python id="7y5twv"
(
    current_month_orders -
    previous_month_orders
)
/
previous_month_orders
```

---

## Business Meaning

Measures:

# seller operational growth trajectory

between:

- consecutive months

---

## Business Value

Supports:

- growth monitoring
- seller expansion analysis
- operational volatility detection
- trend-based seller scoring

This is one of the MOST strategically valuable metrics in the platform.

---

# 5. Seller Performance Category

## Derived Column

```text id="4m2zxo"
seller_performance_category
```

---

## Classification Logic

| Condition                            | Category      |
| ------------------------------------ | ------------- |
| high on-time + high reviews          | Top Performer |
| low on-time OR high negative reviews | At Risk       |
| otherwise                            | Stable        |

---

## Business Meaning

Provides:

# behavioral seller segmentation

based on:

- operational reliability
- customer satisfaction
- delivery consistency

---

## Business Value

Supports:

- seller risk analytics
- operational prioritization
- marketplace quality management
- seller intervention strategies

This becomes a core signal for:

# streaming anomaly detection

inside the real-time architecture.

---

# Streaming Architecture Significance

This dataset plays a critical role in:

# streaming baseline initialization

The streaming layer requires:

# historical seller state

before processing:

- real-time events
- Kafka streams
- operational anomalies

The:

```text id="t8jlwm"
seller_performance_monthly_staging
```

dataset acts as:

# seller baseline memory

for:

- streaming seller scoring
- anomaly comparison
- real-time risk detection

This is one of the MOST advanced architectural capabilities in the entire platform.

---

# Final Dataset Schema

| Column                      | Datatype  | Description                       |
| --------------------------- | --------- | --------------------------------- |
| seller_id                   | string    | Seller identifier                 |
| performance_year            | integer   | Performance year                  |
| performance_month           | integer   | Performance month                 |
| monthly_orders              | integer   | Seller monthly order volume       |
| avg_shipping_days           | decimal   | Average delivery duration         |
| on_time_rate                | decimal   | On-time delivery percentage       |
| avg_delay_days              | decimal   | Average delivery delay            |
| delayed_orders_count        | integer   | Delayed-order volume              |
| avg_review_score            | decimal   | Average customer review score     |
| negative_review_rate        | decimal   | Negative review percentage        |
| monthly_review_count        | integer   | Total monthly reviews             |
| avg_monthly_workload        | decimal   | Average workload intensity        |
| avg_freight_ratio           | decimal   | Freight burden ratio              |
| avg_product_volume_cm3      | decimal   | Product shipping complexity       |
| previous_month_orders       | integer   | Prior month volume                |
| volume_growth_rate          | decimal   | Seller growth trajectory          |
| seller_performance_category | string    | Seller performance classification |
| silver_loaded_at            | timestamp | Pipeline load timestamp           |
| source_system               | string    | Source-system metadata            |
| transformation_version      | string    | Transformation version metadata   |

---

# Grain Integrity Protection

The pipeline explicitly preserves:

# ONE ROW = ONE SELLER PER MONTH

This protection prevents:

- duplicate seller-month records
- KPI inflation
- behavioral metric corruption
- temporal aggregation distortion

The validation layer enforces:

# strict temporal-grain governance

through:

- seller-month uniqueness validation
- KPI-range validation
- growth-rate consistency validation

---

# Validation Strategy

The staging dataset includes enterprise-style validation checks:

| Validation Type                     | Purpose              |
| ----------------------------------- | -------------------- |
| Temporal grain validation           | duplicate prevention |
| Critical null validation            | analytical trust     |
| KPI-range validation                | metric correctness   |
| Growth-rate validation              | trajectory integrity |
| Performance distribution validation | anomaly detection    |

This follows the project’s:

# validation-driven transformation engineering strategy

used throughout the Silver architecture.

---

# Architectural Significance

The `seller_performance_monthly_staging` dataset represents:

# temporal seller behavioral intelligence

inside the warehouse architecture.

Unlike:

```text id="v6f2tz"
order_delivery_staging
```

which models:

# operational delivery events

and:

```text id="e9jlwm"
reviews_staging
```

which models:

# customer behavioral reactions

this staging layer models:

# seller behavioral evolution over time

This distinction is architecturally critical because:

- event data measures transactions
- temporal intelligence measures trajectories

Keeping these processes separated while analytically connected preserves:

- business-process integrity
- KPI correctness
- temporal consistency
- analytical trustworthiness

This follows:

# Kimball dimensional modeling principles

and:

# enterprise behavioral analytics engineering practices.

---

# Operational Intelligence Enabled

This staging layer now supports:

| Capability                        | Enabled |
| --------------------------------- | ------- |
| seller performance analytics      | YES     |
| operational trend analysis        | YES     |
| seller risk detection             | YES     |
| workload trajectory analysis      | YES     |
| customer satisfaction monitoring  | YES     |
| streaming baseline initialization | YES     |
| seller anomaly detection          | YES     |

---

# Business Narrative Contribution

This staging dataset completes the platform’s:

# seller behavioral intelligence architecture

```text id="k2d4vx"
Seller Acquisition
        ↓
Operational Workload
        ↓
Delivery Performance
        ↓
Customer Satisfaction
        ↓
Behavioral Seller Trends
        ↓
Streaming Risk Detection
```

This creates:

# longitudinal seller intelligence

rather than:

# isolated operational reporting

which is significantly more advanced analytically.

---

# Gold Layer Readiness

The dataset is specifically designed to support:

```text id="b4m8ry"
fct_seller_performance
```

inside the Gold analytical layer.

The staging structure ensures:

- clean seller-month grain
- trusted behavioral metrics
- validated temporal aggregation
- streaming-readiness
- KPI-safe analytical enrichment

for downstream:

- dbt modeling
- Power BI dashboards
- seller performance analytics
- real-time risk detection
- operational intelligence reporting.

```

```
