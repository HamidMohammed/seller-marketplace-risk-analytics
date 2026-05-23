# Bronze Layer

## Objective

The Bronze Layer is the first engineering layer in the Medallion Architecture of the Olist Seller Intelligence Platform.

Its primary purpose is to ingest immutable raw source datasets into a structured, replayable, scalable, and audit-ready storage layer while preserving original source fidelity.

The Bronze Layer acts as:

# the system-of-record raw ingestion layer

for all downstream processing.

It provides:

- ingestion standardization
- schema preservation
- lineage tracking
- replayability
- auditability
- scalable batch foundations

The Bronze Layer intentionally avoids:

- business transformations
- cleansing
- KPI derivation
- aggregation
- deduplication

Those responsibilities belong to the Silver Layer.

The project follows:

# Medallion Architecture Principles

using:

```text id="mjlwm1"
RAW → BRONZE → SILVER → GOLD
```

This aligns with the overall architecture of the platform.

---

# 1. Bronze Layer Role in the Architecture

Within the platform architecture, the Bronze Layer acts as the ingestion boundary between raw source files and analytical transformation pipelines.

Architecture flow:

```text id="mjlwm2"
Raw CSV Files
        ↓
Spark Ingestion Pipeline
        ↓
Bronze Layer (Parquet Storage)
        ↓
Silver Transformation Layer
```

The Bronze Layer guarantees that:

- original datasets remain recoverable
- ingestion pipelines are reproducible
- schema evolution can be monitored
- downstream transformations remain isolated from raw-data corruption

---

# 2. Source Datasets

The Bronze Layer ingests all Olist source datasets and marketing funnel datasets.

---

## Core Olist Datasets

| Dataset                           | Purpose                       |
| --------------------------------- | ----------------------------- |
| olist_orders_dataset              | Order lifecycle events        |
| olist_order_items_dataset         | Seller fulfillment operations |
| olist_customers_dataset           | Customer geography            |
| olist_sellers_dataset             | Seller geography              |
| olist_products_dataset            | Product logistics             |
| olist_order_reviews_dataset       | Customer satisfaction         |
| olist_order_payments_dataset      | Payment behavior              |
| olist_geolocation_dataset         | Geographic enrichment         |
| product_category_name_translation | Category translation          |

---

## Marketing Funnel Datasets

| Dataset                         | Purpose                    |
| ------------------------------- | -------------------------- |
| olist_marketing_qualified_leads | Seller acquisition sources |
| olist_closed_deals              | Lead-to-seller conversion  |

The inclusion of marketing funnel datasets supports the project narrative:

```text id="mjlwm3"
Acquisition Quality
        ↓
Seller Performance
        ↓
Delivery Failure
        ↓
Customer Damage
```

as defined in the project proposal.

---

# 3. Bronze Layer Engineering Principles

The Bronze Layer follows five core engineering principles.

---

# 3.1 Raw Data Preservation

Bronze tables preserve source data exactly as received.

No records are:

- deleted
- corrected
- deduplicated
- filtered

This ensures:

# immutable raw storage

which is critical for:

- debugging
- replayability
- lineage
- pipeline recovery

---

# 3.2 Minimal Transformation

Only technical transformations are allowed.

Allowed:

- schema inference
- parquet conversion
- metadata enrichment

Not allowed:

- business logic
- cleansing
- enrichment
- KPI derivation
- deduplication

This preserves:

# clean Medallion separation

between ingestion and transformation responsibilities.

---

# 3.3 Schema Fidelity

Bronze ingestion preserves original source schema as closely as possible.

Special attention is required for:

- timestamps
- decimal values
- ZIP prefixes
- nullable fields

This prevents:

- downstream type corruption
- inconsistent joins
- invalid analytics

A critical example involves Brazilian ZIP prefixes:

```text id="mjlwm4"
01037 → 1037
```

Incorrect numeric inference would corrupt geographic joins and downstream delivery analysis.

---

# 3.4 Ingestion Metadata

Each Bronze dataset contains standardized ingestion lineage metadata.

---

## Mandatory Metadata Fields

| Column              | Purpose                            |
| ------------------- | ---------------------------------- |
| ingestion_timestamp | Exact ingestion execution time     |
| ingestion_date      | Partitioning and debugging support |
| source_file         | Original source filename           |

---

## Optional Future Metadata

| Column           | Purpose                       |
| ---------------- | ----------------------------- |
| batch_id         | Pipeline execution identifier |
| pipeline_version | ETL traceability              |

