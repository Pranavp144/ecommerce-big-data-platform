from pyspark.sql import SparkSession
import pytest

from src.validation.olist_validation import (
    validate_required_columns,
    validate_no_nulls,
    validate_positive_values,
    validate_minimum_rows
)


def create_test_spark():
    return (
        SparkSession.builder
        .appName("ValidationTests")
        .master("local[2]")
        .getOrCreate()
    )


def test_validate_required_columns():
    spark = create_test_spark()

    data = [
        ("1001", "C001", 100.0)
    ]

    columns = ["order_id", "customer_id", "price"]

    df = spark.createDataFrame(data, columns)

    assert validate_required_columns(
        df,
        ["order_id", "customer_id", "price"]
    )

    with pytest.raises(ValueError):
        validate_required_columns(
            df,
            ["order_id", "customer_id", "quantity"]
        )

    spark.stop()


def test_validate_no_nulls():
    spark = create_test_spark()

    data = [
        ("1001", "C001"),
        ("1002", None)
    ]

    columns = ["order_id", "customer_id"]

    df = spark.createDataFrame(data, columns)

    with pytest.raises(ValueError):
        validate_no_nulls(
            df,
            ["customer_id"]
        )

    spark.stop()


def test_validate_positive_values():
    spark = create_test_spark()

    data = [
        ("1001", 100.0),
        ("1002", -50.0)
    ]

    columns = ["order_id", "price"]

    df = spark.createDataFrame(data, columns)

    with pytest.raises(ValueError):
        validate_positive_values(
            df,
            ["price"]
        )

    spark.stop()


def test_validate_minimum_rows():
    spark = create_test_spark()

    data = [
        ("1001",),
        ("1002",)
    ]

    columns = ["order_id"]

    df = spark.createDataFrame(data, columns)

    with pytest.raises(ValueError):
        validate_minimum_rows(
            df,
            3
        )

    assert validate_minimum_rows(df, 2)

    spark.stop()