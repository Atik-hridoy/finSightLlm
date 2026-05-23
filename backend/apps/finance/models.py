import uuid
from django.db import models
from django.conf import settings


class Transaction(models.Model):
    TRANSACTION_TYPES = [
        ("income", "Income"),
        ("expense", "Expense"),
    ]

    PAYMENT_METHODS = [
        ("card", "Card"),
        ("cash", "Cash"),
        ("transfer", "Transfer"),
        ("other", "Other"),
    ]

    id = models.UUIDField(
        primary_key=True,
        default=uuid.uuid4,
        editable=False,
    )
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
    )
    amount = models.DecimalField(max_digits=12, decimal_places=2)
    category = models.CharField(max_length=128, default="Unknown")
    transaction_type = models.CharField(
        max_length=10,
        choices=TRANSACTION_TYPES,
        default="expense",
    )
    payment_method = models.CharField(
        max_length=32,
        choices=PAYMENT_METHODS,
        default="card",
    )
    description = models.TextField(blank=True)
    transaction_date = models.DateField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-transaction_date", "-created_at"]

    def __str__(self):
        return f"{self.user} | {self.transaction_type} | {self.amount}"
