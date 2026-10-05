# AWS Architecture

## Overview

The current Olist e-commerce pipeline runs locally using Hadoop HDFS and
Apache Spark.

The planned AWS architecture moves the storage and Spark processing layer
to AWS while keeping the core PySpark ETL logic largely unchanged.

The AWS architecture is currently a planned extension of the project and
has not yet been deployed.

---

                AWS S3
                  │
          ┌───────┴───────┐
          │               │
       raw/olist/     processed/olist/
          │               ▲
          │               │
          ▼               │
      Olist CSV       Parquet files
          │               ▲
          └──────► PySpark ─┘
                    │
             Data Validation
                    │
              Transformations
                    │
                 Analytics
