# domain/ports.py (Interfaces / Abstract Base Classes)
from abc import ABC, abstractmethod
from .entities import Order

# SECONDARY PORTS (Driven: What the domain needs from the outside)
class OrderRepositoryPort(ABC):
    @abstractmethod
    async def get_by_id(self, order_id: str) -> Order | None: ...
    
    @abstractmethod
    async def save(self, order: Order) -> None: ...

class PaymentGatewayPort(ABC):
    @abstractmethod
    async def process_payment(self, amount: float) -> bool: ...


# PRIMARY PORT (Driving: What operations the outside world can request)
class CheckoutUseCasePort(ABC):
    @abstractmethod
    async def execute(self, order_id: str) -> Order: ...
