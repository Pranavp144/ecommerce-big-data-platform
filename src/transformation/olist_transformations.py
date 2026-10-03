from pyspark.sql.functions import col

def create_enriched_orders(
        orders,
        customers,
        order_items,
        products
):
    """
    create an enriched olist transaction dataset.
    steps:
    1 keep delivered orders.
    2 join orders with order items
    3 join product information
    4 join customer information
    5 calculate total item cost"""
    
    # 1. Keep only delivered orders
    delivered_orders = orders.filter(
        col("order_status") == "delivered")

    # 2. Join orders with order items
    enriched_orders = delivered_orders.join(
        order_items,
        on="order_id",
        how="inner"
    )

    # 3. Join product information
    enriched_orders = enriched_orders.join(
        products,
        on="product_id",
        how="left"
    )

    # 4. Join customer information
    enriched_orders = enriched_orders.join(
        customers,
        on="customer_id",
        how="left"
    )

    # 5. Calculate total item cost
    enriched_orders = enriched_orders.withColumn(
        "total_item_cost",
        col("price") * col("freight_value")
    )

    return enriched_orders