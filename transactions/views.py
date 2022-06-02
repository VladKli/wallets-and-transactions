from django.db.models import F, Q
from django.http import HttpResponse
from rest_framework import generics, permissions
from rest_framework.response import Response

from transactions.models import Transaction
from transactions.serializers import TransactionSerializer
from walets.models import Wallet


class TransactionsList(generics.ListCreateAPIView):
    """Get wallet list, create wallet"""

    permission_classes = [permissions.IsAuthenticated]
    serializer_class = TransactionSerializer
    queryset = Transaction.objects.all()

    def list(self, request):
        """Get list of current logged user transactions"""
        queryset = self.queryset.filter(
            Q(sender__user=request.user) | Q(receiver__user=request.user)
        )
        serializer = TransactionSerializer(queryset, many=True)
        if queryset:
            return Response(serializer.data)
        return HttpResponse(status=204)

    def perform_create(self, serializer):
        """Create transaction for current logged user"""
        sender_wallet = Wallet.objects.filter(user=self.request.user).filter(
            name=self.request.data["sender"]
        )
        receiver_wallet = Wallet.objects.filter(
            name=self.request.data["receiver"]
        )

        if (
            sender_wallet.exists()
            and sender_wallet.filter(
                balance__gte=self.request.data["transfer_amount"]
            )
            and sender_wallet.values("currency").intersection(
                receiver_wallet.values("currency")
            )
        ):
            if Wallet.objects.filter(user=self.request.user).filter(
                name=self.request.data["receiver"]
            ):
                sender_wallet.update(
                    balance=F("balance") - self.request.data["transfer_amount"]
                )
                receiver_wallet.update(
                    balance=F("balance") + self.request.data["transfer_amount"]
                )
                serializer.save()
            else:
                sender_wallet.update(
                    balance=F("balance") - self.request.data["transfer_amount"]
                )
                receiver_wallet.update(
                    balance=F("balance")
                    + float(self.request.data["transfer_amount"]) * 0.9
                )
                serializer.save()
        else:
            raise Exception("Impossible")


class TransactionsDetail(generics.RetrieveAPIView):
    """Get specific transaction of current logged user"""

    permission_classes = [permissions.IsAuthenticated]
    serializer_class = TransactionSerializer
    queryset = Transaction.objects.all()

    def get(self, request, *args, **kwargs):
        """Get specific wallet of current logged user"""
        queryset = self.get_queryset()
        queryset1 = queryset.filter(
            Q(sender__user=request.user) | Q(receiver__user=request.user)
        ).filter(pk=int(self.kwargs.get("pk")))
        if queryset1:
            return self.retrieve(request, *args, **kwargs)
        else:
            raise Exception("User can see only own transactions")


class TransactionsWalletDetail(generics.RetrieveAPIView):
    """Get specific transaction of current logged user"""

    permission_classes = [permissions.IsAuthenticated]
    serializer_class = TransactionSerializer
    queryset = Transaction.objects.all()

    def get(self, request, *args, **kwargs):
        """Get all transactions from specific wallet of current logged user"""
        queryset = self.get_queryset()
        queryset1 = queryset.filter(
            Q(sender__name=self.kwargs.get("pk"))
            | Q(receiver__name=self.kwargs.get("pk"))
            & Q(sender__user=request.user)
            | Q(receiver__user=request.user)
        )
        serializer = TransactionSerializer(queryset1, many=True)
        if queryset1:
            return Response(serializer.data)
        else:
            raise Exception("User can see only own transactions")
