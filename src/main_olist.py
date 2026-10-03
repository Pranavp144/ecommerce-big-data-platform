from utils.spark_session import create_spark_session
from ingestion.read_olist_data import read_olist_data
from transformation.olist_transformations import create_enriched_orders
from analytics.olist_analysis import (
    calculate_customer_revenue,
    calculate_product_revenue,
    calculate_business_metrics
)


HDFS_BASE_PATH = "hdfs://localhost:9000/ecommerce/raw/olist"
PROCESSED_PATH = "hdfs://localhost:9000/ecommerce/processed/olist"


def main():

    # 1. Create Spark session
    spark = create_spark_session("OlistECommercePipeline")

    print("Spark application started.")

    # 2. Read source datasets
    orders, customers, order_items, products = read_olist_data(
        spark,
        HDFS_BASE_PATH
    )

    print("Source datasets loaded.")

    print("Orders:", orders.count())
    print("Customers:", customers.count())
    print("Order items:", order_items.count())
    print("Products:", products.count())

    # 3. Create enriched transaction dataset
    enriched_orders = create_enriched_orders(
        orders,
        customers,
        order_items,
        products
    )

    print("Enriched dataset created.")
    print("Enriched rows:", enriched_orders.count())

    # 4. Write processed data to Parquet
    enriched_orders.write \
        .mode("overwrite") \
        .parquet(PROCESSED_PATH)

    print("Processed data written to Parquet.")

    # 5. Read processed data
    processed_orders = spark.read.parquet(
        PROCESSED_PATH
    )

    print("Processed data loaded from Parquet.")

    # 6. Customer analytics
    customer_revenue = calculate_customer_revenue(
        processed_orders
    )

    print("Customer analytics calculated.")
    customer_revenue.orderBy(
        "total_spent",
        ascending=False
    ).show(10)

    # 7. Product analytics
    product_revenue = calculate_product_revenue(
        processed_orders
    )

    print("Product analytics calculated.")
    product_revenue.orderBy(
        "product_revenue",
        ascending=False
    ).show(10)

    # 8. Business metrics
    business_metrics = calculate_business_metrics(
        processed_orders
    )

    print("Business metrics:")
    business_metrics.show()

    # 9. Stop Spark
    spark.stop()

    print("Spark application stopped.")


if __name__ == "__main__":
    main()