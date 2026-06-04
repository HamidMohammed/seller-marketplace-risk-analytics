# Seller Score Engine

## Project

Olist Seller Intelligence Platform

## Document Type

Business Rules & Scoring Framework

---

# Objective

The Seller Score Engine provides a standardized framework for evaluating seller operational health using historical performance indicators.

The objective is to transform multiple operational KPIs into a single interpretable score that supports:

- Seller performance monitoring
- Operational risk identification
- Seller ranking
- Executive reporting
- Future streaming risk enrichment

The score is designed to be:

- Explainable
- Auditable
- Business-friendly
- Suitable for dashboard consumption

---

# Score Output

The Seller Score Engine produces:

| Metric               | Description                       |
| -------------------- | --------------------------------- |
| seller_health_score  | Standardized score from 0–100     |
| performance_category | Seller performance classification |
| score_date           | Snapshot date                     |

---

# Score Components

The Seller Health Score is composed of four weighted components.

| Component             | Weight |
| --------------------- | ------ |
| Delivery Performance  | 40%    |
| Customer Satisfaction | 30%    |
| Growth Performance    | 20%    |
| Workload Health       | 10%    |

Total Weight:

```text
100%
```

---

# Component 1 — Delivery Performance

## Metric

```text
on_time_rate
```

## Calculation

```text
delivery_component =
on_time_rate × 100
```

## Weight

```text
40%
```

## Business Justification

Delivery reliability is the most important operational KPI because it directly impacts customer experience, seller reputation, and marketplace trust.

---

# Component 2 — Customer Satisfaction

## Metric

```text
avg_review_score
```

## Calculation

```text
review_component =
(avg_review_score / 5) × 100
```

## Weight

```text
30%
```

## Business Justification

Customer reviews represent direct customer feedback and provide a strong indicator of overall seller quality.

---

# Component 3 — Growth Performance

## Metric

```text
seller_growth_category
```

## Scoring Logic

| Growth Category | Score |
| --------------- | ----- |
| High Growth     | 100   |
| Moderate Growth | 80    |
| Stable          | 60    |
| Declining       | 30    |
| New Seller      | 50    |

## Weight

```text
20%
```

## Business Justification

Growth reflects business momentum and marketplace contribution.

---

# Component 4 — Workload Health

## Metric

```text
avg_monthly_workload
```

## Scoring Logic

| Monthly Orders | Score |
| -------------- | ----- |
| ≥ 20           | 100   |
| 10–19          | 80    |
| 5–9            | 60    |
| < 5            | 40    |

## Weight

```text
10%
```

## Business Justification

Sustained operational volume indicates seller maturity and operational stability.

---

# Seller Health Score Formula

```text
Seller Health Score =
(Delivery Component × 0.40)
+
(Review Component × 0.30)
+
(Growth Component × 0.20)
+
(Workload Component × 0.10)
```

---

# Performance Categories

| Score Range | Category  |
| ----------- | --------- |
| 90–100      | Elite     |
| 75–89       | Healthy   |
| 60–74       | Watchlist |
| 0–59        | At Risk   |

---

# Example Calculation

Seller Metrics:

```text
On-Time Rate        = 95%
Average Review      = 4.5
Growth Category     = Moderate Growth
Monthly Workload    = 15 Orders
```

Component Scores:

```text
Delivery Component  = 95
Review Component    = 90
Growth Component    = 80
Workload Component  = 80
```

Final Score:

```text
(95 × 0.40)
+
(90 × 0.30)
+
(80 × 0.20)
+
(80 × 0.10)

= 89
```

Performance Category:

```text
Healthy
```

---

# Business Usage

The Seller Score Engine supports:

- Seller ranking dashboards
- Performance monitoring
- Risk prioritization
- Operational intervention planning
- Executive performance reporting

---

# Future Enhancements (V2)

Future versions may introduce:

- Dynamic weighting
- Seasonal baselines
- Machine learning scoring models
- Real-time Kafka score adjustments
- Predictive seller risk scoring

Version 1 intentionally remains rule-based to ensure transparency, explainability, and business trust.
