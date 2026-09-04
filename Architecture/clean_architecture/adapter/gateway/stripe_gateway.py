# adapters/gateways/stripe_gateway.py
from use_cases.ports import PaymentProcessorGateway

class StripeGatewayAdapter(PaymentProcessorGateway):
    async def charge_card(self, user_id: str, amount: float) -> bool:
        # Interacts with real Stripe SDK/HTTP driver
        return True