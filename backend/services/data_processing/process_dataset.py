from .csv_loader import load_csv
from .cleaner import clean_dataframe
from .normalizer import normalize_transactions
from .feature_engineering import generate_features


def process_financial_dataset():
    df = load_csv()
    if df is None:
        return None

    df = clean_dataframe(df)
    df = normalize_transactions(df)
    df = generate_features(df)

    return df
