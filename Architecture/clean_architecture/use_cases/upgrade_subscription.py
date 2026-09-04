
# use_cases/upgrade_subscription.py
from dataclasses import dataclass
from .ports import UserRepositoryGateway, PaymentProcessorGateway

# Input / Output Boundary DTOs
@dataclass(frozen=True)
class UpgradeInputDTO:
    user_id: str
    payment_token: str

@dataclass(frozen=True)
class UpgradeOutputDTO:
    user_id: str
    new_plan: str
    status: str


class UpgradeSubscriptionUseCase:
    PREMIUM_PRICE = 19.99

    def __init__(
        self, 
        user_repo: UserRepositoryGateway, 
        payment_processor: PaymentProcessorGateway
    ) -> None:
        self.user_repo = user_repo
        self.payment_processor = payment_processor

    async def execute(self, request: UpgradeInputDTO) -> UpgradeOutputDTO:
        user = await self.user_repo.get_by_id(request.user_id)
        if not user:
            raise ValueError("User not found.")

        # Business Rule execution on Entity
        user.upgrade_to_premium()

        # External Gateway invocation
        payment_success = await self.payment_processor.charge_card(
            user_id=user.id, 
            amount=self.PREMIUM_PRICE
        )
        if not payment_success:
            raise RuntimeError("Payment processing failed.")

        await self.user_repo.save(user)
        return UpgradeOutputDTO(
            user_id=user.id, 
            new_plan=user.plan.value, 
            status="SUCCESS"
        )