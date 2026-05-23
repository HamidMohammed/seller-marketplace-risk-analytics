## Objective

This document captures the core dimensional modeling lessons learned during the design of the Olist Seller Intelligence Platform.

Its purpose is to establish:

- professional fact table thinking
- grain-first modeling discipline
- business-process-driven warehouse design
- reusable enterprise modeling principles

The goal is to create a permanent reference for future data engineering projects.

This document represents one of the most important architectural lessons in dimensional modeling:

# fact tables are designed around business processes and grain — not topics.

---

# 1. The Most Important Fact Modeling Lesson

## Incorrect Beginner Thinking

A common beginner mistake is:

```text
"Everything related to sellers belongs in one seller fact table."
```

or:

```text
"Everything related to orders belongs in one big order table."
```

This is:

# topic-based modeling

and it usually creates:

- mixed grains
- duplicated metrics
- broken aggregations
- unreliable KPIs
- impossible analytics

---

# 2. Correct Professional Thinking

Professional dimensional modeling starts with two questions:

---

## Question 1

# What business event happened?

---

## Question 2

# What is the grain of that event?

The answers define:

- the fact table
- the metrics
- the dimensions
- the valid calculations

This is:

# grain-first modeling

and it is one of the foundations of Kimball dimensional modeling.

---

# 3. Fact Tables Represent Business Events

A fact table is:

# an event log of a measurable business process

NOT:

# a folder for related columns

Every fact table must represent:

- one business process
- one consistent grain
- one measurable event type

---

# 4. Example from the Olist Project

The Olist dataset contains multiple business processes related to orders.

Initially, it seemed possible to place everything inside one giant delivery table.

Deeper analysis proved this was incorrect.

---

# Business Process 1 — Seller Fulfillment

## Event

```text
Seller prepares and ships an item.
```

## Grain

```text
One row = one seller item fulfillment event
```

## Dataset

```text
olist_order_items_dataset
```

## Resulting Fact

```text
fct_seller_fulfillment
```

This fact measures:

- seller preparation time
- shipping pressure
- freight intensity
- operational workload

---

# Business Process 2 — Customer Delivery Outcome

## Event

```text
Customer receives the final order.
```

## Grain

```text
One row = one delivered customer order
```

## Dataset

```text
olist_orders_dataset
```

## Resulting Fact

```text
fct_order_delivery
```

This fact measures:

- delivery delays
- on-time performance
- delivery duration
- breached promises
- customer delivery experience

---

# Business Process 3 — Customer Review

## Event

```text
Customer submits a review.
```

## Grain

```text
One row = one customer review
```

## Dataset

```text
olist_order_reviews_dataset
```

## Resulting Fact

```text
fct_customer_reviews
```

This fact measures:

- review scores
- satisfaction trends
- delay-to-review relationships
- customer sentiment

---

# Business Process 4 — Payment Transaction

## Event

```text
Customer payment processed.
```

## Grain

```text
One row = one payment transaction
```

## Dataset

```text
olist_order_payments_dataset
```

## Resulting Fact

```text
fct_order_payments
```

This fact measures:

- payment behavior
- installment usage
- payment value
- payment method trends

---

# 5. Why Multiple Facts Are Correct

All previous examples are related to:

# orders

BUT:
they are:

# different business processes

Therefore:
they MUST be:

# different fact tables

This is a critical professional modeling principle.

---

# 6. Why Giant Unified Facts Fail

A giant “everything table” usually mixes:

- different grains
- unrelated timestamps
- conflicting metrics
- duplicated rows

This silently corrupts analytics.

---

# Example of Grain Corruption

Suppose one table contains:

| Metric         | Real Grain |
| -------------- | ---------- |
| review_score   | review     |
| freight_value  | order item |
| payment_value  | payment    |
| delivery_delay | order      |

Now:
aggregations become unreliable.

Example problems:

- duplicated delivery counts
- inflated revenue
- repeated review scores
- incorrect averages

This problem is called:

# fan-out duplication

and it is one of the most dangerous warehouse mistakes because:

# the numbers often look believable while being wrong.

---

# 7. Grain Defines Everything

Before adding ANY column to a fact table:

first define:

```text
One row = one _____
```

Then:
ONLY add columns that describe exactly that thing.

This is the professional dimensional modeling workflow.

---

# 8. Fact Table Design Rules

## Rule 1 — Declare Grain First

Always write:

```text
One row = one _____
```

before creating columns.

---

## Rule 2 — Facts Represent Events

Fact tables model:

- transactions
- events
- measurable operations

NOT:

- business entities

Entities belong in dimensions.

---

## Rule 3 — Never Mix Grains

Never combine:

- order-level
- item-level
- payment-level
- review-level

inside one fact.

---

## Rule 4 — Dimensions Provide Context

Facts store:

# measurements

Dimensions store:

# descriptive context

Example:

| Fact           | Dimension        |
| -------------- | ---------------- |
| delivery_delay | seller_city      |
| freight_value  | product_category |
| payment_value  | customer_state   |

---

## Rule 5 — Shared Dimensions Are Good

Multiple fact tables can reuse:

- dim_date
- dim_seller
- dim_customer
- dim_product

This is called:

# conformed dimensions

and it creates:

- KPI consistency
- stable joins
- reusable analytics

---

# 9. Why the Dual-Fact Delivery Design Was Correct

The Olist delivery domain contained:

- seller-level shipment operations
- customer-level delivery outcomes

These are:

# different grains

Therefore:
the project intentionally separated them into:

- `fct_order_delivery`
- `fct_seller_fulfillment`

This preserved:

- grain integrity
- correct KPIs
- seller accountability
- streaming compatibility
- scalable architecture

This follows:

# Kimball best practices

exactly as documented in the delivery modeling strategy.

---

# 10. Enterprise Modeling Mindset

Professional warehouses are designed around:

| Focus                 | Correct? |
| --------------------- | -------- |
| Business processes    | ✅       |
| Event grain           | ✅       |
| Measurable operations | ✅       |
| Shared dimensions     | ✅       |
| Topic grouping        | ❌       |
| Giant universal facts | ❌       |

---

# 11. Important Long-Term Lesson

When building ANY future fact table:

DO NOT ask:

```text
"What topic is this about?"
```

Instead ask:

```text
"What business event happened?"
```

Then ask:

```text
"What is the grain of that event?"
```

That mindset shift separates:

# beginner reporting

from:

# professional dimensional modeling.

---

# 12. Final Professional Principle

# Fact tables are grouped by business process and grain — not by topic.

This is one of the most important architectural lessons in data warehousing and should guide every future warehouse design decision.

This principle improves:

- scalability
- maintainability
- KPI trustworthiness
- dimensional integrity
- streaming compatibility
- analytical correctness

across all future projects.
