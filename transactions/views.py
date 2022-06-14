from django.db import transaction
from django.db.models import Q
from rest_framework import permissions, status
from rest_framework.response import Response
from rest_framework.views import APIView

from transactions.models import Transaction
from transactions.serializers import TransactionSerializer


class TransactionsListCreate(APIView):
    """Get transactions list, create transaction"""

    permission_classes = [permissions.IsAuthenticated]

    def get(self, request) -> Response:
        """Get list of current logged user transactions"""
        queryset = Transaction.objects.filter(
            Q(sender__user=request.user) | Q(receiver__user=request.user)
        )
        if queryset:
            serializer = TransactionSerializer(queryset, many=True)
            return Response(serializer.data)
        return Response(status=status.HTTP_404_NOT_FOUND)

    @transaction.atomic
    def post(self, request) -> Response:
        """Create transaction for current logged user"""
        serializer = TransactionSerializer(
            data=request.data, context={"request": request}
        )
        if serializer.is_valid(raise_exception=True):
            serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)


class TransactionsDetail(APIView):
    """Get specific transaction of current logged user"""

    permission_classes = [permissions.IsAuthenticated]

    def get(self, request, *args, **kwargs) -> Response:
        """Get specific wallet of current logged user"""
        queryset = Transaction.objects.filter(
            Q(sender__user=request.user) | Q(receiver__user=request.user)
        ).filter(pk=int(self.kwargs.get("pk")))
        if queryset:
            serializer = TransactionSerializer(queryset, many=True)
            return Response(serializer.data)
        return Response(
            "No such transaction", status=status.HTTP_404_NOT_FOUND
        )


class TransactionsWalletDetail(APIView):
    """Get all user's transaction from specific wallet"""

    permission_classes = [permissions.IsAuthenticated]

    def get(self, request, *args, **kwargs) -> Response:
        """Get all transactions from specific wallet of current logged user"""
        queryset = Transaction.objects.filter(
            (
                Q(sender__name=self.kwargs.get("pk"))
                | Q(receiver__name=self.kwargs.get("pk"))
            )
            & (Q(sender__user=request.user) | Q(receiver__user=request.user))
        )
        serializer = TransactionSerializer(queryset, many=True)
        if queryset:
            return Response(serializer.data)
        return Response("No transactions", status=status.HTTP_404_NOT_FOUND)
