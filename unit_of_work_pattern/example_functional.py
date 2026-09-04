from dataclasses import dataclass
from typing import Callable, TypeVar, Any

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


# 2. TRANSACTION WRAPPER (THE ENGINE)
T = TypeVar("T")

def run_transaction(
    work: Callable[[], T],
    commit: Callable[[], None],
    rollback: Callable[[], None],
) -> T:
    """Executes 'work' inside a controlled transaction context."""
    try:
        result = work()
        commit()
        return result
    except Exception:
        rollback()
        raise


# 3. FUNCTIONAL REPOSITORY FACTORIES (CLOSURES)

def create_user_repository(session: dict[str, Any]):
    def save_user(user: User) -> None:
        session["users"].append(user)

    def get_user_by_id(user_id: str) -> User | None:
        return next((u for u in session["users"] if u.id == user_id), None)

    return save_user, get_user_by_id


def create_application_repository(session: dict[str, Any]):
    def save_application(app: Application) -> None:
        session["applications"].append(app)

    return save_application


# 4. BUSINESS LOGIC (PURE WORK UNITS)

def register_user_workflow(
    save_user: Callable[[User], None],
    save_app: Callable[[Application], None],
    user_id: str,
    name: str,
    app_id: str,
    service_name: str,
) -> User:
    """Pure domain orchestration logic. Knows nothing about transactions, commits, or rollbacks."""
    user = User(id=user_id, name=name)
    app = Application(id=app_id, user_id=user_id, service_name=service_name)

    save_user(user)
    save_app(app)

    return user


# --- USAGE DEMONSTRATION ---

# Mock DB Session
def create_session():
    return {
        "users": [],
        "applications": [],
        "commit": lambda: print("--> Database transaction COMMITTED successfully."),
        "rollback": lambda: print("--> Database transaction ROLLED BACK due to error."),
    }


# Step A: Create session & bind repository closures
db_session = create_session()
save_user, get_user = create_user_repository(db_session)
save_app = create_application_repository(db_session)

# Step B: Define the business 'work' to execute
def register_alice():
    return register_user_workflow(
        save_user=save_user,
        save_app=save_app,
        user_id="usr_101",
        name="Alice",
        app_id="app_501",
        service_name="BillingService",
    )

# Step C: Execute inside the Transaction Wrapper
print("--- Test 1: Successful Registration ---")
created_user = run_transaction(
    work=register_alice,
    commit=db_session["commit"],
    rollback=db_session["rollback"],
)
print(f"Registered User: {created_user}\n")


# Step D: Test Failure & Automatic Rollback
def failing_work():
    save_user(User(id="usr_102", name="Bob"))
    raise RuntimeError("Payment service connection timed out!")

print("--- Test 2: Failed Transaction ---")
try:
    run_transaction(
        work=failing_work,
        commit=db_session["commit"],
        rollback=db_session["rollback"],
    )
except RuntimeError as err:
    print(f"Caught error in application layer: {err}")