This metadata enables:

- auditability
- lineage tracking
- reproducibility
- operational debugging

This represents:

# enterprise-grade ingestion engineering

rather than simple file conversion.

---

# 3.5 Replayability

The Bronze Layer supports:

# deterministic replay

Meaning:
downstream Silver and Gold layers can be rebuilt consistently from preserved Bronze datasets without reprocessing analytical transformations from scratch.

This enables:

- operational recovery
- reproducible pipelines
- debugging
- future orchestration reliability

Replayability is one of the foundational principles of modern data lakehouse architectures.

---

# 4. Technology Decisions

Technology choices were intentionally selected based on scalability, maintainability, and future streaming integration.

---

# 4.1 PySpark for Ingestion

The ingestion framework uses:

# PySpark

---

## Why PySpark?

| Reason                     | Explanation                                |
| -------------------------- | ------------------------------------------ |
| Scalability                | Handles larger datasets efficiently        |
| Architectural consistency  | Same engine reused in Silver and Streaming |
| Schema management          | Strong typing support                      |
| Parquet optimization       | Native columnar support                    |
| Future Kafka compatibility | Shared Spark ecosystem                     |

The project intentionally avoids Pandas-based ingestion because this project is:

# a data engineering platform

rather than a notebook-only analytics project.

---

# 4.2 Apache Parquet Storage

Bronze datasets are stored using:

# Apache Parquet

---

## Why Parquet?

| CSV                   | Parquet                    |
| --------------------- | -------------------------- |
| Row-based             | Columnar                   |
| Larger storage        | Compressed                 |
| Weak schema support   | Strong schema preservation |
| Slow analytical scans | Spark optimized            |

Parquet is the industry standard for modern analytical lakehouse systems.

---

# 4.3 MinIO-Compatible Architecture

The final architecture targets:

# MinIO object storage

as the primary lakehouse storage layer.

However, implementation begins locally first:

```text id="mjlwm5"
data/bronze/
```

before migrating to:

```text id="mjlwm6"
s3a://bronze/
```

This staged approach intentionally avoids:

- unnecessary infrastructure complexity
- credential management overhead
- container orchestration issues

during early development.

---

# 5. Folder Structure

The Bronze Layer follows a standardized enterprise-style project structure.

---

## Raw Data Storage

```text id="mjlwm7"
data/raw/
```

Contains:

- immutable original CSV files
- untouched Kaggle exports

---

## Bronze Storage

```text id="mjlwm8"
data/bronze/
```

Contains:

- parquet-converted raw datasets
- ingestion metadata
- schema-preserved tables

---

## Pipeline Scripts

```text id="mjlwm9"
pipelines/bronze/
```

Contains:

- Spark ingestion pipelines
- reusable ingestion functions
- metadata enrichment logic
- orchestration-ready ingestion scripts

---

# 6. Bronze Dataset Naming Standards

Bronze datasets follow standardized naming conventions.

Examples:

```text id="mjlwm10"
orders
customers
order_items
products
payments
reviews
```

The Bronze layer itself already communicates ingestion stage ownership, making additional prefixes unnecessary.

This improves:

- readability
- maintainability
- orchestration consistency
- warehouse clarity

---

# 7. Storage Layout Standards

Each dataset is stored in its own folder:

```text id="mjlwm11"
data/bronze/orders/
data/bronze/customers/
data/bronze/order_items/
```

instead of:

```text id="mjlwm12"
data/bronze/orders.parquet
```

Folder-based storage supports:

- partitioning
- append operations
- scalable object-storage migration
- Spark optimization

---

# 8. Bronze Ingestion Flow

The Bronze ingestion framework follows a standardized ETL sequence.

---

## Step 1 — Read Raw CSV

PySpark reads source CSV files from:

```text id="mjlwm13"
data/raw/
```

using schema inference.

---

## Step 2 — Infer Schema

Spark infers:

- timestamps
- decimals
- strings
- nullable columns

This creates structured Bronze datasets while preserving source fidelity.

---

## Step 3 — Add Metadata Columns

The pipeline enriches datasets with ingestion lineage metadata.

| Column              | Example                  |
| ------------------- | ------------------------ |
| ingestion_timestamp | 2026-05-19 14:00         |
| ingestion_date      | 2026-05-19               |
| source_file         | olist_orders_dataset.csv |

---

## Step 4 — Write Parquet

Datasets are written into Bronze storage as parquet files.

Example:

```text id="mjlwm14"
data/bronze/orders/
```

---

