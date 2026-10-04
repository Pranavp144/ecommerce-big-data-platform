# Performance Analysis

## Overview

The Olist ETL pipeline was executed using Apache Spark in local mode with
`local[*]`.

The Spark UI was used to inspect jobs, stages, SQL/DataFrame executions,
join strategies, and shuffle activity.

The purpose of this analysis is to understand how Spark executes the
pipeline rather than to perform extensive optimization on the current
local dataset.

---

## Dataset Size

The pipeline processes the following core datasets:

| Dataset | Rows |
|---|---:|
| Orders | 99,441 |
| Customers | 99,441 |
| Order Items | 112,650 |
| Products | 32,951 |
| Delivered Orders | 96,478 |
| Enriched Order Items | 110,197 |

---

## Execution Overview

The Spark UI showed the following execution characteristics:

- 65 completed Spark jobs/stages were observed during the pipeline run.
- 24 SQL/DataFrame executions were recorded.
- The Parquet write execution involved 5 associated Spark jobs.
- Multiple Spark actions such as `count()`, `show()`, and `write()` triggered
  separate executions.

The relatively high number of executions is partly caused by the data-quality
validation layer, where individual validation checks use Spark actions such
as `count()`.

---

## Join Strategies

Spark selected different physical join strategies for the pipeline.

### Orders and Order Items

The join between delivered orders and order items was executed using a
`SortMergeJoin`.

The execution plan showed:

```text
Orders
   ↓
Filter
   ↓
Exchange
   ↓
Sort
   \
    SortMergeJoin
   /
Sort
   ↑
Exchange
   ↑
Order Items
