from rest_framework import serializers
from rest_framework.exceptions import ValidationError

from transactions.models import Transaction
from walets.models import Wallet


class TransactionSerializer(serializers.ModelSerializer):
    """Transaction serializer"""

    class Meta:
        model = Transaction
        fields = [
            "id",
            "sender",
            "receiver",
            "transfer_amount",
            "commission",
            "status",
            "timestamp",
        ]

    def create(self, validated_data):
        """Create transaction for current logged user"""
        sender_wallet = Wallet.objects.filter(
            user=self.context["request"].user,
            name=validated_data["sender"].name,
        )
        receiver_wallet = Wallet.objects.filter(
            name=self.validated_data["receiver"].name
        )
        if not sender_wallet.filter(
            balance__gte=validated_data["transfer_amount"]
        ).exists():
            raise ValidationError("Not enough balance")
        if not (
            sender_wallet.values("currency")
            .intersection(receiver_wallet.values("currency"))
            .exists()
        ):
            raise ValidationError("Currencies should be the same")
        transactions = Transaction.objects.create(**validated_data)
        transactions.save()
        return validated_data
