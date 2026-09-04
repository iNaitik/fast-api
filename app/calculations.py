def add(num1: int, num2: int):
    return num1 + num2


def subtract(num1: int, num2: int):
    return num1 - num2


def multiply(num1: int, num2: int):
    return num1 * num2


def divide(num1: int, num2: int):
    if num2 == 0:
        raise ValueError("Cannot divide by zero")
    return num1 / num2


class BankAccount:
    def __init__(self, starting_balance: float = 0):
        self.balance = starting_balance

    def deposit(self, amount: float):
        if amount < 0:
            raise ValueError("Deposit amount must be positive")
        self.balance += amount
        return self.balance

    def withdraw(self, amount: float):
        if amount < 0:
            raise ValueError("Withdrawal amount must be positive")
        if amount > self.balance:
            raise ValueError("Insufficient funds")
        self.balance -= amount
        return self.balance

    def collect_interest(self):
        self.balance *= 1.1
        return self.balance