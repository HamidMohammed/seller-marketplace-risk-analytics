# fct_customer_reviews

## Overview

The `fct_customer_reviews` fact table captures customer satisfaction outcomes across the Olist marketplace.

The fact serves as the Voice of Customer layer within the Olist Seller Intelligence Platform and provides the final outcome measurement of the seller lifecycle.

This fact enables analysis of customer sentiment, review behavior, delivery satisfaction, and the relationship between operational performance and customer experience.

---

# Business Purpose

The primary purpose of `fct_customer_reviews` is to measure customer satisfaction and evaluate how seller operations and delivery performance impact customer perception.

The fact supports analysis of:

- Customer satisfaction
- Review sentiment
- Delivery-related complaints
- Seller reputation
- Delivery experience quality
- Customer feedback trends
- Operational impact on satisfaction

---

# Fact Details

## Fact Name

```text
fct_customer_reviews
```

## Layer

```text
Gold
```

## Grain

```text
ONE ROW = ONE CUSTOMER REVIEW
```

Each record represents a single customer review associated with a completed order.

---

# Source

## Primary Source

```text
reviews_staging
```

The staging dataset combines:

- Customer reviews
- Seller attribution
- Delivery performance metrics
- Delivery experience classifications
- Customer sentiment classifications

---

# Dimensions

## Seller Dimension

Relationship:

```text
fct_customer_reviews.seller_sk_fk
=
dim_seller.seller_sk
```

Supports:

- Seller reputation analysis
- Acquisition-to-satisfaction analysis
- Seller quality monitoring

---

## Date Dimension

Relationships:

```text
review_date_sk
response_date_sk
```

Supports:

- Daily review trends
- Monthly satisfaction trends
- Seasonal sentiment analysis
- Customer feedback monitoring

---

# Business Measures

## Satisfaction Metrics

| Measure                | Description                        |
| ---------------------- | ---------------------------------- |
| review_score           | Customer rating (1–5)              |
| review_response_days   | Time taken to respond to review    |
| delivery_duration_days | Delivery duration                  |
| delay_days             | Delivery delay relative to promise |

---

# Business Flags

## Positive Review Flag

```text
positive_review_flag = True
```

Review score represents positive customer satisfaction.

---

## Negative Review Flag

```text
negative_review_flag = True
```

Review score represents customer dissatisfaction.

---

## Neutral Review Flag

```text
neutral_review_flag = True
```

Review score represents a neutral customer experience.

---

## Delayed Delivery Review Flag

```text
delayed_delivery_review_flag = True
```

Negative review associated with delayed delivery.

Used to quantify logistics-driven dissatisfaction.

---

## Low Rating Flag

```text
low_rating_flag = True
```

Review score ≤ 2.

Used for customer risk monitoring.

---

## Excellent Rating Flag

```text
excellent_rating_flag = True
```

Review score = 5.

Used for customer delight analysis.

---

# Delivery Experience Segments

| Segment             | Description                       |
| ------------------- | --------------------------------- |
| Successful Delivery | Positive delivery experience      |
| Mixed Experience    | Moderate delivery outcome         |
| Complex Fulfillment | Multi-seller or complex logistics |
| Delivery Failure    | Delivery-related dissatisfaction  |

These segments provide business-friendly customer experience categories.

---

# Data Quality Assessment

## Fact Grain Validation

| Validation                        | Result |
| --------------------------------- | ------ |
| Duplicate Review Grain Violations | 0      |
| Duplicate Fact SK                 | 0      |

The fact successfully maintains one row per customer review.

---

## Foreign Key Validation

| Foreign Key      | Null Count |
| ---------------- | ---------- |
| review_date_sk   | 0          |
| response_date_sk | 0          |
| seller_sk_fk     | 759        |

---

## Seller Key Investigation

A total of 759 reviews could not be linked to a Seller Dimension record.

### Root Cause

Investigation revealed that the same records also appear as:

```text
distance_bucket = Unknown
```

These reviews originate from orders that could not be reliably attributed to a seller.

This condition already exists within the delivery process and therefore propagates naturally into customer review analytics.

### Business Impact

| Metric                     | Value  |
| -------------------------- | ------ |
| Total Reviews              | 99,224 |
| Missing Seller Attribution | 759    |
| Impact Rate                | 0.76%  |

The impact is minimal and does not materially affect reporting quality.

The records are retained to preserve customer feedback completeness.

---

# Review Quality Validation

