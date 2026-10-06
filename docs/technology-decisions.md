# Technology Decisions

## Overview

The project was built incrementally, starting with local Hadoop and Spark components and then extending the pipeline to Amazon S3.

The technology choices were made to first understand the underlying Big Data concepts and then apply the same processing workflow in a cloud-based architecture.

---

## Python

Python is used as the primary programming language.

The main reason for this choice is the mature PySpark API, which allows Apache Spark applications to be developed using Python.

Python is used throughout the project for:

- Spark application code
- Data ingestion
- Data transformation
- Data validation
- Analytics
- Testing

**Status:** Implemented

---

## Apache Spark

Apache Spark is used as the main distributed processing engine.

Spark is responsible for:

- Reading large datasets
- Filtering data
- Joining datasets
- Transforming records
- Performing aggregations
- Writing processed data
- Running analytical workloads

Spark was chosen because the project is intended to demonstrate distributed data processing rather than only local Python data manipulation.

**Status:** Implemented

---

## PySpark

PySpark provides the Python interface to Apache Spark.

The project uses the PySpark DataFrame API for the main processing pipeline.

PySpark is used for:

- DataFrame creation
- Filtering
- Joins
- Column transformations
- Aggregations
- Parquet processing
- Data-quality validation

The production-style Olist pipeline is primarily implemented using PySpark DataFrames.

**Status:** Implemented

---

## Hadoop HDFS

Hadoop HDFS was used during the initial learning phase of the project.

The purpose of HDFS was to understand:

- Distributed storage
- Hadoop filesystem concepts
- HDFS paths
- NameNode and DataNode architecture
- Spark interaction with distributed storage

The project later moved its active cloud storage layer to Amazon S3.

HDFS therefore remains an important part of the project's learning and development history but is not the current storage layer for the Olist production-style pipeline.

**Status:** Completed learning phase

---

## Spark SQL

Spark SQL was explored during the development and notebook phase.

It allows Spark DataFrames to be queried using SQL while still using Spark as the underlying execution engine.

The project demonstrated:

- Temporary views
- SQL queries
- Aggregations
- Sorting
- Analytical queries

Spark SQL is primarily used for exploration and learning in the current project. The main Olist pipeline uses the PySpark DataFrame API.

**Status:** Implemented / Exploration

---

## Parquet

Parquet is used as the processed storage format.

The pipeline converts the enriched Olist transaction data into Parquet and stores it in Amazon S3.

Parquet was selected because it is a columnar storage format that is well suited to analytical workloads.

Using Parquet also creates a clear separation between:

```text
Raw CSV
   ↓
Processed Parquet
```

The processed Parquet dataset is then read back by Spark for analytics.

**Status:** Implemented

---

## Git and GitHub

Git is used for version control throughout the project.

Git provides:

- Source-code versioning
- Meaningful commit history
- Tracking of project evolution
- Branch management
- Recovery from previous versions

GitHub is used as the remote repository for the project.

The repository history reflects the incremental development of the project, including the initial Spark implementation, Olist pipeline, validation, AWS integration, documentation, and cleanup.

**Status:** Implemented

---

## AWS S3

Amazon S3 is the current cloud storage layer.

The project initially used local HDFS and was later extended to Amazon S3.

The current S3 architecture contains separate raw and processed layers:

```text
Amazon S3
│
├── raw/
│   └── olist/
│       ├── olist_orders_dataset.csv
│       ├── olist_customers_dataset.csv
│       ├── olist_order_items_dataset.csv
│       └── olist_products_dataset.csv
│
└── processed/
    └── olist/
        └── Parquet files
```

S3 was selected because it provides cloud object storage and allows the project to move beyond a local HDFS environment while keeping Spark as the processing engine.

**Status:** Implemented

---

## Hadoop S3A

Hadoop S3A is used to connect Apache Spark with Amazon S3.

The pipeline uses S3A paths such as:

```text
s3a://olist-bigdata-project-2026-8472/raw/olist/
```

S3A allows Spark to read the raw Olist CSV files and write the processed Parquet data directly to S3.

The Spark session is configured with the Hadoop AWS dependency and AWS profile credential provider.

**Status:** Implemented

---

## Raw and Processed Storage Layers

The project intentionally separates raw data from processed data.

### Raw Layer

The raw layer contains the original source CSV files.

