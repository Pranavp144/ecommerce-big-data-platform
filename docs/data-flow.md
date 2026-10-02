# Data Flow

## Current Pipeline

The current pipeline processes an intentionally dirty e-commerce dataset to demonstrate data quality handling.

```text
orders_dirty.csv
       |
       v
      HDFS
       |
       v
   PySpark Read
       |
       v
 Data Validation
       |
       +----------------------------+
       |                            |
       v                            v
 Missing customer ID          Invalid values
       |                       quantity <= 0
       |                       price <= 0
       |                            |
       +-------------+--------------+
                     |
                     v
              Duplicate Removal
                     |
                     v
                Clean Orders
                     |
                     v
              total_amount
                     |
                     v
                  Parquet
                     |
                     v
                Spark SQL
                     |
          +----------+----------+
          |          |          |
          v          v          v
      Customer    Product    Business
      Revenue     Sales        KPIs
