from typing import Protocol


class Observer(Protocol):

    def update(self, price: float) -> None:
        ...

class MobileApp:

    def update(self, price: float) -> None:
        print(f"Mobile app: {price}")


class TradingBot:

    def update(self, price: float) -> None:
        print(f"Trading bot: {price}")

