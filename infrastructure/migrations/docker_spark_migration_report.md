# Docker Spark Migration Report

## Project

**Olist Seller Intelligence Platform**

---

# 1. Objective

The objective of this migration was to transform the platform from a local Spark execution environment into a containerized distributed processing environment using Docker.

The migration enables Spark workloads to run within a dedicated infrastructure layer while integrating with MinIO object storage and PostgreSQL warehouse services.

---

# 2. Initial Architecture

The original platform architecture relied entirely on local execution.

```text
Raw Data
    ↓
Local Spark
    ↓
Bronze
    ↓
Silver
    ↓
Gold
```

### Limitations

- Dependent on local machine configuration
- Limited portability
- No infrastructure abstraction
- Difficult environment replication
- Not representative of enterprise deployments

---

# 3. Target Architecture

The target architecture introduces containerized infrastructure components.

```text
Docker Compose

├── MinIO
├── PostgreSQL
├── pgAdmin
├── Spark Master
└── Spark Worker
```

Data Flow:

```text
Raw Data
    ↓
MinIO Bronze
    ↓
Spark Cluster
    ↓
MinIO Silver
    ↓
Spark Cluster
    ↓
MinIO Gold
    ↓
PostgreSQL Warehouse
```

---

# 4. Infrastructure Components

## MinIO

Purpose:

- Object storage layer
- Bronze storage
- Silver storage
- Gold storage

Buckets:

```text
bronze
silver
gold
```

---

## PostgreSQL

Purpose:

- Enterprise warehouse layer
- Fact table storage
- Dimension table storage
- Data mart storage

Database:

```text
olist_dw
```

---

## pgAdmin

Purpose:

- PostgreSQL administration
- SQL validation
- Warehouse inspection

---

## Spark Master

Purpose:

- Cluster coordination
- Job scheduling
- Worker management

Port:

```text
7077
```

UI:

```text
http://localhost:8080
```

---

## Spark Worker

Purpose:

- Distributed task execution
- Resource allocation

UI:

```text
http://localhost:8081
```

---

# 5. Docker Migration Activities

## Phase 1 — MinIO Deployment

Completed Activities:

- Dockerized MinIO
- Created storage buckets
- Validated read/write operations

Status:

```text
Completed
```

---

## Phase 2 — PostgreSQL Deployment

Completed Activities:

- Dockerized PostgreSQL
- Dockerized pgAdmin
- Warehouse connectivity validation

Status:

```text
Completed
```

---

## Phase 3 — Gold Layer Warehouse Loading

Completed Activities:

- Spark JDBC integration
- PostgreSQL load automation
- Warehouse validation framework

Status:

```text
Completed
```

---

## Phase 4 — Spark Cluster Deployment

Completed Activities:

- Spark Master deployment
- Spark Worker deployment
- Cluster communication validation

Status:

```text
Completed
```

---

## Phase 5 — Spark Container Integration

Completed Activities:

- Project directory mounting
- MinIO connectivity validation
- S3A configuration
- Hadoop AWS integration
- PostgreSQL JDBC integration

Status:

```text
Completed
```

---

# 6. Technical Challenges Encountered

## Challenge 1

Spark container could not access MinIO.

### Root Cause

Incorrect endpoint configuration:

```text
http://localhost:9000
```

Inside Docker, localhost refers to the container itself.

### Resolution

Updated endpoint:

```text
http://minio:9000
```

---

## Challenge 2

Spark jobs could not locate required S3A libraries.

### Resolution

Added required JARs:

```text
hadoop-aws-3.3.4.jar
aws-java-sdk-bundle-1.12.262.jar
```

---

## Challenge 3

Spark jobs could not access PostgreSQL.

### Resolution

Added JDBC driver:

```text
postgresql-42.7.4.jar
```

---

## Challenge 4

Containerized Spark could not access project source code.

### Resolution

Mounted project root directory into Spark containers.

```text
/workspace/project
```

---

# 7. Validation Results

## Spark Cluster Validation

Validation:

```text
Spark Master Online
Spark Worker Online
```

Result:

```text
PASS
```

---

## MinIO Validation

Validation:

```text
Spark Read
Spark Write
```

Result:

```text
PASS
```

---

## PostgreSQL Validation

Validation:

```text
Warehouse Load
Warehouse Verification
```

Result:

```text
PASS
```

---

# 8. Final Architecture

```text
Raw CSV
    ↓
MinIO Bronze
    ↓
Spark Cluster
    ↓
MinIO Silver
    ↓
Spark Cluster
    ↓
MinIO Gold
    ↓
Spark JDBC
    ↓
PostgreSQL Warehouse
    ↓
Power BI
```

---

# 9. Business Value

The migration provides:

- Environment portability
- Infrastructure reproducibility
- Distributed processing capability
- Enterprise-style architecture
- Cloud-ready storage abstraction
- Simplified deployment process

---

# 10. Outcome

The Docker Spark migration successfully transformed the Olist Seller Intelligence Platform from a local Spark environment into a containerized distributed data platform.

All infrastructure components were validated, including MinIO storage integration, Spark cluster deployment, PostgreSQL warehouse connectivity, and Spark-based object storage operations.

Migration Status:

```text
SUCCESSFUL
```
