# fct_order_sales

## Overview

The `fct_order_sales` fact table captures the commercial sales transactions of the Olist marketplace.

It represents the revenue-generating business process and serves as the primary source for sales, revenue, payment, product, seller, and customer analytics.

---

# Fact Details

## Fact Name

fct_order_sales

## Layer

Gold

## Grain

ONE ROW = ONE ORDER ITEM SOLD

Each record represents a single product sold within an order.

Natural Grain:

- order_id
- order_item_id

---

# Business Purpose

This fact enables analysis of:

- Revenue performance
- Product sales performance
- Seller sales performance
- Customer purchasing behavior
- Payment behavior
- Freight economics
- Acquisition-to-revenue analysis

---

# Source

Primary Source:

sales_staging

The staging dataset combines:

- Order item sales
- Payment allocation
- Product intelligence
- Seller attribution
- Customer attribution

---

# Dimensions

                dim_date
                    |
                    |

dim_product --- fct_order_sales --- dim_customer
|
|
dim_seller

## dim_product

Relationship:

fct_order_sales.product_sk_fk

→ dim_product.product_sk

Supports:

- Product analysis
- Category analysis
- Product profitability

---

## dim_seller

Relationship:

fct_order_sales.seller_sk_fk

→ dim_seller.seller_sk

Supports:

- Seller revenue analysis
- Acquisition performance analysis
- Seller productivity analysis

---

## dim_customer

Relationship:

fct_order_sales.customer_sk_fk

→ dim_customer.customer_sk

Supports:

- Customer geography analysis
- Regional sales analysis
- Customer purchasing trends

---

## dim_date

Relationship:

fct_order_sales.sales_date_sk

→ dim_date.date_sk

Date Source:

order_purchase_timestamp

Supports:

- Daily sales trends
- Monthly sales trends
- Seasonal analysis

---

# Measures

## Revenue Measures

| Measure                 | Description              |
| ----------------------- | ------------------------ |
| price                   | Product selling price    |
| freight_value           | Shipping charge          |
| gross_item_value        | Product price + freight  |
| total_order_item_value  | Total order value        |
| allocated_payment_value | Allocated payment amount |

---

## Payment Measures

| Measure                    | Description                    |
| -------------------------- | ------------------------------ |
| total_payment_installments | Installment count              |
| installment_flag           | Installment purchase indicator |

---

## Logistics Measures

| Measure                    | Description                    |
| -------------------------- | ------------------------------ |
| freight_ratio              | Freight cost percentage        |
| product_volume_cm3         | Product volume                 |
| seller_item_count_in_order | Seller item count within order |

---

# Derived Business Flags

## Installment Flag

True when:

total_payment_installments > 1

Used to analyze installment purchasing behavior.

---

## High Ticket Order Flag

True when:

gross_item_value >= 1000

Used to identify premium-value transactions.

---

## High Freight Item Flag

True when:

freight_ratio > 0.30

Used to identify logistics-intensive products.

---

# Data Quality Controls

## Fact Grain Validation

- Duplicate order item records
- Duplicate surrogate keys

---

## Foreign Key Validation

- product_sk_fk
- seller_sk_fk
- customer_sk_fk
- sales_date_sk

---

## Revenue Validation

- Negative prices
- Negative payments
- Negative order values

---

## Freight Validation

- Negative freight values
- Freight ratio monitoring

---

# Analytical Use Cases

## Revenue Analytics

Examples:

- Revenue by month
- Revenue by seller
- Revenue by category
- Revenue by region

---

## Product Analytics

Examples:

- Top selling products
- Product category performance
- Product profitability

---

## Seller Analytics

Examples:

- Seller revenue ranking
- Revenue by acquisition channel
- Seller contribution analysis

---

## Customer Analytics

Examples:

- Revenue by state
- Revenue by region
- Customer purchase trends

---

## Payment Analytics

Examples:

- Installment adoption
- High-ticket purchases
- Payment allocation analysis

---

# Power BI Usage

Recommended KPIs:

- Total Revenue
- Average Order Value
- Installment Adoption Rate
- High Ticket Sales
- Freight Cost Ratio

Recommended Visuals:

- Revenue Trend Line
- Top Seller Ranking
- Top Product Categories
- Customer Geography Map
- Acquisition Revenue Analysis

---

# Architecture Position

Bronze
↓
Silver Order Items
Silver Orders
Silver Payments
↓
Sales Staging
↓
fct_order_sales
↓
Sales Mart
↓
Power BI

---

# Business Storytelling Value

This fact introduces the commercial layer of the platform.

Marketing Acquisition
↓
Seller Onboarding
↓
Revenue Generation
↓
Seller Fulfillment
↓
Order Delivery
↓
Customer Satisfaction

It enables the platform to measure how seller acquisition strategies ultimately translate into marketplace revenue and business growth.

---

# Summary

`fct_order_sales` is the central commercial fact table of the Olist Seller Intelligence Platform.

It provides trusted sales intelligence and serves as the foundation for revenue analysis, seller performance measurement, customer purchasing analytics, and executive reporting.
