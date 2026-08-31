"""
You're building a small HTTP API client.

The core client can make a request:

response = client.request(
    method="GET",
    url="/users"
)

Initially:

BasicApiClient

just makes the request.

But the application may optionally need:

Authentication
Logging
Retry
Metrics

You want to combine them dynamically.

For example:

Metrics
   │
Logging
   │
Retry
   │
Authentication
   │
BasicApiClient

The client should still expose:

request(method, url)


Requirements
Base component

Create:

BasicApiClient

with:

request(method, url)

It can simply return something like:

{
    "status": 200,
    "url": url
}
Decorator 1 — Authentication

Before the request:

Attach authentication

Then delegate.

Decorator 2 — Logging

Before:

Log request

After:

Log response

Decorator 3 — Retry

If the underlying request fails:

Try again

You can simulate failure with an exception.

Decorator 4 — Metrics

Measure:

How long did the request take?

You can use:

time.perf_counter()


Your job

Implement the project in:

Version 1
Classical GoF
ABC
abstractmethod
Base Decorator
Concrete Decorators
Version 2
Modern Python

Use:

Protocol

No ABC.

Version 3
Pythonic function decorators

Your underlying operation can be a function:

def request(method, url):
    ...

Then create decorators like:

@logging
@retry
@metrics
def request(...):
    ...
"""



#version 1
from abc import ABC,abstractmethod
import time
class ApiClient(ABC):
    @abstractmethod
    def request(self,method:str,url:str)->dict:
        pass

class BasicApiClient(ApiClient):
    def request(self,method,url)->dict:
        return {"status": 200,"url": url}

class BaseDecorator(ApiClient):
    def __init__(self,api_client:ApiClient) -> None:
        self.api_client=api_client

class Authentication(BaseDecorator):
    def request(self,method,url)->dict:
        print("authenticating")
        return self.api_client.request(method,url)
class Logging(BaseDecorator):
    def request(self, method: str, url: str) -> dict:
        print("start logging")
        result=self.api_client.request(method,url)
        print("finished logging")
        return result
class Retry(BaseDecorator):
    def request(self, method: str, url: str) -> dict:
        last_exception:Exception | None=None
        for attempt in range(3):
            try:
                result=self.api_client.request(method,url)
                return result
            except Exception as e:
                print(f"retrying {attempt+1}")
                last_exception=e
        raise RuntimeError(f"failed attempts") from last_exception
class Mertrics(BaseDecorator):
    def request(self, method: str, url: str) -> dict:
        start_time=time.time()
        result=self.api_client.request(method,url)
        finish_time=time.time()
        request_time=finish_time-start_time
        print(request_time)
        return result

###version 2 
from typing import Protocol

class Apiclien2(Protocol):
    def request(self,method,url)->dict:
        ...                
class BasicApiClient2:
    def request(self,method,url):
        return {"status": 200,"url": url}

class Logging2:
    def __init__(self,api_client2:Apiclien2) -> None:
        self.api_client2=api_client2
    def request(self,method,url):
        print("start logging")
        result=self.api_client2.request(method,url)
        print("finished logging")
        return result
class Retry2:
    def __init__(self,api_client2:Apiclien2) -> None:
            self.api_client2=api_client2
    def request(self, method: str, url: str) -> dict:
        last_exception:Exception | None=None
        for attempt in range(3):
            try:
                result=self.api_client2.request(method,url)
                return result
            except Exception as e:
                print(f"retrying {attempt+1}")
                last_exception=e
        raise RuntimeError(f"failed attempts") from last_exception
class Mertrics2:
    def __init__(self,api_client2:Apiclien2) -> None:
            self.api_client2=api_client2
    def request(self, method: str, url: str) -> dict:
        start_time=time.time()
        result=self.api_client2.request(method,url)
        finish_time=time.time()
        request_time=finish_time-start_time
        print(request_time)
        return result

#version3 functional
from functools import wraps

def logging(func):
    @wraps(func)
    def wrapper(*args,**kwargs):
        print("start logging")
        result=func(*args,**kwargs)
        print("finish logging")
        return result
    return wrapper

def retry(func):
    @wraps(func)
    def wrapper(*args,**kwargs):
        last_exception=None
        for attempt in range(3):
            try:
                result=func(*args,**kwargs)
                return result
            except Exception as exc:
                last_exception = exc
                print(f"Attempt {attempt + 1} failed")
        raise RuntimeError("All attempts failed") from last_exception     
    return wrapper

def metric(func):
    @wraps(func)
    def wrapper(*args,**kwargs):
        start_time=time.time()
        result=func(*args,**kwargs)
        finish_time=time.time()
        print(f"finish time ={finish_time-start_time}")
        return result
    return wrapper


#use case
@logging
@retry
@metric
def request(method,url)->dict:
    return {"status": 200,"url": url}

request(method="GET",url="/user")