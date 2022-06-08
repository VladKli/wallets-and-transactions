import pytest


@pytest.mark.django_db
def test_registration_body_and_code(client):
    """Test correct response for user_name, email fields and response code during registration."""
    response = client.post(
        "/api/register/",
        data={
            "username": "test_user",
            "email": "test_user@at.com",
            "password": "test_user",
        },
    )
    response_body = response.json()
    assert response_body["user"]["username"] == "test_user"
    assert response_body["user"]["email"] == "test_user@at.com"
    assert response.status_code == 200


@pytest.mark.django_db
def test_registration_user_exists(client):
    """Test capability to create user with the same data. Username qwerty exists in DB"""
    response = client.post(
        "/api/register/",
        data={
            "username": "qwerty",
            "email": "qwerty@at.com",
            "password": "qwerty",
        },
    )
    assert response.status_code == 400


@pytest.mark.django_db
def test_login_answer_code(client):
    """Test login response code. Username qwerty exists in DB"""
    response_login = client.post(
        "/api/login/",
        data={
            "username": "qwerty",
            "password": "qwerty",
        },
    )
    assert response_login.status_code == 200


@pytest.mark.django_db
def test_registration_without_credential(client):
    """Test a response in case credentials for login are not provided."""
    response = client.post(
        "/api/register/",
        data={
            "username": "",
            "email": "",
            "password": "",
        },
    )
    assert response.status_code == 400


@pytest.mark.django_db
def test_registration_with_incorrect_email(client):
    """Test a response code in case email is not valid."""
    response = client.post(
        "/api/register/",
        data={
            "username": "test",
            "email": "test",
            "password": "test",
        },
    )
    assert response.status_code == 400


@pytest.mark.django_db
def test_registration_with_small_password(client):
    """Test a response code in case password is less than 8 signs."""
    response = client.post(
        "/api/register/",
        data={
            "username": "test123",
            "email": "test@test.com",
            "password": "test123",
        },
    )
    response_body = response.json()
    assert response_body == "Password should be at least 8 characters."
    assert response.status_code == 400
