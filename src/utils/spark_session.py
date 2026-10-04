# from pyspark.sql import SparkSession


# def create_spark_session(app_name):
#     """
#     Create and return a SparkSession.
#     """

#     spark = (
#         SparkSession.builder
#         .appName(app_name)
#         .master("local[*]")
#         .getOrCreate()
#     )

#     return spark

from pyspark.sql import SparkSession


def create_spark_session(app_name):
    """
    Create and return a SparkSession.
    """

    spark = (
        SparkSession.builder
        .appName(app_name)
        .master("local[*]")
        .config(
            "spark.jars.packages",
            "org.apache.hadoop:hadoop-aws:3.5.0"
        )
        .getOrCreate()
    )

    return spark