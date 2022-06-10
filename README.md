<h1>Remittance</h1>

<h3>Project Description</h3>
Implemented ability to create new wallets and provide transactions between them. Transactions are available only for wallets with the same currency. From RUB to RUB - good, from RUB to USD - wrong, show exception for user. When user sends money from his wallet to his another wallet - no commission, and when he sends to wallet, related to another user - commission=10%

<h3>How to Install and Run the Project</h3>

* create and activate virtualenv

* git clone https://github.com/VladKli/wallets-and-transactions.git

* cd wallets-and-transactions

* pip install -r requirements.txt

* create postgres db and connect it in remittance/settings.py

* python manage.py migrate

* python manage.py runserver

<h3>Available endpoints</h3>
<h4>All endpoints except `/api/register/ `requires HEADERS {Authorization: Token}</h4>

___

GET /api/register/ - register

`{
    "username": "test",
    "email": "123@at.com",
    "password": "testtest"
}`

___

POST /api/register/ - login

`{
    "username": "test",
    "password": "testtest"
}`
___

POST api/logout/ - logout

___

GET wallets/ - get user's wallets list

___

POST wallets/ - create wallet. types - visa, mastercard. currency - RUB, EUR, USD

When user creates new wallet he gets default bonus from bank: if wallet currency USD or EUR - balance=3.00, if RUB - balance=100.00

`{
 "type": "visa",
 "currency": "RUB"
}`

___
GET wallets/<wallet_name>/  e.g. wallets/2D1TB85X/ - get user's wallet
___

DELETE wallets/<wallet_name>/ - remove user's wallet
___

POST wallets/transactions/ - create transaction

`{
"sender": "<wallet_name>",
"receiver": "<wallet_name>",
"transfer_amount": "10"
}`
___

GET wallets/transactions/<pk> - get user's specific transaction
___

GET wallets/transactions/<wallet_name> - get all transactions were specific user's wallet was used
___
<h3>Pytest</h3>

To run tests just run `pytest` command

To see more detailed info about running tests use flag `-v`