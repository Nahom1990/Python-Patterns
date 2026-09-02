## we can use protocols but the below is the even modern way of using the state pattern

###################### Even Modern Way ##################
from enum import Enum, auto

class OrderState(Enum):
    PENDING = auto()
    PAID = auto()
    SHIPPED = auto()
    CANCELLED = auto()

class Order:
    def __init__(self):
        self.state = OrderState.PENDING

    def pay(self):
        match self.state:
            case OrderState.PENDING:
                print("Payment successful")
                self.state = OrderState.PAID
            case OrderState.PAID | OrderState.SHIPPED:
                print("Order is already paid")
            case OrderState.CANCELLED:
                print("Cancelled orders cannot be paid")

    def ship(self):
        match self.state:
            case OrderState.PENDING:
                print("Cannot ship an unpaid order")
            case OrderState.PAID:
                print("Order shipped")
                self.state = OrderState.SHIPPED
            case OrderState.SHIPPED:
                print("Order has already shipped")
            case OrderState.CANCELLED:
                print("Cancelled orders cannot be shipped")

    def cancel(self):
        match self.state:
            case OrderState.PENDING:
                print("Order cancelled")
                self.state = OrderState.CANCELLED
            case OrderState.PAID:
                print("Refunding payment...")
                self.state = OrderState.CANCELLED
            case OrderState.SHIPPED:
                print("Cannot cancel a shipped order")
            case OrderState.CANCELLED:
                print("Order is already cancelled")

# 1. Create a brand new order instance
my_order = Order()
print(f"Initial State: {my_order.state.name}")  # Output: PENDING

# 2. Try an invalid action (shipping an unpaid order)
my_order.ship()  
# Output: Cannot ship an unpaid order

# 3. Pay for the order (this triggers the state transition to PAID)
my_order.pay()  
# Output: Payment successful
print(f"Current State: {my_order.state.name}")  # Output: PAID

# 4. Ship the order (this triggers the state transition to SHIPPED)
my_order.ship()  
# Output: Order shipped
print(f"Current State: {my_order.state.name}")  # Output: SHIPPED

# 5. Try another invalid action (cancelling after it shipped)
my_order.cancel()  
# Output: Cannot cancel a shipped order

