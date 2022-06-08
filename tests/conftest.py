import pytest

from remittance import settings


@pytest.fixture(scope="session")
def django_db_setup():
    """Connect test DB"""
    settings.DATABASES["default"] = {
        "ENGINE": "django.db.backends.postgresql",
        "NAME": "drf_test",
        "USER": "dev",
        "PASSWORD": "3a9...To 91",
        "HOST": "localhost",
        "PORT": "5432",
    }


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
