"""
Scenario: Legacy Email System

You're building a modern notification system.

Your application's notification code expects to work with this conceptual interface:

send(recipient, subject, message)  -Target

However, your company has an old internal email library that you cannot modify.

The legacy library works like this:

send_email(
    to_address,
    email_subject,
    email_body,
    sender_address
)---adaptee

There are also two complications:

1. The legacy system requires a sender

Your modern application should not need to know which sender address the legacy system uses.

The Adapter should handle that configuration.

2. The legacy system returns a different result

The legacy library returns:

"EMAIL_SENT"

when successful.

Your application's notification system expects:

True

when successful.

The Adapter should translate that result too.

Requirements

Build a small system where:

The application works with a modern notification interface:
send(recipient, subject, message)
The existing legacy email library cannot be modified.
The Adapter translates:
recipient → to_address
subject → email_subject
message → email_body
The Adapter supplies the sender address internally.
"EMAIL_SENT" should become True.
Anything else returned by the legacy system should become False.
The application/client should not know that the legacy email system exists.
Demonstrate the solution with a small client/application.
Implement it twice:
Classical OOP using ABC
Modern Python using Protocol

"""
from abc import ABC, abstractmethod
class Notification(ABC):
    @abstractmethod
    def send(self,recipient, subject, message)->bool|None:
        pass

class LegacyNotification:
    def send_email(self,to_address,
        email_subject,email_body,
        sender_address
        ):
        # r=somesengin action here
        # if r:
        #     return "EMAIL_SENT"
        return "EMAIL_SENT"

class LegacyAdapter(Notification):
    def __init__(self,sender_address,legacy_notification:LegacyNotification):
        self.legacy_notification=legacy_notification
        self.sender_address=sender_address

    def send(self,recipient,subject,message):
        result=self.legacy_notification.send_email(recipient,subject,message,self.sender_address)
        return result=="EMAIL_SENT"
            
#use case
legacy=LegacyNotification()
notify=LegacyAdapter("addis_ababa",legacy,)
notify.send("cat","hello","how are you",)


############## pythonic approach
from typing import Protocol
class Notification2(Protocol):
    def send(self,recipient, subject, message)->bool:
        ...


class LegacyNotification2:
    def send_email(self,to_address,
        email_subject,email_body,
        sender_address
        ):
        # r=somesengin action here
        # if r:
        #     return "EMAIL_SENT"
        return "EMAIL_SENT"
    
class LegacyAdapter2:
    def __init__(self,sender_address,legacy_notification:LegacyNotification2):
        self.legacy_notification=legacy_notification
        self.sender_address=sender_address

    def send(self,recipient,subject,message):
        result=self.legacy_notification.send_email(recipient,subject,message,self.sender_address)
        return result=="EMAIL_SENT"
            

class Sending:
    def __init__(self,notification:Notification2):
        self.notification=notification

    def send_it(self,recipient,subject,message):
        return self.notification.send(recipient,subject,message)


legacy = LegacyNotification2()

adapter = LegacyAdapter2("noreply@example.com",legacy,)

sender = Sending(adapter)

success = sender.send_it(
    "customer@example.com",
    "Welcome",
    "Welcome to our platform!",
)