```text
s3://olist-bigdata-project-2026-8472/raw/olist/
```

The source data is not modified during ingestion.

### Processed Layer

The processed layer contains the enriched and validated dataset in Parquet format.

```text
s3://olist-bigdata-project-2026-8472/processed/olist/
```

This separation makes the pipeline easier to understand and allows the original source data to remain available for reprocessing.

**Status:** Implemented

---

## Delivered-Order Filtering

The Olist dataset contains orders with multiple statuses.

For the main revenue analysis, the pipeline only processes:

```text
order_status = delivered
```

This decision keeps the main analytical dataset focused on completed transactions.

The filtering is performed before the main enrichment joins.

**Status:** Implemented

---

## Modular Project Structure

The project separates the main stages of the pipeline into different modules.

```text
src/
├── ingestion/
├── transformation/
├── validation/
├── analytics/
└── utils/
```

This design separates responsibilities:

- `ingestion` — reads source data
- `transformation` — filters and enriches data
- `validation` — performs data-quality checks
- `analytics` — calculates business metrics
- `utils` — manages shared Spark configuration

The modular design makes individual components easier to understand, test, maintain, and explain during technical interviews.

**Status:** Implemented

---

## Why Not Use Pandas for the Main Pipeline?

Pandas is useful for local data analysis, but the main project is intended to demonstrate distributed data processing.

Apache Spark was therefore selected for the primary pipeline so that the project demonstrates:

- Distributed processing
- Spark transformations
- Spark actions
- Joins
- Aggregations
- Partitioned processing
- Parquet-based analytical storage

Pandas was not required for the main Olist pipeline.

---

## Databricks

Databricks is planned as a future managed Spark and lakehouse platform.

The current pipeline already separates storage and processing in a way that can be extended toward a managed cloud environment.

The planned architecture is:

```text
Amazon S3
    ↓
Databricks
    ↓
Delta Lake
    ↓
Databricks SQL
    ↓
Dashboard
```

Databricks is **not part of the current implementation**.

**Status:** Planned

---

## Delta Lake

Delta Lake is planned for a future lakehouse version of the project.

The current pipeline uses Parquet as the processed storage format.

A future Delta Lake implementation could provide a more advanced transactional lakehouse storage layer.

**Status:** Planned

---

## Databricks SQL

Databricks SQL is planned for the future analytics and visualization stage.

The current project performs analytics directly through PySpark.

A future implementation can expose processed Delta Lake data through Databricks SQL for dashboards and business reporting.

**Status:** Planned

---

## Technology Status

| Technology | Role | Status |
|------------|------|--------|
| Python | Application and data-processing language | Implemented |
| Apache Spark | Distributed processing engine | Implemented |
| PySpark | Python API for Spark | Implemented |
| Hadoop HDFS | Initial distributed storage | Completed learning phase |
| Spark SQL | SQL-based Spark exploration | Implemented / Exploration |
| Parquet | Processed analytical storage | Implemented |
| Git | Version control | Implemented |
| GitHub | Remote repository | Implemented |
| Amazon S3 | Cloud object storage | Implemented |
| Hadoop S3A | Spark-to-S3 integration | Implemented |
| Databricks | Managed Spark/lakehouse platform | Planned |
| Delta Lake | Lakehouse storage layer | Planned |
| Databricks SQL | SQL analytics and reporting | Planned |

---

## Design Principle

The project intentionally follows an incremental architecture:

```text
Local Hadoop + Spark
        ↓
Understand Big Data fundamentals
        ↓
Olist Dataset
        ↓
Amazon S3 + PySpark
        ↓
Processed Parquet + Analytics
        ↓
Future Databricks / Lakehouse
```

This approach allows the underlying concepts to be understood before introducing managed cloud abstractions.

The current implementation therefore demonstrates both the fundamentals of the Hadoop/Spark ecosystem and their application in a cloud-based data pipeline.

---

## Summary

The technology stack was selected to provide a clear progression from local Big Data fundamentals to cloud-based data processing.

The current implemented stack is:

```text
Python
   ↓
PySpark / Apache Spark
   ↓
Hadoop S3A
   ↓
Amazon S3
   ↓
Parquet
   ↓
PySpark Analytics
```

HDFS and Spark SQL were important parts of the learning and development phase.

Databricks, Delta Lake, and Databricks SQL remain planned extensions rather than current implementations.