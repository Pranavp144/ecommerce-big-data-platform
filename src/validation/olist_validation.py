from pyspark.sql.functions import col


def validate_required_columns(df, required_columns):
    """
    Check whether all required columns exist in the DataFrame.
    """

    missing_columns = [
        column for column in required_columns
        if column not in df.columns
    ]

    if missing_columns:
        raise ValueError(
            f"Missing required columns: {missing_columns}"
        )

    return True


def validate_no_nulls(df, columns):
    """
    Check that specified columns do not contain null values.
    """

    for column in columns:
        null_count = df.filter(
            col(column).isNull()
        ).count()

        if null_count > 0:
            raise ValueError(
                f"Column '{column}' contains {null_count} null values."
            )

    return True


def validate_positive_values(df, columns):
    """
    Check that specified numeric columns contain only
    positive values.
    """

    for column in columns:
        invalid_count = df.filter(
            col(column) < 0
        ).count()

        if invalid_count > 0:
            raise ValueError(
                f"Column '{column}' contains "
                f"{invalid_count} non-positive values."
            )

    return True


def validate_minimum_rows(df, minimum_rows):
    """
    Ensure that the DataFrame contains at least
    the expected minimum number of rows.
    """

    row_count = df.count()

    if row_count < minimum_rows:
        raise ValueError(
            f"Expected at least {minimum_rows} rows, "
            f"but found {row_count}."
        )

    return True