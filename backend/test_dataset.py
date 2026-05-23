from services.data_processing.process_dataset import process_financial_dataset


def main():
    df = process_financial_dataset()
    if df is None:
        print(
            "Dataset processing failed. Check that backend/datasets/raw/personal_finance_ml.csv "
            "or backend/datasets/raw/personal_finance.csv exists."
        )
        return

    print("Dataset processed successfully.")
    print(f"Rows: {len(df)}")
    print(f"Columns: {len(df.columns)}")
    print("Column names:", list(df.columns))
    print("\nFirst 5 rows:")
    print(df.head().to_string(index=False))

    feature_columns = [col for col in ["savings", "expense_ratio"] if col in df.columns]
    if feature_columns:
        print("\nDerived feature columns:", feature_columns)
        print(df[feature_columns].head().to_string(index=False))
    else:
        print("\nDerived feature columns were not created. Check the income/expenses column names.")


if __name__ == "__main__":
    main()
