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
        .config(
            "spark.hadoop.fs.s3a.aws.credentials.provider",
            "org.apache.hadoop.fs.s3a.auth.ProfileAWSCredentialsProvider"
        )
        # .config(
        #     "spark.hadoop.fs.s3a.input.stream.type",
        #     "classic"
        # )
        .getOrCreate()
    )

    return spark