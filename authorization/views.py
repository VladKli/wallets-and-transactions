from django.contrib.auth import login
from knox.models import AuthToken
from knox.views import LoginView as KnoxLoginView
from rest_framework import generics, permissions, status
from rest_framework.authtoken.serializers import AuthTokenSerializer
from rest_framework.response import Response

from .serializers import RegisterSerializer, UserSerializer


class LoginAPI(KnoxLoginView):
    """Login API"""

    permission_classes = (permissions.AllowAny,)

    def post(self, request, format=None):
        """Login process on POST method"""
        serializer = AuthTokenSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data["user"]
        login(request, user)
        return super(LoginAPI, self).post(request, format=None)


class RegisterAPI(generics.GenericAPIView):
    """Register API"""

    serializer_class = RegisterSerializer
    MIN_PASSWORD_LEN = 8

    def post(self, request, *args, **kwargs):
        """Register process on POST method"""
        if len(self.request.data["password"]) < 8:
            return Response(
                "Password should be at least 8 characters.",
                status=status.HTTP_400_BAD_REQUEST,
            )
        else:
            serializer = self.get_serializer(data=request.data)
            serializer.is_valid(raise_exception=True)
            user = serializer.save()
        return Response(
            {
                "user": UserSerializer(
                    user, context=self.get_serializer_context()
                ).data,
                "token": AuthToken.objects.create(user)[1],
            }
        )
