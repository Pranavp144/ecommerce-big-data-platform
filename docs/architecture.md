# System Architecture

## Current Architecture

The current implementation is a local Big Data processing pipeline using Hadoop HDFS and Apache Spark.

```text
                    E-Commerce Data
                           |
                           v
                         HDFS
                           |
                           v
                    PySpark Ingestion
                           |
                           v
                    Data Validation
                           |
                           v
                     Transformation
                           |
                           v
                        Parquet
                           |
                           v
                      Spark SQL
                           |
              +------------+------------+
              |            |            |
              v            v            v
         Customer       Product      Business
         Analytics      Analytics       KPIs
