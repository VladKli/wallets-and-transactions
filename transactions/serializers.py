from decimal import Decimal

from rest_framework import serializers
from rest_framework.exceptions import ValidationError

from transactions.models import Transaction
from transactions.utils import balance_transfer, get_commission
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

    def get_sender_wallet(self, validated_data):
        sender_wallet = Wallet.objects.filter(
            user=self.context["request"].user,
            name=self.context["request"].data["sender"],
        )
        return sender_wallet

    def get_receiver_wallet(self, validated_data):
        receiver_wallet = Wallet.objects.filter(
            name=self.context["request"].data["receiver"]
        )
        return receiver_wallet

    def validate_sender(self, validated_data):
        """Validate if user is owner of a sender wallet"""

        sender_wallet = self.get_sender_wallet(validated_data)
        if not sender_wallet.exists():
            raise ValidationError("You do not have such wallet")

    def validate_transfer_amount(self, validated_data):
        """Check if sender has enough balance"""

        sender_wallet = self.get_sender_wallet(validated_data)
        if not sender_wallet.filter(
            balance__gte=Decimal(
                self.context["request"].data["transfer_amount"]
            )
        ).exists():
            raise ValidationError("Not enough balance")

    def validate_currencies(self, validated_data):
        """Check if currencies are the same"""

        sender_wallet = self.get_sender_wallet(validated_data)
        receiver_wallet = self.get_receiver_wallet(validated_data)
        if not (
            sender_wallet.values("currency")
            .intersection(receiver_wallet.values("currency"))
            .exists()
        ):
            raise ValidationError("Currencies should be the same")

    def create(self, validated_data):
        """Create transaction for current logged user"""

        sender_user = self.context["request"].user
        receiver_wallet_name = self.context["request"].data["receiver"]
        sender_wallet = self.get_sender_wallet(validated_data)
        receiver_wallet = self.get_receiver_wallet(validated_data)
        transfer_amount = self.context["request"].data["transfer_amount"]

        validated_data["sender"] = Wallet.objects.get(
            name=self.context["request"].data["sender"]
        )
        validated_data["receiver"] = Wallet.objects.get(
            name=self.context["request"].data["receiver"]
        )
        validated_data["transfer_amount"] = transfer_amount
        validated_data["commission"] = get_commission(
            sender_user, receiver_wallet_name
        ) * Decimal(transfer_amount)

        self.validate_currencies(validated_data)

        balance_transfer(
            sender_wallet,
            receiver_wallet,
            sender_user,
            receiver_wallet_name,
            transfer_amount,
        )

        transactions = Transaction.objects.create(**validated_data)
        transactions.save()
        return validated_data
