#Layer 4: Infrastructure & UI (Outer Ring)

# infrastructure/persistence/postgres_repository.py
from typing import Optional
from Architecture.onion_architecture.domain.entities import Product
from Architecture.onion_architecture.domain.interfaces import IProductRepository

# Infrastructure implements the Domain Interface
class PostgresProductRepository(IProductRepository):
    def __init__(self, db_session) -> None:
        self.db = db_session

    async def get_by_sku(self, sku: str) -> Optional[Product]:
        record = await self.db.fetch_one("SELECT * FROM products WHERE sku = :sku", {"sku": sku})
        if not record:
            return None
        return Product(
            id=record["id"],
            sku=record["sku"],
            stock_quantity=record["stock_quantity"],
            unit_price=record["unit_price"]
        )

    async def save(self, product: Product) -> None:
        await self.db.execute(
            "UPDATE products SET stock_quantity = :qty WHERE sku = :sku",
            {"qty": product.stock_quantity, "sku": product.sku}
        )