## Step 5 — Validate Ingestion

Validation checks include:

- row-count reconciliation
- schema validation
- parquet readability
- metadata validation
- timestamp validation

This prevents silent ingestion corruption.

---

# 9. Bronze Validation Strategy

Validation is mandatory before downstream transformations begin.

The Bronze Layer validates:

# technical ingestion integrity

NOT:

# business correctness

Business-rule validation is intentionally deferred to:

# the Silver transformation layer

This separation reflects proper:

# Medallion Architecture responsibility boundaries

---

# Validation Checks

| Check                    | Purpose                     |
| ------------------------ | --------------------------- |
| CSV rows == parquet rows | Prevent missing records     |
| Schema correctness       | Prevent type corruption     |
| Timestamp validation     | Preserve temporal integrity |
| Metadata validation      | Ensure lineage consistency  |
| Parquet readability      | Prevent corrupted writes    |

---

# Validation Notebook

```text id="mjlwm15"
notebooks/bronze_validation.ipynb
```

The notebook supports:

- debugging
- ingestion verification
- schema inspection
- academic demonstrations
- operational validation

---

# 10. Configuration Management

The project intentionally avoids:

# hardcoded file paths

inside ingestion scripts.

Instead:
centralized configuration files are used.

Recommended structure:

```text id="mjlwm16"
configs/
└── paths.yaml
```

Example:

```yaml id="mjlwm17"
raw_path: data/raw/
bronze_path: data/bronze/
silver_path: data/silver/
gold_path: data/gold/
```

This improves:

- portability
- maintainability
- environment migration
- MinIO readiness
- Airflow integration

---

# 11. Implemented Bronze Components

The following Bronze engineering components were successfully implemented.

| Component                   | Status      |
| --------------------------- | ----------- |
| Spark ingestion framework   | Implemented |
| Config-driven paths         | Implemented |
| Reusable ingestion function | Implemented |
| Metadata enrichment         | Implemented |
| Apache Parquet conversion   | Implemented |
| Bronze validation notebook  | Implemented |
| Multi-dataset ingestion     | Implemented |
| Row-count validation        | Implemented |

---

# 12. Common Bronze Mistakes Avoided

The architecture intentionally avoids several common beginner mistakes.

---

## Mistake 1 — Cleaning in Bronze

Wrong:

- null handling
- deduplication
- KPI derivation

Correct:
Bronze preserves raw ingestion only.

---

## Mistake 2 — Using Pandas Instead of Spark

The platform uses Spark because:

- the project is engineering-focused
- future streaming reuses Spark
- parquet integration is native

---

## Mistake 3 — Missing Metadata

Without ingestion metadata:

- lineage breaks
- debugging becomes difficult
- replay tracking becomes unreliable

The project therefore enforces metadata standards across all Bronze datasets.

---

## Mistake 4 — Dashboard-First Development

Dashboards are intentionally deferred until:

- marts are trusted
- facts are validated
- KPIs are correct

This prevents analytics from being built on unstable foundations.

---

## Mistake 5 — Hardcoded File Paths

All storage paths are centralized using configuration files.

This supports:

- Docker migration
- MinIO migration
- Airflow orchestration
- environment portability

---

# 13. Bronze Deliverables

The Bronze phase is considered complete when the following deliverables exist.

| Deliverable              | Status   |
| ------------------------ | -------- |
| Raw CSV storage          | Required |
| Bronze parquet storage   | Required |
| Spark ingestion pipeline | Required |
| Metadata enrichment      | Required |
| Validation notebook      | Required |
| Config-driven paths      | Required |
| Multi-dataset ingestion  | Required |
| Bronze documentation     | Required |

---

# 14. Relationship to Silver Layer

The Bronze Layer feeds:

# the Silver Transformation Layer

which is responsible for:

- cleansing
- deduplication
- business rules
- derived metrics
- dimensional preparation

This separation ensures:

# clean engineering boundaries

between:

- raw ingestion
- analytical transformation

---

# 15. Final Architectural Outcome

The Bronze Layer establishes:

- reproducible ingestion
- scalable lakehouse foundations
- enterprise lineage tracking
- schema-preserving storage
- replayable datasets
- future streaming compatibility

The final Bronze architecture transforms raw Olist CSV datasets into:

# structured, replayable, audit-ready parquet datasets

that support:

- dimensional modeling
- streaming enrichment
- warehouse construction
- scalable analytics
- operational intelligence

within the Medallion Architecture of the Olist Seller Intelligence Platform.
