# System Architecture

## Olist Seller Intelligence Platform

---

# 1. Overview

The Olist Seller Intelligence Platform is an end-to-end Data Engineering solution designed to transform raw e-commerce data into trusted analytical assets for business intelligence, operational monitoring, and seller performance evaluation.

The platform follows a modern Medallion Architecture consisting of Bronze, Silver, and Gold layers, supported by distributed data processing using Apache Spark and cloud-native object storage using MinIO.

The primary objective is to provide scalable, reliable, and business-ready datasets for reporting, analytics, and decision support.

---

# 2. Architecture Principles

The platform was designed according to the following principles:

- Layered Data Architecture
- Data Quality Enforcement
- Separation of Concerns
- Scalability
- Reproducibility
- Containerized Infrastructure
- Business-Oriented Data Modeling
- Kimball Dimensional Modeling

---

# 3. High-Level Architecture

```text
Raw Data Sources
        |
        v
Bronze Layer (MinIO)
        |
        v
Silver Layer (MinIO)
        |
        v
Gold Layer (MinIO)
        |
        v
PostgreSQL Data Warehouse
        |
        v
Power BI Dashboards
```

---

# 4. Raw Data Layer

## Purpose

Stores source datasets exactly as received from Olist.

## Characteristics

- CSV format
- Immutable source records
- No transformations applied
- Single source of truth

## Datasets

- Orders
- Order Items
- Customers
- Sellers
- Products
- Payments
- Reviews
- Geolocation
- Marketing Qualified Leads
- Closed Deals
- Product Category Translation

---

# 5. Bronze Layer

## Purpose

Provides trusted ingestion storage while preserving source fidelity.

## Responsibilities

- Data ingestion
- Metadata enrichment
- Source tracking
- Landing zone storage

## Outputs

Parquet datasets stored in MinIO Bronze.

---

# 6. Silver Layer

## Purpose

Creates trusted, cleaned, and business-aligned datasets.

## Responsibilities

- Data cleansing
- Null handling
- Data standardization
- Business rule implementation
- Data quality validation

## Core Datasets

- silver_orders
- silver_customers
- silver_sellers
- silver_products
- silver_reviews
- silver_payments
- silver_order_items

## Staging Datasets

- order_delivery_staging
- seller_fulfillment_staging
- reviews_staging
- sales_staging
- seller_acquisition_staging
- seller_performance_monthly_staging

---

# 7. Gold Layer

## Purpose

Creates analytical data models optimized for reporting and business intelligence.

## Modeling Approach

Kimball Dimensional Modeling

---

## Dimensions

### dim_date

Central calendar dimension.

### dim_customer

Customer analytical attributes.

### dim_seller

Seller intelligence and acquisition attributes.

### dim_product

Product classification and category attributes.

---

## Fact Tables

### fct_order_delivery

Delivery performance metrics.

### fct_seller_fulfillment

Seller operational performance metrics.

### fct_customer_reviews

Customer satisfaction metrics.

### fct_order_sales

Sales and revenue metrics.

---

# 8. Data Mart Layer

## Seller Performance Mart

Provides seller performance scoring and ranking.

### Key Outputs

- Seller Score
- Risk Level
- Rank Tier
- Growth Classification

---

# 9. Warehouse Layer

## Technology

PostgreSQL

## Purpose

Serves as the analytical warehouse for reporting tools and dashboard consumption.

## Responsibilities

- Fact storage
- Dimension storage
- Data mart serving
- SQL analytics

---

# 10. Processing Layer

## Technology

Apache Spark

## Responsibilities

- Distributed processing
- ETL execution
- Data transformation
- Aggregation
- Validation

---

# 11. Storage Layer

## Technology

MinIO Object Storage

### Bronze Bucket

Raw trusted ingestion storage.

### Silver Bucket

Curated business-ready storage.

### Gold Bucket

Analytical storage.

---

# 12. Infrastructure Layer

## Containerization

Docker Compose

### Components

- MinIO
- PostgreSQL
- pgAdmin
- Spark Master
- Spark Worker

---

# 13. Orchestration Layer

## Master Pipeline

```text
run_pipeline.py

    ↓

Bronze Pipeline

    ↓

Silver Pipeline

    ↓

Gold Pipeline

    ↓

Warehouse Load
```

---

# 14. End-to-End Data Flow

```text
Raw CSV Files
        ↓
Bronze Layer
        ↓
Silver Layer
        ↓
Gold Layer
        ↓
PostgreSQL Warehouse
        ↓
Power BI Dashboards
```

---

# 15. Architecture Outcome

The platform delivers a scalable, containerized, enterprise-style data architecture capable of supporting operational reporting, seller intelligence analytics, performance monitoring, and future real-time extensions.
