from pyspark.sql.functions import col

from utils.spark_session import create_spark_session
from ingestion.read_data import read_orders
from transformation.cleaning import clean_order_data
from analytics.customer_analysis import calculate_customer_metrics


spark = create_spark_session("ECommerceBigData")

print("Spark application started successfully.")

# 1. Read raw data
orders = read_orders(
    spark,
    "hdfs://localhost:9000/ecommerce/raw/orders_dirty.csv"
)

print("Raw orders:")
orders.show()

# 2. Clean data
clean_orders = clean_order_data(orders)

print("Clean orders:")
clean_orders.show()

# 3. Create business column
clean_orders = clean_orders.withColumn(
    "total_amount",
    col("quantity") * col("price")
)

# 4. Write cleaned data to parquet
clean_orders.write.mode("overwrite").parquet(
    "hdfs://localhost:9000/ecommerce/processed/orders"
)

#5. Read processed data from Parquet
processed_orders = spark.read.parquet(
    "hdfs://localhost:9000/ecommerce/processed/orders"
)
print("number of partitions:", processed_orders.rdd.getNumPartitions())
# tells spark that treat this dataframe as a table called orders, it doesnt create a physical table in hdfs
processed_orders.createOrReplaceTempView("orders")

# sql query 
result = spark.sql("""
    select 
        customer_id,
        SUM(total_amount) AS total_revenue
    From orders
    group by customer_id
    order by total_revenue desc
    
""")
result.show()

product_sales = spark.sql("""
    select 
        product,
        sum(quantity) as units_sold,
        sum(total_amount) as revenue
    from orders
    group by product
    order by revenue desc
""")
print (" Product Sales :")
product_sales.show()

business_metrics = spark.sql("""
    select 
        count(*) as total_orders,
        sum(total_amount) as total_revenue,
        avg(total_amount) as average_order_value
    from orders
    
""")
print (" business metrics :")
business_metrics.show()


print("Processed orders form Parquet:")
processed_orders.show()

#6. calculate customer analytics
customer_metrics = calculate_customer_metrics(
    processed_orders
)
print("Customer metrics:")
customer_metrics.show()

spark.stop()