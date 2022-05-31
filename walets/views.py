from django.http import HttpResponse
from rest_framework import generics, permissions
from rest_framework.response import Response

from walets.models import Wallet
from walets.serializers import WalletSerializer


class WalletsList(generics.ListCreateAPIView):
    """Get wallet list, create wallet"""

    permission_classes = [permissions.IsAuthenticated]
    serializer_class = WalletSerializer

    def get_queryset(self, *args, **kwargs):
        """Get queryset of current user objects"""
        return Wallet.objects.filter(user=self.request.user)

    def list(self, request):
        """Get list of current logged user wallets"""
        queryset = self.get_queryset()
        serializer = WalletSerializer(queryset, many=True)
        if queryset:
            return Response(serializer.data)
        return HttpResponse(status=204)

    def perform_create(self, serializer):
        """Create wallet for current logged user"""
        current_user = Wallet.objects.filter(user=self.request.user)
        if current_user.count() < 5:
            serializer.save(user=self.request.user)
            if serializer.data["currency"] in ("USD", "EUR"):
                current_wallet = current_user.get(name=serializer.data["name"])
                current_wallet.balance = 3
                current_wallet.save()
            else:
                current_wallet = current_user.get(name=serializer.data["name"])
                current_wallet.balance = 100
                current_wallet.save()
        else:
            raise Exception("User can create only 5 wallets")


class WalletsDetail(generics.RetrieveDestroyAPIView):
    """Get/destroy specific wallet of current logged user"""

    permission_classes = [permissions.IsAuthenticated]
    serializer_class = WalletSerializer
    lookup_field = "name"

    def get_queryset(self, *args, **kwargs):
        """Get queryset of current user objects"""
        return Wallet.objects.filter(user=self.request.user)

    def get(self, request, *args, **kwargs):
        """Get specific wallet of current logged user"""
        queryset = self.get_queryset()
        if queryset:
            return self.retrieve(request, *args, **kwargs)

    def delete(self, request, *args, **kwargs):
        """Destroy specific wallet of current logged user"""
        queryset = self.get_queryset()
        if queryset:
            return self.destroy(request, *args, **kwargs)
