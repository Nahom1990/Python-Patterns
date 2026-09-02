from enum import Enum, auto
from typing import NamedTuple, Optional

class OrderState(Enum):
    PENDING = auto()
    PAID = auto()
    SHIPPED = auto()
    CANCELLED = auto()

# 1. IMMUTABLE DATA STRUCTURE
# Once created, an Order instance can NEVER be modified.
class Order(NamedTuple):
    id: int
    state: OrderState
    balance_refunded: bool = False

# 2. PURE TRANSITION FUNCTIONS
# These take an Order, print nothing (no side effects), and return a NEW Order.

def pay(order: Order) -> tuple[Order, str]:
    match order.state:
        case OrderState.PENDING:
            # We return a NEW copied order with the updated state, plus a message
            return order._replace(state=OrderState.PAID), "Payment successful"
        case OrderState.PAID | OrderState.SHIPPED:
            return order, "Order is already paid"
        case OrderState.CANCELLED:
            return order, "Cancelled orders cannot be paid"

def ship(order: Order) -> tuple[Order, str]:
    match order.state:
        case OrderState.PENDING:
            return order, "Cannot ship an unpaid order"
        case OrderState.PAID:
            return order._replace(state=OrderState.SHIPPED), "Order shipped"
        case OrderState.SHIPPED:
            return order, "Order has already shipped"
        case OrderState.CANCELLED:
            return order, "Cancelled orders cannot be shipped"

def cancel(order: Order) -> tuple[Order, str]:
    match order.state:
        case OrderState.PENDING:
            return order._replace(state=OrderState.CANCELLED), "Order cancelled"
        case OrderState.PAID:
            return order._replace(state=OrderState.CANCELLED, balance_refunded=True), "Refunding payment..."
        case OrderState.SHIPPED:
            return order, "Cannot cancel a shipped order"
        case OrderState.CANCELLED:
            return order, "Order is already cancelled"


# Create initial immutable state
order_v1 = Order(id=101, state=OrderState.PENDING)

# Try to ship it (fails, returns unchanged order)
order_v2, msg1 = ship(order_v1)
print(msg1)  # "Cannot ship an unpaid order"

# Pay it (returns a NEW order instance)
order_v3, msg2 = pay(order_v2)
print(msg2)  # "Payment successful"

# Ship it (returns a NEW order instance)
order_v4, msg3 = ship(order_v3)
print(msg3)  # "Order shipped"

# Try to cancel it (fails, returns unchanged order)
final_order, msg4 = cancel(order_v4)
print(msg4)  # "Cannot cancel a shipped order"

# Proof of Immutability:
print(order_v1.state)    # OrderState.PENDING (The original never changed!)
print(final_order.state)   # OrderState.SHIPPED
