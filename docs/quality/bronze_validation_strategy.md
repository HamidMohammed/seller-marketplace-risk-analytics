# `bronze_validation_strategy.md`

Add here:

```text id="jlwm3m"
docs/quality/bronze_validation_strategy.md
```

---

# Bronze Validation Strategy

## Objective

This document explains the validation strategy implemented for the Bronze layer of the Delivery Intelligence Platform and clarifies the purpose of Bronze-level validation within the Medallion Architecture.

The Bronze layer is responsible for:

- raw data ingestion
- schema preservation
- lineage tracking
- replayability
- ingestion reliability

It is NOT responsible for:

- business-rule validation
- cleaning
- deduplication
- KPI generation

Those responsibilities belong to the Silver layer.

This separation follows:

# Medallion Architecture principles

and ensures:

- scalable pipelines
- clear data-layer responsibilities
- maintainable transformations
- reliable data lineage

---

# 1. Bronze Layer Purpose

The Bronze layer acts as:

# immutable raw analytical storage

where original Olist CSV datasets are ingested into Spark-managed parquet files with minimal transformation.

The layer preserves:

- original dataset structure
- source fidelity
- ingestion traceability
- replay capability

while standardizing:

- storage format
- metadata
- ingestion framework

---

# 2. Bronze Validation Philosophy

The Bronze layer validates:

# technical ingestion integrity

NOT:

# business correctness

This distinction is extremely important in modern data engineering architectures.

---

# Bronze Validation Answers

Bronze validation answers questions such as:

| Question                       | Validation Goal        |
| ------------------------------ | ---------------------- |
| Did ingestion succeed?         | parquet readability    |
| Was schema parsed correctly?   | schema validation      |
| Was metadata added?            | lineage validation     |
| Were files corrupted?          | parquet access test    |
| Did row counts load correctly? | ingestion completeness |

---

# Bronze Does NOT Validate

Bronze intentionally avoids:

- business-rule enforcement
- data cleaning
- KPI calculations
- null remediation
- deduplication
- operational transformations

because these belong to:

# the Silver transformation layer

---

# 3. Why Bronze Validation Is Lightweight

The architecture intentionally keeps Bronze validation lightweight because Bronze datasets must remain:

# replayable raw data assets

Heavy transformation logic inside Bronze would:

- blur architectural responsibilities
- complicate replayability
- reduce ingestion reliability
- weaken Medallion separation

The Bronze layer therefore focuses only on:

# ingestion trustworthiness

---

# 4. Bronze Validation Levels

The project separates validation into:

# two distinct engineering layers

---

## Level 1 — Bronze Validation

Purpose:

# validate ingestion health

Focus:

- infrastructure integrity
- parquet readability
- metadata consistency
- schema preservation

---

## Level 2 — Silver Validation

Purpose:

# validate business correctness

Focus:

- delivery logic
- timestamp consistency
- geographic correctness
- operational business rules
- analytical reliability

---

# 5. Bronze Validation Rules Implemented

The project implements the following Bronze validations.

---

# 5.1 Parquet Readability Validation

## Objective

Verify that Spark can successfully read parquet outputs after ingestion.

---

## Why It Matters

This ensures:

- ingestion succeeded
- parquet files are not corrupted
- storage layer is operational

---

# Validation Example

```python id="yzd9qu"
spark.read.parquet(path)
```

---

# 5.2 Schema Validation

## Objective

Verify that schemas were inferred correctly during CSV ingestion.

---

## Important Focus Areas

Special attention is given to:

- timestamps
- decimals
- ZIP-code prefixes

because Spark schema inference may incorrectly interpret certain fields.

---

## Example Risk

```text id="f9qqjq"
01037
```

incorrectly becoming:

```text id="c8g0va"
1037
```

which would later break geographic joins.

---

# 5.3 Metadata Validation

## Objective

Ensure all Bronze datasets contain standardized ingestion lineage metadata.

---

## Required Metadata Columns

| Column              | Purpose                      |
| ------------------- | ---------------------------- |
| ingestion_timestamp | ingestion execution tracking |
| ingestion_date      | debugging and partitioning   |
| source_file         | source lineage traceability  |

---

## Why Metadata Matters

Metadata supports:

- auditability
- lineage
- debugging
- replayability
- future orchestration

This represents:

# enterprise-grade ingestion design

---

# 5.4 Row Count Validation

## Objective

Verify ingestion completeness.

---

## Validation Logic

```text id="2lt9hh"
CSV row count == parquet row count
```

---

## Why It Matters

This ensures:

- no silent ingestion loss
- no corrupted writes
- complete parquet conversion

---

# 5.5 Multi-Dataset Validation

## Objective

Validate ingestion success across all Bronze datasets.

---

## Validation Scope

The pipeline validates:

- orders
- order_items
- customers
- sellers
- products
- payments
- reviews
- geolocation
- marketing datasets

using:

# automated validation loops

rather than repetitive manual checks.

This reflects:

# scalable ingestion engineering

---

# 6. Why Only One Dataset Was Deeply Inspected

The validation notebook performs:

# automated validation for all datasets

but uses:

# `orders`

as the primary inspection example for:

- schema review
- metadata inspection
- timestamp analysis
- sample data inspection

This approach avoids:

- repetitive notebook sections
- duplicated validation logic
- unnecessary notebook complexity

while still demonstrating:

# representative ingestion inspection

This is a common engineering practice during early pipeline development.

---

# 7. Bronze Replayability

One of the most important Bronze objectives is:

# replayability

Meaning:
if Bronze datasets are deleted or corrupted,
the ingestion pipeline can fully rebuild them from:

# immutable raw source files

This supports:

- operational recovery
- debugging
- pipeline reliability
- future orchestration systems

---

# 8. Relationship to Medallion Architecture

The project follows the following layer responsibilities:

| Layer  | Responsibility                 |
| ------ | ------------------------------ |
| Raw    | Immutable source files         |
| Bronze | Ingestion + lineage            |
| Silver | Cleaning + business validation |
| Gold   | KPIs + analytics               |

This separation is fundamental to:

# modern data platform architecture

---

# 9. Architectural Benefits

The Bronze validation strategy provides:

| Benefit              | Impact                           |
| -------------------- | -------------------------------- |
| Reliable ingestion   | Trustworthy pipeline foundation  |
| Replay capability    | Operational resilience           |
| Schema observability | Easier debugging                 |
| Metadata lineage     | Auditability                     |
| Scalable validation  | Reusable engineering patterns    |
| Medallion alignment  | Clean layer separation           |
| Enterprise realism   | Professional ingestion standards |

---

# 10. Final Outcome

The Bronze layer successfully provides:

- reliable parquet ingestion
- schema preservation
- ingestion metadata lineage
- replayable raw storage
- scalable ingestion architecture
- validation observability

while intentionally avoiding:

- business transformations
- cleaning logic
- analytical calculations

which are deferred to:

# the Silver transformation layer

This design reflects:

# enterprise-grade Medallion Architecture engineering principles

and establishes a trustworthy foundation for all downstream:

- Silver transformations
- Gold marts
- streaming pipelines
- analytical dashboards
- operational intelligence systems.
