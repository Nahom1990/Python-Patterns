"""Exercise 

You're building a small HTTP client library.

Your library needs to allow developers to construct an HTTP request with different optional configuration.

A request must contain:

    HTTP method
    URL

It may optionally contain:

    headers
    query parameters
    body
    timeout
    authentication token
    retry count

There are some rules:

    HTTP method and URL are required.
    HTTP method must be one of:
    GET
    POST
    PUT
    PATCH
    DELETE
    timeout must be greater than 0.
    retry_count cannot be negative.
    A GET request cannot have a body.
    The final Request object should contain the completed configuration.
    Construction should be readable through method chaining.
    Invalid configurations should be rejected when build() is called.
"""
from typing import Literal,Set,Dict,Any,Optional
HTTP_METHODS=Literal["GET","POST","PUT","PATCH","DELETE"]

class Request:
    def __init__(self,http_method,url,headers,query_params,body,
                 timeout,authentication_token,retry_count) -> None:
        self.http_method=http_method
        self.url=url
        self.headers=headers
        self.query_params=query_params
        self.body=body
        self.timeout=timeout
        self.authentication_token=authentication_token
        self.retry_count=retry_count

class RequestBuilder:
    VALID_METHODS: Set[str] = {"GET", "POST", "PUT", "PATCH", "DELETE"}
    def __init__(self,http_method,url) -> None:
        self.http_method=http_method
        self.url=url
        self.headers:Dict[str,str]={}
        self.query_params:Dict[str,Any]={}
        self.body:Any=None
        self.timeout:float=30
        self.authentication_token:Optional[str]=None
        self.retry_count:int=0

    def set_headers(self,headers):
        self.headers=headers
        return self
    def set_query_parameters(self,qp):
        self.query_params=qp
        return self
    def set_body(self,body):
        self.body=body
        return self
    def set_timeout(self,to):
        if to<0:
            raise ValueError("timeout must be above 0")
        self.timeout=to
        return self
    def set_auth(self,auth_token):
        self.authentication_token=auth_token
        return self
    def set_retry_count(self,rc):
        if rc < 0:
            raise ValueError("Retry count cannot be negative.")
        self.retry_count=rc
        return self
    
    def build(self,):
        if self.http_method is None:
            raise ValueError("http method is required")
        if self.url is None:
            raise ValueError("url is needed")
        if self.http_method not in self.VALID_METHODS:
            raise ValueError(f"http methods can only be one of {self.VALID_METHODS}")
        if self.http_method=="GET" and self.body is not None:
            raise ValueError("GET cant have a body")

        return Request(self.http_method,
                self.url,
                self.headers,
                self.query_params,
                self.body,
                self.timeout,
                self.authentication_token,
                self.retry_count)

#use case
request=(RequestBuilder("POST","www.nahom.com")
         .set_headers("header `")
         .set_body("Hi my name is nahom")
         .set_query_parameters("what is this")
         .set_auth("jhkjsdfd")
         .set_retry_count(4)
         .set_timeout(4)
         .build())


#######functional Programmin way of answering would be
VALID_METHODS: Set[str] = {"GET", "POST", "PUT", "PATCH", "DELETE"}

def create_request(http_method:HTTP_METHODS,
                   url:str,
                   headers: Optional[Dict[str, str]] = None,
                   query_params:Optional[Dict[str, Any]] = None,
                   body:Optional[Any] = None,
                   timeout:Optional[float] = 30.0,
                   authentication_token: Optional[str] = None,
                   retry_count: int = 0,):
    if not http_method:
        raise ValueError("http method is needed")
    if not url:
        raise ValueError("url is needed")

    if http_method not in VALID_METHODS:
        raise ValueError(f"http methods can only be one of {VALID_METHODS}")
    if http_method=="GET" and body is not None:
        raise ValueError("GET cant have a body")
    if timeout is not None and timeout < 0:
        raise ValueError("Timeout cant be negative")
    if retry_count<0:
        raise ValueError("retry count cant be negative")

    return Request(http_method,url,headers,query_params,body,
                 timeout,authentication_token,retry_count)

#use case 
request=create_request(http_method="GET",url="www.g.com")