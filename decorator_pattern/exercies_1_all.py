"""
Create a DataStore system.

The client expects:

store.save(key, value)
store.load(key)

Create:

Base implementation

MemoryStore

Then create two decorators:

LoggingStore

and:

CachingStore

You should be able to compose them:

store = LoggingStore(
    CachingStore(
        MemoryStore()
    )
)

The client should still only use:

store.save(...)
store.load(...)"""

##version 1
from abc import ABC,abstractmethod
from typing import Any, Protocol
class DataStoreSystem(ABC):
    @abstractmethod
    def save(self,key,value): pass

    @abstractmethod
    def load(self,key):pass

class MemoryStore(DataStoreSystem):
    def __init__(self) -> None:
        self._store:dict[str,Any]={}

    def save(self,key,value):
        self._store[key]=value

    def load(self,key):
        return self._store[key]

class BaseDecorator(DataStoreSystem):
    def __init__(self,data_store:DataStoreSystem) -> None:
        self.data_store=data_store

class LoggingDataStore(BaseDecorator):
    def save(self,key,value):
        print(f"saving key={key}, value={value}")
        return self.data_store.save(key,value)

    def load(self,key):
        print(f"loading key={key}")
        return self.data_store.load(key)

class CachingDataStore(BaseDecorator):
    def __init__(self, data_store: DataStoreSystem) -> None:
        super().__init__(data_store)
        self._cache:dict[str,Any]={}
    def save(self,key,value):
        self._cache[key] = value
        return self.data_store.save(key,value)

    def load(self,key):
        if key in self._cache:
            return self._cache[key]
        return self.data_store.load(key)

store=LoggingDataStore(CachingDataStore(MemoryStore()))
store.save("user_1","Nahom")
store.load("user_1")

####  version 2 pythonic way ####

class DataStore2(Protocol):
    def save(self, key,value):
        ...
    def load(self,key):
        ...

class MemoryStore2:
    def __init__(self) -> None:
        self._store:dict[str,Any]={}
    def save(self,key,value):
        self._store[key]=value

    def load(self,key):
        return self._store[key]

class LoggingDataStore2:
    def __init__(self,datastore:DataStore2) -> None:
        self.datastore=datastore

    def save(self,key, value):
        print(f"logging {key} and {value}")
        self.datastore.save(key,value)

    def load(self,key):
        print(f"loggin load {key}")
        return self.datastore.load(key)


class CachingDataStore2:
    def __init__(self,datastore:DataStore2) -> None:
        self.datastore=datastore
        self._cache:dict[str,Any]={}

    def save(self,key, value):
        self._cache[key]=value
        self.datastore.save(key,value)
        
    def load(self,key):
        if key in self._cache:
            return self._cache[key]
        return self.datastore.load(key)

########## version 3
from functools import wraps

store3={}
cache3={}

def loggingdecorator(func):
    @wraps(func)
    def wrapper(*args,**kwargs):
        print(f"logging started ")
        result=func(*args,**kwargs)
        print("finished logging")
        return result
    return wrapper

def cache_save_decorator(func):
    @wraps(func)
    def wrapper(key,value):
        print(f"caching {key} to cache3")
        cache3[key]=value
        return func(key,value)
    return wrapper

def cache_load_decorator(func):
    @wraps(func)
    def wrapper(key):
        if key in cache3:
            return cache3[key]
        return func(key)
    return wrapper

@loggingdecorator
@cache_save_decorator
def save(key,value):
    store3[key]=value

@loggingdecorator
@cache_load_decorator
def load(key):
    return store3[key]

