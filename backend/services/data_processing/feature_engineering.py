import pandas as pd


def generate_features(df: pd.DataFrame) -> pd.DataFrame:
    df = df.copy()

    income_columns = [
        col for col in ["income", "monthly_income_usd", "monthly_income"]
        if col in df.columns
    ]
    expense_columns = [
        col for col in ["expenses", "monthly_expenses_usd", "monthly_expenses"]
        if col in df.columns
    ]

    if income_columns and expense_columns:
        income_col = income_columns[0]
        expense_col = expense_columns[0]

        df["savings"] = df[income_col] - df[expense_col]
        income = df[income_col].replace({0: pd.NA})
        df["expense_ratio"] = (df[expense_col] / income).fillna(0)

    return df
