# Deployment Guide

## Olist Seller Intelligence Platform

---

# 1. Purpose

This document describes the deployment process for the Olist Seller Intelligence Platform.

The guide covers infrastructure startup, data lake initialization, warehouse deployment, Spark cluster deployment, and pipeline execution.

---

# 2. System Requirements

## Hardware Requirements

Minimum:

- 8 GB RAM
- 4 CPU Cores
- 20 GB Free Disk Space

Recommended:

- 16 GB RAM
- 8 CPU Cores
- SSD Storage

---

## Software Requirements

### Operating Systems

- macOS
- Linux
- Windows (Docker Desktop)

### Required Software

- Docker Desktop
- Docker Compose
- Python 3.10+
- Java 17
- Apache Spark 3.5.3

---

# 3. Project Structure

```text
Olist_Seller_Intelligence_Platform/

├── data/
├── pipelines/
├── infrastructure/
├── configs/
├── docs/
└── run_pipeline.py
```

---

# 4. Infrastructure Startup

Navigate to infrastructure directory:

```bash
cd infrastructure
```

Start infrastructure:

```bash
docker compose up -d --build
```

---

# 5. Infrastructure Validation

Verify running containers:

```bash
docker ps
```

Expected containers:

```text
minio
olist-postgres
olist-pgadmin
spark-master
spark-worker
```

---

# 6. MinIO Validation

Open:

```text
http://localhost:9001
```

Login:

```text
Username: admin
Password: admin123
```

Expected buckets:

```text
bronze
silver
gold
```

---

# 7. PostgreSQL Validation

Open pgAdmin:

```text
http://localhost:5050
```

Login:

```text
admin@olist.com
admin123
```

Verify:

```text
olist_dw
```

database exists.

---

# 8. Spark Validation

Open Spark Master UI:

```text
http://localhost:8080
```

Expected:

```text
Alive Workers: 1
```

Open Spark Worker UI:

```text
http://localhost:8081
```

Expected:

```text
Worker Registered
```

---

# 9. Bronze Layer Execution

Run:

```bash
spark-submit pipelines/bronze/run_bronze_pipeline.py
```

Expected Output:

```text
Bronze Pipeline Completed Successfully
```

Expected Storage:

```text
s3a://bronze
```

---

# 10. Silver Layer Execution

Run:

```bash
spark-submit pipelines/silver/run_silver_pipeline.py
```

Expected Output:

```text
Silver Pipeline Completed Successfully
```

Expected Storage:

```text
s3a://silver
```

---

# 11. Gold Layer Execution

Run:

```bash
spark-submit pipelines/gold/run_gold_pipeline.py
```

Expected Output:

```text
Gold Pipeline Completed Successfully
```

Expected Storage:

```text
s3a://gold
```

---

# 12. Warehouse Loading

Run:

```bash
spark-submit infrastructure/postgres/load_gold_to_postgres.py
```

Expected Output:

```text
Warehouse Load Successful
```

---

# 13. End-to-End Pipeline Execution

Execute full platform:

```bash
spark-submit run_pipeline.py
```

Execution Flow:

```text
Bronze
    ↓
Silver
    ↓
Gold
    ↓
Warehouse Load
```

---

# 14. Validation Queries

Example:

```sql
SELECT COUNT(*)
FROM dim_seller;
```

```sql
SELECT COUNT(*)
FROM fct_order_delivery;
```

```sql
SELECT COUNT(*)
FROM seller_performance_mart;
```

---

# 15. Troubleshooting

## Spark Cannot Connect To MinIO

Verify:

```text
http://minio:9000
```

inside Docker network.

---

## Spark Cannot Connect To PostgreSQL

Verify JDBC URL:

```text
jdbc:postgresql://postgres:5432/olist_dw
```

---

## Bucket Not Found

Verify:

```text
bronze
silver
gold
```

exist in MinIO.

---

# 16. Deployment Outcome

A successful deployment results in a fully operational containerized data platform capable of executing the complete Medallion Architecture and loading analytical assets into PostgreSQL for reporting and dashboarding.
