---

# MISTAKE 3 — NO METADATA

# What beginners usually do

They ingest CSV → parquet.

Done.

Example:

```
order_idcustomer_idpricestatus
```

That’s it.

Looks fine.

But enterprise-wise:

# this is weak.

Because later:  
you lose traceability.

---

# WHAT IS METADATA?

Metadata =

# data ABOUT the data

Not business data.

System data.

---

# Example

Business columns:

```
order_idpricecustomer_id
```

Metadata columns:

```
ingestion_timestamp source_file batch_id pipeline_run_id
```

---

# WHY METADATA MATTERS

Imagine this happens:

---

# SCENARIO 1 — Corrupted File

Your dashboard suddenly shows:

- 50% less orders

Boss asks:

# “What happened?”

Without metadata:  
you panic.

You don’t know:

- which file loaded
- when loaded
- which pipeline run failed

---

# WITH METADATA

You can trace:

```
source_file = olist_orders_dataset.csvingestion_timestamp = 2026-05-19 14:00
```

Immediately:  
you know which ingestion caused issue.

---

# SCENARIO 2 — Replay Pipeline

Suppose:

- schema changed
- Spark logic broke
- parquet corrupted

You need:

# replay ingestion

Metadata helps identify:

- which data was affected
- which run to rebuild

---

# SCENARIO 3 — AUDITABILITY

Very important academically and professionally.

Suppose committee asks:

> “How do you guarantee lineage?”

Your answer:

> “Each Bronze table preserves ingestion metadata including source file and ingestion timestamp to support auditability and replayability.”

That sounds professional because:

# it is.

---

# MOST IMPORTANT BRONZE METADATA

For YOUR project:

Column

Purpose

ingestion_timestamp

when data entered bronze

source_file

original CSV

ingestion_date

partitioning later

batch_id

optional advanced

---

# SIMPLE REAL EXAMPLE

Bronze orders:

order_id

customer_id

ingestion_timestamp

source_file

A1

C1

2026-05-19 15:00

orders.csv

---

# HOW COMPANIES USE THIS

Real companies use metadata for:

- debugging
- compliance
- monitoring
- governance
- lineage
- reproducibility

---

# WHY THIS FITS YOUR PROJECT

Your project explicitly mentions:

- scalable architecture
- reproducibility
- streaming integration
- medallion architecture

  archticture

Metadata is part of real medallion architecture.

---

# BEST PRACTICE

Bronze should preserve:

# original raw meaning + ingestion lineage

NOT business transformations.

---

# MISTAKE 5 — HARDCODING PATHS EVERYWHERE

This is a MASSIVE beginner mistake.

---

# WHAT BEGINNERS DO

Inside every script:

Python

Run

```
df = spark.read.csv("/Users/hamid/Desktop/project/data/raw/orders.csv")
```

Looks harmless.

But this becomes a disaster later.

---

# WHY HARDCODING IS BAD

---

# PROBLEM 1 — Not Portable

Works:

- only on YOUR laptop

Fails:

- Docker
- Airflow
- Linux server
- teammate machine

---

# PROBLEM 2 — Impossible Environment Management

You eventually need:

Environment

Different Paths

local

local folders

docker

container paths

minio

s3a:// paths

production

cloud storage

Hardcoded paths destroy scalability.

---

# PROBLEM 3 — Maintenance Nightmare

Imagine:  
10 scripts.

All contain:

Python

Run

```
/Users/hamid/Desktop/project/
```

Now project folder changes.

You must edit:

# EVERY script.

Very bad engineering.

---

# PROFESSIONAL SOLUTION

# CENTRALIZED CONFIGURATION

Instead:

```
configs/config.yaml
```

Example:

YAML

```
raw_data_path: data/raw/bronze_data_path: data/bronze/silver_data_path: data/silver/
```

Now scripts read config.

---

# WHY THIS IS ENTERPRISE-GRADE

Because:

- environments change
- storage changes
- orchestration changes

But logic stays same.

Only config changes.

---

# HOW THIS HELPS YOUR PROJECT

Right now:  
you start local.

Later:  
you move to MinIO.

Olist_Data_Dictionary

Without config:  
you rewrite everything.

With config:  
just change:

YAML

```
bronze_path: s3a://bronze/
```

DONE.

---

# REAL ENTERPRISE THINKING

Good engineers separate:

Type

Example

Logic

transformations

Configuration

paths, credentials

---

# PROFESSIONAL PROJECT STRUCTURE

You already planned configs folder correctly.

Olist_Data_Dictionary

Now use it seriously.

Example:

```
configs/├── paths.yaml├── spark_config.yaml└── pipeline_config.yaml
```

---

# SIMPLE PROFESSIONAL FLOW

```
Script starts    ↓Load config    ↓Read raw path from config    ↓Run ingestion
```

NOT:

```
Script starts    ↓Hardcoded laptop path    ↓Everything breaks later
```

---

# WHAT I RECOMMEND FOR YOU NOW

For Bronze phase:

# MINIMUM PROFESSIONAL VERSION

Create:

```
configs/paths.yaml
```

Example:

YAML

```
raw_path: data/raw/bronze_path: data/bronze/
```

Then:  
your ingestion script reads from it.

---

# WHY THIS WILL IMPRESS COMMITTEE

Because students usually build:

# script collections

You are building:

# pipeline architecture

Huge difference.

---

# THE BIG PICTURE

These two “small” things actually represent:

Concept

Meaning

Metadata

governance & lineage

Configs

maintainability & scalability

These are:

# real data engineering principles

not just coding tricks.

---

# THE PROFESSIONAL SUMMARY

You can literally say this later:

> “The Bronze layer was designed with ingestion lineage metadata and centralized configuration management to improve auditability, reproducibility, portability, and future migration toward object storage orchestration.”
