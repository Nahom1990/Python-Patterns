"""Build an Order Event System.

Your system should have an Order component that can emit events such as:

    order created
    order paid
    order shipped
    order cancelled

Different parts of the application may be interested in these events:

email notification
inventory update
analytics tracking
audit logging

The Order component should not directly know about these services.

It should be possible to register and unregister observers dynamically.

When an event occurs, every registered observer interested in that event should receive the notification.

Requirements

Implement three versions:

Classical OOP version
    Use an abstract Observer
    Concrete observer classes
    A Subject/event source
Pythonic version
    Use Protocol
    No unnecessary inheritance
Functional version
    Use functions as observers
    No observer classes"""

    
###version 1####
from abc import ABC,abstractmethod

class Observers(ABC):
    @abstractmethod
    def update_state(self,state):
        pass

class EmailNotification(Observers):
    def update_state(self, state):
        print(f"Email: order_state changed to: {state}")


class InventoryUpdate(Observers):
    def update_state(self, state):
        print(f"Inventory:order_state changed to: {state}")

class AnalyticsTracking(Observers):
    def update_state(self, state):
        print(f"Analytics: order_state changed to: {state}")

class Order:
    def __init__(self) -> None:
        self.observers:list[Observers]=[]
        self.order_status=None

    def subscribe(self,observer):
        self.observers.append(observer)

    def unsubscribe(self,observer):
        self.observers.remove(observer)

    def set_order_status(self,status):
        self.order_status=status
        self.notify(state=status)

    def notify(self,state):
        for observer in self.observers:
            observer.update_state(state)


email_observer=EmailNotification()
inventory_update=InventoryUpdate()
anaytics=AnalyticsTracking()
order=Order()
order.subscribe(email_observer)
order.subscribe(inventory_update)
order.subscribe(anaytics)

order.set_order_status(status="created")



###   version 2  #####

from typing import Protocol

class Observers2(Protocol):
    def update_state(self,state):
        ...

class EmailNotification2:
    def update_state(self, state):
        print(f"Email: order_state changed to: {state}")


class InventoryUpdate2:
    def update_state(self, state):
        print(f"Inventory:order_state changed to: {state}")

class AnalyticsTracking2:
    def update_state(self, state):
        print(f"Analytics: order_state changed to: {state}")

class Order2:
    def __init__(self) -> None:
        self.observers:list[Observers2]=[]
        self.order_status=None

    def subscribe(self,observer):
        self.observers.append(observer)

    def unsubscribe(self,observer):
        self.observers.remove(observer)

    def set_order_status(self,status):
        self.order_status=status
        self.notify(state=status)

    def notify(self,state):
        for observer in self.observers:
            observer.update_state(state)

email_observer2=EmailNotification2()
inventory_update2=InventoryUpdate2()
anaytics2=AnalyticsTracking2()
order2=Order2()
order2.subscribe(email_observer2)
order2.subscribe(inventory_update2)
order2.subscribe(anaytics2)

order2.set_order_status(status="created")
order2.set_order_status(status="paid")


###version 3

from typing import Callable

class Order3:
    def __init__(self) -> None:
        self.observers:list[Callable[[str],None]]=[]
        self.order_status=None

    def subscribe(self,observer):
        self.observers.append(observer)

    def unsubscribe(self,observer):
        self.observers.remove(observer)

    def set_order_status(self,status):
        self.order_status=status
        self.notify(state=status)

    def notify(self,state):
        for observer in self.observers:
            observer(state)

def email_notification(state):
    print(f"Email: order_state changed to: {state}")


def inventory_update_(state):
    print(f"Inventory: order_state changed to: {state}")


def analytic_tracking(state):
    print(f"Analytics: order_state changed to: {state}")


#usecase
email3=email_notification
inventory=inventory_update_
analytics=analytic_tracking
order3=Order3()
order3.subscribe(email3)
order3.subscribe(inventory)
order3.subscribe(analytics)

order3.set_order_status(status="created")
order3.set_order_status(status="delivered")
