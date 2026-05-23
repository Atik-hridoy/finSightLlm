from pathlib import Path

import pandas as pd

BASE_DIR = Path(__file__).resolve().parent.parent.parent
RAW_DATASET_OPTIONS = [
    BASE_DIR / "datasets/raw/personal_finance_ml.csv",
    BASE_DIR / "datasets/raw/personal_finance.csv",
]


def load_csv():
    for path in RAW_DATASET_OPTIONS:
        if path.exists():
            try:
                df = pd.read_csv(path, low_memory=False)
                print(f"CSV Loaded Successfully from {path.name}")
                return df
            except Exception as exc:
                print(f"CSV Loading Error from {path.name}: {exc}")
                return None

    available = [str(path.name) for path in RAW_DATASET_OPTIONS]
    print(
        "CSV Loading Error: dataset file not found. Expected one of:",
        ", ".join(available),
    )
    return None