| Validation                          | Result |
| ----------------------------------- | ------ |
| Invalid Review Scores               | 0      |
| Negative Response Days              | 0      |
| Negative Delivery Duration          | 0      |
| Inconsistent Negative Flags         | 0      |
| Inconsistent Positive Flags         | 0      |
| Inconsistent Low Rating Flags       | 0      |
| Inconsistent Excellent Rating Flags | 0      |

All review metrics and derived KPIs passed validation successfully.

---

# Sentiment Distribution

| Sentiment | Reviews |
| --------- | ------- |
| Positive  | 76,470  |
| Neutral   | 8,179   |
| Negative  | 14,575  |

### Key Observation

Customer satisfaction is overwhelmingly positive.

Approximately:

```text
77.1%
```

of all reviews are positive.

This suggests strong marketplace performance and effective delivery execution.

---

# Delivery Experience Distribution

| Segment             | Reviews |
| ------------------- | ------- |
| Successful Delivery | 74,335  |
| Mixed Experience    | 20,122  |
| Delivery Failure    | 4,000   |
| Complex Fulfillment | 767     |

### Key Observation

Most customers experience successful deliveries, while only a small fraction report delivery failures.

This reinforces the strong operational performance observed in delivery analytics.

---

# Delivery Complaint Analysis

| KPI                               | Value |
| --------------------------------- | ----- |
| Delayed Delivery Negative Reviews | 4,000 |

### Key Observation

A substantial portion of negative reviews can be directly linked to delayed deliveries.

This provides strong evidence that delivery performance significantly influences customer satisfaction.

This relationship is one of the most important analytical findings within the project.

---

# Distance Analysis

| Distance Bucket | Reviews |
| --------------- | ------- |
| Cross Region    | 39,470  |
| Same State      | 35,393  |
| Same Region     | 23,602  |
| Unknown         | 759     |

### Key Observation

A large proportion of reviews are associated with cross-region deliveries.

This highlights the complexity of the Brazilian logistics network and its influence on customer experience.

---

# KPI Summary

| KPI                         | Value  |
| --------------------------- | ------ |
| Total Reviews               | 99,224 |
| Positive Reviews            | 76,470 |
| Negative Reviews            | 14,575 |
| Excellent Ratings           | 57,328 |
| Delayed Delivery Complaints | 4,000  |

---

# Analytical Use Cases

## Customer Satisfaction Analysis

Examples:

- Customer satisfaction trends
- Positive versus negative review analysis
- Customer sentiment monitoring

---

## Seller Reputation Analysis

Examples:

- Seller review rankings
- Negative review concentration
- Seller satisfaction benchmarking

---

## Delivery Impact Analysis

Examples:

- Delayed delivery impact on ratings
- Delivery duration versus review score
- Delivery experience segmentation

---

## Acquisition Performance Analysis

Examples:

- Marketing origin versus customer satisfaction
- Acquisition channel quality
- Seller acquisition effectiveness

Using:

```text
fct_customer_reviews
        ↓
seller_sk_fk
        ↓
dim_seller
        ↓
marketing_origin
```

the platform can evaluate which acquisition channels produce the highest customer satisfaction outcomes.

---

# Power BI Usage

Recommended slicers:

- Sentiment Category
- Delivery Experience Segment
- Distance Bucket
- Seller Region
- Marketing Origin

Recommended visuals:

- Customer Satisfaction KPI Cards
- Review Sentiment Trends
- Delivery Failure Analysis
- Seller Satisfaction Rankings
- Acquisition-to-Satisfaction Analysis

---

# Architecture Position

```text
Bronze
    ↓
Silver Reviews
Silver Orders
Silver Delivery Staging
    ↓
Reviews Staging
    ↓
fct_customer_reviews
    ↓
Customer Experience Mart
    ↓
Power BI
```

---

# Business Storytelling Value

This fact table completes the seller lifecycle narrative.

```text
Marketing Acquisition
        ↓
Seller Onboarding
        ↓
Seller Fulfillment
        ↓
Order Delivery
        ↓
Customer Satisfaction
```

The fact provides the final outcome measurement of marketplace success.

It allows the platform to connect operational performance directly to customer experience and business value.

---

# Summary

`fct_customer_reviews` is the Voice of Customer fact table of the Olist Seller Intelligence Platform.

It delivers trusted, validated, and business-focused customer satisfaction intelligence that enables sentiment analysis, seller reputation monitoring, delivery impact assessment, and end-to-end seller lifecycle storytelling.
