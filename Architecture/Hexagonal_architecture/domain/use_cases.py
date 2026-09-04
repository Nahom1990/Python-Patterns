# domain/use_cases.py (Pure Business Logic)
from .ports import OrderRepositoryPort,PaymentGatewayPort,CheckoutUseCasePort
from entities import Order,OrderStatus

class CheckoutUseCase(CheckoutUseCasePort):
    def __init__(
        self, 
        order_repo: OrderRepositoryPort, 
        payment_gateway: PaymentGatewayPort
    ) -> None:
        self.order_repo = order_repo
        self.payment_gateway = payment_gateway

    async def execute(self, order_id: str) -> Order:
        order = await self.order_repo.get_by_id(order_id)
        if not order:
            raise ValueError(f"Order {order_id} not found.")

        if order.status == OrderStatus.PAID:
            raise ValueError("Order is already paid.")

        # Business logic call via abstracted ports
        success = await self.payment_gateway.process_payment(order.amount)
        if not success:
            raise RuntimeError("Payment processing failed.")

        order.status = OrderStatus.PAID
        await self.order_repo.save(order)
        return order