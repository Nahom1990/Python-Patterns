"""The Strategy Pattern means:
Encapsulate different algorithms/ways of doing something so 
they can be selected and changed independently from the code that uses them.

Example:

Payment
 ├── CreditCardStrategy
 ├── PayPalStrategy
 └── BankTransferStrategy

The payment system doesn't need to know the details of each payment algorithm.

It simply says:

"Use this strategy to process the payment.The destination hasn't changed. just the way"""

from abc import ABC, abstractmethod


class PaymentStrategy(ABC):

    @abstractmethod
    def pay(self, amount):
        pass

class CreditCardStrategy(PaymentStrategy):

    def pay(self, amount):
        print(f"Paid ${amount} using credit card")


class PayPalStrategy(PaymentStrategy):

    def pay(self, amount):
        print(f"Paid ${amount} using PayPal")


class BankTransferStrategy(PaymentStrategy):

    def pay(self, amount):
        print(f"Paid ${amount} using bank transfer")

class PaymentProcessor:

    def __init__(self, strategy: PaymentStrategy):
        self.strategy = strategy

    def process_payment(self, amount):
        self.strategy.pay(amount)

##use 
processor = PaymentProcessor(CreditCardStrategy())

processor.process_payment(100)

#or
processor = PaymentProcessor(PayPalStrategy())

processor.process_payment(100)