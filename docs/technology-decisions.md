# Technology Decisions

## Python

Python is used as the primary programming language because PySpark provides a mature Python API for Apache Spark.

## Apache Spark

Apache Spark is used as the processing engine for distributed data transformation and analytics.

## PySpark

PySpark allows the Spark processing pipeline to be implemented using Python.

## Hadoop HDFS

HDFS provides the distributed storage layer and helps demonstrate the fundamentals of the Hadoop ecosystem.

## Spark SQL

Spark SQL allows analytical workloads to be expressed using SQL while still executing through Spark.

## Parquet

Parquet is used for processed analytical data because it is a columnar storage format suitable for analytical workloads.

## Git

Git is used for version control and to track the evolution of the project.

## AWS S3

AWS S3 is planned as the cloud object-storage layer for the cloud version of the pipeline.

## Databricks

Databricks is planned as the managed Spark/lakehouse platform for the cloud version.

## Delta Lake

Delta Lake is planned for the cloud data layer to provide a more reliable lakehouse storage architecture.

## Design Principle

The project intentionally starts with local Hadoop and Spark components before moving to managed cloud services.

This allows the underlying Big Data concepts to be understood before introducing cloud abstractions.
