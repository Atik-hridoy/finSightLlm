"""financial_context.py

Functions that aggregate a user's transaction data into a compact dictionary
which can be consumed by the prompt builder.

Assumes a ``Transaction`` model exists in ``apps.finance.models`` with the
following fields (at minimum):
* ``user`` – ForeignKey to the auth user
* ``date`` – DateField or DateTimeField
* ``amount`` – DecimalField (positive for income, negative for expense)
* ``category`` – CharField describing the spend/income category

If the model differs, adjust the import and field names accordingly.
"""

from datetime import date, timedelta
from collections import defaultdict
from typing import Dict, List, Tuple

from django.db.models import Sum, F, Q
from django.db.models.functions import ExtractMonth

# Import the Transaction model – adjust the path if your app name differs.
try:
    from apps.finance.models import Transaction
except Exception:
    # Fallback placeholder for early development – returns empty data.
    Transaction = None


def _last_n_months(n: int = 1) -> List[date]:
    """Return the first day of the last *n* months (including the current month)."""
    today = date.today()
    months = []
    for i in range(n):
        month = (today.month - i - 1) % 12 + 1
        year = today.year - ((today.month - i - 1) // 12)
        months.append(date(year, month, 1))
    return months[::-1]


def get_financial_context(user) -> Dict:
    """Aggregate financial data for *user*.

    Returns a dictionary containing:
    * ``month`` – human readable month string (e.g. "2024-09")
    * ``total_expense`` – sum of negative amounts
    * ``total_income`` – sum of positive amounts
    * ``top_categories`` – list of (category, amount) sorted desc.
    * ``savings_rate`` – optional percentage of income saved.
    * ``anomalies`` – list of string descriptions of unusual spikes.
    """
    if Transaction is None:
        # No model available – return a minimal placeholder.
        return {
            "month": date.today().strftime("%Y-%m"),
            "total_expense": 0,
            "total_income": 0,
            "top_categories": [],
            "savings_rate": None,
            "anomalies": [],
            "monthly_expenses": [],
            "average_expense": 0.0,
            "risk_level": "low",
            "savings": 0.0,
        }

    # Filter transactions for the user for the current month.
    start_of_month = date.today().replace(day=1)
    qs = Transaction.objects.filter(user=user, date__gte=start_of_month)

    # Aggregate totals.
    totals = qs.aggregate(
        total_income=Sum('amount', filter=Q(amount__gt=0)),
        total_expense=Sum('amount', filter=Q(amount__lt=0)),
    )

    total_income = totals["total_income"] or 0
    total_expense = totals["total_expense"] or 0

    # Top spending categories (absolute expense amount).
    cat_sums = (
        qs.filter(amount__lt=0)
        .values('category')
        .annotate(spent=Sum('amount'))
        .order_by('spent')[:5]
    )
    top_categories: List[Tuple[str, float]] = [
        (c["category"], float(c["spent"])) for c in cat_sums
    ]

    monthly_expenses_qs = (
        qs.filter(amount__lt=0)
        .annotate(month=ExtractMonth('date'))
        .values('month')
        .annotate(total=Sum('amount'))
        .order_by('month')
    )
    monthly_expenses = [
        {"month": item["month"], "total": float(item["total"])}
        for item in monthly_expenses_qs
    ]

    average_expense = float(abs(total_expense)) / max(qs.count(), 1)
    savings = float(total_income + total_expense)

    savings_rate = None
    if total_income:
        savings_rate = ((total_income + total_expense) / total_income) * 100

    risk_level = "low"
    if total_expense > total_income:
        risk_level = "high"
    elif total_expense > (total_income * 0.8):
        risk_level = "medium"

    # Simple anomaly detection – any single category > 30% of total expense.
    anomalies = []
    expense_abs = abs(total_expense) if total_expense else 0
    for cat, amt in top_categories:
        if expense_abs and abs(amt) / expense_abs > 0.3:
            anomalies.append(f"High spend on {cat}: {_format_currency(amt)}")

    return {
        "month": date.today().strftime("%Y-%m"),
        "total_income": float(total_income),
        "total_expense": float(total_expense),
        "savings": savings,
        "top_categories": top_categories,
        "savings_rate": float(savings_rate) if savings_rate is not None else None,
        "anomalies": anomalies,
        "monthly_expenses": monthly_expenses,
        "average_expense": average_expense,
        "risk_level": risk_level,
    }

# Helper for formatting values used in anomalies.
def _format_currency(value):
    try:
        return f"${float(value):,.2f}"
    except Exception:
        return str(value)
