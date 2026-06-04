# Docker Architecture

## Olist Seller Intelligence Platform

---

# 1. Objective

The Docker architecture provides a reproducible and portable infrastructure layer for executing data engineering workloads in a containerized environment.

The architecture eliminates local environment dependencies and enables consistent deployment across development and production environments.

---

# 2. Infrastructure Overview

The platform is deployed using Docker Compose.

```text
Docker Compose

├── MinIO
├── PostgreSQL
├── pgAdmin
├── Spark Master
└── Spark Worker
```

---

# 3. Container Responsibilities

## MinIO Container

### Purpose

Object storage and Data Lake implementation.

### Responsibilities

- Bronze storage
- Silver storage
- Gold storage

### Exposed Ports

```text
9000
9001
```

---

## PostgreSQL Container

### Purpose

Analytical Data Warehouse.

### Responsibilities

- Fact table storage
- Dimension storage
- Data mart storage

### Exposed Port

```text
5432
```

---

## pgAdmin Container

### Purpose

Database administration interface.

### Responsibilities

- Query execution
- Warehouse validation
- Database management

### Exposed Port

```text
5050
```

---

## Spark Master Container

### Purpose

Cluster management and job scheduling.

### Responsibilities

- Cluster coordination
- Job scheduling
- Worker allocation

### Exposed Ports

```text
7077
8080
```

---

## Spark Worker Container

### Purpose

Distributed task execution.

### Responsibilities

- ETL execution
- Data transformation
- Aggregation processing

### Exposed Port

```text
8081
```

---

# 4. Network Architecture

Docker Compose automatically creates a shared virtual network.

```text
spark-master
      |
      |
spark-worker
      |
      |
postgres
      |
      |
minio
```

Container communication is performed using Docker service names.

Examples:

```text
http://minio:9000

jdbc:postgresql://postgres:5432/olist_dw
```

---

# 5. Storage Architecture

## MinIO Buckets

### Bronze

```text
s3a://bronze
```

Stores ingested source datasets.

### Silver

```text
s3a://silver
```

Stores cleaned and validated datasets.

### Gold

```text
s3a://gold
```

Stores dimensional models and marts.

---

# 6. Spark Integration

Spark accesses MinIO using Hadoop S3A.

### Required Libraries

- hadoop-aws-3.3.4.jar
- aws-java-sdk-bundle-1.12.262.jar

### Configuration

```text
spark.hadoop.fs.s3a.endpoint=http://minio:9000
spark.hadoop.fs.s3a.access.key=admin
spark.hadoop.fs.s3a.secret.key=admin123
```

---

# 7. Warehouse Integration

Spark writes analytical assets directly into PostgreSQL using JDBC.

### Driver

```text
postgresql-42.7.4.jar
```

### JDBC Endpoint

```text
jdbc:postgresql://postgres:5432/olist_dw
```

---

# 8. Pipeline Execution

The platform executes through a centralized orchestration entry point.

```text
run_pipeline.py
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

All layers are executed through Spark.

---

# 9. Deployment Flow

```text
Docker Compose
        ↓
Infrastructure Startup
        ↓
Spark Cluster Initialization
        ↓
MinIO Initialization
        ↓
PostgreSQL Initialization
        ↓
Pipeline Execution
```

---

# 10. Validation Results

Infrastructure validation successfully confirmed:

- Spark Master availability
- Spark Worker registration
- MinIO connectivity
- PostgreSQL connectivity
- Bronze execution
- Silver execution
- Gold execution
- Warehouse loading

---

# 11. Benefits

The Docker architecture provides:

- Environment consistency
- Simplified deployment
- Infrastructure portability
- Reproducibility
- Scalability readiness
- Reduced configuration drift
- Enterprise deployment practices

---

# 12. Architecture Outcome

The Dockerized infrastructure transformed the platform from a local Spark implementation into a distributed containerized data platform capable of supporting enterprise-scale analytical workloads.
