from django.db import models

from walets.models import Wallet


class Transaction(models.Model):
    """Transaction model"""

    sender = models.ForeignKey(
        Wallet,
        on_delete=models.CASCADE,
        related_name="sender",
        to_field="name",
    )
    receiver = models.ForeignKey(
        Wallet,
        on_delete=models.CASCADE,
        related_name="receiver",
        to_field="name",
    )
    transfer_amount = models.DecimalField(
        max_digits=10, decimal_places=2, default=0.00
    )
    commission = models.DecimalField(
        max_digits=3, decimal_places=2, default=0.00, editable=False
    )
    status = models.CharField(
        choices=[("paid", "PAID"), ("failed", "FAILED")],
        max_length=6,
        default="paid",
        editable=False,
    )
    timestamp = models.DateTimeField(
        auto_now_add=True, null=True, editable=False
    )
