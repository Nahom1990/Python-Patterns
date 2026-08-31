from typing import Protocol

# for protocol no need of creating a decorator baseclass because if the loggingnotifier class has a send -> it automatically satisfies being a Notifier based on the protocol we defined

class Notifier(Protocol):
    def send(self,message):
        ...

class EmailNotifier:
    def send(self, message):
        print(f"sending email {message}")

class LoggingNotifier:
    def __init__(self,notifier:Notifier) -> None:
        self.notifier=notifier

    def send(self, message):
        print("logging notification")
        self.notifier.send(message)

class RetryNotifier:
    def __init__(self,notifier:Notifier) -> None:
        self.notifier=notifier
    def send(self,message):
        for attempt in range(3):
            try:
                self.notifier.send(message)
            except Exception:
                print(f"retry attempt {attempt+1}") 
# that is it 

#use case

notifier=LoggingNotifier(RetryNotifier(EmailNotifier()))



"""note :
Modern Python libraries frequently don't literally implement the GoF Decorator structure.

Instead, they may use:

Middleware
Hooks
Transports
Interceptors
Event handlers


but 
Middleware pipelines often contain ideas from patterns:

Decorator
+
Chain of Responsibility
"""