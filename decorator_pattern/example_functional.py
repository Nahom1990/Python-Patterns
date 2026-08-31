
def logging_decorator(func):
    def wrapper(*args,**kwargs):
        print("logging notification")
        result=func(*args,**kwargs)
        print("finished logging")
        return result
    return wrapper

#use case
@logging_decorator
def send_notification(message:str)->None:
    print(f"sending {message}")
