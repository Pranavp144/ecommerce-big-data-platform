def read_orders(spark, path):
    """
    Read raw order data from a CSV file.
    """

    return spark.read.csv(
        path,
        header=True,
        inferSchema=True
    )


def read_customers(spark, path):
    """
    Read customer data from a CSV file.
    """

    return spark.read.csv(
        path,
        header=True,
        inferSchema=True
    )