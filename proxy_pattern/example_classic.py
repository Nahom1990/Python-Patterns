"""
A Proxy is a stand-in for another object.
The client thinks it's talking to the real object, but the Proxy gets an opportunity to control access.

Client
  │
  ▼
 Proxy
  │
  ▼
Real Object

ou want to speak to the CEO.

You don't walk directly into the CEO's office.

Instead:

You
 ↓
Receptionist
 ↓
CEO

The receptionist might:

verify who you are
check whether the CEO is available
deny access
schedule a meeting
redirect you somewhere else

The receptionist is acting as a Proxy.

The CEO is the real subject.

proxy is not just a gate to the ceo but it also controls access to the real object -ceo"""

from abc import ABC, abstractmethod


class UserServiceInterface(ABC):

    @abstractmethod
    def get_user(self, user_id: int)->dict:
        pass

class UserService(UserServiceInterface):

    def get_user(self, user_id: int):
        print(f"Fetching user {user_id} from database")

        return {
            "id": user_id,
            "name": "Nahom",
        }

class UserServiceProxy(UserServiceInterface):

    def __init__(
        self,
        user_service: UserServiceInterface,
        is_admin: bool,
    ):
        self.user_service = user_service
        self.is_admin = is_admin

    def get_user(self, user_id: int):

        if not self.is_admin:
            raise PermissionError(
                "Only administrators can access users"
            )

        return self.user_service.get_user(user_id)


##use
service = UserService()

proxy = UserServiceProxy(
    user_service=service,
    is_admin=True,
)

user = proxy.get_user(123)

"""
The client interacts with:

proxy.get_user(123)

rather than directly with:

service.get_user(123)

The Proxy controls whether the client can reach the real object.

Client
  ↓
AuthorizationProxy
  ↓
RealService

It checks permissions before allowing access.

other usecase: 

RateLimitProxy
AuthenticationProxy
PermissionProxy
TenantIsolationProxy
Protection / authorization
Lazy loading
Caching
Remote access
Rate limiting"""