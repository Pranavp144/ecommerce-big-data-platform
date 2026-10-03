from pyspark.sql.functions import sum, countDistinct

def calculate_customer_revenue(df):
    """
    calculate revenue and order metrics for each customer.
    """

    return (
        df.groupBy("customer_unique_id")
        .agg(
            sum("price").alias("total_spent"),
            countDistinct("order_id").alias("number_of_orders")
        )
    )
def calculate_product_revenue(df):
    """
    calculate revenue and order metrics for each product.
    """

    return (
        df.groupBy("product_id")
        .agg(
            sum("price").alias("product_revenue"),
            countDistinct("order_id").alias("number_of_orders")
        )
    )

def calculate_business_metrics(df):
    """
    calculate overall business metrics.
    """

    return (
        df.agg(
            sum("price").alias("total_product_revenue"),
            sum("freight_value").alias("total_freight"),
            sum("total_item_cost").alias("total_value"),
        )
    )