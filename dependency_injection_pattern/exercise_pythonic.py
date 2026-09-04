from typing import Protocol


# 1. DEFINE PROTOCOLS (Interfaces, not Factories)
class UserRepository(Protocol):
    def create_user(self, username: str, hashed_password: str) -> None: ...
    def get_user(self, username: str) -> bool: ...


class PasswordHasher(Protocol):
    def hash(self, password: str) -> str: ...


class NotificationSender(Protocol):
    def welcome_email(self, message: str) -> str: ...


# 2. CONCRETE IMPLEMENTATIONS
class InMemoUserRepository:
    def __init__(self) -> None:
        self.storage: dict[str, str] = {}

    def create_user(self, username: str, hashed_password: str) -> None:
        self.storage[username] = hashed_password

    def get_user(self, username: str) -> bool:
        return username in self.storage


class SimplePasswordHasher:
    def hash(self, password: str) -> str:
        # In real life: return bcrypt.hash(password)
        return f"hashed_{password}"


class ConsoleNotificationSender:
    def welcome_email(self, message: str) -> str:
        print(f"Sent email: {message}")
        return "sent"


# 3. SERVICE ORCHESTRATOR (Proper Dependency Injection)
class UserRegistrationService:
    def __init__(
        self,
        repository: UserRepository,
        password_hasher: PasswordHasher,
        notification_sender: NotificationSender,
    ) -> None:
        # Type hints bind the parameters to the Protocols above
        self._repository = repository
        self._password_hasher = password_hasher
        self._notification_sender = notification_sender

    def register(self, username: str, raw_password: str) -> None:
        """Orchestrates the entire registration workflow in one place."""
        if self._repository.get_user(username):
            raise ValueError(f"User '{username}' already exists.")

        # Step 1: Hash Password
        hashed_password = self._password_hasher.hash(raw_password)

        # Step 2: Store in Repository
        self._repository.create_user(username, hashed_password)

        # Step 3: Notify User
        self._notification_sender.welcome_email(
            f"Welcome, {username}! Your account is active."
        )


# --- USAGE ---
repo = InMemoUserRepository()
hasher = SimplePasswordHasher()
sender = ConsoleNotificationSender()

# Inject concrete dependencies into service
service = UserRegistrationService(
    repository=repo, password_hasher=hasher, notification_sender=sender
)

service.register("alice", "secret123")

