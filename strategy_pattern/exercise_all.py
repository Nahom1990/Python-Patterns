"""You are building a notification system.

Your application needs to send notifications, but the way a notification is delivered can vary.

The system currently supports:

Email delivery
SMS delivery
Push notification delivery

Later, more delivery methods may be added.

Requirements

Create a system where:

A notification service should not contain if/elif statements checking which delivery method to use.
The delivery behavior should be injectable into the notification service.
Every delivery method should follow the same conceptual interface.
The client should be able to choose a delivery strategy.
The client should also be able to change the delivery strategy at runtime.
Implement this in your preferred modern Python style using Protocol.
Your task
"""


from abc import ABC,abstractmethod

class NotificationDelivery(ABC):
    @abstractmethod
    def send(self,message):
        pass
class EmailDelivery(NotificationDelivery):
    def send(self,message):
        print(f"sent using the email delivery: {message}")

class SMSDelivery(NotificationDelivery):
    def send(self,message):
        print(f"sent using sms: {message}")

class PushDelivery(NotificationDelivery):
    def send(self,message):
        print(f"sent using push {message}")

class DelvierySystem:
    def __init__(self,delivery_strategy:NotificationDelivery) -> None:
        self.delivery_strategy=delivery_strategy

    def deliver(self,message):
        self.delivery_strategy.send(message)

delivery=DelvierySystem(EmailDelivery())
delivery.deliver(message="Hi nahom")

###vesrion 2

from typing import Protocol

class NotificationDelivery2(Protocol):
    def send(self,message):
        ...
class EmailDelivery2:
    def send(self,message):
        print(f"sent using the email delivery: {message}")

class SMSDelivery2:
    def send(self,message):
        print(f"sent using sms: {message}")

class PushDelivery2:
    def send(self,message):
        print(f"sent using push {message}")

class DelvierySystem2:
    def __init__(self,delivery_strategy:NotificationDelivery2) -> None:
        self.delivery_strategy=delivery_strategy

    def deliver(self,message):
        self.delivery_strategy.send(message)

#use
delivery2=DelvierySystem2(SMSDelivery2())
delivery2.deliver(message="Hi nahom")


###version 3
from typing import Callable

class DelvierySystem3:
    def __init__(self,delivery_strategy:Callable[[str],str]) -> None:
        self.delivery_strategy=delivery_strategy

    def deliver(self,message):
        return self.delivery_strategy(message)

def smsdelivery3(message):
    return f"sent using the sms delivery: {message}"

def emaildelivery(message):
    return f"sent using the email delivery: {message}"

def pushdelivery(message):
    return f"sent using the push delivery: {message}"

#use

delivery3=DelvierySystem3(smsdelivery3)
print(delivery3.deliver(message="Hi bro"))