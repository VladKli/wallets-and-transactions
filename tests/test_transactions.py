import pytest

from transactions.models import Transaction
from walets.models import Wallet


@pytest.mark.django_db
def test_transaction_create(create_wallets):
    """Test normal behaviour during transaction creating"""
    wallet_sender = Wallet.objects.first().name
    wallet_receiver = Wallet.objects.last().name
    response = create_wallets.post(
        "/wallets/transactions/",
        data={
            "sender": wallet_sender,
            "receiver": wallet_receiver,
            "transfer_amount": "10",
        },
    )
    response_body = response.json()
    assert response_body["sender"] == wallet_sender
    assert response_body["receiver"] == wallet_receiver
    assert response_body["transfer_amount"] == "10.00"
    assert response_body["commission"] == "1.00"
    assert response.status_code == 201


@pytest.mark.django_db
def test_transaction_create_balance_low(create_wallets):
    """Test transaction creation when balance is low"""
    wallet_sender = Wallet.objects.first().name
    wallet_receiver = Wallet.objects.last().name
    response = create_wallets.post(
        "/wallets/transactions/",
        data={
            "sender": wallet_sender,
            "receiver": wallet_receiver,
            "transfer_amount": "100",
        },
    )
    response_body = response.json()
    assert response_body == ["Not enough balance"]
    assert response.status_code == 400


@pytest.mark.django_db
def test_transaction_create_wrong_wallet(create_wallets):
    """Test transaction creation when wallet number is wrong"""
    wallet_receiver = Wallet.objects.last().name
    response = create_wallets.post(
        "/wallets/transactions/",
        data={
            "sender": "12345678",
            "receiver": wallet_receiver,
            "transfer_amount": "100",
        },
    )
    response_body = response.json()
    assert response_body == "No such wallet"
    assert response.status_code == 400


@pytest.mark.django_db
def test_transaction_create_wrong_currency(create_wallets):
    """Test transaction creation when currency is wrong"""
    wallet_sender = Wallet.objects.first().name
    wallet_receiver = Wallet.objects.last()
    wallet_receiver.currency = "USD"
    wallet_receiver.save()
    response = create_wallets.post(
        "/wallets/transactions/",
        data={
            "sender": wallet_sender,
            "receiver": wallet_receiver.name,
            "transfer_amount": "10",
        },
    )
    response_body = response.json()
    assert response_body == ["Currencies should be the same"]
    assert response.status_code == 400


@pytest.mark.django_db
def test_transaction_list(create_wallets):
    """Test normal behaviour to get list of transactions"""
    test_transaction_create(create_wallets)
    response = create_wallets.get("/wallets/transactions/")
    assert response.status_code == 200


@pytest.mark.django_db
def test_transaction_empty_list(create_wallets):
    """Test to get list of transactions when it is empty"""
    response = create_wallets.get("/wallets/transactions/")
    assert response.status_code == 404


@pytest.mark.django_db
def test_get_all_transaction_of_certain_wallet(create_wallets):
    """Test to get list of transactions of certain wallet"""
    test_transaction_create(create_wallets)
    test_transaction_create(create_wallets)
    wallet_sender = Wallet.objects.first().name
    response = create_wallets.get(
        f"/wallets/transactions/{wallet_sender}", follow=True
    )
    assert response.status_code == 200


@pytest.mark.django_db
def test_get_all_transaction_of_non_existent_wallet(create_wallets):
    """Test to get list of transactions of non-existent wallet"""
    response = create_wallets.get(
        "/wallets/transactions/12345678", follow=True
    )
    response_body = response.json()
    assert response_body == "No such transaction"
    assert response.status_code == 400


@pytest.mark.django_db
def test_get_transaction_by_pk(create_wallets):
    """Test to get transaction by id"""
    test_transaction_create(create_wallets)
    transaction_id = Transaction.objects.first().id
    response = create_wallets.get(
        f"/wallets/transactions/{transaction_id}", follow=True
    )
    assert response.status_code == 200


@pytest.mark.django_db
def test_get_transaction_by_non_existent_pk(create_wallets):
    """Test to get non-existent transaction by id"""
    response = create_wallets.get("/wallets/transactions/444", follow=True)
    response_body = response.json()
    assert response_body == "No such transaction"
    assert response.status_code == 400
