# dim_date

## Objective

The `dim_date` dimension provides a centralized calendar reference for all business processes within the Olist Seller Intelligence Platform.

It enables:

- time-series analysis
- trend analysis
- period-over-period comparisons
- KPI aggregation by date
- seasonality analysis
- executive reporting
- conformed date intelligence across all marts

The dimension acts as:

# the enterprise calendar dimension

used consistently across all analytical domains.

---

# Dimension Type

Conformed Dimension

---

# Business Purpose

The date dimension standardizes temporal analysis across:

- Delivery Performance
- Seller Fulfillment
- Customer Reviews
- Sales Analytics
- Payment Analytics
- Seller Acquisition Analytics

Without a shared date dimension:

- inconsistent date calculations occur
- duplicated calendar logic appears
- reporting becomes difficult to maintain

---

# Grain

# ONE ROW = ONE CALENDAR DATE

Example:

| date_sk  | full_date  |
| -------- | ---------- |
| 20160101 | 2016-01-01 |
| 20160102 | 2016-01-02 |
| 20160103 | 2016-01-03 |

---

# Table Name

```sql
dim_date
```

---

# Primary Key

```sql
date_sk
```

Format:

```text
YYYYMMDD
```

Example:

```text
20180115
```

---

# Source

Generated Dimension

The dimension is not sourced directly from Olist datasets.

It is generated programmatically to provide complete calendar coverage for all analytical periods.

---

# Recommended Date Range

```text
2015-01-01
to
2020-12-31
```

This range fully covers:

- historical Olist transactions
- acquisition events
- future reporting periods
- dashboard filtering requirements

---

# Attributes

| Column Name      | Description          |
| ---------------- | -------------------- |
| date_sk          | Surrogate date key   |
| full_date        | Calendar date        |
| day_number       | Day of month         |
| day_name         | Day name             |
| week_of_year     | ISO week number      |
| month_number     | Month number         |
| month_name       | Month name           |
| quarter_number   | Quarter number       |
| year_number      | Calendar year        |
| day_of_week      | Day position in week |
| is_weekend       | Weekend indicator    |
| is_month_start   | First day of month   |
| is_month_end     | Last day of month    |
| is_quarter_start | First day of quarter |
| is_quarter_end   | Last day of quarter  |
| is_year_start    | First day of year    |
| is_year_end      | Last day of year     |

---

# Relationships

## fct_order_delivery

| Foreign Key                |
| -------------------------- |
| purchase_date_sk           |
| approval_date_sk           |
| carrier_date_sk            |
| delivered_date_sk          |
| estimated_delivery_date_sk |

---

## fct_seller_fulfillment

| Foreign Key            |
| ---------------------- |
| purchase_date_sk       |
| shipping_limit_date_sk |

---

## fct_order_sales

| Foreign Key       |
| ----------------- |
| purchase_date_sk  |
| approval_date_sk  |
| delivered_date_sk |

---

## fct_order_payments

| Foreign Key      |
| ---------------- |
| purchase_date_sk |
| approval_date_sk |

---

## fct_customer_reviews

| Foreign Key             |
| ----------------------- |
| review_creation_date_sk |
| review_answer_date_sk   |

---

## fct_seller_acquisition

| Foreign Key                |
| -------------------------- |
| first_contact_date_sk      |
| lead_qualification_date_sk |
| conversion_date_sk         |

---

# Business Questions Supported

The dimension enables:

- How many orders were placed per month?
- Which quarter has the highest revenue?
- How does delivery performance change over time?
- What is the trend of customer satisfaction?
- Which periods generate the most seller acquisitions?
- How does seller performance vary by season?

---

# Validation Rules

## Primary Key Validation

```text
date_sk must be unique
```

Expected Result:

```text
0 duplicate date_sk values
```

---

## Date Completeness Validation

```text
No missing calendar dates
```

Expected Result:

```text
Continuous date sequence
```

---

## Weekend Validation

```text
Saturday/Sunday
    → is_weekend = TRUE
```

---

## Calendar Integrity Validation

Validate:

```text
month_number between 1 and 12
quarter_number between 1 and 4
day_number between 1 and 31
```

---

# Architectural Value

The `dim_date` dimension provides:

- reusable calendar intelligence
- conformed reporting periods
- KPI consistency
- simplified dashboard development
- enterprise-grade dimensional modeling

It is the most widely shared dimension in the warehouse and serves as the temporal foundation for all Gold-layer fact tables.

---

# Layer

```text
Gold
```

---

# Modeling Approach

```text
Kimball Dimensional Modeling
```

Dimension Classification:

```text
Conformed Dimension
```
