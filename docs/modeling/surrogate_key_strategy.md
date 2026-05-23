---

# `surrogate_key_strategy.md`

```md
# Surrogate Key Strategy

## Objective

This document defines the surrogate key strategy used across the Olist Seller Intelligence Platform.

The warehouse follows:
# Kimball dimensional modeling standards

where:
- business keys identify real-world entities
- surrogate keys identify warehouse records

---

# Why Surrogate Keys Exist

Business keys are unstable because:

- source systems may change
- duplicates may exist
- operational systems are not warehouse-safe

Surrogate keys solve:

- historical tracking
- SCD Type 2 versioning
- warehouse join performance
- source-system independence

---

# Key Design Principles

| Principle                           | Applied |
| ----------------------------------- | ------- |
| Integer-based warehouse keys        | Yes     |
| Source keys preserved separately    | Yes     |
| Dimensions own surrogate keys       | Yes     |
| Facts reference dimensions using FK | Yes     |
| SCD Type 2 compatible               | Yes     |

---

# DIMENSION KEY STRATEGY

## `dim_customer`

| Column      | Purpose                 |
| ----------- | ----------------------- |
| customer_sk | Warehouse surrogate key |
| customer_id | Source business key     |

---

## `dim_seller`

| Column    | Purpose                 |
| --------- | ----------------------- |
| seller_sk | Warehouse surrogate key |
| seller_id | Source business key     |

Supports:

# SCD Type 2

---

## `dim_product`

| Column     | Purpose                 |
| ---------- | ----------------------- |
| product_sk | Warehouse surrogate key |
| product_id | Source business key     |

---

## `dim_date`

## Special Case

`dim_date`
uses:

# intelligent surrogate keys

Example:

```text
20180115
```
