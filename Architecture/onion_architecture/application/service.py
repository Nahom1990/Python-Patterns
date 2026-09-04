#Layer 3: Application Services (Use Cases)
# core/application/services.py

from Architecture.onion_architecture.domain.entities import Product
from Architecture.onion_architecture.domain.interfaces import IProductRepository, InventoryDomainService

class FulfillOrderApplicationService:
    def __init__(self, product_repo: IProductRepository) -> None:
        self.product_repo = product_repo  # Injected via Interface

    async def fulfill_item(self, sku: str, quantity: int) -> dict:
        product = await self.product_repo.get_by_sku(sku)
        if not product:
            raise ValueError(f"Product with SKU '{sku}' not found.")

        # Execute business logic on Domain Entity
        product.reduce_stock(quantity)

        # Check domain rule using Domain Service
        needs_reorder = InventoryDomainService.calculate_reorder_level(product)

        # Persist through interface contract
        await self.product_repo.save(product)

        return {
            "sku": product.sku,
            "remaining_stock": product.stock_quantity,
            "needs_reorder": needs_reorder
        }