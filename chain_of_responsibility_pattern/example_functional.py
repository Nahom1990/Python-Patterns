from typing import Callable


Handler = Callable[[dict], dict]

def authentication(request):

    if not request.get("token"):
        raise PermissionError("Authentication required")

    print("Authentication passed")

    return request

def authorization(request):

    if request.get("user") != "admin":
        raise PermissionError("Not authorized")

    print("Authorization passed")

    return request

def rate_limit(request):

    print("Rate limit passed")

    return request


#pipeline 
handlers = [
    authentication,
    authorization,
    rate_limit,
]

def process_request(request, handlers):

    for handler in handlers:
        request = handler(request)

    return request



#use
request={"user":"admin","token":"qwerty"}
process_request(
    request,
    handlers,
)