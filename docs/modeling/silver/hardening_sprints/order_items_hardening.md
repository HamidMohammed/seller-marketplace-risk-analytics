# Sprint 2 — Order Items Hardening Report

## Dataset

```text
silver_order_items
```

---

# Objective

The purpose of Sprint 2 was to restore referential integrity between:

```text
silver_orders
        ↓
silver_order_items
```

after the Orders Hardening initiative introduced order-level quarantine processing.

This sprint ensures that no order item remains linked to an invalid, quarantined, or non-existent parent order.

---

# Business Problem

After Sprint 1:

```text
1390 orders
```

were quarantined due to:

- chronology violations
- delivered orders missing delivery timestamps

These orders were intentionally removed from:

```text
silver_orders
```

to preserve business truth.

However:

```text
silver_order_items
```

still originated from Bronze data and therefore contained child records whose parent orders no longer existed.

This created:

# Referential Integrity Violations

---

# Architecture Before Hardening

```text
Bronze Order Items
        ↓
Silver Orders (Clean)
        ↓
Join
```

Result:

```text
Order Items
may reference
non-existent parent orders
```

---

# Architecture After Hardening

```text
Silver Orders (Trusted)
        ↓
Parent Validation
        ↓

 ┌────────────────────┬────────────────────┐
 │                    │
 ↓                    ↓

Silver Order Items    Order Items Quarantine
(Clean)               (Orphans)
```

---

# Hardening Rule

## Business Rule

Every order item must belong to a valid order.

Valid relationship:

```text
order_item
      ↓
order_id
      ↓
silver_orders
```

Invalid relationship:

```text
order_item
      ↓
order_id
      ↓
NOT FOUND
```

These records are considered:

```text
ORPHAN_ORDER_ITEM
```

and are quarantined.

---

# Cascade Quarantine Strategy

The hardening process performs:

```text
Left Anti Join
```

between:

```text
order_items
```

and

```text
silver_orders
```

to isolate orphaned records.

---

# Validation Results

## Quarantine Summary

```text
Quarantined Order Items: 1609
```

| Quarantine Reason | Count |
| ----------------- | ----- |
| ORPHAN_ORDER_ITEM | 1609  |

---

# Relationship Analysis

Sprint 1 quarantined:

```text
1390 orders
```

Sprint 2 quarantined:

```text
1609 order items
```

Relationship:

```text
1609 ÷ 1390
≈ 1.16 items per order
```

This aligns closely with the observed Olist marketplace behavior where most orders contain one item and a smaller percentage contain multiple items.

This provides strong evidence that the cascade quarantine process is functioning correctly.

---

# Referential Integrity Validation

Validation confirmed:

```text
Remaining Orphan Order Items = 0
```

Meaning:

```text
Every order item
belongs to a valid order
```

after hardening.

---

# Why Quarantine Instead of Delete

The platform follows:

# Zero Silent Data Loss Policy

Therefore:

- invalid records remain auditable
- investigations remain possible
- lineage remains preserved
- business transparency remains intact

---

# Business Impact

This hardening improves:

## Delivery Analytics

Prevents:

- delivery KPI inflation
- incorrect seller attribution
- inaccurate logistics analysis

---

## Sales Analytics

Prevents:

- invalid sales aggregation
- revenue duplication
- orphaned transactional records

---

## Customer Experience Analytics

Improves:

- review attribution
- delivery correlation
- seller accountability analysis

---

## Seller Performance Analytics

Ensures:

- accurate workload calculations
- valid seller metrics
- reliable fulfillment intelligence

---

# Architectural Significance

This sprint introduces:

# Referential Integrity Governance

inside the Silver Layer.

The Silver Layer now guarantees:

```text
Parent Records Exist
```

before data proceeds to:

- staging datasets
- Gold facts
- dashboards
- streaming systems

---

# Final Status

## Sprint 2 — Order Items Hardening

Status:

```text
COMPLETED SUCCESSFULLY
```

Results:

- Referential integrity restored
- Cascade quarantine implemented
- Orphan order items isolated
- Validation framework upgraded
- Auditability preserved

The `silver_order_items` dataset is now considered:

```text
TRUSTED OPERATIONAL LOGISTICS DATA
```

for downstream analytics and dimensional modeling.
