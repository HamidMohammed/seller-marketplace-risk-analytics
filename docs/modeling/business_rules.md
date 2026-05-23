# Business Rules

## Objective

This document defines the official business rules governing the Phase 1 Delivery Performance Mart.

Business rules ensure:

- KPI consistency
- trustworthy analytics
- reproducible calculations
- dimensional integrity
- defensible business insights

These rules are enforced during:

- ETL transformations
- dbt modeling
- data quality testing
- dashboard calculations
- streaming enrichment

This document represents:

# the operational logic of the warehouse

---

# RULE 1 — DELIVERED ORDERS ONLY

## Rule

Phase 1 delivery analysis includes only:

```sql
WHERE order_status = 'delivered'

Why This Rule Exists
--------------------

Orders that are:

*   canceled

*   unavailable

*   invoiced

*   processing

*   shipped but not completed


do not contain valid final delivery outcomes.

Using them would corrupt:

*   delay calculations

*   on-time KPIs

*   delivery duration metrics

*   seller performance analysis


Business Justification
----------------------

The business question is:

> “How successful was the final delivery experience?”

Only delivered orders can answer that question.

RULE 2 — SINGLE-SELLER KPI ANALYSIS
===================================

Rule
----

Operational seller accountability KPIs use:

`   WHERE seller_count = 1   `

Why This Rule Exists
--------------------

Some Olist orders contain:

multiple sellers
================

In these cases:

*   one customer order

*   may involve multiple shipments

*   from different sellers

*   with different operational performance


But the dataset provides:

one final delivery timestamp
============================

for the entire order.

This creates:

seller responsibility ambiguity
===============================

Business Justification
----------------------

Without this rule:

*   late deliveries may be assigned to the wrong seller

*   seller on-time rates become unreliable

*   operational accountability becomes inaccurate


This rule ensures:

trustworthy seller performance metrics
======================================

Important Note
--------------

The project still preserves:

*   seller\_count

*   is\_multi\_seller\_order


for advanced future analysis.

The data is preserved,but KPI accountability is controlled.

RULE 3 — DELIVERY DELAY CALCULATION
===================================

Rule
----

`   delay_days =actual_delivery_date - estimated_delivery_date   `

Business Meaning
----------------

Measures:

how much the final delivery missed the promised date
====================================================

Negative values mean:

*   delivery arrived early


Positive values mean:

*   delivery arrived late


RULE 4 — BUFFER DAYS CALCULATION
================================

Rule
----

`   buffer_days =estimated_delivery_date - purchase_timestamp   `

Business Meaning
----------------

Measures:

how much delivery padding Olist added
=====================================

This metric is central to the project narrative.

Prior research suggests Olist systematically padded delivery estimates by approximately 12 days.

The project investigates:

*   whether the 90% on-time rate is artificially inflated

*   which sellers break even the padded estimate

*   whether breached buffers indicate structural seller weakness


RULE 5 — DELIVERY STATUS CLASSIFICATION
=======================================

Rule
----

ConditionDelivery Statusdelay\_days < 0Earlydelay\_days = 0On-Timedelay\_days BETWEEN 1 AND 3Slight Delaydelay\_days BETWEEN 4 AND 7Latedelay\_days > 7Breached Buffer

Why This Rule Exists
--------------------

Raw delay numbers are difficult for business users to interpret.

Categorization enables:

*   executive dashboards

*   seller risk segmentation

*   operational alerting

*   streaming thresholds

*   storytelling visuals


Most Important Category
-----------------------

Breached Buffer
===============

This category means:

*   the seller failed even Olist’s padded promise


These are considered:

genuinely serious operational failures
======================================

RULE 6 — MULTI-SELLER ORDER FLAGGING
====================================

Rule
----

Plain textANTLR4BashCC#CSSCoffeeScriptCMakeDartDjangoDockerEJSErlangGitGoGraphQLGroovyHTMLJavaJavaScriptJSONJSXKotlinLaTeXLessLuaMakefileMarkdownMATLABMarkupObjective-CPerlPHPPowerShell.propertiesProtocol BuffersPythonRRubySass (Sass)Sass (Scss)SchemeSQLShellSwiftSVGTSXTypeScriptWebAssemblyYAMLXML`   is_multi_seller_order =seller_count > 1   `

Business Meaning
----------------

Identifies orders involving:

*   multiple sellers

*   multiple fulfillment operations

*   potentially multiple shipments


Why It Matters
--------------

Multi-seller orders may:

*   increase logistics complexity

*   increase delay risk

*   create fragmented fulfillment behavior


This flag supports future advanced analysis.

RULE 7 — FREIGHT AGGREGATION
============================

Rule
----

`   freight_total_value =SUM(freight_value)GROUP BY order_id   `

Business Meaning
----------------

Calculates:

total shipping cost per customer order
======================================

This metric supports:

*   delivery cost analysis

*   freight burden investigation

*   shipping efficiency analysis


RULE 8 — CUSTOMER IDENTITY STANDARDIZATION
==========================================

Rule
----

Repeat-customer analysis uses:

`   customer_unique_id   `

NOT:

`   customer_id   `

Why This Rule Exists
--------------------

The Olist dataset may assign:

*   multiple customer\_id values

*   to the same real customer


Using customer\_id directly would:

*   overcount customers

*   break retention metrics

*   corrupt repeat-purchase analysis


RULE 9 — GEOLOCATION DEDUPLICATION
==================================

Rule
----

Geolocation coordinates are standardized using:

median latitude and longitude per ZIP prefix
============================================

Why This Rule Exists
--------------------

The geolocation dataset contains:

*   duplicate ZIP entries

*   multiple coordinates per region


Without deduplication:

*   distance calculations become inconsistent

*   geographic KPIs become unstable


RULE 10 — ROLE-PLAYING DATE DIMENSION
=====================================

Rule
----

The same dim\_date is reused for:

*   purchase dates

*   estimated delivery dates

*   actual delivery dates

*   shipping deadlines


Why This Rule Exists
--------------------

This follows:

Kimball role-playing dimension design
=====================================

Benefits:

*   standardized time intelligence

*   reusable date logic

*   consistent dashboard filtering


RULE 11 — SURROGATE KEY USAGE
=============================

Rule
----

All dimensions use warehouse-generated surrogate keys.

Business IDs are preserved as:

*   natural business identifiers

*   not warehouse relationships


Why This Rule Exists
--------------------

Surrogate keys support:

*   dimensional stability

*   SCD Type 2 implementation

*   warehouse scalability

*   faster joins


RULE 12 — STREAMING RISK ENRICHMENT
===================================

Rule
----

The streaming pipeline uses:

historical seller baseline metrics
==================================

loaded from the batch layer at startup.

Business Meaning
----------------

Real-time risk scoring is based on:

*   seller historical on-time rate

*   seller operational trends

*   historical workload behavior


NOT arbitrary hardcoded assumptions.

This creates:

statistically grounded operational intelligence
===============================================

RULE 13 — FACT TABLE SEPARATION
===============================

Rule
----

Customer delivery outcomes and seller fulfillment operations remain in separate fact tables.

Why This Rule Exists
--------------------

The dataset tracks logistics at:

Business ProcessGrainCustomer DeliveryOrder LevelSeller FulfillmentItem/Seller Level

Combining them would create:

*   duplicate rows

*   mixed-grain corruption

*   unreliable KPIs

*   fan-out aggregation problems


This separation preserves:

dimensional integrity
=====================
```
