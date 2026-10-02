# Performance Analysis

Performance benchmarking will be added as the project develops.

## Planned Experiments

### 1. CSV vs Parquet

Compare the performance of reading equivalent datasets from CSV and Parquet.

### 2. Partitioning

Measure how different partition counts affect processing time.

### 3. Shuffle

Analyze operations such as:

- `groupBy`
- `join`
- `distinct`
- `orderBy`

and observe their effect on Spark stages.

### 4. Caching

Compare workloads with and without caching.

### 5. Broadcast Joins

Compare a normal join with a broadcast join when the smaller dataset is suitable for broadcasting.

### 6. Execution Plans

Use Spark's execution-plan tools to understand how Spark optimizes queries.

## Evidence

Performance results will be measured experimentally and documented here.

No benchmark values are included until they have been measured on the project environment.
