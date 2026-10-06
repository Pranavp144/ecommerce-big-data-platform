# Performance Analysis

## Overview

The Olist ETL pipeline was executed using Apache Spark in local mode with:

```text
local[*]
```

The Spark UI was used during development to inspect jobs, stages, SQL/DataFrame executions, execution plans, join strategies, and task activity.

The purpose of this analysis is to document the observed execution behavior of the pipeline and identify areas for future optimization. It is not intended to present a formal benchmark of Spark performance.

---

## Dataset Size

The current pipeline processes the following core Olist datasets:

| Dataset | Rows |
|---|---:|
| Orders | 99,441 |
| Customers | 99,441 |
| Order Items | 112,650 |
| Products | 32,951 |
| Delivered Orders | 96,478 |
| Enriched Order Items | 110,197 |

The final enriched dataset contains 110,197 delivered order-item records.

---

## Execution Model

The pipeline runs Spark locally using:

```python
.master("local[*]")
```

This allows Spark to use the available local CPU cores for task execution.

Although the current environment is a single machine, the application uses Spark's DataFrame and execution model. The same general processing concepts can later be transferred to a distributed Spark environment such as Databricks.

---

## Spark Actions and Execution

Spark transformations are lazily evaluated.

Operations such as:

- `filter()`
- `join()`
- `withColumn()`
- `groupBy()`

build an execution plan but do not immediately execute the computation.

Actions such as:

- `count()`
- `show()`
- `write()`

trigger Spark jobs.

The current pipeline contains several actions, including:

```text
Source row counts
Enriched row count
Parquet write
Analytics show()
Business metrics show()
```

The optional validation layer also uses `count()` for individual checks.

Therefore, enabling all validation and diagnostic counts increases the number of Spark actions and can increase total execution time.

---

## Spark UI Observations

The Spark UI was used to inspect:

- Jobs
- Stages
- Tasks
- SQL/DataFrame executions
- Execution plans
- Shuffle activity
- Task progress

The UI demonstrated that a single high-level DataFrame operation can result in multiple Spark stages.

This is especially visible for joins and aggregations, where data may need to be exchanged and sorted before the operation can complete.

The project uses the Spark UI primarily as a learning and debugging tool rather than as a formal benchmarking system.

---

## Join Strategies

The Olist pipeline performs several joins:

```text
Delivered Orders
       |
       +-- Order Items
       |
       +-- Products
       |
       +-- Customers
```

### Orders and Order Items

The join between delivered orders and order items was observed using a `SortMergeJoin`.

Conceptually, the execution follows:

```text
Orders
  ↓
Filter
  ↓
Exchange
  ↓
Sort
     SortMergeJoin
  /
Sort
  ↑
Exchange
  ↑
Order Items
```

A `SortMergeJoin` requires data to be partitioned and sorted according to the join key.

This can introduce shuffle and sorting work.

---

## Join Keys

The main join keys are:

```text
orders.order_id
        ↕
order_items.order_id
```

```text
order_items.product_id
        ↕
products.product_id
```

```text
orders.customer_id
        ↕
customers.customer_id
```

These joins are necessary to construct the enriched analytical dataset.

---

## Shuffle Behavior

Shuffle is one of the important performance characteristics of this pipeline.

Operations that can involve shuffle include:

- Sort-merge joins
- `groupBy()`
- `countDistinct()`
- `orderBy()`

For example:

```python
df.groupBy("customer_unique_id").agg(...)
```

requires records belonging to the same customer to be brought together for aggregation.

Similarly:

```python
.orderBy("total_spent", ascending=False)
```

requires global ordering and can introduce additional distributed work.

Shuffle is therefore expected in several parts of the pipeline.

---

## Analytics Workloads

The analytics layer performs several aggregations:

```text
Customer Revenue
        ↓
groupBy(customer_unique_id)

Product Revenue
        ↓
groupBy(product_id)

Category Revenue
        ↓
groupBy(product_category_name)

State Revenue
        ↓
groupBy(customer_state)
```

