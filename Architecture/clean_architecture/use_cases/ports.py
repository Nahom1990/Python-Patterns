# use_cases/ports.py
from abc import ABC, abstractmethod
from ..domain.user.entities import User

class UserRepositoryGateway(ABC):
    @abstractmethod
    async def get_by_id(self, user_id: str) -> User | None: ...
    
    @abstractmethod
    async def save(self, user: User) -> None: ...

class PaymentProcessorGateway(ABC):
    @abstractmethod
    async def charge_card(self, user_id: str, amount: float) -> bool: ...

