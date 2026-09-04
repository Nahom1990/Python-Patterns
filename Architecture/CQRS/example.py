from dataclasses import dataclass
from typing import Any, Optional
from abc import ABC, abstractmethod

# =====================================================================
# 1. WRITE SIDE (COMMANDS & DOMAIN)
# =====================================================================

@dataclass(frozen=True)
class CreateProductCommand:
    product_id: str
    name: str
    price: float
    initial_stock: int


class ProductWriteModel:
    """Domain Entity optimized for business validation and transactional safety."""
    def __init__(self, product_id: str, name: str, price: float, stock: int) -> None:
        if price <= 0:
            raise ValueError("Price must be positive.")
        if stock < 0:
            raise ValueError("Stock cannot be negative.")
            
        self.id = product_id
        self.name = name
        self.price = price
        self.stock = stock


class ProductCommandHandler:
    def __init__(self, write_repo: "IWriteRepository", event_bus: "IEventBus") -> None:
        self.write_repo = write_repo
        self.event_bus = event_bus

    async def handle_create_product(self, cmd: CreateProductCommand) -> None:
        # 1. Enforce Domain Rules
        product = ProductWriteModel(cmd.product_id, cmd.name, cmd.price, cmd.initial_stock)
        
        # 2. Persist to Transactional Write Store
        await self.write_repo.save(product)
        
        # 3. Publish Event to Sync Read Store
        await self.event_bus.publish({
            "event": "ProductCreated",
            "product_id": product.id,
            "name": product.name,
            "price": product.price,
            "stock": product.stock,
        })


# =====================================================================
# 2. READ SIDE (QUERIES & PROJECTIONS)
# =====================================================================

@dataclass(frozen=True)
class GetProductCatalogQuery:
    min_price: float = 0.0


@dataclass(frozen=True)
class ProductReadDTO:
    """Read-optimized flat DTO (no methods or business logic)."""
    id: str
    display_name: str
    formatted_price: str
    in_stock: bool


class ProductQueryHandler:
    def __init__(self, read_repo: "IReadRepository") -> None:
        self.read_repo = read_repo

    async def handle_get_catalog(self, query: GetProductCatalogQuery) -> list[ProductReadDTO]:
        # Bypasses domain model; queries flat read-optimized store directly
        raw_data = await self.read_repo.query_products(query.min_price)
        return [
            ProductReadDTO(
                id=item["id"],
                display_name=item["name"].upper(),
                formatted_price=f"${item['price']:.2f}",
                in_stock=item["stock"] > 0,
            )
            for item in raw_data
        ]


# =====================================================================
# 3. PROJECTION / SYNC EVENT HANDLER
# =====================================================================

class ProductProjectionHandler:
    """Listens to events from the Write side and updates the Read store."""
    def __init__(self, read_repo: "IReadRepository") -> None:
        self.read_repo = read_repo

    async def on_product_created(self, event: dict[str, Any]) -> None:
        # Pre-computes and denormalizes data for fast reading
        await self.read_repo.insert_read_model({
            "id": event["product_id"],
            "name": event["name"],
            "price": event["price"],
            "stock": event["stock"],
        })