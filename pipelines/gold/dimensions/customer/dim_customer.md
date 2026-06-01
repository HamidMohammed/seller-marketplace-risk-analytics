# dim_customer

## Overview

The `dim_customer` dimension provides a unified Customer 360 view for the Olist Seller Intelligence Platform.

This dimension centralizes customer geographic and location intelligence, enabling analysis of customer distribution, delivery performance by region, customer satisfaction trends, and future customer-centric analytics.

The dimension is designed as a conformed dimension and serves as a reusable business entity across multiple Gold Layer fact tables.

---

# Business Purpose

The primary purpose of `dim_customer` is to provide geographic context for marketplace activity.

While the project focuses primarily on seller intelligence, customer geography plays an important role in:

- Delivery performance analysis
- Review and satisfaction analysis
- Regional demand analysis
- Logistics intelligence
- Future sales and revenue analysis

This dimension allows business users to understand where customers are located and how geography influences marketplace outcomes.

---

# Dimension Details

## Dimension Name

```text
dim_customer
```

## Layer

```text
Gold
```

## Grain

```text
ONE ROW = ONE CUSTOMER
```

Each record represents a unique customer identifier from the Olist marketplace.

---

# Data Sources

## Primary Source

```text
silver_customers
```

### Source Fields

- customer_id
- customer_unique_id
- customer_zip_code_prefix
- customer_city
- customer_state
- median_latitude
- median_longitude

---

# Business Enrichments

The dimension extends raw customer information through additional business classifications.

## Customer Region

Customers are assigned to one of Brazil's major geographic regions.

### Regions

- Southeast
- South
- Central-West
- Northeast
- North
- Unknown

### Business Value

Supports:

- Regional sales analysis
- Delivery performance analysis
- Geographic segmentation
- Customer distribution reporting

---

## Customer Location Type

Customers are classified into location categories.

### Categories

#### Metropolitan

Major Brazilian metropolitan areas such as:

- São Paulo
- Rio de Janeiro
- Brasília
- Salvador
- Fortaleza
- Belo Horizonte
- Curitiba
- Manaus
- Recife
- Porto Alegre

#### Urban

Customers located within major commercial states.

#### Regional

Customers located outside metropolitan and major urban areas.

### Business Value

Supports:

- Urban vs regional demand analysis
- Delivery complexity analysis
- Logistics segmentation

---

# Surrogate Key Strategy

## Customer Surrogate Key

```text
customer_sk
```

Generated using:

```text
ROW_NUMBER()
```

Purpose:

- Warehouse optimization
- Fact table integration
- Dimensional modeling best practices

---

# Attributes

| Column                   | Description                     |
| ------------------------ | ------------------------------- |
| customer_sk              | Customer surrogate key          |
| customer_id              | Customer business key           |
| customer_unique_id       | Unique customer identifier      |
| customer_zip_code_prefix | Customer ZIP prefix             |
| customer_city            | Customer city                   |
| customer_state           | Customer state                  |
| customer_region          | Derived geographic region       |
| customer_location_type   | Derived location classification |
| median_latitude          | Geographic latitude             |
| median_longitude         | Geographic longitude            |
| source_system            | Source system identifier        |
| transformation_version   | ETL version                     |
| gold_loaded_at           | Gold layer load timestamp       |

---

# Relationships

## Fact Tables

### fct_order_delivery

Relationship:

```text
dim_customer.customer_id
=
fct_order_delivery.customer_id
```

Used for:

- Delivery performance by region
- Customer delivery analytics

---

### fct_reviews (Future)

Relationship:

```text
dim_customer.customer_id
=
fct_reviews.customer_id
```

Used for:

- Customer satisfaction by region
- Sentiment analysis

---

### fct_sales (Future)

Relationship:

```text
dim_customer.customer_id
=
fct_sales.customer_id
```

Used for:

- Revenue by geography
- Customer value analysis

---

# Data Quality Rules

## Customer Grain Validation

Rule:

```text
ONE ROW = ONE CUSTOMER
```

Validation:

```text
Duplicate customer_id count = 0
```

---

## Surrogate Key Validation

Rule:

```text
customer_sk must be unique
```

Validation:

```text
Duplicate customer_sk count = 0
```

---

## Geographic Validation

Rule:

```text
customer_region must be populated
```

