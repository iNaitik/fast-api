# Testing file name should be ..._test  or test_...
# Functions name also should follow this conventions in oder to find them automatically 
import pytest
from app.calculations import add, subtract, multiply, divide, BankAccount

@pytest.fixture
def zero_bank_account():
    return BankAccount()

@pytest.fixture
def bank_account():
    return BankAccount(50)



@pytest.mark.parametrize("num1, num2, expected", [
    (3,2,5),
    (7,1,8), # These are values (num1 + num2 = expected)
    (12,4,16)
])
def test_add(num1, num2, expected):
    assert add(num1, num2) == expected


def test_subtract():
    assert subtract(10, 4) == 6


def test_multiply():
    assert multiply(6, 7) == 42


def test_divide():
    assert divide(12, 3) == 4


def test_divide_by_zero():
    try:
        divide(5, 0)
    except ValueError as exc:
        assert str(exc) == "Cannot divide by zero"
    else:
        assert False, "Expected ValueError for divide by zero"

# IF YOU WANT THE PRINT STATEMENT ALSO APPEAR INSTEAD OF pytest
# USE pytest -v -s


def test_bank_set_initial_amount(bank_account):
    assert bank_account.balance == 50

def test_bank_default_amount(zero_bank_account):
    assert zero_bank_account.balance == 0

def test_withdrawa(bank_account):
    bank_account.withdraw(20)
    assert bank_account.balance == 30