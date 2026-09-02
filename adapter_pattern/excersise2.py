#####  classic   ######
from abc import ABC,abstractmethod
class Storage(ABC):
    @abstractmethod
    def save(self,data):pass
    @abstractmethod
    def load(self,key):pass

class RedisGateway:
    def __init__(self) -> None:
        self.data={}
    def set(self,key,value):
        self.data[key]=value
    def get(self,key):
        return self.data[key]

class Redisadapter(Storage):
    def __init__(self,redis_gateway) -> None:
        self.redis_gateway=redis_gateway

    def save(self,data):
        for key,value in data.items():
            self.redis_gateway.set(key,value)

    def load(self,key):
        return self.redis_gateway.get(key)

#usecase 
redis=RedisGateway()
host=Redisadapter(redis)
host.save({"cat":"dog"})
host.load("cat")

######### Pythonic ##############
from typing import Protocol

class Storage2(Protocol):
    def save(self,data)->None:
        ...

    def load(self,key)->None:
        ...


class RedisGateway2:
    def __init__(self) -> None:
        self.data={}
    def set(self,key,value):
        self.data[key]=value
    def get(self,key):
        return self.data[key]

class Redisadapter2:
    def __init__(self,redis_gateway) -> None:
        self.redis_gateway=redis_gateway

    def save(self,data):
        for key,value in data.items():
           return self.redis_gateway.set(key,value)

    def load(self,key):
        return self.redis_gateway.get(key)

class checkout:
    def __init__(self,event_processor:Storage2) -> None:
        self.event_processor=event_processor

    def save_processor(self,data):
        self.event_processor.save(data)

    def load_processor(self,key):
        self.event_processor.load(key)



redis=RedisGateway()
adapter=Redisadapter2 (redis)
chechout=checkout(adapter)
chechout.save_processor(data={"cat":"dog"})
chechout.load_processor("cat")
