# fct_order_delivery

## Overview

The `fct_order_delivery` fact table serves as the core operational fact table of the Olist Seller Intelligence Platform.

The fact captures the complete delivery lifecycle of customer orders and provides the foundation for delivery performance analytics, logistics monitoring, seller accountability reporting, and customer experience analysis.

This fact table is the central component of the Delivery Performance Mart.

---

# Business Purpose

The primary purpose of `fct_order_delivery` is to measure how efficiently customer orders move through the delivery process.

The fact supports analysis of:

- Delivery performance
- On-time delivery rates
- Late delivery trends
- Freight costs
- Multi-seller complexity
- Geographic delivery patterns
- Seller accountability
- Customer delivery experience

---

# Fact Details

## Fact Name

```text
fct_order_delivery
```

## Layer

```text
Gold
```

## Grain

```text
ONE ROW = ONE CUSTOMER ORDER
```

Each record represents a single customer order and its associated delivery outcome.

---

# Source

## Primary Source

```text
order_delivery_staging
```

The fact is built from the Silver Layer delivery staging dataset.

The staging layer combines:

- Order lifecycle events
- Aggregated order item metrics
- Seller enrichment
- Customer enrichment
- Delivery performance metrics

---

# Dimensions

## Customer Dimension

Relationship:

```text
fct_order_delivery.customer_sk_fk
=
dim_customer.customer_sk
```

Supports:

- Geographic analysis
- Regional delivery performance
- Customer segmentation

---

## Seller Dimension

Relationship:

```text
fct_order_delivery.seller_sk_fk
=
dim_seller.seller_sk
```

Supports:

- Seller accountability
- Seller delivery performance
- Seller operational analysis

---

## Date Dimension

Relationships:

```text
purchase_date_sk
estimated_delivery_date_sk
actual_delivery_date_sk
```

Supports:

- Time-series analysis
- Monthly trends
- Seasonal reporting
- Delivery forecasting

---

# Business Measures

## Delivery Metrics

| Measure                | Description                         |
| ---------------------- | ----------------------------------- |
| delivery_duration_days | Total delivery duration             |
| delay_days             | Delivery delay relative to estimate |
| buffer_days            | Estimated delivery buffer           |
| freight_total_value    | Total freight cost                  |
| total_items_count      | Number of items in order            |
| seller_count           | Number of sellers in order          |

---

# Business Flags

## On-Time Delivery Flag

```text
True
```

Order delivered on or before the promised delivery date.

---

## Late Delivery Flag

```text
True
```

Order delivered after the promised delivery date.

---

## Multi Seller Order Flag

```text
True
```

Order contains products from multiple sellers.

These orders typically involve increased logistical complexity.

---

# Data Quality Assessment

## Fact Grain Validation

| Validation        | Result |
| ----------------- | ------ |
| Duplicate Orders  | 0      |
| Duplicate Fact SK | 0      |

The fact table successfully maintains the intended grain of one row per customer order.

---

## Foreign Key Validation

| Foreign Key                | Null Count |
| -------------------------- | ---------- |
| customer_sk_fk             | 0          |
| purchase_date_sk           | 0          |
| estimated_delivery_date_sk | 0          |
| actual_delivery_date_sk    | 0          |
| seller_sk_fk               | 775        |

---

## Seller Key Investigation

A total of 775 records were missing a seller surrogate key.

### Root Cause

Investigation revealed that these orders also appear within the staging layer as:

```text
distance_bucket = Unknown
```

The missing seller keys originate from orders that could not be associated with a seller during order item aggregation.

These are not warehouse processing failures.

They represent legitimate source-system records with incomplete seller attribution.

### Business Impact

| Metric                            | Value  |
| --------------------------------- | ------ |
| Total Orders                      | 99,441 |
| Orders Missing Seller Attribution | 775    |
| Impact Rate                       | 0.78%  |

The impact is considered minimal and does not materially affect analytical reporting.

The records are retained to preserve data completeness.

---

# Delivery Performance Validation

| Validation                 | Result |
| -------------------------- | ------ |
| Negative Delivery Duration | 0      |
| Negative Freight Values    | 0      |
| Invalid Item Counts        | 0      |
| Invalid Seller Counts      | 0      |
| Inconsistent On-Time Flags | 0      |
| Inconsistent Late Flags    | 0      |

All delivery metrics passed validation successfully.

---

# Delivery Status Distribution

| Delivery Status | Orders |
| --------------- | ------ |
| Early           | 87,309 |
| Late            | 6,511  |
| On Time         | 1,283  |
| Unknown         | 2,948  |

### Key Observation

The Olist platform frequently provided conservative delivery estimates.

As a result, the vast majority of orders arrived earlier than the estimated delivery date.

This creates a strong customer experience outcome and contributes positively to customer satisfaction metrics.

---

# Distance Analysis

| Distance Bucket | Orders |
| --------------- | ------ |
| Cross Region    | 36,742 |
| Same State      | 34,941 |
| Same Region     | 25,593 |
| Unknown         | 775    |

### Key Observation

A significant proportion of deliveries occur across regional boundaries.

This highlights the complexity of Brazil's nationwide logistics network and demonstrates the importance of delivery performance monitoring.

---

# Delivery KPI Summary

| KPI                  | Value  |
| -------------------- | ------ |
| Total Orders         | 99,441 |
| On-Time Orders       | 88,592 |
| Late Orders          | 6,511  |
| Multi-Seller Orders  | 1,226  |
| Single-Seller Orders | 96,050 |

### On-Time Delivery Rate

```text
89.1%
```

### Late Delivery Rate

```text
6.5%
```

### Multi-Seller Order Rate

```text
1.23%
```

---

# Analytical Use Cases

## Seller Performance Analysis

Examples:

- Sellers with highest late delivery rates
- Delivery performance by seller region
- Seller fulfillment effectiveness

---

## Logistics Analysis

Examples:

- Freight cost analysis
- Delivery duration trends
- Geographic delivery performance

---

## Customer Experience Analysis

Examples:

- Delivery performance vs review score
- Delayed delivery impact on sentiment
- Delivery satisfaction monitoring

---

## Executive KPI Dashboard

Examples:

- On-time delivery rate
- Average delivery duration
- Late delivery trends
- Delivery volume trends

---

# Power BI Usage

Recommended slicers:

- Seller Region
- Customer Region
- Distance Bucket
- Delivery Status
- Multi-Seller Flag

Recommended visuals:

- Delivery KPI cards
- Delivery trend analysis
- Regional performance maps
- Seller performance rankings
- Logistics performance dashboards

---

# Architecture Position

```text
Bronze
    ↓
Silver Orders
Silver Order Items
Silver Customers
Silver Sellers
    ↓
Order Delivery Staging
    ↓
fct_order_delivery
    ↓
Delivery Performance Mart
    ↓
Power BI
```

---

# Summary

`fct_order_delivery` is the core operational fact table of the Olist Seller Intelligence Platform.

The fact provides a trusted and validated source of delivery intelligence, enabling detailed analysis of logistics performance, seller accountability, customer experience, and operational efficiency across the marketplace.
