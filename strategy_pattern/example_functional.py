from typing import Callable

# Strategy signature: a function that accepts a float and returns None
PaymentStrategyFn = Callable[[float], None]

# Simple strategy functions
def pay_with_cash(amount: float) -> None:
    print(f"Paid ${amount:.2f} in Cash at pickup.")

def pay_with_apple_pay(amount: float) -> None:
    print(f"Paid ${amount:.2f} via Apple Pay device token.")

class QuickCheckout:
    def __init__(self, strategy_fn: PaymentStrategyFn):
        self.strategy_fn = strategy_fn

    def pay(self, amount: float) -> None:
        self.strategy_fn(amount)

# Usage
checkout = QuickCheckout(strategy_fn=pay_with_cash)
checkout.pay(45.50)

checkout.strategy_fn = pay_with_apple_pay
checkout.pay(45.50)