from rest_framework import permissions, status
from rest_framework.response import Response
from rest_framework.views import APIView

from walets.models import Wallet
from walets.serializers import WalletCreateSerializer


class WalletView(APIView):
    """Get wallet list, create wallet"""

    MAX_WALLETS = 5

    permission_classes = [permissions.IsAuthenticated]

    def get(self, request) -> Response:
        """Get wallet list"""
        wallets = Wallet.objects.filter(user=self.request.user)
        if wallets:
            serializer = WalletCreateSerializer(wallets, many=True)
            return Response(serializer.data)
        return Response(status=status.HTTP_204_NO_CONTENT)

    def post(self, request) -> Response:
        """Create wallet"""
        serializer = WalletCreateSerializer(
            data=request.data, context={"request": request}
        )
        count_wallets = Wallet.objects.filter(user=request.user).count()
        if count_wallets >= self.MAX_WALLETS:
            return Response(
                {"max_wallets": self.MAX_WALLETS},
                status=status.HTTP_400_BAD_REQUEST,
            )
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)


class WalletsDetail(APIView):
    """Get/delete specific wallet of current logged user"""

    permission_classes = [permissions.IsAuthenticated]

    def get(self, request, *args, **kwargs) -> Response:
        """Get specific wallet of current logged user"""
        wallet = Wallet.objects.filter(user=self.request.user).filter(
            name=self.kwargs.get("name")
        )
        if wallet:
            serializer = WalletCreateSerializer(wallet, many=True)
            return Response(serializer.data)
        return Response("No such wallet", status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, *args, **kwargs) -> Response:
        """Delete specific wallet of current logged user"""
        wallet = Wallet.objects.filter(user=self.request.user).filter(
            name=self.kwargs.get("name")
        )
        if wallet:
            wallet.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        return Response("No such wallet", status=status.HTTP_400_BAD_REQUEST)
