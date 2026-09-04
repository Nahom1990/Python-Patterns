"""Don't let an object create its own dependencies when those dependencies should be replaceable. Give the dependencies to the object from outside.


The three main types of DI
1. Constructor Injection ⭐ Most important

class UserService:
    def __init__(self, repository):
        self.repository = repository

Dependency comes through the constructor.

This is the preferred approach most of the time.


2. Method Injection
class ReportService:

    def generate(self, exporter):
        exporter.export()
        
The dependency is supplied to a method.

Useful when the dependency is only needed temporarily.

3. Setter Injection
class UserService:

    def set_repository(self, repository):
        self.repository = repository

Usually less preferred because the object can exist in an invalid state:

Constructor injection is generally safer.
"""
######################################the problem 
class EmailService:
    def send(self, to: str, body: str):
        print(f"Sending real email to {to}...")

class OrderProcessor2:
    def __init__(self):
        # Hardcoded dependency - impossible to unit test without sending real emails!
        self.email_service = EmailService()#####################################

    def checkout(self, user_email: str):
        # business logic
        self.email_service.send(user_email, "Your order confirmed!")

##correct
from abc import ABC, abstractmethod

# 1. DEFINE INTERFACE / CONTRACT
class NotificationService(ABC):
    @abstractmethod
    def notify(self, recipient: str, message: str) -> None:
        pass

# 2. CONCRETE IMPLEMENTATIONS
class EmailNotificationService(NotificationService):
    def notify(self, recipient: str, message: str) -> None:
        print(f"[Email] Sent to {recipient}: {message}")

class SmsNotificationService(NotificationService):
    def notify(self, recipient: str, message: str) -> None:
        print(f"[SMS] Sent to {recipient}: {message}")

class MockNotificationService(NotificationService):
    """Used for fast, isolated unit testing."""
    def __init__(self):
        self.sent_messages = []

    def notify(self, recipient: str, message: str) -> None:
        self.sent_messages.append((recipient, message))


# 3. CLASSICAL OOP INJECTION
class OrderProcessor:
    def __init__(self, notifier: NotificationService) -> None:
        # Injected dependency stored as an instance variable
        self._notifier = notifier ######################################the injection

    def process_order(self, user_id: str, amount: float) -> None:
        # Core domain logic
        print(f"Processing order for {user_id} (${amount})...")
        # Delegate side-effect to injected dependency
        self._notifier.notify(user_id, f"Order of ${amount} confirmed.")


# --- USAGE / COMPOSITION ROOT ---

# Production: Inject Email Service
email_processor = OrderProcessor(notifier=EmailNotificationService())
email_processor.process_order("user_101", 99.99)

# Production: Inject SMS Service without changing a single line of OrderProcessor
sms_processor = OrderProcessor(notifier=SmsNotificationService())
sms_processor.process_order("user_102", 49.50)

# Testing: Inject Mock Service
test_notifier = MockNotificationService()
test_processor = OrderProcessor(notifier=test_notifier)
test_processor.process_order("test_user", 10.00)
assert len(test_notifier.sent_messages) == 1  # Tested purely in memory!