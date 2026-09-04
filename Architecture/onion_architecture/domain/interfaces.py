#Layer 2: Domain Services & Interfaces

# core/domain/interfaces.py
from abc import ABC, abstractmethod
from typing import Optional
from Architecture.onion_architecture.domain.entities import Product

# Core Repository Interface defined in the inner domain
class IProductRepository(ABC):
    @abstractmethod
    async def get_by_sku(self, sku: str) -> Optional[Product]: ...

    @abstractmethod
    async def save(self, product: Product) -> None: ...


# Core Domain Service for business operations crossing entity boundaries
class InventoryDomainService:
    @staticmethod
    def calculate_reorder_level(product: Product) -> bool:
        # Business logic: Alert if stock drops below 5 units
        return product.stock_quantity < 5