# Data Flow

## Overview

The E-Commerce Big Data Analytics Platform was developed in two major stages.

The initial stage used a small intentionally dirty e-commerce dataset with Hadoop HDFS and PySpark to learn data cleaning, transformation, Parquet storage, and Spark SQL.

The current production-style pipeline uses the Olist Brazilian E-Commerce dataset stored in Amazon S3 and processes it with PySpark.

---

## Phase 1 — Initial Learning Data Flow

The first version of the project used a small intentionally dirty dataset to understand data-quality handling.

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
 Data Cleaning
      |
      +----------------------------+
      |                            |
      v                            v
Missing customer ID          Invalid values
                            quantity <= 0
                            price <= 0
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
```

### Data Cleaning Rules

The initial learning pipeline demonstrated four basic cleaning rules:

1. Remove records with a missing `customer_id`.
2. Remove records where `quantity <= 0`.
3. Remove records where `price <= 0`.
4. Remove duplicate `order_id` values.

The cleaned dataset was then used to calculate `total_amount` and perform downstream analytics.

---

## Phase 2 — Current Olist Data Flow

The current pipeline processes the Olist Brazilian E-Commerce Public Dataset.

The core datasets used by the pipeline are:

- `olist_orders_dataset.csv`
- `olist_customers_dataset.csv`
- `olist_order_items_dataset.csv`
- `olist_products_dataset.csv`

The data is stored in Amazon S3.

```text
                    Olist CSV Datasets
                           |
                           v
                 Amazon S3 - Raw Layer
                           |
                           v
                    PySpark Ingestion
                           |
              +------------+------------+
              |            |            |
              v            v            v
           Orders      Customers    Order Items
              |            |            |
              |            |            |
              +------------+------------+
                           |
                           v
                    Product Data
                           |
                           v
                 Delivered Order Filter
                           |
                           v
                Orders + Order Items Join
                           |
                           v
                    + Products Join
                           |
                           v
                   + Customers Join
                           |
                           v
                Calculate total_item_cost
                           |
                           v
                  Data Quality Validation
                           |
                           v
                 Processed Parquet Dataset
                           |
                           v
              Amazon S3 - Processed Layer
                           |
                           v
                    PySpark Analytics
                           |
          +----------------+----------------+
          |                |                |
          v                v                v
     Customer          Product          Category
     Analytics         Analytics        Analytics
          |                |                |
          +----------------+----------------+
                           |
                           v
                     State Analytics
                           |
                           v
                    Business KPIs
```

---

## 1. Data Ingestion

Spark reads the four core Olist datasets from the S3 raw layer.

```text
s3a://olist-bigdata-project-2026-8472/raw/olist/
```

The ingestion module is responsible only for reading the source datasets.

The files are loaded into Spark DataFrames using CSV headers and inferred schemas.

---

## 2. Delivered Order Filtering

The pipeline focuses its main analytical dataset on completed transactions.

Orders are filtered using:

```python
order_status == "delivered"
```

This removes orders with statuses such as:

- shipped
- canceled
- unavailable
- invoiced
- processing
- created
- approved

The delivered orders are then used for the downstream joins and revenue calculations.

---

## 3. Dataset Joins

The pipeline combines the Olist datasets using their relational keys.

```text
customers.customer_id
          |
          v
orders.customer_id

orders.order_id
          |
          v
order_items.order_id

order_items.product_id
          |
          v
products.product_id
```

The actual processing sequence is:

```text
Delivered Orders
       |
       v
Join Order Items
       |
       v
Join Products
       |
       v
Join Customers
       |
       v
Enriched Orders
```

The resulting DataFrame contains transaction, product, order, and customer information required for analytics.

---

## 4. Derived Columns

The pipeline creates a derived column called:

```text
total_item_cost
```

It is calculated as:

```text
total_item_cost = price + freight_value
```

This allows product price and freight cost to be represented together for business-level calculations.

---

## 5. Data Quality Validation

After enrichment, the pipeline performs reusable data-quality checks.

The validation layer checks:

```text
Required columns
       |
       v
Required identifiers are not NULL
       |
       v
Numeric values are not negative
       |
       v
Minimum expected row count
```

The current validation checks include:

- Required columns exist.
- `order_id` is not NULL.
- `customer_id` is not NULL.
- `product_id` is not NULL.
- `price` is not negative.
- `freight_value` is not negative.
- `total_item_cost` is not negative.
- At least 100,000 enriched records are present.

The enriched dataset currently contains:

```text
110,197 delivered order-item records
```

---

## 6. Processed Storage

After validation, the enriched dataset is written to Parquet.

```text
PySpark
   |
   v
