##### Version 3.1---Function Parameter Injection ##############
from typing import Callable, Any

# --- DEPENDENCY FUNCTIONS ---
storage: dict[str, str] = {}

def db_create_user(username: str, hashed_password: str) -> None:
    storage[username] = hashed_password

def db_get_user(username: str) -> bool:
    return username in storage

def hash_password(password: str) -> str:
    return f"hashed_{password}"

def send_welcome_email(recipient: str, message: str) -> str:
    print(f"Sent email to {recipient}: {message}")
    return "sent"


# --- TYPE ALIASES FOR CLEANER FUNCTION SIGNATURES ---
UserExistenceCheck = Callable[[str], bool]
PasswordHasherFunc = Callable[[str], str]
UserSaverFunc = Callable[[str, str], None]
NotificationFunc = Callable[[str, str], str]


# --- SERVICE FUNCTION (INJECTING DEPENDENCIES VIA PARAMETERS) ---
def register_user(
    username: str,
    raw_password: str,
    # Injected dependencies:
    check_exists: UserExistenceCheck,
    hash_pwd: PasswordHasherFunc,
    save_user: UserSaverFunc,
    send_email: NotificationFunc,
) -> None:
    """Pure functional workflow orchestrator."""
    if check_exists(username):
        raise ValueError(f"User {username} already exists")

    # 1. Hash
    hashed = hash_pwd(raw_password)

    # 2. Save
    save_user(username, hashed)

    # 3. Notify
    send_email(username, "Welcome to the system!")


# --- USAGE ---
register_user(
    username="alice",
    raw_password="secret123",
    check_exists=db_get_user,
    hash_pwd=hash_password,
    save_user=db_create_user,
    send_email=send_welcome_email,
)
##### Version 3.2 Closure  ##############

from typing import Callable, Any

# --- DEPENDENCY FUNCTIONS ---
storage2: dict[str, str] = {}

def db_create_user2(username: str, hashed_password: str) -> None:
    storage[username] = hashed_password

def db_get_user2(username: str) -> bool:
    return username in storage

def hash_password2(password: str) -> str:
    return f"hashed_{password}"

def send_welcome_email2(recipient: str, message: str) -> str:
    print(f"Sent email to {recipient}: {message}")
    return "sent"


# --- TYPE ALIASES FOR CLEANER FUNCTION SIGNATURES ---
UserExistenceCheck2 = Callable[[str], bool]
PasswordHasherFunc2 = Callable[[str], str]
UserSaverFunc2 = Callable[[str, str], None]
NotificationFunc2 = Callable[[str, str], str]

#above here its the same as the 3.1 approach
RegisterUserFunc2 = Callable[[str, str], None]

# 3. CLOSURE FACTORY (INJECT DEPENDENCIES HERE)
def make_user_registration_service(
    check_exists: UserExistenceCheck2,
    hash_pwd: PasswordHasherFunc2,
    save_user: UserSaverFunc2,
    send_email: NotificationFunc2,
) -> RegisterUserFunc2:
    """
    Factory function: Accepts dependencies in the outer scope,
    and returns a inner function that closes over them.
    """
    def register(username: str, raw_password: str) -> None:
        # The inner function has access to the outer dependencies via Closure
        if check_exists(username):
            raise ValueError(f"User {username} already exists")

        # 1. Hash
        hashed = hash_pwd(raw_password)

        # 2. Save
        save_user(username, hashed)

        # 3. Notify
        send_email(username, "Welcome to the system!")

    return register

##use case # --- STEP 1: COMPOSITION ROOT (App Startup) ---
# Inject dependencies into the closure ONCE
register_user2 = make_user_registration_service(
    check_exists=db_get_user2,
    hash_pwd=hash_password2,
    save_user=db_create_user2,
    send_email=send_welcome_email2,
)

# --- STEP 2: APPLICATION RUNTIME ---
# Anywhere in your web framework, API route, or CLI:
# You call `register_user` WITHOUT passing the dependencies every time!

register_user2("alice", "secret123")
register_user2("bob", "password456")