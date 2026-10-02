# E-Commerce Big Data Analytics Platform

An end-to-end Big Data engineering project built using Apache Hadoop, HDFS, Apache Spark, PySpark, Spark SQL and Parquet.

The project demonstrates a complete data pipeline starting from raw e-commerce data, followed by data quality processing, transformation, analytical processing and structured storage.

The architecture is being developed incrementally, starting with a local Hadoop/Spark environment and later extending to AWS and Databricks.

---

## Project Overview

This project simulates an e-commerce data engineering platform that processes order data and produces customer, product and business-level analytics.

The current pipeline:

```text
Raw E-Commerce Data
        |
        v
      HDFS
        |
        v
   PySpark ETL
        |
        +-------------------+
        |                   |
        v                   v
 Data Validation       Data Enrichment
        |                   |
        +---------+---------+
                  |
                  v
              Parquet
                  |
                  v
             Spark SQL
                  |
        +---------+---------+
        |         |         |
        v         v         v
    Customer   Product   Business
    Analytics  Analytics   KPIs

