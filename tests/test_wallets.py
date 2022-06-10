import pytest
from rest_framework.test import APIClient


@pytest.mark.django_db
def test_wallet_creation_without_auth_token(client):
    """Test a correct response when user is not authorized and try to create wallet."""
    response = client.post(
        "/wallets/",
        data={"type": "visa", "currency": "RUB"},
    )
    response_body = response.json()
    assert (
        response_body["detail"]
        == "Authentication credentials were not provided."
    )
    assert response.status_code == 401


@pytest.mark.django_db
def test_wallet_creation(login_user):
    """Test a correct response when user is authorized and try to create wallet."""
    BANK_BONUS = "100.00"
    client = APIClient()
    data = {"type": "visa", "currency": "RUB"}
    client.credentials(HTTP_AUTHORIZATION="Token " + login_user)
    response = client.post(
        "/wallets/",
        data=data,
    )
    response_body = response.json()
    assert response_body["type"] == data["type"]
    assert response_body["currency"] == data["currency"]
    assert response_body["balance"] == BANK_BONUS
    assert response.status_code == 201
    return response_body


@pytest.mark.django_db
def test_user_wallets_no_auth(login_user):
    """Test a correct response when user is not authorized and try to see all wallets."""
    client = APIClient()
    response = client.get("/wallets/")
    assert response.status_code == 401


@pytest.mark.django_db
def test_user_wallets_empty_list(login_user):
    """Test a correct response when user is authorized and try to see all wallets but did not create any."""
    client = APIClient()
    client.credentials(HTTP_AUTHORIZATION="Token " + login_user)
    response = client.get("/wallets/")
    assert response.status_code == 404


@pytest.mark.django_db
def test_user_wallets_list(login_user):
    """Test a correct response when user is authorized and try to see all personal wallets."""
    test_wallet_creation(login_user)
    test_wallet_creation(login_user)
    client = APIClient()
    client.credentials(HTTP_AUTHORIZATION="Token " + login_user)
    response = client.get("/wallets/")
    assert response.status_code == 200


@pytest.mark.django_db
def test_another_user_wallets_list(login_user, login_user1):
    """Test a correct response when user is authorized and try to see wallets which did not create."""
    test_wallet_creation(login_user)
    client = APIClient()
    client.credentials(HTTP_AUTHORIZATION="Token " + login_user1)
    response = client.get("/wallets/")
    assert response.status_code == 404


@pytest.mark.django_db
def test_get_specific_user_wallet(login_user):
    """Test a correct response when user is authorized and try to see specific wallet."""
    test_wallet_creation(login_user)
    client = APIClient()
    client.credentials(HTTP_AUTHORIZATION="Token " + login_user)
    response = client.get("/wallets/")
    response1 = client.get(f"/wallets/{response.json()[0]['name']}/")
    assert response1.status_code == 200


@pytest.mark.django_db
def test_delete_specific_user_wallet(login_user):
    """Test a correct response when user is authorized and try to delete specific wallet."""
    test_wallet_creation(login_user)
    client = APIClient()
    client.credentials(HTTP_AUTHORIZATION="Token " + login_user)
    response = client.get("/wallets/")
    response1 = client.delete(f"/wallets/{response.json()[0]['name']}/")
    assert response1.status_code == 204