Parquet
   |
   v
Amazon S3
```

Output location:

```text
s3a://olist-bigdata-project-2026-8472/processed/olist/
```

The processed dataset is stored as multiple Parquet part files.

Parquet provides a columnar storage format suitable for analytical workloads.

---

## 7. Read Processed Data

The pipeline reads the generated Parquet dataset back from S3.

```text
Amazon S3 - Processed Layer
              |
              v
       Spark.read.parquet()
              |
              v
      Processed DataFrame
```

This demonstrates the separation between the transformation/storage stage and the analytics stage.

---

## 8. Analytics

The processed dataset is used for several analytical operations.

### Customer Analytics

Customer-level analysis calculates:

- Total customer spending
- Number of orders
- Average order value

The grouping key is the Olist `customer_unique_id`.

---

### Product Analytics

Product-level analysis calculates:

- Product revenue
- Number of distinct orders containing the product

The grouping key is `product_id`.

---

### Category Analytics

Products are grouped by:

```text
product_category_name
```

The pipeline calculates category-level revenue and sorts categories by revenue.

---

### State Analytics

Customers are grouped by:

```text
customer_state
```

The pipeline calculates revenue by customer state.

---

### Business KPIs

The pipeline calculates overall business metrics:

```text
Total Product Revenue
Total Freight
Total Value
```

Current results from the pipeline are approximately:

```text
Total Product Revenue : ₹13,221,498.11
Total Freight         : ₹2,198,275.64
Total Value           : ₹15,419,773.75
```

---

## Complete Current Data Flow

```text
                         OLIST DATASET
                              |
                              v
                    Amazon S3 - Raw Layer
                              |
                              v
                     PySpark Ingestion
                              |
                              v
                  Delivered Order Filter
                              |
                              v
                  Orders + Order Items
                              |
                              v
                     + Products
                              |
                              v
                     + Customers
                              |
                              v
                 Enriched Transaction Data
                              |
                              v
                    Data Quality Checks
                              |
                              v
                     Processed Parquet
                              |
                              v
                  Amazon S3 - Processed
                              |
                              v
                    Read Parquet Data
                              |
                              v
                         Analytics
                              |
             +----------------+----------------+
             |                |                |
             v                v                v
         Customer          Product          Category
         Revenue           Revenue          Revenue
             |                |                |
             +----------------+----------------+
                              |
                              v
                       State Revenue
                              |
                              v
                        Business KPIs
```

---

## Data Volume Through the Pipeline

The current Olist source data contains approximately:

| Dataset | Records |
|---|---:|
| Orders | 99,441 |
| Customers | 99,441 |
| Order Items | 112,650 |
| Products | 32,951 |

After filtering for delivered orders and joining the datasets, the enriched transaction dataset contains:

```text
110,197 records
```

This provides a realistic dataset for demonstrating Spark-based processing rather than relying only on the small learning dataset.

---

## Module Mapping

The data flow maps directly to the project source code:

```text
Data Flow Stage             Source Module
----------------------------------------------------------
Spark Session               src/utils/spark_session.py
Data Ingestion              src/ingestion/read_olist_data.py
Transformation              src/transformation/olist_transformations.py
Validation                  src/validation/olist_validation.py
Customer Analytics          src/analytics/olist_analysis.py
Product Analytics           src/analytics/olist_analysis.py
Category Analytics          src/analytics/olist_analysis.py
State Analytics             src/analytics/olist_analysis.py
Business KPIs               src/analytics/olist_analysis.py
Pipeline Entry Point        src/main_olist.py
```

This modular structure keeps each stage of the data flow separated and makes the pipeline easier to maintain, test, and explain during technical interviews.

---

## Summary

The project demonstrates two stages of data processing.

The initial local pipeline used HDFS and a small dirty dataset to learn the fundamentals of data cleaning and Spark processing.

The current pipeline uses Amazon S3 and the Olist dataset to demonstrate a more realistic big-data workflow:

```text
S3 Raw
  ↓
PySpark Ingestion
  ↓
Filtering
  ↓
Joins
  ↓
Enrichment
  ↓
Validation
  ↓
Parquet
  ↓
S3 Processed
  ↓
Analytics
```

This separation between raw data, processing, validation, processed storage, and analytics provides the foundation for future Databricks and lakehouse integration.