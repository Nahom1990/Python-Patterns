"""Its main goal is:

Hide subsystem complexity behind a simple entry point.

Facade usually doesn't need ABC or Protocol.

Why?

Because the pattern isn't fundamentally about polymorphism.
It's about organizing a workflow."""


##example lets say we have the following supsystem classes 
class InventoryService:
    def check_stock(self, product: str) -> bool:
        print(f"Checking stock for {product}")
        return True

    def reserve(self, product: str) -> None:
        print(f"Reserving {product}")

class PaymentService:
    def charge(self, user: str, amount: float) -> bool:
        print(f"Charging {user}: ${amount}")
        return True

class ShippingService:
    def ship(self, product: str, user: str) -> None:
        print(f"Shipping {product} to {user}")

class NotificationService:
    def send(self, user: str, message: str) -> None:
        print(f"Sending notification to {user}: {message}")

# The Facade
class OrderFacade:

    def __init__(
        self,
        inventory: InventoryService,
        payment: PaymentService,
        shipping: ShippingService,
        notification: NotificationService,
    ):
        self.inventory = inventory
        self.payment = payment
        self.shipping = shipping
        self.notification = notification

    def place_order(
        self,
        user: str,
        product: str,
        amount: float,
    ) -> bool:

        # Step 1
        if not self.inventory.check_stock(product):
            return False

        # Step 2
        self.inventory.reserve(product)

        # Step 3
        if not self.payment.charge(user, amount):
            return False

        # Step 4
        self.shipping.ship(product, user)

        # Step 5
        self.notification.send(
            user,
            "Your order has been placed successfully!",
        )

        return True
##Client code

#Without Facade:
inventory=InventoryService()
payment=PaymentService()
shipping=ShippingService()
notification=NotificationService()
inventory.check_stock("product")
inventory.reserve("product")
payment.charge("user", 50)
shipping.ship("product", "user")
notification.send("user", "message")

#With Facade:
order_facade=OrderFacade(inventory=InventoryService(),payment=PaymentService()
                         ,shipping=ShippingService(),notification=NotificationService())
order_facade.place_order(
    user="Nahom",
    product="Laptop",
    amount=1000,
)