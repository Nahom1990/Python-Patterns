from typing import Protocol


class User:

    def __init__(self, id, name, email):
        self.id = id
        self.name = name
        self.email = email

class UserRepository(Protocol):

    def get_by_id(self, user_id: int) -> User | None:
        ...

    def save(self, user: User) -> None:
        ...


class PostgreSQLUserRepository:

    def get_by_id(self, user_id: int) -> User | None:
        ...

    def save(self, user: User) -> None:
        ...


class UserService:

    def __init__(self, repository: UserRepository):
        self.repository = repository  #And this is where Repository + Dependency Injection connect:

    def get_user(self, user_id: int):
        return self.repository.get_by_id(user_id)



service = UserService(PostgreSQLUserRepository())