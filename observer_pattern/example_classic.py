"""
When something happens, automatically notify all interested objects 
without the thing producing the event needing to know who they are


Imagine you have an order system:

Order placed

When an order is placed, several things need to happen:

Send confirmation email
Update inventory
Notify analytics
Notify warehouse
Send customer notification

A naive implementation might be:

class OrderService:

    def create_order(self, order):
        save_order(order)

        send_email(order)
        update_inventory(order)
        update_analytics(order)
        notify_warehouse(order)
        
        
Now OrderService knows about every consumer.


Instead:

                    ┌── EmailService
                    │
Order ── event ─────┼── InventoryService
                    │
                    ├── AnalyticsService
                    │
                    └── WarehouseService

The Order doesn't need to know the concrete services.

It simply announces:

"An order was placed."

Anyone interested can subscribe.."""


from abc import ABC, abstractmethod


class Observer(ABC):

    @abstractmethod
    def update(self, price):
        pass

class MobileApp(Observer):

    def update(self, price):
        print(f"Mobile app: stock price is {price}")

class TradingBot(Observer):

    def update(self, price):
        print(f"Trading bot: stock price is {price}")


class EmailAlert(Observer):

    def update(self, price):
        print(f"Email alert: stock price is {price}")


class Stock:

    def __init__(self):
        self.observers = []

    def subscribe(self, observer):
        self.observers.append(observer)

    def unsubscribe(self, observer):
        self.observers.remove(observer)

    def set_price(self, price):
        self.price = price
        self.notify()

    def notify(self):
        for observer in self.observers:
            observer.update(self.price)


stock = Stock()

mobile = MobileApp()
bot = TradingBot()
email = EmailAlert()

stock.subscribe(mobile)
stock.subscribe(bot)
stock.subscribe(email)

stock.set_price(150)

"""
Stock price changed
       ↓
     notify()
       ↓
 ┌─────┼─────┐
 ↓     ↓     ↓
Mobile Bot  Email

Stock doesn't know:

MobileApp
TradingBot
EmailAlert

It only knows:

observer.update(...)
"""