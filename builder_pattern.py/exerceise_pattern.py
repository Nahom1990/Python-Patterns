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

