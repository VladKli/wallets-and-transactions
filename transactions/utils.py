from decimal import Decimal

from django.db.models import F

from walets.models import Wallet

NO_COMMISSION = 0
BANK_COMMISSION = 0.1
TRANSFER_AMOUNT_WITH_COMMISSION = 0.9


def get_commission(sender_user, receiver_wallet_name):
    """Get commission"""

    commission = (
        NO_COMMISSION
        if Wallet.objects.filter(user=sender_user, name=receiver_wallet_name)
        else BANK_COMMISSION
    )
    return Decimal(commission)


def get_funds_amount(sender_user, receiver_wallet_name, transfer_amount):
    """Get funds transfer amount"""

    funds_amount = (
        transfer_amount
        if Wallet.objects.filter(user=sender_user, name=receiver_wallet_name)
        else (
            Decimal(transfer_amount) * Decimal(TRANSFER_AMOUNT_WITH_COMMISSION)
        )
    )
    return funds_amount


def balance_transfer(
    sender_wallet,
    receiver_wallet,
    sender_user,
    receiver_wallet_name,
    transfer_amount,
):
    """Balance transfers from sender wallet to receiver"""

    funds_amount = get_funds_amount(
        sender_user, receiver_wallet_name, transfer_amount
    )
    sender_wallet.update(balance=F("balance") - transfer_amount)
    receiver_wallet.update(balance=F("balance") + funds_amount)
