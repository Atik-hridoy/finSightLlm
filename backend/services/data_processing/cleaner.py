import pandas as pd


def clean_dataframe(df: pd.DataFrame) -> pd.DataFrame:
    df = df.copy()

    # Remove duplicates and empty rows.
    df = df.drop_duplicates()
    df = df.dropna(how="all")

    # Fill missing numerical values with the median for that column.
    numeric_columns = df.select_dtypes(include=["number"]).columns
    for col in numeric_columns:
        df[col] = df[col].fillna(df[col].median())

    # Fill missing categorical values with a safe placeholder.
    categorical_columns = df.select_dtypes(include=["object"]).columns
    for col in categorical_columns:
        df[col] = df[col].fillna("Unknown")

    return df
