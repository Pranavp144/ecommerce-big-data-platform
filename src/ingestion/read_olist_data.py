def read_olist_data(spark, base_path):
    """
    Read the core Olist datasets from HDFS.
    """

    orders = spark.read.csv(
        f"{base_path}/olist_orders_dataset.csv",
        header=True,
        inferSchema=True
    )

    customers = spark.read.csv(
        f"{base_path}/olist_customers_dataset.csv",
        header=True,
        inferSchema=True
    )

    order_items = spark.read.csv(
        f"{base_path}/olist_order_items_dataset.csv",
        header=True,
        inferSchema=True
    )

    products = spark.read.csv(
        f"{base_path}/olist_products_dataset.csv",
        header=True,
        inferSchema=True
    )

    return orders, customers, order_items, products