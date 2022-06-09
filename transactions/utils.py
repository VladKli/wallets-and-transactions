from django.db.models import F

from walets.models import Wallet

BANK_COMMISSION = 0.1
TRANSFER_AMOUNT_WITH_COMMISSION = 0.9


def balance_transfer(
    sender_wallet,
    receiver_wallet,
    sender_user,
    receiver_wallet_name,
    transfer_amount,
):
    """Balance transfers from sender wallet to receiver"""

    funds_amount = (
        transfer_amount
        if Wallet.objects.filter(user=sender_user, name=receiver_wallet_name)
        else (float(transfer_amount) * TRANSFER_AMOUNT_WITH_COMMISSION)
    )
    commission = (
        0
        if Wallet.objects.filter(user=sender_user, name=receiver_wallet_name)
        else BANK_COMMISSION
    )
    sender_wallet.update(balance=F("balance") - transfer_amount)
    receiver_wallet.update(balance=F("balance") + funds_amount)
    return commission
