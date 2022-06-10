import pytest
from rest_framework.test import APIClient

from tests.test_wallets import test_wallet_creation
from walets.models import Wallet


@pytest.fixture(scope="function")
def login_user(client):
    """Login is required for operations"""
    response = client.post(
        "/api/register/",
        data={
            "username": "test_user",
            "email": "test_user@at.com",
            "password": "test_user",
        },
    )
    token = response.json()["token"]
    return token


@pytest.fixture(scope="function")
def login_user1(client):
    """Login is required for operations"""
    response = client.post(
        "/api/register/",
        data={
            "username": "test_user1",
            "email": "test_user@at.com",
            "password": "test_user1",
        },
    )
    token = response.json()["token"]
    return token


@pytest.fixture(scope="function")
def create_wallets(login_user, login_user1):
    """Create wallets for testing"""
    client = APIClient()
    client.credentials(HTTP_AUTHORIZATION="Token " + login_user)
    test_wallet_creation(login_user)
    prelast_wallet = Wallet.objects.last().name
    client1 = APIClient()
    client1.credentials(HTTP_AUTHORIZATION="Token " + login_user1)
    test_wallet_creation(login_user1)
    return client, prelast_wallet
