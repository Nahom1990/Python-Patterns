#Python has duck typing.We don't necessarily need:ABC, abstractmethod ,inheritance

from typing import Protocol

class StripeGateway:

    def charge(self, amount: float) -> None:
        print(f"Charging ${amount} through Stripe")


class PaypalGateway:

    def transact(self, amount: float) -> None:
        print(f"Charging ${amount} through Paypal")


class MockGateway:

    def trade(self, amount: float) -> None:
        print(f"Charging ${amount} through Mock")


class PaymentProcessor(Protocol):  #this is good only for type checking here for mypy or ide ? can work without this because python has duck typting and python executes if it finds same process_payment method name

    def process_payment(self, amount: float) -> None:
           ...
#the benefit of the above class is it says any class that implements process_payment is goos to go that is what protocol is doing

class StripeAdapter:

    def __init__(self, stripe_gateway):
        self.stripe_gateway = stripe_gateway

    def process_payment(self, amount: float) -> None:
        self.stripe_gateway.charge(amount)


class PayPalAdapter:
    def __init__(self, paypal_gateway):
        self.paypal_gateway = paypal_gateway

    def process_payment(self, amount: float) -> None:
        self.paypal_gateway.transact(amount)

class MockAdapter:
    def __init__(self, mock_gateway):
        self.mock_gateway = mock_gateway

    def process_payment(self, amount: float) -> None:
        self.mock_gateway.trade(amount)
        
class Checkout:

    def __init__(self, processor: PaymentProcessor): #this is where the type check happens without inheritance just any class with process payment method
        self.processor = processor

    def checkout(self, amount):
        self.processor.process_payment(amount)

#implementation
stripe=StripeGateway()
paypal=PaypalGateway()
mock=MockGateway()
checkout_stripe = Checkout(StripeAdapter(stripe))
checkout_stripe.checkout(100.0)

checkout_paypal = Checkout(PayPalAdapter(paypal))
checkout_paypal.checkout(200.0)



########## function approach easiest ########

class StripeGateway2:

    def charge(self, amount: float) -> None:
        print(f"Charging ${amount} through Stripe")

def process_payment(stripe_gateway,amount):
    return stripe_gateway.charge(amount)
