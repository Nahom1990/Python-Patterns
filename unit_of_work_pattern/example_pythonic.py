from dataclasses import dataclass
from typing import Any, Callable, List, Optional, Protocol, Self, TypeVar


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


# 2. PROTOCOLS (Structural Typing Interfaces)
class UserRepository(Protocol):
    def add(self, user: User) -> None: ...
    def get_by_id(self, user_id: str) -> Optional[User]: ...


class ApplicationRepository(Protocol):
    def add(self, application: Application) -> None: ...
    def get_by_id(self, app_id: str) -> Optional[Application]: ...


class UnitOfWork(Protocol):
    users: UserRepository
    applications: ApplicationRepository

    def __enter__(self) -> Self: ...
    def __exit__(self, exc_type, exc_val, exc_tb) -> None: ...
    def commit(self) -> None: ...
    def rollback(self) -> None: ...


# 3. CONCRETE REPOSITORIES (No inheritance required!)

# --- In-Memory Implementations ---
class InMemoryUserRepository:
    def __init__(self, storage: Optional[List[User]] = None) -> None:
        self._storage = storage if storage is not None else []

    def add(self, user: User) -> None:
        self._storage.append(user)

    def get_by_id(self, user_id: str) -> Optional[User]:
        return next((u for u in self._storage if u.id == user_id), None)


class InMemoryApplicationRepository:
    def __init__(self, storage: Optional[List[Application]] = None) -> None:
        self._storage = storage if storage is not None else []

    def add(self, application: Application) -> None:
        self._storage.append(application)

    def get_by_id(self, app_id: str) -> Optional[Application]:
        return next((a for a in self._storage if a.id == app_id), None)


# --- Database Implementations ---
class SqlAlchemyUserRepository:
    def __init__(self, session: Any) -> None:
        self.session = session

    def add(self, user: User) -> None:
        self.session.users.append(user)

    def get_by_id(self, user_id: str) -> Optional[User]:
        return next((u for u in self.session.users if u.id == user_id), None)


class SqlAlchemyApplicationRepository:
    def __init__(self, session: Any) -> None:
        self.session = session

    def add(self, application: Application) -> None:
        self.session.applications.append(application)

    def get_by_id(self, app_id: str) -> Optional[Application]:
        return next((a for a in self.session.applications if a.id == app_id), None)


# 4. CONCRETE UNITS OF WORK (Zero Base Inheritance)

class SqlAlchemyUnitOfWork:
    def __init__(
        self,
        session_factory: Callable[[], Any],
        user_repo_cls: Callable[[Any], UserRepository] = SqlAlchemyUserRepository, #uninstantiated because it needs the session factory to be instantaiated 
        app_repo_cls: Callable[[Any], ApplicationRepository] = SqlAlchemyApplicationRepository,#same
    ) -> None:
        self.session_factory = session_factory
        self.user_repo_cls = user_repo_cls
        self.app_repo_cls = app_repo_cls

    def __enter__(self) -> Self:
        self.session = self.session_factory()
        self.users = self.user_repo_cls(self.session) #now instantiated
        self.applications = self.app_repo_cls(self.session)
        return self

    def __exit__(self, exc_type, exc_val, exc_tb) -> None:
        if exc_type is not None:
            self.rollback()
        self.session.close()

    def commit(self) -> None:
        self.session.commit()

    def rollback(self) -> None:
        self.session.rollback()


class FakeUnitOfWork:
    """In-memory Unit of Work matching the UnitOfWork Protocol structural contract."""

    def __init__(self) -> None:
        self.users: UserRepository = InMemoryUserRepository()
        self.applications: ApplicationRepository = InMemoryApplicationRepository()
        self.committed = False

    def __enter__(self) -> Self:
        return self

    def __exit__(self, exc_type, exc_val, exc_tb) -> None:
        if exc_type is not None:
            self.rollback()

    def commit(self) -> None:
        self.committed = True

    def rollback(self) -> None:
        pass


# 5. APPLICATION SERVICE LAYER (Consumes the Protocol interface)
class RegistrationService:
    def __init__(self, uow: UnitOfWork) -> None:
        self.uow = uow

    def register_user_with_app(
        self, user_id: str, name: str, app_id: str, service_name: str
    ) -> None:
        with self.uow:
            user = User(id=user_id, name=name)
            app = Application(id=app_id, user_id=user_id, service_name=service_name)

            self.uow.users.add(user)
            self.uow.applications.add(app)
            self.uow.commit()


# --- DEMO USAGE ---

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


# 1. Production Execution
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

# 2. Unit Test Execution
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