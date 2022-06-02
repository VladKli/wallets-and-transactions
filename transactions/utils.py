from django.db.models import F
from rest_framework import status
from rest_framework.response import Response

from walets.models import Wallet


def transaction_validation(
    serializer, sender_wallet, receiver_wallet, request
) -> Response:
    if (
        sender_wallet.exists()
        and sender_wallet.filter(balance__gte=request.data["transfer_amount"])
        and sender_wallet.values("currency").intersection(
            receiver_wallet.values("currency")
        )
    ):
        if Wallet.objects.filter(user=request.user).filter(
            name=request.data["receiver"]
        ):
            sender_wallet.update(
                balance=F("balance") - request.data["transfer_amount"]
            )
            receiver_wallet.update(
                balance=F("balance") + request.data["transfer_amount"]
            )
            if serializer.is_valid():
                serializer.save()
                return Response(
                    serializer.data, status=status.HTTP_201_CREATED
                )
        else:
            sender_wallet.update(
                balance=F("balance") - request.data["transfer_amount"]
            )
            receiver_wallet.update(
                balance=F("balance")
                + float(request.data["transfer_amount"]) * 0.9
            )
            if serializer.is_valid():
                serializer.validated_data["commission"] = (
                    float(request.data["transfer_amount"]) * 0.1
                )
                serializer.save()
                return Response(
                    serializer.data, status=status.HTTP_201_CREATED
                )
    return Response(
        "Impossible process transaction. Check wallets numbers, currency, balance amount.",
        status=status.HTTP_400_BAD_REQUEST,
    )
