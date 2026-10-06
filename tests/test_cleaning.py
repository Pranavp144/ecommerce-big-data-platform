from pyspark.sql import SparkSession
from src.transformation.cleaning import clean_order_data

def create_test_spark():
    return(
        SparkSession.builder
        .appName("Cleaning Test")
        .master("local[2]")
        .getOrCreate()
    )
def test_clean_orders_data():
    spark = create_test_spark()
    data = [
        ("1001", "C001", 2, 100.0),
        ("1002", None, 1, 200.0),
        ("1003", "C002", -1, 300.0),
        ("1004", "C003", 2, -50.0),
        ("1001", "C001", 2, 100.0),
    ]
    columns = ["order_id",
                "customer_id",
                  "quantity",
                    "price"]
    df = spark.createDataFrame(data, columns)

    cleaned_df = clean_order_data(df)

    assert cleaned_df.count() == 1

    spark.stop()