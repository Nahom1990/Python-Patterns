# domain/entities.py
from dataclasses import dataclass
from enum import Enum

class OrderStatus(Enum):
    PENDING = "PENDING"
    PAID = "PAID"

@dataclass
class Order:
    id: str
    amount: float
    status: OrderStatus



