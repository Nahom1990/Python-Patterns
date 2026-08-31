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



def place_order(
    user,
    product,
    amount,
    inventory,
    payment,
    shipping,
    notification,
):

    if not inventory.check_stock(product):
        return False

    inventory.reserve(product)

    if not payment.charge(user, amount):
        return False

    shipping.ship(product, user)

    notification.send(user, "Order successful")

    return True
#usecase
place_order(user="nahom",
            product="laptop",
            amount=20,
            inventory=InventoryService(),
            payment=PaymentService(),
            shipping=ShippingService(),
            notification=NotificationService(),)