"""
You're building the backend for a SaaS application.

When a new user registers, many things need to happen.

You have these existing subsystems:

UserRepository
PasswordService
EmailVerificationService
SubscriptionService
NotificationService
AuditLogger

Their responsibilities are roughly:

UserRepository
create_user(...)
PasswordService
hash_password(password)
EmailVerificationService
create_verification(user)
SubscriptionService
create_free_subscription(user)
NotificationService
send_welcome_email(user)
AuditLogger
log(event)
The Problem

Without a Facade, your API endpoint might look like:

API Endpoint
    │
    ├── Hash password
    ├── Create user
    ├── Create verification
    ├── Create subscription
    ├── Send welcome email
    └── Log registration

That means your API layer knows too much about the internal onboarding process.

You want the API layer to simply do:

onboarding.register_user(
    email="...",
    password="..."
)
Your Task

Create:

class UserOnboardingFacade:

It should receive the subsystem services through its constructor.

Then implement:

register_user(email, password)

The method should coordinate this workflow:

1. Hash password
        ↓
2. Create user
        ↓
3. Create email verification
        ↓
4. Create free subscription
        ↓
5. Send welcome email
        ↓
6. Log registration
Requirements
Version 1 — OOP/Class-based

Implement:

Subsystem classes
        +
UserOnboardingFacade

The API/client should only need:

facade.register_user(
    "user@example.com",
    "secret-password"
)
Version 2 — Pythonic/Functional

Try implementing the same idea using a function as the Facade:

def register_user(...):
    ...

The function coordinates the subsystem operations."""

class UserRepository:
    def create_user(self,username):
        print(f"user created with {username}")
        return username
class PasswordService:
    def hashpassword(self,password):
        print(f"hash the {password}")
        return "hashed the password"
class EmailVerificationService:
    def create_verification(self,user):
        print(f"verified {user}")
        return "verified email"
class SubscriptionService:
    def create_free_subscription(self,user):
        print(f"created free subscription for {user}")
        return "free sub created"
class NotificationService:
    def send_welcome_email(self,user):
        print(f"send welcome email to {user}")
        return "sent welcome email"
class AuditLogger:
    def log(self,events):
        for event in events:
            print(f"logged event {event}")



###version 1 class
class OnboardingFacade:
    def __init__(self,user_repo:UserRepository,
                 hash:PasswordService,
                 email:EmailVerificationService,
                 sub:SubscriptionService,
                 notification:NotificationService,
                 log:AuditLogger) -> None:
        self.user_repo=user_repo
        self.hash=hash
        self.email=email
        self.sub=sub
        self.notification=notification
        self.log=log

    def register_user(self,username,password):

        passwd=self.hash.hashpassword(password)
        user=self.user_repo.create_user(username=username)
        verify=self.email.create_verification(user)
        subscription=self.sub.create_free_subscription(user)
        notify=self.notification.send_welcome_email(user)
        self.log.log([user,passwd,verify,subscription,notify])

        return True
#use case
onboarding=OnboardingFacade(UserRepository(),PasswordService(),
                            EmailVerificationService(),
                           SubscriptionService(),NotificationService(),
                             AuditLogger())
onboarding.register_user("Nahom","mypassword")

#version2 functional

def register_user(username,password,
                  user_repo:UserRepository,
                 hash:PasswordService,
                 email:EmailVerificationService,
                 sub:SubscriptionService,
                 notification:NotificationService,
                 log:AuditLogger):
    
    passwd=hash.hashpassword(password)
    user=user_repo.create_user(username=username)
    verify=email.create_verification(user)
    subscription=sub.create_free_subscription(user)
    notify=notification.send_welcome_email(user)
    log.log([user,passwd,verify,subscription,notify])

    return True

#usecase
register_user("Nahom","mypassword",
              UserRepository(),PasswordService(),
                            EmailVerificationService(),
                           SubscriptionService(),NotificationService(),
                             AuditLogger())
