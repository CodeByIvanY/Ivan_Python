import pytest
import sqlite3
from unittest.mock import patch, MagicMock
from project import Account, login, sign_out, get_input

# Setup a test database
@pytest.fixture(scope='module')
def test_db():
    connection = sqlite3.connect(":memory:")  # Use an in-memory database for testing
    cursor = connection.cursor()
    cursor.execute("CREATE TABLE tb_accounts (id INTEGER PRIMARY KEY, Password TEXT NOT NULL);")
    cursor.execute("CREATE TABLE tb_userinfo (Account_id INTEGER, First_Name TEXT, Last_Name TEXT, Gender TEXT, Birthday DATE, Address TEXT, ContactNumber TEXT);")
    cursor.execute("CREATE TABLE tb_transactions (Account_id INTEGER, TransType TEXT, Amount REAL);")
    connection.commit()
    yield connection
    connection.close()

# Test Account deposit method
def test_account_deposit(test_db):
    account = Account(account=1)
    account.balance = 100.0
    account.deposit(50.0)

    assert account.balance == 150.0

def test_account_deposit_negative_amount(test_db):
    account = Account(account=1)
    account.balance = 100.0
    result = account.deposit(-50.0)

    assert result == 'NPAmt'
    assert account.balance == 100.0

# Test Account withdraw method
def test_account_withdraw(test_db):
    account = Account(account=1)
    account.balance = 100.0
    account.withdraw(50.0)

    assert account.balance == 50.0

def test_account_withdraw_insufficient_funds(test_db):
    account = Account(account=1)
    account.balance = 50.0
    result = account.withdraw(100.0)

    assert result == 'NSF'
    assert account.balance == 50.0

def test_account_withdraw_negative_amount(test_db):
    account = Account(account=1)
    account.balance = 100.0
    result = account.withdraw(-50.0)

    assert result == 'NPAmt'
    assert account.balance == 100.0


# Run the tests
if __name__ == "__main__":
    pytest.main()
