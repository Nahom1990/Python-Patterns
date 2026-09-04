"""
Imagine your government-service application has several repositories:

    ServiceRepository
    UserRepository
    DocumentRepository
    OfficeRepository

Now imagine one application operation:

Register a user for a government service.

The operation might do:

    Save/update the user
    Save their submitted documents
    Create a service application
    Update eligibility information

Conceptually:

    user_repo.save(user)
    document_repo.save(document)
    application_repo.save(application)

The problem is:

    What if step 3 fails?

    You might end up with:

        ✅ User saved
        ✅ Document saved
        ❌ Application failed

Now your database is in an inconsistent state.

You want:

Either everything succeeds and commits together, or everything fails and rolls back together.

That's the main problem Unit of Work solves

A Unit of Work represents: One business transaction..

Register User
    │
    ├── UserRepository
    ├── DocumentRepository
    ├── ApplicationRepository
    │
    ▼
UnitOfWork
    │
    ├── COMMIT everything
    │
    └── OR ROLLBACK everything

Application Service
        │
        ▼
   UnitOfWork
   /    |    \
  /     |     \
Users  Docs  Services
Repos  Repos   Repos
        │
        ▼
    Database Session

The important thing is that the repositories participating
 in one Unit of Work usually share the same database transaction/session.

Repositories generally should not commit themselves.

UserRepository.save()
        ↓
      COMMIT ❌

DocumentRepository.save()
        ↓
      COMMIT ❌

ApplicationRepository.save()
        ↓
      COMMIT ❌

Now you have three separate transaction boundaries.

Better:

save user
save document
save application
        ↓
    ONE COMMIT ✅

You rarely see a explicit AbstractUnitOfWork class written in production 
SQLAlchemy code for three main reasons: SQLAlchemy’s Session already is a
 Unit of Work implementation, Python developers value pragmatic simplicity over 
 enterprise abstraction layers, and modern async/web patterns handle transaction 
 scoping at the framework middleware level.

In frameworks like FastAPI or Flask, session lifecycles are tied to the 
HTTP request lifecycle via middleware or request-scoped dependencies.

Instead of writing a custom UoW class, developers inject the session directly
"""


from abc import ABC, abstractmethod
from dataclasses import dataclass
from typing import List, Optional, Type,Any


# 1. DOMAIN ENTITIES
@dataclass
class User:
    id: str
    name: str


@dataclass
class Application:
    id: str
    user_id: str
    service_name: str


# 2. ABSTRACT REPOSITORIES
class UserRepository(ABC):
    @abstractmethod
    def __init__(self, session: Any) -> None:
        """Enforce that every UserRepository implementation accepts a session/database context."""
        pass

    @abstractmethod
    def add(self, user: User) -> None:
        pass

    @abstractmethod
    def get_by_id(self, user_id: str) -> Optional[User]:
        pass


class ApplicationRepository(ABC):
    @abstractmethod
    def __init__(self, session: Any) -> None:
        """Enforce that every ApplicationRepository implementation accepts a session/database context."""
        pass
    @abstractmethod
    def add(self, application: Application) -> None:
        pass

    @abstractmethod
    def get_by_id(self, app_id: str) -> Optional[Application]:
        pass


# 3. ABSTRACT UNIT OF WORK
class AbstractUnitOfWork(ABC):
    users: UserRepository
    applications: ApplicationRepository

    def __enter__(self) -> "AbstractUnitOfWork":
        return self

    def __exit__(self, exc_type, exc_val, exc_tb) -> None:
        if exc_type is not None:
            self.rollback()

    @abstractmethod
    def commit(self) -> None:
        pass

    @abstractmethod
    def rollback(self) -> None:
        pass


# 4. CONCRETE REPOSITORIES

# --- In-Memory Implementations (For Testing) ---
class InMemoryUserRepository(UserRepository):
    def __init__(self, storage: Optional[List[User]] = None) -> None:
        self._storage = storage if storage is not None else []

    def add(self, user: User) -> None:
        self._storage.append(user)

    def get_by_id(self, user_id: str) -> Optional[User]:
        return next((u for u in self._storage if u.id == user_id), None)


