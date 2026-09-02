"""a behavioral design pattern that passes a request along 
a sequential chain of potential handlers. Upon receiving a request, 
each handler decides either to process the request or forward it to 
the next handler in the chain.Think of it as an object-oriented alternative 
to a massive if-elif-elif-else block. 
It decouples the sender of a request from its receivers, allowing you to
 dynamically rearrange or add new handlers at runtime without breaking existing code.
 
 mostly seen in 
HTTP middleware
authentication pipelines
validation pipelines
event processing
exception handling
approval workflows.

example:

Request
   ↓
handler 1=Authentication
   ↓
handler2=Authorization
   ↓
h3=Validation
   ↓
h4=Rate Limiting
   ↓
h5=Business Logic


A handler can say:

Continue

My responsibility succeeded
        ↓
Next handler

or 

Stop
Something failed
        ↓
STOP """
#here protocol is a bad designbecause we actually need inheritance , so we would lose
#the state like self.next_handler, if we use protocol we would have to copy paste boiler plate so many times
#because chain by nature must have some shared state to work as a pattern. so its not the right tool here
class Request:
    def __init__(self, user: str | None, token: str | None):
        self.user = user
        self.token = token


from abc import ABC, abstractmethod


class Handler(ABC):

    def __init__(self):
        self.next_handler = None #shared

    def set_next(self, handler): #shared
        self.next_handler = handler
        return handler

    @abstractmethod
    def handle(self, request):
        pass

    def next(self,request):#shared

        if self.next_handler:#what creates the chain is this 
            return self.next_handler.handle(request)

        return None

class AuthenticationHandler(Handler):

    def handle(self, request):

        if request.token is None:
            raise PermissionError("Authentication required")

        print("Authentication passed")

        return self.next(request)

class AuthorizationHandler(Handler):

    def handle(self, request):

        if request.user != "admin":
            raise PermissionError("Not authorized")

        print("Authorization passed")

        return self.next(request)

class RateLimitHandler(Handler):

    def handle(self, request):

        print("Rate limit check passed")

        return self.next(request)

#use 
authentication = AuthenticationHandler()

authorization = AuthorizationHandler()

rate_limit = RateLimitHandler()

##create the chain 
authentication.set_next(authorization).set_next(rate_limit)
"""Authentication
      ↓
Authorization
      ↓
Rate Limit"""
request=Request(user="nahom",token="qwerty")
authentication.handle(request)   #executes all the chain from auth to rate limit


"""The client does:

authentication.handle(request)

The client does not do:

authentication.handle(request)
authorization.handle(request)
rate_limit.handle(request)"""