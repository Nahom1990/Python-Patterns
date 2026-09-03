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
class UserRegistrationService:
    def __init__(self,repository,passwordhasher,sender) -> None:
        self.repository=repository
        self.passwordhasher=passwordhasher
        self.sender=sender


    def register(self,username,password):
        self.repository.create_user(username,password)

    def check_user(self,username):
        user=self.repository.get_user(username)
        return user
    def hash_password(self,password):
        self.passwordhasher.hash(password)

    def send_welcome_email(self,message):
        self.sender.welcome_email(message)

from abc import ABC, abstractmethod
class UserRepositoryFactory(ABC):
    @abstractmethod
    def create_user(self,username,password): pass

    @abstractmethod
    def get_user(self,username)->bool: pass

class PasswordHasherFactory(ABC):
    @abstractmethod
    def hash(self,password): pass

class NotificationSenderFactory(ABC):
    @abstractmethod
    def welcome_email(self,message) ->str:
        pass


class UserRepository(UserRepositoryFactory):
    def __init__(self) -> None:
        self.storage:dict[str,str]={}

    def create_user(self,username,password):
        self.storage[username]=password

    def get_user(self,username):
        if username in self.storage:
            return True
        return False

class PasswordHasher(PasswordHasherFactory):
    def hash(self,password):
        return password

class NotificationSender(NotificationSenderFactory):
    def welcome_email(self, message):
        print(f"sent message {message}")
        return "sent"

#######  Version 2 #######
class UserRegistrationService2:
    def __init__(self,repository,passwordhasher,sender) -> None:
        self.repository=repository
        self.passwordhasher=passwordhasher
        self.sender=sender


    def register(self,username,password):
        self.repository.create_user(username,password)

    def check_user(self,username):
        user=self.repository.get_user(username)
        return user
    def hash_password(self,password):
        self.passwordhasher.hash(password)

    def send_welcome_email(self,message):
        self.sender.welcome_email(message)

from typing import Protocol

class UserRepositoryFactory2(Protocol):
    @abstractmethod
    def create_user(self,username,password): ...

    @abstractmethod
    def get_user(self,username)->bool: ...

class PasswordHasherFactory2(Protocol):
    @abstractmethod
    def hash(self,password): ...

class NotificationSenderFactory2(Protocol):
    @abstractmethod
    def welcome_email(self,message) ->str:
        ...


class UserRepository2:
    def __init__(self) -> None:
        self.storage:dict[str,str]={}

    def create_user(self,username,password):
        self.storage[username]=password

    def get_user(self,username):
        if username in self.storage:
            return True
        return False

class PasswordHasher2:
    def hash(self,password):
        return password

class NotificationSender2:
    def welcome_email(self, message):
        print(f"sent message {message}")
        return "sent"

##### Version 3.1---Function Parameter Injection ##############




##### Version 3.2 Closure  ##############