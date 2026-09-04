"""
The Repository Pattern is a design pattern that abstracts data access 
behind a collection-like interface, completely separating your core business logic 
from the underlying data storage technology. 

It serves as a mediator between your domain model and the database, 
pretending that all data resides directly in memory like a standard Python list or dictionary.


Instead of:

UserService → SQLAlchemy → PostgreSQL

we want:

                 ┌── SQLAlchemy → PostgreSQL
UserService → UserRepository
                 └── InMemoryRepository
                 
                 
For example:

UserRepository

might expose:

    get_by_id()
    get_by_email()
    save()
    delete()
    list()

The important part is that the application doesn't need to know whether these operations use:

    PostgreSQL
    MySQL
    MongoDB
    Redis
    an API
    an in-memory dictionary


REALWORLD->Repository + SQLAlchemy

A realistic architecture might eventually look something like:

    FastAPI
    ↓
    Application Service
    ↓
    Repository Protocol
    ↓
    SQLAlchemy Repository
    ↓
    SQLAlchemy Session
    ↓
    PostgreSQL

And Dependency Injection wires everything together:
    """

from abc import ABC, abstractmethod

class User:

    def __init__(self, id, name, email):
        self.id = id
        self.name = name
        self.email = email

class UserRepository(ABC):

    @abstractmethod
    def get_by_id(self, user_id: int) -> User | None:
        pass

    @abstractmethod
    def save(self, user: User) -> None:
        pass

class PostgreSQLUserRepository(UserRepository):

    def get_by_id(self, user_id: int) -> User | None:
        # SQLAlchemy query
        ...

    def save(self, user: User) -> None:
        # SQLAlchemy insert/update
        ...


class InMemoryUserRepository(UserRepository):

    def __init__(self):
        self.users = {}

    def get_by_id(self, user_id: int) -> User | None:
        return self.users.get(user_id)

    def save(self, user: User) -> None:
        self.users[user.id] = user

#Now our service doesn't care.

class UserService:

    def __init__(self, repository: UserRepository):
        self.repository = repository  #And this is where Repository + Dependency Injection connect:

    def get_user(self, user_id: int):
        return self.repository.get_by_id(user_id)

repository = PostgreSQLUserRepository()
service = UserService(repository)

#Or during testing:

repository2 = InMemoryUserRepository()
service = UserService(repository2)