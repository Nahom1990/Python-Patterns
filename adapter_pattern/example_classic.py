from abc import ABC, abstractmethod


class PaymentProcessor(ABC):

    @abstractmethod
    def process_payment(self, amount: float) -> None:
        pass

class StripeGateway:

    def charge(self, amount: float) -> None:
        print(f"Charging ${amount} through Stripe")

class StripeAdapter(PaymentProcessor):

    def __init__(self, stripe_gateway: StripeGateway):
        self.stripe_gateway = stripe_gateway   #composition

    def process_payment(self, amount: float) -> None:
        self.stripe_gateway.charge(amount)


#use case
stripe = StripeGateway()

processor = StripeAdapter(stripe)

processor.process_payment(100)


