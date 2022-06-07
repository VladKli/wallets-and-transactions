import pytest

from remittance import settings


@pytest.fixture(scope="session")
def django_db_setup():
    """Test DB data"""
    settings.DATABASES["default"] = {
        "ENGINE": "django.db.backends.postgresql",
        "NAME": "drf_test",
        "USER": "dev",
        "PASSWORD": "3a9...To 91",
        "HOST": "localhost",
        "PORT": "5432",
    }
