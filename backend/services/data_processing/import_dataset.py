from pathlib import Path

from django.contrib.auth import get_user_model

from services.data_processing.csv_loader import load_csv
from services.data_processing.bulk_insert import bulk_insert_transactions

User = get_user_model()
BASE_DIR = Path(__file__).resolve().parent.parent.parent
CSV_PATHS = [
    BASE_DIR / "datasets/raw/personal_finance_ml.csv",
    BASE_DIR / "datasets/raw/personal_finance.csv",
]


def _find_dataset_path() -> Path | None:
    for path in CSV_PATHS:
        if path.exists():
            return path
    return None


def import_transactions(user_email: str | None = None, username: str | None = None) -> int:
    """Import the selected Kaggle dataset into PostgreSQL transactions.

    Parameters
    ----------
    user_email:
        Email of the user to assign imported transactions to.
    username:
        Username of the user to assign imported transactions to.

    Returns
    -------
    int
        Number of imported Transaction records.
    """
    if not user_email and not username:
        raise ValueError("Either user_email or username must be provided.")

    try:
        if username:
            user = User.objects.get(username=username)
        else:
            user = User.objects.get(email=user_email)
    except User.DoesNotExist as exc:
        raise ValueError(f"User not found: {exc}") from exc

    dataset_path = _find_dataset_path()
    if dataset_path is None:
        raise FileNotFoundError(
            "Could not find dataset. Expected one of: "
            "backend/datasets/raw/personal_finance_ml.csv or backend/datasets/raw/personal_finance.csv"
        )

    df = load_csv()
    if df is None:
        raise RuntimeError("Failed to load the dataset. See earlier error logs.")

    inserted_count = bulk_insert_transactions(df, user)
    return inserted_count
