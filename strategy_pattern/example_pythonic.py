from typing import Protocol


class PaymentStrategy(Protocol):

    def pay(self, amount: float) -> None:
        ...

class CreditCardStrategy:

    def pay(self, amount: float) -> None:
        print(f"Paid ${amount} using credit card")


class PayPalStrategy:

    def pay(self, amount: float) -> None:
        print(f"Paid ${amount} using PayPal")


class PaymentProcessor:

    def __init__(self, strategy: PaymentStrategy):
        self.strategy = strategy

    def process_payment(self, amount: float):
        self.strategy.pay(amount)