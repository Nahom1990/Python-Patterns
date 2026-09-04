
from contextlib import contextmanager
from dataclasses import dataclass
from typing import Callable, Generator, Any

# 1. IMMUTABLE DOMAIN ENTITIES
@dataclass(frozen=True)
class User:
    id: str
    name: str


@dataclass(frozen=True)
class Application:
    id: str
    user_id: str
    service_name: str


# 2. FUNCTIONAL REPOSITORY FACTORIES (CLOSURES)

def create_user_repository(session: dict[str, Any]):
    """Returns functions closed over the active transaction session."""
    def save_user(user: User) -> None:
        session["users"].append(user)

    def get_user(user_id: str) -> User | None:
        return next((u for u in session["users"] if u.id == user_id), None)

    return save_user, get_user


def create_application_repository(session: dict[str, Any]):
    def save_app(app: Application) -> None:
        session["applications"].append(app)

    return save_app


# 3. FUNCTIONAL UOW (GENERATOR CONTEXT MANAGER FACTORY)

# Immutable bundle of repository functions yielded to the caller
@dataclass(frozen=True)
class FunctionalUoW:
    save_user: Callable[[User], None]
    get_user: Callable[[str], User | None]
    save_app: Callable[[Application], None]


def make_uow_runner(session_factory: Callable[[], dict[str, Any]]):
    """
    Higher-order function returning a functional UoW context manager.
    Injects dependencies at application startup (Composition Root).
    """
    @contextmanager
    def uow() -> Generator[FunctionalUoW, None, None]:
        session = session_factory()

        # Bind repository functions to this specific session context
        save_user, get_user = create_user_repository(session)
        save_app = create_application_repository(session)

        uow_bundle = FunctionalUoW(
            save_user=save_user,
            get_user=get_user,
            save_app=save_app,
        )

        try:
            yield uow_bundle
            session["commit"]()  # Auto-commit on clean completion
        except Exception:
            session["rollback"]()  # Auto-rollback on error
            raise
        finally:
            session["close"]()  # Auto-close connection resources

    return uow


# 4. PURE BUSINESS LOGIC WORKFLOW

def register_user_service(
    uow_runner: Callable[[], Generator[FunctionalUoW, None, None]],
    user_id: str,
    name: str,
    app_id: str,
    service_name: str,
) -> User:
    """Business workflow running inside the functional context manager."""
    user = User(id=user_id, name=name)
    app = Application(id=app_id, user_id=user_id, service_name=service_name)

    # Context manager handles enter, commit, rollback, and exit automatically
    with uow_runner() as uow:
        uow.save_user(user)
        uow.save_app(app)

    return user


# --- USAGE / DEMONSTRATION ---

def create_db_session():
    return {
        "users": [],
        "applications": [],
        "commit": lambda: print("--> Transaction COMMITTED"),
        "rollback": lambda: print("--> Transaction ROLLED BACK"),
        "close": lambda: print("--> Session CLOSED"),
    }


# Startup: Configure UoW runner with session factory
run_uow = make_uow_runner(session_factory=create_db_session)

# Execution 1: Success path
print("--- Execution 1: Successful Registration ---")
register_user_service(
    uow_runner=run_uow,
    user_id="usr_101",
    name="Alice",
    app_id="app_501",
    service_name="BillingService",
)

# Execution 2: Error handling path
print("\n--- Execution 2: Error & Auto Rollback ---")
def failing_workflow(uow_runner):
    with uow_runner() as uow:
        uow.save_user(User(id="usr_102", name="Bob"))
        raise RuntimeError("Database constraint violated!")

try:
    failing_workflow(run_uow)
except RuntimeError as err:
    print(f"Caught error: {err}")