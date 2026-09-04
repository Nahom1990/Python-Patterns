from collections.abc import Callable
class ShoppingCart:

    def __init__(
        self,
        discount_strategy: Callable[[float], float]#it expects a function 
    ):
        self.discount_strategy = discount_strategy

    def final_price(self, price: float) -> float:
        return self.discount_strategy(price)


#the strategies
def no_discount(price):
    return price


def student_discount(price):
    return price * 0.9


def vip_discount(price):
    return price * 0.8

#usecase
cart = ShoppingCart(student_discount)

print(cart.final_price(100))


##or if we want cofigurable strategy factory like/ this utilizes closures to carry the func and percent
def percentage_discount(percent):
    
    def discount(price):
        return price * (1 - percent / 100)

    return discount

ten_percent = percentage_discount(10) #strategy 1
twenty_percent = percentage_discount(20) #strategy 2

#use

cart = ShoppingCart(ten_percent)

cart.final_price(100)

#or

cart = ShoppingCart(twenty_percent)

cart.final_price(100)