class InMemoryApplicationRepository(ApplicationRepository):
    def __init__(self, storage: Optional[List[Application]] = None) -> None:
        self._storage = storage if storage is not None else []

    def add(self, application: Application) -> None:
        self._storage.append(application)

    def get_by_id(self, app_id: str) -> Optional[Application]:
        return next((a for a in self._storage if a.id == app_id), None)


# --- SQLAlchemy / Database Implementations ---
class SqlAlchemyUserRepository(UserRepository):
    def __init__(self, session) -> None:
        self.session = session

    def add(self, user: User) -> None:
        # Real code: self.session.add(user)
        self.session.users.append(user)

    def get_by_id(self, user_id: str) -> Optional[User]:
        return next((u for u in self.session.users if u.id == user_id), None)


class SqlAlchemyApplicationRepository(ApplicationRepository):
    def __init__(self, session) -> None:
        self.session = session

    def add(self, application: Application) -> None:
        # Real code: self.session.add(application)
        self.session.applications.append(application)

    def get_by_id(self, app_id: str) -> Optional[Application]:
        return next((a for a in self.session.applications if a.id == app_id), None)


# 5. CONCRETE UNITS OF WORK

class SqlAlchemyUnitOfWork(AbstractUnitOfWork):
    def __init__(
        self,
        session_factory,
        user_repo_cls: Type[UserRepository] = SqlAlchemyUserRepository,
        app_repo_cls: Type[ApplicationRepository] = SqlAlchemyApplicationRepository,
    ) -> None:
        self.session_factory = session_factory
        self.user_repo_cls = user_repo_cls
        self.app_repo_cls = app_repo_cls

    def __enter__(self) -> "SqlAlchemyUnitOfWork":
        # Create session and inject it into repository instances
        self.session = self.session_factory()
        self.users = self.user_repo_cls(self.session)
        self.applications = self.app_repo_cls(self.session)
        return self

    def __exit__(self, exc_type, exc_val, exc_tb) -> None:
        super().__exit__(exc_type, exc_val, exc_tb)
        self.session.close()

    def commit(self) -> None:
        self.session.commit()

    def rollback(self) -> None:
        self.session.rollback()


class FakeUnitOfWork(AbstractUnitOfWork):
    """In-memory Unit of Work for fast unit testing without DB setup."""

    def __init__(self) -> None:
        self.users = InMemoryUserRepository()
        self.applications = InMemoryApplicationRepository()
        self.committed = False

    def commit(self) -> None:
        self.committed = True

    def rollback(self) -> None:
        pass


# 6. APPLICATION SERVICE LAYER (Consumer of UoW)
class RegistrationService:
    def __init__(self, uow: AbstractUnitOfWork) -> None:
        self.uow = uow

    def register_user_with_app(
        self, user_id: str, name: str, app_id: str, service_name: str
    ) -> None:
        # Context manager handles setup, auto-rollback on error, and teardown
        with self.uow:
            user = User(id=user_id, name=name)
            app = Application(id=app_id, user_id=user_id, service_name=service_name)

            self.uow.users.add(user)
            self.uow.applications.add(app)
            self.uow.commit()


# --- DEMO USAGE ---

# Mock database session for illustration
class MockSession:
    def __init__(self) -> None:
        self.users: List[User] = []
        self.applications: List[Application] = []

    def commit(self) -> None:
        print("Database transaction COMMITTED.")

    def rollback(self) -> None:
        print("Database transaction ROLLED BACK.")

    def close(self) -> None:
        print("Database session CLOSED.")


# 1. Production Workflow (using SqlAlchemyUnitOfWork)
print("=== Production Execution ===")
session_factory = lambda: MockSession()
prod_uow = SqlAlchemyUnitOfWork(session_factory=session_factory)

service = RegistrationService(uow=prod_uow)
service.register_user_with_app(
    user_id="usr_101",
    name="Alice",
    app_id="app_501",
    service_name="BillingService",
)

# 2. Unit Testing Workflow (using FakeUnitOfWork)
print("\n=== Unit Test Execution ===")
test_uow = FakeUnitOfWork()
test_service = RegistrationService(uow=test_uow)

test_service.register_user_with_app(
    user_id="usr_102",
    name="Bob",
    app_id="app_502",
    service_name="AuthService",
)

assert test_uow.committed is True
assert test_uow.users.get_by_id("usr_102").name == "Bob"
print("Unit test assertions PASSED successfully!")