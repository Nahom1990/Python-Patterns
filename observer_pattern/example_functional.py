#### this is the better one because functions are first class objects 
# on python so its similar to what we do with the others but 
# this is less boiler plate so recommended is this one

class Stock:

    def __init__(self):
        self.observers = set()# better to defend against duplcate observers, but sets dont care about order so tradeoff

    def subscribe(self, observer):
        self.observers.add(observer)

    def notify(self, price):
        for observer in self.observers:
            observer(price)

def mobile_notification(price):
    print(f"Mobile: {price}")


def trading_notification(price):
    print(f"Trading: {price}")


def email_notification(price):
    print(f"Email: {price}")

stock = Stock()

stock.subscribe(mobile_notification)
stock.subscribe(trading_notification)
stock.subscribe(email_notification)

stock.notify(150)