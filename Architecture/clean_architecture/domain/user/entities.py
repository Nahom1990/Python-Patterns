# domain/entities/user.py
from dataclasses import dataclass
from enum import Enum

class PlanTier(Enum):
    FREE = "FREE"
    PREMIUM = "PREMIUM"

@dataclass
class User:
    id: str
    email: str
    plan: PlanTier

    def upgrade_to_premium(self) -> None:
        if self.plan == PlanTier.PREMIUM:
            raise ValueError("User is already on Premium tier.")
        self.plan = PlanTier.PREMIUM