from django.contrib.auth.models import User
from rest_framework import serializers

from walets.models import Wallet


class WalletCreateSerializer(serializers.ModelSerializer):
    """
    Serializer for create wallet
    """

    name = serializers.CharField(
        max_length=8, default=Wallet.wallet_name_generator
    )
    balance = serializers.DecimalField(
        max_digits=100, decimal_places=2, default=0
    )
    user = serializers.PrimaryKeyRelatedField(read_only=True)

    class Meta:
        model = Wallet
        fields = (
            "id",
            "name",
            "user",
            "type",
            "currency",
            "balance",
            "created_on",
            "modified_on",
        )

    def create(self, validated_data):
        """bonus from bank: if wallet currency USD or EUR - balance=3.00, if RUB - balance=100.00)"""
        if validated_data["currency"] == "RUB":
            validated_data["balance"] = 100
        else:
            validated_data["balance"] = 3
        user = self.context["request"].user
        wallet = Wallet.objects.create(**validated_data, user=user)
        wallet.save()
        return validated_data


class UserSerializer(serializers.ModelSerializer):
    """User serizlizer"""

    owner = serializers.PrimaryKeyRelatedField(
        many=True, queryset=Wallet.objects.all()
    )

    class Meta:
        model = User
        fields = ["id", "username", "owner"]
