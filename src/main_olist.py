from utils.spark_session import create_spark_session
from ingestion.read_olist_data import read_olist_data
from transformation.olist_transformations import create_enriched_orders
from analytics.olist_analysis import (
    calculate_customer_revenue,
    calculate_product_revenue,
    calculate_business_metrics
)
from validation.olist_validation import (
    validate_required_columns,
    validate_no_nulls,
    validate_positive_values,
    validate_minimum_rows
)



# HDFS_BASE_PATH = "hdfs://localhost:9000/ecommerce/raw/olist"
S3_BASE_PATH = "s3a://olist-bigdata-project-2026-8472/raw/olist"

# PROCESSED_PATH = "hdfs://localhost:9000/ecommerce/processed/olist"
PROCESSED_PATH = "s3a://olist-bigdata-project-2026-8472/processed/olist"


def main():

    # 1. Create Spark session
    spark = create_spark_session("OlistECommercePipeline")

    print("Spark application started.")

    # 2. Read source datasets
    orders, customers, order_items, products = read_olist_data(
        spark,
        S3_BASE_PATH
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
    print("Running data quality checks...")

    validate_required_columns(
        enriched_orders,
        [
            "order_id",
            "customer_id",
            "product_id",
            "price",
            "freight_value",
            "total_item_cost"
        ]
    )

    validate_no_nulls(
        enriched_orders,
        [
            "order_id",
            "customer_id",
            "product_id"
        ]
)

    validate_positive_values(
        enriched_orders,
        [
            "price",
            "freight_value",
            "total_item_cost"
        ]
)

    validate_minimum_rows(
        enriched_orders,
        100000
)

    print("All data quality checks passed.")

    print("Enriched dataset created.")
    print("Enriched rows:", enriched_orders.count())

    # from pyspark.sql.functions import col
    
    # invalid_freight = enriched_orders.filter(
    # col("freight_value") <= 0
    # )

    # print("Invalid freight rows:", invalid_freight.count())
    
    # invalid_freight.select(
    #     "order_id",
    #     "product_id",
    #     "price",
    #     "freight_value",
    #     "total_item_cost"
    #     ).show(20)
    
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
    
    

    # 9.Keep Spark running for inspection
    input("Press Enter to stop Spark...")
    spark.stop()

    print("Spark application stopped.")


if __name__ == "__main__":
    main()