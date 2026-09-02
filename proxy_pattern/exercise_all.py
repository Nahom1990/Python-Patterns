"""
Existing system

You have a real service conceptually like:

DocumentRepository

It loads documents:

- load_document(document_id)

Loading a document is considered expensive.

You need to introduce a layer between the client and the real repository.

Requirements

Your system should have a client-facing document interface with operations conceptually like:

get_document(document_id)

Your Proxy should sit in front of the real document service.

Client
   ↓
DocumentProxy
   ↓
DocumentRepository



Required behavior

The Proxy must coordinate these rules:

1. Authorization

Before accessing a document, determine whether the user is allowed to access it.

Unauthorized users should never reach the real repository.

2. Caching

If an authorized user requests a document that has already been loaded:

Proxy
   ↓
Cache hit?
   │
   ├── YES → Return cached document
   │
   └── NO → Call real repository

3. Lazy access

The expensive repository should only be called when necessary.
The client shouldn't need to know anything about:

authorization
caching
repository access

The client should simply call:

document_service.get_document(document_id)
Your task

Implement the project in the three styles you've been practicing:

Version 1 — Classical OOP

You may use:

ABC
Abstract interface
Real Subject
Proxy
Client



Version 2 — Modern Python

Use:

Protocol
Composition
Dependency injection

No unnecessary inheritance.

Version 3 — Functional / Procedural

Try to think of how the same architectural idea works with functions.

Hint: You don't need to force classes into the functional version.

Think in terms of:

function
   ↓
authorization check
   ↓
cache check
   ↓
real function

The client should still have one clean entry point."""
######version 1####
from abc import ABC,abstractmethod

class DocumentRepository(ABC):
    @abstractmethod
    def load_document(self,document_id)->str|None:
        pass

class ConcreteDocRepo(DocumentRepository):
   def __init__(self) -> None:
       self.docs={1:"animal_doc",2:"plant_doc",3:"physics_doc"}
   def load_document(self,document_id)->str|None:
        return self.docs[document_id]

class DocRepoProxy(DocumentRepository):
    def __init__(self,doc_repo:DocumentRepository,is_admin) -> None:
        self.doc_repo=doc_repo
        self.is_admin=is_admin
        self._cache:dict[Any,Any]={}

    def load_document(self,document_id)->str|None:
         if not self.is_admin:
            raise PermissionError("only admin can load a document")
         if document_id in self._cache:
            print("cache hit")
            return self._cache[document_id]

         result=self.doc_repo.load_document(document_id)
         print("cache miss")
         self._cache[document_id]=result
        
         return result


#####  version 2 ####
from typing import Protocol,Any

class DocumentRepositoryProtocol(Protocol):
   def load_document(self,document_id)->str|None: ...

class DocumentRepo:
   def __init__(self) -> None:
       self.docs={1:"animal_doc",2:"plant_doc",3:"physics_doc"}
   def load_document(self,document_id)->str|None:
        return self.docs[document_id]
   
class DocumentRepoProxy:
    def __init__(self,doc_repo:DocumentRepositoryProtocol,is_admin) -> None:
        self.doc_repo=doc_repo
        self.is_admin=is_admin
        self._cache:dict[Any,Any]={}
    def load_document(self,document_id)->str|None:
         if not self.is_admin:
            raise PermissionError("only admin can load a document")
         if document_id in self._cache:
            print("cache hit")
            return self._cache[document_id]

         result=self.doc_repo.load_document(document_id)
         print("cache miss")
         self._cache[document_id]=result
        
         return result

documents=DocumentRepoProxy(doc_repo=DocumentRepo(),is_admin=True)
print(documents.load_document(2))

###version 3 functional
docs={1:"animal_doc",2:"plant_doc",3:"physics_doc"}
def load_document(document_id):
    return docs[document_id]

cache:dict[int|str,int|str]={}
def load_document_proxy(document_id,is_admin):
    if not is_admin:
      raise PermissionError("only admin can load a document")
    if document_id in cache:
      print("cache hit")
      return  cache[document_id]

    result=load_document(document_id)
    print("cache miss")
    cache[document_id]=result

    return result