Some analytics also use:

```text
countDistinct(order_id)
```

which can require additional aggregation work.

The project intentionally keeps these operations in Spark rather than collecting the entire dataset into Python.

---

## Parquet Output

The enriched dataset is written to Parquet:

```text
s3a://olist-bigdata-project-2026-8472/processed/olist/
```

The processed output was observed in S3 as multiple Parquet part files together with the `_SUCCESS` marker.

Using Parquet provides a columnar representation for the processed analytical dataset and avoids repeatedly reading the original CSV source for downstream analytics.

---

## Partitioning

The processed output is written by Spark as multiple Parquet part files.

The current observed S3 output contained:

```text
_SUCCESS
part-00000
part-00001
...
part-00015
```

This represents 16 output part files from the observed pipeline execution.

The project does not currently implement explicit business-key partitioning such as:

```text
partitionBy("customer_state")
```

This is intentional at the current stage. The dataset is moderate in size, and the project is focused on understanding Spark processing before introducing more advanced storage optimization.

---

## Runtime Observations

The current pipeline was executed on a local development machine.

The full Olist processing pipeline completed in approximately the range observed during development, with a typical full run taking around 10 minutes in the current setup.

Runtime can vary depending on:

- Local CPU availability
- Spark execution state
- S3 network behavior
- Number of Spark actions
- Validation settings
- File-system I/O
- Current machine workload

Therefore, the runtime should be treated as an environment-specific observation rather than a benchmark.

---

## S3 Performance Observations

The pipeline was also tested against Amazon S3 using the Hadoop S3A connector.

A direct Spark read of the Olist orders dataset successfully loaded:

```text
99,441 rows
```

The project also verified the processed Parquet output directly in S3.

S3 access therefore works as the current storage layer for both:

```text
S3 Raw
   ↓
Spark
   ↓
S3 Processed
```

S3-related performance can vary from local filesystem performance because object storage introduces network I/O and remote filesystem behavior.

---

## Validation Performance

The validation layer contains checks that use Spark actions such as:

```python
df.filter(...).count()
```

Each such action requires Spark to evaluate the relevant computation.

For example:

```text
Required-column validation
        ↓
Null validation
        ↓
Positive-value validation
        ↓
Minimum-row validation
```

These checks improve data quality but can increase execution time when each check scans the dataset independently.

This represents an important trade-off:

```text
More validation
      ↓
Higher data quality confidence
      ↓
Potentially more Spark actions
      ↓
Higher execution cost
```

A future optimization could combine validation logic into fewer Spark passes where appropriate.

---

## Diagnostic Counts

The pipeline contains an optional flag:

```python
SHOW_COUNTS = False
```

When enabled, the source datasets are counted individually.

This is useful during development:

```text
Orders
Customers
Order Items
Products
```

However, each `count()` is a Spark action.

For normal execution, the flag is disabled to avoid unnecessary computation.

---

## Validation Toggle

The pipeline also contains:

```python
RUN_VALIDATION = False
```

This allows data-quality validation to be enabled when required without forcing the checks during every development run.

The validation checks were successfully executed during verification.

The checks confirmed that the enriched dataset satisfied the configured data-quality rules.

---

## Performance Trade-offs

The current project intentionally favors clarity and maintainability over aggressive optimization.

Examples include:

### Separate validation functions

Advantages:

- Easy to understand
- Reusable
- Easy to test
- Clear error messages

Trade-off:

- Individual checks can trigger additional Spark actions.

### Multiple analytics operations

Advantages:

- Clear separation of business metrics
- Easy to understand and extend

Trade-off:

- Each action can result in additional computation.

### Parquet storage

Advantages:

- Columnar analytical format
- Better suited to downstream Spark analytics than raw CSV

Trade-off:

- Adds a processing/write stage before analytics.

### S3 storage

Advantages:

- Cloud-based object storage
- Durable storage layer
- Separates storage from compute

