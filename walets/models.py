import random
import string

from django.db import models


class Wallet(models.Model):
    """Wallet model"""

    MAX_WALLETS = 5
    BANK_BONUS_USD_EUR = 3.00
    BANK_BONUS_RUB = 100.00

    PAYMENT_METHOD_VISA = "visa"
    PAYMENT_METHOD_MASTERCARD = "mastercard"
    TYPE_CHOICES = (
        (PAYMENT_METHOD_VISA, "Visa"),
        (PAYMENT_METHOD_MASTERCARD, "Mastercard"),
    )

    CURRENCY_METHOD_RUB = "RUB"
    CURRENCY_METHOD_USD = "USD"
    CURRENCY_METHOD_EUR = "EUR"
    CURRENCY_CHOICES = (
        (CURRENCY_METHOD_RUB, "RUB"),
        (CURRENCY_METHOD_USD, "USD"),
        (CURRENCY_METHOD_EUR, "EUR"),
    )

    def wallet_name_generator(
        size=8, chars=string.ascii_uppercase + string.digits
    ):
        """Generate unique code for wallet name"""
        my_code = "".join(random.choice(chars) for _ in range(size))
        if Wallet.objects.filter(name=my_code).exists():
            return Wallet.wallet_name_generator(size=8, chars=string.digits)
        else:
            return my_code

    name = models.SlugField(
        max_length=8,
        default=wallet_name_generator,
        editable=False,
        unique=True,
    )
    type = models.CharField(
        choices=TYPE_CHOICES, max_length=10, default="visa"
    )
    currency = models.CharField(
        choices=CURRENCY_CHOICES, max_length=3, default="rub"
    )
    balance = models.DecimalField(
        max_digits=100, decimal_places=2, default=0.00, editable=False
    )
    user = models.ForeignKey(
        "auth.User", related_name="owner", on_delete=models.CASCADE
    )
    created_on = models.DateTimeField(auto_now_add=True, null=True)
    modified_on = models.DateTimeField(auto_now=True, null=True)

    def __repr__(self):
        """Return name repr"""
        return self.name
