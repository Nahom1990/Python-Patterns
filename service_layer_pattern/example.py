#just a normal service layer that hides business logics and custom exceptions from the router,
#it takes in the repositories as dependecy injection 
#router should only handle service abstractions and http /status code exceptions
#the service layer shouldnt be a mere copy of the repository layer it should use the repository layer with somemore 
#business logics , this is here the logic of the main application lives
"""
Imagine your API endpoint starts looking like this:

@app.post("/applications")
async def create_application(data):
    user = await db.get_user(data.user_id)

    if not user:
        raise Exception("User not found")

    if user.age < 18:
        raise Exception("Not eligible")

    if not await db.has_required_documents(user):
        raise Exception("Missing documents")

    application = Application(...)

    await db.save(application)

    await send_email(user.email)

    await publish_event("application_created")

    return application


The endpoint is now doing everything:

    HTTP handling
    validation
    business rules
    database access
    persistence
    email
    events

That's a problem


                     HTTP 
                       │
                       ▼
              ┌─────────────────┐
              │  API /Router    │
              └────────┬────────┘
                       │
                       ▼
              ┌─────────────────┐
              │  Service Layer  │
              │          /      │
              │ Application     │
              └───────┬─────────┘
                      │
          ┌───────────┼───────────┐
          ▼           ▼           ▼
     Repository      UoW      External APIs
"""

from dataclasses import dataclass


@dataclass
class Application:
    id: str
    user_id: str
    service_id: str
    status: str

class UserRepository:
    def get_by_id(self, user_id):
        ...


class ApplicationRepository:
    def save(self, application):
        ...


class DocumentRepository:
    def has_required_documents(self, user_id, service_id):
        ...


class NotificationService:
    def send(self, user_id, message):
        ...

class ApplicationService:

    def __init__(
        self,
        users,
        applications,
        documents,
        notifications,
    ):
        self.users = users
        self.applications = applications
        self.documents = documents
        self.notifications = notifications

    def create_application(
        self,
        user_id,
        service_id,
    ):
        user = self.users.get_by_id(user_id)

        if user is None:
            raise ValueError("User not found")

        if not self.documents.has_required_documents(
            user_id,
            service_id,
        ):
            raise ValueError("Missing required documents")

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


"""
                FastAPI
                   │
                   ▼
           Application Service
                   │
        ┌──────────┼──────────┐
        ▼          ▼          ▼
   Repository  Repository  External API
        │          │
        └─────┬────┘
              ▼
       Unit of Work
              │
              ▼
           Database"""