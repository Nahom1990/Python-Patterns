# infrastructure/adapters/stripe_adapter.py
import httpx
from domain.ports import PaymentGatewayPort

class StripePaymentAdapter(PaymentGatewayPort):
    def __init__(self, api_key: str) -> None:
        self.api_key = api_key

    async def process_payment(self, amount: float) -> bool:
        # Calls external HTTP endpoint for Stripe API
        async with httpx.AsyncClient() as client:
            response = await client.post(
                "https://api.stripe.com/v1/charges",
                headers={"Authorization": f"Bearer {self.api_key}"},
                data={"amount": int(amount * 100), "currency": "usd"}
            )
            return response.status_code == 200