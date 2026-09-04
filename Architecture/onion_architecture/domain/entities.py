# core/domain/entities.py
#Layer 1: Domain Model (Core Center)
from dataclasses import dataclass

@dataclass
class Product:
    id: str
    sku: str
    stock_quantity: int
    unit_price: float

    def reduce_stock(self, count: int) -> None:
        if count > self.stock_quantity:
            raise ValueError(f"Insufficient stock for SKU {self.sku}. Requested: {count}, Available: {self.stock_quantity}")
        self.stock_quantity -= count