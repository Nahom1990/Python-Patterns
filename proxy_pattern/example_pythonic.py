from typing import Protocol


class UserServiceProtocol(Protocol):

    def get_user(self, user_id: int)->dict:
        ...

class UserService:

    def get_user(self, user_id: int):
        print(f"Fetching user {user_id}")

        return {
            "id": user_id,
            "name": "Nahom",
        }

class UserServiceProxy:

    def __init__(
        self,
        service: UserServiceProtocol,
        is_admin: bool,
    ):
        self.service = service
        self.is_admin = is_admin

    def get_user(self, user_id: int):

        if not self.is_admin:
            raise PermissionError(
                "Only administrators can access users"
            )

        return self.service.get_user(user_id)

service = UserService()

proxy = UserServiceProxy(
    service,
    is_admin=True,
)

proxy.get_user(123)