Validation:

```text
Unknown region count monitored
```

---

## Coordinate Validation

Rule:

```text
Latitude and longitude should exist whenever available.
```

Validation:

```text
Missing coordinate count monitored.
```

---

# Analytical Use Cases

## Delivery Intelligence

Examples:

- On-time delivery by region
- Late deliveries by state
- Regional logistics analysis

---

## Customer Satisfaction

Examples:

- Average review score by region
- Negative review concentration
- Customer sentiment distribution

---

## Geographic Reporting

Examples:

- Customer distribution map
- Customer concentration by state
- Regional marketplace penetration

---

# Power BI Usage

Recommended slicers:

- Customer Region
- Customer State
- Customer City
- Customer Location Type

Recommended visuals:

- Regional maps
- Customer distribution charts
- Delivery performance heatmaps
- Satisfaction by geography dashboards

---

# Architecture Position

```text
Bronze
    ↓
silver_customers
    ↓
dim_customer
    ↓
Order Delivery Mart
Reviews Mart
Sales Mart
Power BI
```

The dimension acts as the central customer geography reference for the Gold Layer.

---

# Design Decision

This dimension intentionally does not implement Slowly Changing Dimension (SCD) logic.

Reason:

- Customer records are primarily geographic identifiers.
- The Olist dataset does not provide meaningful customer profile history.
- SCD implementation would add complexity without significant analytical value.

The dimension therefore follows a simple Type 1 dimensional modeling approach.

---

# Summary

`dim_customer` provides a reusable Customer 360 dimension that enriches customer records with geographic intelligence and supports delivery, review, and future sales analytics.

The dimension serves as the authoritative customer reference for the Olist Seller Intelligence Platform and enables customer-focused analysis across all Gold Layer marts.

# Data Quality Assessment

## Customer Data Completeness

The customer dimension demonstrates a high level of data completeness across all critical business attributes.

### Critical Attribute Validation

| Attribute          | Status   |
| ------------------ | -------- |
| customer_id        | Complete |
| customer_unique_id | Complete |
| customer_city      | Complete |
| customer_state     | Complete |
| customer_region    | Complete |
| customer_sk        | Complete |

No critical business identifiers or geographic classifications were missing during dimension construction.

---

## Geographic Coordinate Coverage

Customer geographic coordinates were enriched using ZIP-prefix-based geolocation reference data.

### Validation Results

| Metric                        | Value  |
| ----------------------------- | ------ |
| Total Customers               | 99,441 |
| Customers Missing Coordinates | 278    |
| Coordinate Coverage           | 99.72% |

### Analysis

Investigation of missing coordinate records revealed that customer location information remained available for all affected customers.

The missing values were limited to:

- median_latitude
- median_longitude

while the following attributes remained populated:

- customer_city
- customer_state
- customer_region

### Root Cause

The issue was traced to incomplete ZIP-prefix coverage within the geolocation reference dataset used during Silver Layer enrichment.

The customer master data itself was complete.

### State Distribution of Missing Coordinates

A significant concentration of missing coordinates was observed within Distrito Federal (DF).

| State  | Missing Coordinates |
| ------ | ------------------- |
| DF     | 171                 |
| SP     | 15                  |
| RJ     | 13                  |
| MG     | 11                  |
| PR     | 11                  |
| Others | 57                  |

Distrito Federal accounted for approximately 61.5% of all missing coordinate records.

### Business Impact Assessment

The missing coordinate rate represents only:

0.28% of the customer population.

Because city, state, and regional classifications remain available, analytical reporting is not materially affected.

The following analyses remain fully supported:

- Regional delivery analysis
- Customer geographic segmentation
- Customer satisfaction by region
- State-level reporting
- Power BI geographic dashboards

Only highly precise latitude/longitude-based mapping may be impacted for a small subset of customers.

### Resolution Strategy

No corrective action was applied.

The records were retained because:

- Customer business keys remain valid.
- Geographic hierarchy remains available.
- Data loss would provide no analytical benefit.
- Coverage exceeds industry expectations for geospatial enrichment.

### Conclusion

The customer dimension achieved a geographic enrichment coverage rate of 99.72%.

The remaining coordinate gaps are attributable to limitations in the external geolocation reference dataset rather than customer data quality issues and do not materially impact analytical outcomes.
