from pyspark.sql import DataFrame


def clean_order_data(df: DataFrame) -> DataFrame:
    """
    Clean raw e-commerce order data.

    Rules:
    1. Customer ID cannot be null.
    2. Quantity must be greater than zero.
    3. Price must be greater than zero.
    4. Order ID must be unique.
    """

    df = df.dropna(
        subset=["customer_id"]
    )

    df = df.filter(
        df.quantity > 0
    )

    df = df.filter(
        df.price > 0
    )

    df = df.dropDuplicates(
        ["order_id"]
    )

    return df