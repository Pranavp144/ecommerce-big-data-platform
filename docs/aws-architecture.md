# AWS Architecture

## Overview

The current version of the E-Commerce Big Data Analytics Platform uses
Amazon S3 as the cloud storage layer and Apache Spark/PySpark as the
distributed data processing engine.

The pipeline separates raw source data from processed analytical data
using two S3 layers:

- Raw layer — original Olist CSV datasets
- Processed layer — enriched Parquet datasets

---

## Architecture

```text
                Olist Dataset
                     │
                     ▼
             Amazon S3 - Raw
                     │
                     ▼
                PySpark
                     │
          ┌──────────┴──────────┐
          ▼                     ▼
   Data Validation        Data Enrichment
          │                     │
          └──────────┬──────────┘
                     ▼
             Processed Parquet
                     │
                     ▼
          Amazon S3 - Processed
                     │
                     ▼
                 Analytics