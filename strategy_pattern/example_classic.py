from typing import Protocol


# =====================================================================
# 1. Strategy Interface (Protocol for static typing)
# =====================================================================
class PaymentStrategy(Protocol):
    """The common interface all payment algorithms must implement."""
    def pay(self, amount: float) -> None:
        ...


# =====================================================================
# 2. Concrete Strategies (Encapsulated Algorithms)
# =====================================================================
class CreditCardPayment:
    def __init__(self, card_number: str, cvv: str) -> None:
        self.card_number = card_number
        self.cvv = cvv

    def pay(self, amount: float) -> None:
        masked_card = f"****-****-****-{self.card_number[-4:]}"
        print(f"Paid ${amount:.2f} using Credit Card ({masked_card}).")


class PayPalPayment:
    def __init__(self, email: str) -> None:
        self.email = email

    def pay(self, amount: float) -> None:
        print(f"Paid ${amount:.2f} using PayPal account ({self.email}).")


class CryptoPayment:
    def __init__(self, wallet_address: str) -> None:
        self.wallet_address = wallet_address

    def pay(self, amount: float) -> None:
        short_wallet = f"{self.wallet_address[:6]}...{self.wallet_address[-4:]}"
        print(f"Paid ${amount:.2f} using Crypto Wallet ({short_wallet}).")


# =====================================================================
# 3. Context (Maintains a reference to a Strategy object)
# =====================================================================
class ShoppingCart:
    def __init__(self, payment_strategy: PaymentStrategy) -> None:
        self._items: list[tuple[str, float]] = []
        # Inject initial strategy dependency
        self.payment_strategy = payment_strategy

    def add_item(self, item_name: str, price: float) -> None:
        self._items.append((item_name, price))

    def calculate_total(self) -> float:
        return sum(price for _, price in self._items)

    def set_payment_strategy(self, strategy: PaymentStrategy) -> None:
        """Allows changing payment strategy dynamically at runtime."""
        self.payment_strategy = strategy

    def checkout(self) -> None:
        total = self.calculate_total()
        if total == 0:
            print("Cart is empty.")
            return

        # Delegate the actual payment behavior to the current strategy
        self.payment_strategy.pay(total)


# =====================================================================
# 4. Execution & Runtime Strategy Switching
# =====================================================================
if __name__ == "__main__":
    # Create concrete strategy objects
    card_strategy = CreditCardPayment("4111222233334444", "123")
    paypal_strategy = PayPalPayment("user@example.com")
    crypto_strategy = CryptoPayment("0x71C7656EC7ab88b098defB751B7401B5f6d8976F")

    # Instantiate Context with Credit Card strategy
    cart = ShoppingCart(payment_strategy=card_strategy)
    cart.add_item("Mechanical Keyboard", 120.00)
    cart.add_item("Wireless Mouse", 50.00)

    print("--- First Checkout ---")
    cart.checkout()

    # Dynamic Strategy Switching at Runtime!
    print("\n--- Switching strategy to PayPal ---")
    cart.set_payment_strategy(paypal_strategy)
    cart.checkout()

    print("\n--- Switching strategy to Crypto ---")
    cart.set_payment_strategy(crypto_strategy)
    cart.checkout()