# Seller Performance Mart

## Overview

The Seller Performance Mart is a business-oriented analytical mart designed to consolidate historical seller performance indicators into a single trusted dataset for performance monitoring, risk assessment, seller ranking, and future real-time scoring applications.

The mart transforms operational KPIs into a standardized seller health score that enables business users to quickly identify high-performing sellers, monitor performance deterioration, and prioritize intervention efforts.

---

# Business Objective

The Seller Performance Mart answers the following business questions:

- Which sellers consistently deliver strong customer experiences?
- Which sellers are exhibiting early warning signs of performance decline?
- Which sellers require operational intervention?
- How does seller performance evolve over time?
- Which sellers should be prioritized for growth initiatives?
- Which sellers represent operational or customer satisfaction risks?

The mart serves as the analytical foundation for:

- Executive Performance Dashboards
- Seller Performance Monitoring
- Operational Risk Management
- Seller Ranking Programs
- Future Real-Time Seller Risk Engine

---

# Dataset Grain

**One Row = One Seller Per Month**

Each record represents a monthly performance snapshot for a specific seller.

Example:

| Seller   | Year | Month |
| -------- | ---- | ----- |
| Seller A | 2018 | 01    |
| Seller A | 2018 | 02    |
| Seller B | 2018 | 01    |

This grain enables historical trend analysis and month-over-month performance monitoring.

---

# Source Datasets

The Seller Performance Mart is built from:

### Silver Layer

- seller_performance_monthly_staging

### Gold Layer

- dim_seller

---

# Key Metrics

## Delivery Performance

| Metric               | Description                            |
| -------------------- | -------------------------------------- |
| monthly_orders       | Total seller orders during the month   |
| avg_shipping_days    | Average delivery duration              |
| on_time_rate         | Percentage of orders delivered on time |
| avg_delay_days       | Average delivery delay                 |
| delayed_orders_count | Number of delayed orders               |

---

## Customer Satisfaction

| Metric               | Description                    |
| -------------------- | ------------------------------ |
| avg_review_score     | Average customer rating        |
| negative_review_rate | Percentage of negative reviews |
| monthly_review_count | Total reviews received         |

---

## Fulfillment Performance

| Metric                 | Description                     |
| ---------------------- | ------------------------------- |
| avg_monthly_workload   | Average monthly seller workload |
| avg_freight_ratio      | Freight cost efficiency         |
| avg_product_volume_cm3 | Average product volume handled  |

---

## Growth Metrics

| Metric                 | Description                   |
| ---------------------- | ----------------------------- |
| previous_month_orders  | Previous month order count    |
| volume_growth_rate     | Month-over-month order growth |
| seller_growth_category | Seller growth classification  |

---

# Seller Health Score Framework

The Seller Health Score transforms multiple operational KPIs into a standardized score ranging from 0 to 100.

The objective is to create a single, interpretable indicator representing overall seller health.

---

# Score Components

## 1. Delivery Performance Component (40%)

Delivery performance is the most important factor because it directly impacts customer satisfaction and operational reliability.

Formula:

```text
on_time_component = on_time_rate × 100
```

Weight:

```text
40%
```

Rationale:

- Delivery reliability is a core marketplace KPI.
- Late deliveries negatively affect reviews and repeat purchases.
- Historical analysis shows delivery performance is a leading indicator of seller quality.

---

## 2. Customer Satisfaction Component (30%)

Customer reviews represent direct customer feedback.

Formula:

```text
review_component =
(avg_review_score ÷ 5) × 100
```

Weight:

```text
30%
```

Rationale:

- Reviews capture customer perception.
- Customer sentiment reflects both operational quality and product quality.
- Reviews complement delivery metrics by measuring experience rather than execution.

---

## 3. Growth Component (20%)

Growth measures business momentum.

Growth Categories:

| Category        | Score |
| --------------- | ----- |
| High Growth     | 100   |
| Moderate Growth | 80    |
| Stable          | 60    |
| Declining       | 30    |
| New Seller      | 50    |

Weight:

```text
20%
```

Rationale:

- Growth reflects seller business development.
- Growing sellers contribute more marketplace value.
- Declining sellers may indicate emerging operational issues.
- New sellers receive a neutral score due to limited history.

---

## 4. Workload Health Component (10%)

Workload evaluates seller operational capacity.

Workload Categories:

| Average Monthly Workload | Score |
| ------------------------ | ----- |
| ≥ 20 Orders              | 100   |
| 10–19 Orders             | 80    |
| 5–9 Orders               | 60    |
| < 5 Orders               | 40    |

Weight:

```text
10%
```

Rationale:

- Consistent operational volume demonstrates seller stability.
- Higher volumes indicate operational maturity.
- Workload receives the lowest weight because volume alone does not guarantee quality.

---

# Seller Health Score Formula

```text
Seller Score =
(On-Time Component × 0.40)
+
(Review Component × 0.30)
+
(Growth Component × 0.20)
+
(Workload Component × 0.10)
```

Score Range:

```text
0 – 100
```

---

# Seller Risk Classification

The seller score is translated into actionable business risk levels.

| Score Range | Risk Level |
| ----------- | ---------- |
| 85 – 100    | Healthy    |
| 70 – 84     | Warning    |
| 50 – 69     | At Risk    |
| Below 50    | Critical   |

---

# Seller Ranking Framework

The mart also assigns seller tiers to support ranking and segmentation initiatives.

| Score Range | Tier                   |
| ----------- | ---------------------- |
| 90 – 100    | Elite Seller           |
| 80 – 89     | Top Seller             |
| 65 – 79     | Standard Seller        |
| Below 65    | Underperforming Seller |

---

# Current Distribution

| Risk Level | Percentage |
| ---------- | ---------- |
| Healthy    | ~30%       |
| Warning    | ~43%       |
| At Risk    | ~9%        |
| Critical   | ~18%       |

This distribution provides meaningful segmentation and prevents excessive concentration within a single category.

---

# Business Value

The Seller Performance Mart provides:

- Unified seller performance measurement
- Early risk detection
- Seller ranking and segmentation
- Historical trend analysis
- Executive KPI reporting
- Operational intervention prioritization
- Foundation for future real-time monitoring

---

# Future Enhancements

### Score Engine V2

Potential future improvements include:

- Dynamic KPI weighting
- Seasonal performance normalization
- Category-specific benchmarks
- Machine learning-based seller scoring
- Real-time Kafka-driven score updates
- Automated seller risk alerts

These enhancements can be layered on top of the current framework without changing the underlying warehouse architecture.

---

# Output Dataset

**Dataset Name**

```text
seller_performance_mart
```

**Storage Layer**

```text
Gold Mart Layer
```

**Grain**

```text
One Row = One Seller Per Month
```

**Primary Purpose**

```text
Seller Intelligence, Risk Monitoring,
Performance Management, and Future
Real-Time Scoring Enablement
```
