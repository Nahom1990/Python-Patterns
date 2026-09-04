from dataclasses import dataclass
from typing import Protocol, Optional, List, Dict


# 1. DOMAIN MODEL
@dataclass
class Service:
    id: str
    name: str


# 2. PROTOCOL INTERFACE
class ServiceRepository(Protocol):
    def get_service_by_id(self, id: str) -> Optional[Service]: ...
    def get_service_by_name(self, name: str) -> Optional[Service]: ...
    def get_all_services(self) -> List[Service]: ...
    def save_service(self, service: Service) -> Service: ...
    def delete_service(self, id: str) -> bool: ...


# 3. REPOSITORY IMPLEMENTATIONS

class PostgresRepository:
    """Mock SQL/SQLAlchemy implementation returning Service dataclass instances."""

    def get_service_by_id(self, id: str) -> Optional[Service]:
        # Simulating DB query fetch
        return Service(id=id, name=f"Postgres-Service-{id}")

    def get_service_by_name(self, name: str) -> Optional[Service]:
        return Service(id="pg_123", name=name)

    def get_all_services(self) -> List[Service]:
        return [
            Service(id="1", name="Auth Service"),
            Service(id="2", name="Payment Service"),
        ]

    def save_service(self, service: Service) -> Service:
        # Simulating session.add(service) / session.commit()
        return service

    def delete_service(self, id: str) -> bool:
        return True


class InMemRepository:
    """In-Memory implementation backed by a dictionary."""

    def __init__(self) -> None:
        # Storage maps id -> Service object
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


# 4. APPLICATION SERVICE LAYER
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

# Initialize in-memory storage and inject into service layer
repo = InMemRepository()
service_layer = ServiceManagementService(repository=repo)

# 1. Register a service
new_service = service_layer.register_new_service(id="srv_01", name="Billing API")
print(f"Registered: {new_service}")

# 2. Retrieve service by ID
fetched = service_layer.get_service_by_id("srv_01")
print(f"Fetched by ID: {fetched}")

# 3. List all services
all_services = service_layer.list_services()
print(f"All Services: {all_services}")