Trade-off:

- Remote I/O introduces network and object-storage overhead.

---

## Current Performance Bottlenecks

The current project is not large enough to require extensive optimization.

The main areas that could affect runtime are:

1. Repeated Spark actions such as `count()`.
2. Shuffle-heavy joins.
3. Aggregations and `countDistinct()`.
4. Global `orderBy()` operations.
5. S3 network I/O.
6. Local-machine CPU and memory limitations.

These are more relevant to understanding Spark execution than to optimizing the current dataset.

---

## Future Optimization Opportunities

If the dataset grows substantially, the following optimizations could be evaluated.

### Reduce unnecessary actions

Avoid repeated diagnostic operations such as:

```python
df.count()
```

when the result is not required.

### Cache reused DataFrames

A frequently reused DataFrame could potentially be cached:

```python
df.cache()
```

This should only be done when reuse justifies the additional memory usage.

### Reduce unnecessary shuffles

Join and aggregation strategies can be reviewed as the dataset grows.

### Consider broadcast joins

If one side of a join is sufficiently small, a broadcast join could reduce shuffle.

This should be based on actual dataset size and Spark execution plans rather than applied automatically.

### Tune partition counts

Spark partitioning can be adjusted when the workload or cluster size requires it.

### Use optimized lakehouse storage

A future Delta Lake implementation could provide additional capabilities for larger analytical workloads.

### Move compute to a distributed environment

Databricks is planned as a future managed Spark environment.

---

## What Was Actually Measured vs. What Is Planned

The current project distinguishes observed behavior from future optimization.

### Observed

- Olist dataset processing with PySpark.
- Local Spark execution using `local[*]`.
- Delivered-order filtering.
- Multiple joins.
- Sort-merge join behavior.
- Shuffle-producing operations.
- Parquet output.
- 16 observed Parquet part files.
- S3 raw and processed storage.
- Data-quality validation.
- Spark UI inspection.
- Approximately 10-minute full pipeline runtime in the current development environment.

### Planned / Not Yet Benchmarked

- Formal runtime comparison between different partition counts.
- Broadcast-join benchmarking.
- Cache vs. non-cache comparison.
- Cluster-scale performance testing.
- Databricks performance benchmarking.
- Delta Lake performance comparison.
- Large-scale load testing.

No performance improvement is claimed for these future items until they are actually measured.

---

## Performance Lessons

The project provided several practical Spark performance lessons:

1. **Transformations are lazy.**
   Spark builds an execution plan until an action is triggered.

2. **Actions cause computation.**
   Repeated `count()`, `show()`, and `write()` operations can result in repeated work.

3. **Joins can cause shuffles.**
   Sort-merge joins require data exchange and sorting.

4. **Aggregations can cause shuffles.**
   `groupBy()` and `countDistinct()` require data to be brought together by key.

5. **Global ordering can be expensive.**
   `orderBy()` can require substantial distributed work.

6. **Object storage introduces I/O considerations.**
   Reading and writing through S3 involves remote storage and network communication.

7. **Optimization should follow measurement.**
   Spark execution plans and the Spark UI should be inspected before changing partitioning, caching, or join strategies.

---

## Summary

The current Olist pipeline is primarily a learning and portfolio project rather than a production-scale benchmark.

Its performance analysis demonstrates how Spark executes:

```text
S3
 ↓
PySpark
 ↓
Filtering
 ↓
Joins
 ↓
Shuffle
 ↓
Aggregations
 ↓
Parquet
 ↓
Analytics
```

The main performance characteristics observed are:

- Local Spark execution using `local[*]`
- Shuffle-producing joins and aggregations
- Multiple Spark actions
- Parquet output split across multiple part files
- Remote S3 I/O
- Additional computation introduced by validation and diagnostic counts

The current architecture is intentionally kept simple. Future versions can introduce more advanced optimization, distributed compute, Delta Lake, and Databricks once there is a clear need and measurable workload to optimize.