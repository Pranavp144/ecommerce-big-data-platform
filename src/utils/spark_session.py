from pyspark.sql import SparkSession


def create_spark_session(app_name):
    """
    Create and return a SparkSession.
    """

    spark = (
        SparkSession.builder
        .appName(app_name)
        .master("local[*]")
        .getOrCreate()
    )

    return spark