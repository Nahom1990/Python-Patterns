"""
You're building the persistence layer for your government-service platform.

Your application has these domain objects:

Service
Document
Office
ServiceStep

A Service might look conceptually like:

Service
├── id
├── name
├── description
├── category
├── active

Your application needs to perform operations such as:

    get service by ID
    get service by name
    list active services
    save a service
    delete a service


Your task

Design and implement a ServiceRepository that separates application logic from persistence.

Your implementation should have:

    A repository abstraction.
    A concrete persistence implementation.
    An in-memory implementation useful for testing.
    A service/application layer that depends only on the repository abstraction.
    Dependency injection at the composition/wiring point.


Important architectural requirement

Don't just make a thin wrapper around a dictionary.

Think about what the repository boundary should expose to the application, rather than exposing storage-specific operations.

For example, the application should be able to say:

service = repository.get_by_id(service_id)

but shouldn't care whether the implementation uses:

    PostgreSQL
    SQLAlchemy
    a dictionary
    an HTTP API


Constraints

Build it in two versions:

Version 1 — Classical OOP

    Use:

    ABC
    abstractmethod
    concrete repository implementations
    constructor injection

Version 2 — Modern Python

    Use:

    Protocol
    structural typing
    type hints
    constructor injection
"""

from abc import ABC, abstractmethod
from dataclasses import dataclass
from typing import Optional, List, Dict


# 1. DOMAIN MODEL
@dataclass
class Service:
    id: str
    name: str


# 2. ABSTRACT BASE CLASS (INTERFACE CONTRACT)
class ServiceRepository(ABC):
    @abstractmethod
    def get_service_by_id(self, id: str) -> Optional[Service]:
        pass

    @abstractmethod
    def get_service_by_name(self, name: str) -> Optional[Service]:
        pass

    @abstractmethod
    def get_all_services(self) -> List[Service]:
        pass

    @abstractmethod
    def save_service(self, service: Service) -> Service:
        pass

    @abstractmethod
    def delete_service(self, id: str) -> bool:
        pass


# 3. REPOSITORY IMPLEMENTATIONS (EXPLICIT SUBCLASSING)

class PostgresRepository(ServiceRepository):
    """Mock SQLAlchemy/Postgres repository subclassing ServiceRepository."""

    def get_service_by_id(self, id: str) -> Optional[Service]:
        return Service(id=id, name=f"Postgres-Service-{id}")

    def get_service_by_name(self, name: str) -> Optional[Service]:
        return Service(id="pg_999", name=name)

    def get_all_services(self) -> List[Service]:
        return [
            Service(id="1", name="Auth Service"),
            Service(id="2", name="Payment Service"),
        ]

    def save_service(self, service: Service) -> Service:
        # Simulating DB persist
        return service

    def delete_service(self, id: str) -> bool:
        return True


class InMemRepository(ServiceRepository):
    """In-Memory dictionary repository subclassing ServiceRepository."""

    def __init__(self) -> None:
        self._storage: Dict[str, Service] = {}

    def get_service_by_id(self, id: str) -> Optional[Service]:
        return self._storage.get(id)

    def get_service_by_name(self, name: str) -> Optional[Service]:
        for service in self._storage.values():
            if service.name == name:
                return service
        return None

    def get_all_services(self) -> List[Service]:
        return list(self._storage.values())

    def save_service(self, service: Service) -> Service:
        self._storage[service.id] = service
        return service

    def delete_service(self, id: str) -> bool:
        if id in self._storage:
            del self._storage[id]
            return True
        return False


# 4. APPLICATION SERVICE LAYER/ now its just using the repo api but this is for
#demo only it would add a lot of business logic ontop of it like ratelimits , redis,custom exceptions ,business logics, etc...
class ServiceManagementService:
    def __init__(self, repository: ServiceRepository) -> None:
        self._repository = repository

    def get_service_by_id(self, id: str) -> Optional[Service]:
        return self._repository.get_service_by_id(id)

    def register_new_service(self, id: str, name: str) -> Service:
        service = Service(id=id, name=name)
        return self._repository.save_service(service)

    def list_services(self) -> List[Service]:
        return self._repository.get_all_services()

    def remove_service(self, id: str) -> bool:
        return self._repository.delete_service(id)


# --- USAGE DEMONSTRATION ---

# 1. Inject Postgres implementation
postgres_repo = PostgresRepository()
service_layer_pg = ServiceManagementService(repository=postgres_repo)
print(service_layer_pg.get_service_by_id("pg_01"))

# 2. Inject In-Memory implementation
in_mem_repo = InMemRepository()
service_layer_mem = ServiceManagementService(repository=in_mem_repo)

created = service_layer_mem.register_new_service("srv_100", "Analytics API")
print(f"Created: {created}")
print(f"Fetched: {service_layer_mem.get_service_by_id('srv_100')}")