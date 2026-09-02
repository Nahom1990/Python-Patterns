"""
if i wanted My HTTP Client
+ Logging
+ Authentication
+ Retry
+ Metrics
+ Caching


and if use inheritance approach  i would endup with Class explosion. 
HttpClient
│
├── LoggingHttpClient
├── AuthHttpClient
├── RetryHttpClient
├── LoggingRetryHttpClient
├── AuthRetryHttpClient
├── LoggingAuthHttpClient
└── LoggingAuthRetryHttpClient

And what happens when you add caching?

LoggingCachingHttpClient
AuthCachingHttpClient
RetryCachingHttpClient
LoggingAuthRetryCachingHttpClient"""
from abc import ABC, abstractmethod


class Notifier(ABC):

    @abstractmethod
    def send(self, message: str) -> None:
        pass

class EmailNotifier(Notifier):

    def send(self, message: str) -> None:
        print(f"Sending email: {message}")

class NotifierDecorator(Notifier): #inherits the Notifier/ this is the base class for all decorators to be applied on the notifier object

    def __init__(self, notifier: Notifier):
        self.notifier = notifier #and contains the notifier

#so the notifier decorator is a notifier(inheritance) and has a notifier(composition), what it returns after its modification is still a notifier objects
"""
It IS a Notifier-> class NotifierDecorator(Notifier)
It HAS a Notifier-> self.notifier = notifier
"""

class LoggingNotifier(NotifierDecorator):

    def send(self, message: str) -> None:
        print("Logging notification...")

        self.notifier.send(message)

        print("Notification logged.")

class RetryNotifier(NotifierDecorator):

    def send(self, message: str) -> None:

        for attempt in range(3):
            try:
                self.notifier.send(message)
                return

            except Exception:
                print(f"Retry attempt {attempt + 1}")

"""
             Component=Notifier
                 ▲
          ┌──────┴──────────────────────────┐
          │                                 │
ConcreteComponent=emailnotifier          Decorator=NotifierDecorator
                                          ▲
                                    ┌─────┴─────────────┐
                                    │                   │
                        ConcreteDecoratorA          Concrete DecoratorB
                         -LoggingNotifier            -RetryNotifier  """

#use
notifier=LoggingNotifier(RetryNotifier(EmailNotifier()))#stack them up like this
lognotifier=LoggingNotifier(EmailNotifier()) #or individually
notifier.send("Hello")
#important EmailNotifier is a Notifier and RetryNotifier(EmailNotifier()) is a notifier and LoggingNotifier(RetryNotifier(EmailNotifier())) all a notifier object, that is why one is can take the other 