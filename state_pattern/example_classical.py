"""State lets an object change its behavior when its internal state changes.
The object's current state determines its behavior.
classic problem looks like this:

if order.state == "pending":
    ...
elif order.state == "paid":
    ...
elif order.state == "shipped":
    ...
elif order.state == "cancelled":
    ...
    
    
    
    With State, transitions can also be part of the model:

Pending
   │ pay()
   ↓
Paid
   │ ship()
   ↓
Shipped

This is particularly useful when not every operation is valid in every state.

For example:

Pending → cancel()     ✓
Pending → ship()       ✗

Paid → ship()          ✓
Paid → cancel()        maybe

Shipped → ship()       ✗
Shipped → cancel()     ✗

we move the behavior into state objects:

                 ┌── PendingState
                 │
Order ───────────┼── PaidState
                 │
                 ├── ShippedState
                 │
                 └── CancelledState

The Order delegates behavior to its current state."""

from abc import ABC, abstractmethod


class OrderState(ABC):

    @abstractmethod
    def pay(self, order):
        pass

    @abstractmethod
    def ship(self, order):
        pass

    @abstractmethod
    def cancel(self, order):
        pass


class PendingState(OrderState):

    def pay(self, order):
        print("Payment successful")
        order.state = PaidState()

    def ship(self, order):
        print("Cannot ship an unpaid order")

    def cancel(self, order):
        print("Order cancelled")
        order.state = CancelledState()

class PaidState(OrderState):

    def pay(self, order):
        print("Order is already paid")

    def ship(self, order):
        print("Order shipped")
        order.state = ShippedState()

    def cancel(self, order):
        print("Refunding payment...")
        order.state = CancelledState()

class ShippedState(OrderState):

    def pay(self, order):
        print("Order is already paid")

    def ship(self, order):
        print("Order has already shipped")

    def cancel(self, order):
        print("Cannot cancel a shipped order")

class CancelledState(OrderState):

    def pay(self, order):
        print("Cancelled orders cannot be paid")

    def ship(self, order):
        print("Cancelled orders cannot be shipped")

    def cancel(self, order):
        print("Order is already cancelled")

class Order:

    def __init__(self):
        self.state = PendingState()

    def pay(self):
        self.state.pay(self)

    def ship(self):
        self.state.ship(self)

    def cancel(self):
        self.state.cancel(self)

order = Order()

order.ship()
# Cannot ship an unpaid order

order.pay()
# Payment successful

order.ship()
# Order shipped

order.cancel()
# Cannot cancel a shipped order