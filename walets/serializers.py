from django.contrib.auth.models import User
from rest_framework import serializers

from walets.models import Wallet


class WalletSerializer(serializers.ModelSerializer):
    """Wallet serizlizer"""

    class Meta:
        model = Wallet
        fields = [
            "id",
            "name",
            "type",
            "currency",
            "balance",
            "created_on",
            "modified_on",
        ]


class UserSerializer(serializers.ModelSerializer):
    """User serizlizer"""

    owner = serializers.PrimaryKeyRelatedField(
        many=True, queryset=Wallet.objects.all()
    )

    class Meta:
        model = User
        fields = ["id", "username", "owner"]
