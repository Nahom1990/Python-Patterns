# adapters/controllers/user_controller.py
from use_cases.upgrade_subscription import (
    UpgradeSubscriptionUseCase, 
    UpgradeInputDTO
)

class UserController:
    def __init__(self, use_case: UpgradeSubscriptionUseCase) -> None:
        self.use_case = use_case

    async def handle_upgrade_request(self, user_id: str, payload: dict) -> tuple[dict, int]:
        """Translates transport protocol (HTTP/JSON) into Use Case DTOs."""
        try:
            dto = UpgradeInputDTO(user_id=user_id, payment_token=payload.get("token", ""))
            result = await self.use_case.execute(dto)
            return {"user_id": result.user_id, "plan": result.new_plan}, 200
        except ValueError as err:
            return {"error": str(err)}, 400
        except RuntimeError as err:
            return {"error": str(err)}, 402


