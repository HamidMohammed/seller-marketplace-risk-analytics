# dim_product

## Overview

The `dim_product` dimension provides a unified Product 360 view for the Olist Seller Intelligence Platform.

This dimension centralizes product catalog information, physical product characteristics, logistics attributes, and product classifications used throughout the warehouse.

The dimension serves as a conformed product reference across fulfillment, delivery, sales, and customer satisfaction analytics.

---

# Business Purpose

The primary purpose of `dim_product` is to provide product intelligence that enables business users to understand how product characteristics influence operational performance.

The dimension supports analysis of:

- Seller fulfillment performance
- Delivery complexity
- Logistics optimization
- Product category trends
- Customer satisfaction by product type
- Future sales intelligence

Unlike raw product data, the dimension contains enriched business classifications that simplify analytical reporting and dashboard development.

---

# Dimension Details

## Dimension Name

```text
dim_product
```

## Layer

```text
Gold
```

## Grain

```text
ONE ROW = ONE PRODUCT
```

Each record represents a unique product offered within the Olist marketplace.

---

# Data Source

## Primary Source

```text
silver_products
```

The dimension is built from the trusted Silver Layer product dataset and inherits all product quality improvements, standardization rules, and business enrichments implemented during Silver processing.

---

# Product Catalog Attributes

## Product Identification

| Attribute  | Description           |
| ---------- | --------------------- |
| product_sk | Product surrogate key |
| product_id | Product business key  |

---

## Product Category

| Attribute                     | Description                  |
| ----------------------------- | ---------------------------- |
| product_category_name         | Original Portuguese category |
| product_category_name_english | Translated English category  |

### Business Value

Supports:

- Category analysis
- Product segmentation
- Product performance reporting
- Dashboard filtering

---

## Product Content Attributes

| Attribute                  | Description                |
| -------------------------- | -------------------------- |
| product_name_lenght        | Product name length        |
| product_description_lenght | Product description length |
| product_photos_qty         | Number of product photos   |

### Business Value

Supports product catalog quality analysis and future product completeness investigations.

---

# Logistics Attributes

## Physical Measurements

| Attribute          | Description               |
| ------------------ | ------------------------- |
| product_weight_g   | Product weight (grams)    |
| product_length_cm  | Product length            |
| product_height_cm  | Product height            |
| product_width_cm   | Product width             |
| product_volume_cm3 | Calculated product volume |

### Business Value

Physical characteristics are important drivers of:

- Delivery cost
- Freight cost
- Fulfillment complexity
- Logistics planning

---

# Product Classifications

## Product Size Category

Products are classified into operational size groups.

### Categories

- Small
- Medium
- Large
- Oversized

### Validation Results

| Size Category | Product Count |
| ------------- | ------------- |
| Medium        | 17,887        |
| Large         | 10,398        |
| Oversized     | 2,459         |
| Small         | 2,205         |

### Business Value

Supports:

- Logistics segmentation
- Warehouse planning
- Delivery performance analysis

---

## Heavy Product Flag

Identifies products with significant shipping weight.

### Validation Results

| Metric         | Value |
| -------------- | ----- |
| Heavy Products | 4,197 |

### Business Value

Supports:

- Freight analysis
- Delivery complexity analysis
- Fulfillment workload analysis

---

# Data Quality Attributes

## Logistics Completeness Flag

Indicates whether all required logistics attributes are available.

### Validation Results

| Metric                        | Value |
| ----------------------------- | ----- |
| Incomplete Logistics Profiles | 0     |

### Interpretation

All products contain sufficient logistics information for downstream delivery and fulfillment analytics.

---

## Catalog Completeness Flag

Indicates whether required catalog information is available.

### Validation Results

| Metric                      | Value |
| --------------------------- | ----- |
| Incomplete Catalog Profiles | 609   |

### Interpretation

A small subset of products contains incomplete catalog information.

These products remain analytically usable because logistics information remains complete.

---

# Data Quality Assessment

## Product Dimension Quality

### Grain Validation

| Validation            | Result |
| --------------------- | ------ |
| Duplicate Product IDs | 0      |
| Duplicate Product SKs | 0      |

### Critical Attribute Validation

| Attribute                     | Null Count |
| ----------------------------- | ---------- |
| product_sk                    | 0          |
| product_id                    | 0          |
| product_category_name_english | 0          |
| product_size_category         | 0          |

### Physical Attribute Validation

| Validation     | Result |
| -------------- | ------ |
| Missing Weight | 0      |
| Missing Volume | 0      |

### Assessment

The dimension achieved complete coverage for all logistics-critical attributes.

No data quality issues were identified that would materially impact fulfillment or delivery analytics.

---

# Product Category Analysis

The marketplace product catalog is concentrated around a small number of dominant categories.

### Top Categories

| Category        | Products |
| --------------- | -------- |
| bed_bath_table  | 3,029    |
| sports_leisure  | 2,867    |
| furniture_decor | 2,657    |
| health_beauty   | 2,444    |
| housewares      | 2,335    |

### Business Insight

The product catalog is heavily weighted toward:

- Home products
- Lifestyle products
- Health and beauty products
- Sports and leisure products

These categories are expected to drive a large proportion of operational activity.

---

# Relationships

## fct_seller_fulfillment

Relationship:

```text
dim_product.product_id
=
fct_seller_fulfillment.product_id
```

Supports:

- Product fulfillment analysis
- Seller specialization analysis
- Operational workload analysis

---

## Future Sales Mart

Relationship:

```text
dim_product.product_id
=
fct_sales.product_id
```

Supports:

- Revenue analysis
- Product performance analysis
- Category profitability

---

## Future Reviews Mart

Relationship:

```text
dim_product.product_id
=
fct_reviews.product_id
```

Supports:

- Product satisfaction analysis
- Product sentiment analysis

---

# Power BI Usage

Recommended slicers:

- Product Category
- Product Size Category
- Heavy Product Flag

Recommended visuals:

- Product category performance
- Product size distribution
- Fulfillment analysis by category
- Delivery performance by product type

---

# Architecture Position

```text
Bronze
    ↓
silver_products
    ↓
dim_product
    ↓
Seller Fulfillment Mart
Delivery Mart
Future Sales Mart
Future Review Mart
Power BI
```

The dimension acts as the central product intelligence reference for the Gold Layer.

---

# Design Decision

The dimension follows a Type 1 dimensional modeling strategy.

No Slowly Changing Dimension (SCD) implementation was required because product history is not tracked within the Olist dataset.

This simplifies maintenance while preserving analytical value.

---

# Summary

`dim_product` provides a trusted Product 360 dimension that combines product catalog information, logistics characteristics, and business classifications.

The dimension serves as the authoritative product reference across the Olist Seller Intelligence Platform and enables product-centric operational, fulfillment, delivery, and future sales analytics.
