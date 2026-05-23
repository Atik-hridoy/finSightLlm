from datetime import datetime, date

import pandas as pd

from apps.finance.models import Transaction


def _parse_date(value):
    if value is None or (isinstance(value, float) and pd.isna(value)):
        return None
    if isinstance(value, datetime):
        return value.date()
    if isinstance(value, date):
        return value

    try:
        parsed = pd.to_datetime(value, errors="coerce")
        return parsed.date() if not pd.isna(parsed) else None
    except Exception:
        return None


def bulk_insert_transactions(df: pd.DataFrame, user):
    transactions = []

    for _, row in df.iterrows():
        tx_date = _parse_date(
            row.get("record_date")
            or row.get("date")
            or row.get("transaction_date")
        )
        category = row.get("category") or "Unknown"
        payment_method = row.get("payment_method") or "card"
        description = "Imported from CSV"

        income_value = None
        if "income" in row and pd.notna(row["income"]):
            income_value = float(row["income"])
        elif "monthly_income_usd" in row and pd.notna(row["monthly_income_usd"]):
            income_value = float(row["monthly_income_usd"])

        if income_value not in (None, 0):
            transactions.append(
                Transaction(
                    user=user,
                    amount=income_value,
                    category="Income",
                    transaction_type="income",
                    payment_method=payment_method,
                    description=description,
                    transaction_date=tx_date,
                )
            )

        expense_value = None
        if "expenses" in row and pd.notna(row["expenses"]):
            expense_value = float(row["expenses"])
        elif "monthly_expenses_usd" in row and pd.notna(row["monthly_expenses_usd"]):
            expense_value = float(row["monthly_expenses_usd"])

        if expense_value not in (None, 0):
            transactions.append(
                Transaction(
                    user=user,
                    amount=-abs(expense_value),
                    category=category,
                    transaction_type="expense",
                    payment_method=payment_method,
                    description=description,
                    transaction_date=tx_date,
                )
            )

    Transaction.objects.bulk_create(transactions, batch_size=1000)
    return len(transactions)
