"""
UserRegistrationService
        │
        ├── UserRepository
        ├── PasswordHasher
        ├── EmailSender
        └── EventPublisher
"""

"""
The service should do this:

register(username, password)

        ↓

check if user exists

        ↓

hash password

        ↓

save user

        ↓

send welcome email

        ↓

publish "user_registered" event
Your task

Implement it in three versions, like we've been doing.

Version 1 — Classical

Use:

ABC
abstractmethod
Constructor injection

Your abstractions should represent:

UserRepository
PasswordHasher
EmailSender
EventPublisher

Create concrete implementations.

Then inject everything into:

UserRegistrationService
Version 2 — Pythonic

Use:

Protocol

instead of ABC.

Same architecture.

Version 3 — Functional / Procedural

This is where I especially want you to think.

Instead of classes like:

PostgresUserRepository()

you can inject functions:

register_user(
    username,
    password,
    user_exists=...,
    save_user=...,
    hash_password=...,
    send_email=...,
    publish_event=...,
)

Functions can be dependencies too.

So DI is not an OOP-only concept.
"""

###### Version 1 ####
from abc import ABC,abstractmethod
#baseclasses
class UserRepository(ABC):
    @abstractmethod
    def create_user(self,username,hashed_password)->None: ...

    @abstractmethod
    def get_user(self,username)->bool: ...
class PasswordHasher(ABC):
    @abstractmethod
    def hash(self,password)->str: ...

class NotificationSender(ABC):
    @abstractmethod
    def welcome_email(self,message) ->str: ...

#concrete classes
class InMemoUserRepository(UserRepository):
    def __init__(self) -> None:
        self.storage:dict[str,str]={}

    def create_user(self,username,hashed_password):
        self.storage[username]=hashed_password

    def get_user(self,username):
        return username in self.storage

class SimplePasswordHasher(PasswordHasher):
    def hash(self,password):
        return f"{password}hashed"

class ConsoleNotificationSender(NotificationSender):
    def welcome_email(self, message):
        print(f"sent message {message}")
        return "sent"

class UserRegistrationService2:
    def __init__(self,repository:UserRepository,
                 passwordhasher:PasswordHasher,
                 sender:NotificationSender) -> None:
        self.repository=repository
        self.passwordhasher=passwordhasher
        self.sender=sender


    def register(self,username,password):
        if self.repository.get_user(username):
            raise ValueError(f"User '{username}' already exists.")
        self.repository.create_user(username,password)
        hashed_password = self.passwordhasher.hash(password)
        self.repository.create_user(username, hashed_password)
        self.sender.welcome_email(
            f"Welcome, {username}! Your account is active."
        )
