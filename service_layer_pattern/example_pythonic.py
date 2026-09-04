from typing import Protocol
from dataclasses import dataclass


@dataclass
class Application:
    id: str
    user_id: str
    service_id: str
    status: str

class UserRepository(Protocol):

    def get_by_id(self, user_id: str):
        ...


class ApplicationRepository(Protocol):

    def save(self, application: Application):
        ...


class DocumentRepository(Protocol):

    def has_required_documents(
        self,
        user_id: str,
        service_id: str,
    ) -> bool:
        ...


class NotificationService(Protocol):

    def send(
        self,
        user_id: str,
        message: str,
    ) -> None:
        ...


class ApplicationService:

    def __init__(
        self,
        users: UserRepository,
        applications: ApplicationRepository,
        documents: DocumentRepository,
        notifications: NotificationService,
    ):
        self.users = users
        self.applications = applications
        self.documents = documents
        self.notifications = notifications

    def create_application(
        self,
        user_id: str,
        service_id: str,
    ) -> Application:

        user = self.users.get_by_id(user_id)

        if user is None:
            raise ValueError("User not found")

        if not self.documents.has_required_documents(
            user_id,
            service_id,
        ):
            raise ValueError("Missing documents")

        application = Application(
            id="123",
            user_id=user_id,
            service_id=service_id,
            status="submitted",
        )

        self.applications.save(application)

        self.notifications.send(
            user_id,
            "Application submitted",
        )

        return application