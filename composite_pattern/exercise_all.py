"""
Problem: Permission System

You're building an authorization system for a company.

A user can be given:

Individual permissions

READ_USERS
CREATE_USERS
DELETE_USERS
VIEW_REPORTS
EXPORT_REPORTS

An individual permission should be able to answer:

permission.allows("READ_USERS")

But the company also wants Permission Groups.

For example:

USER_MANAGER
├── READ_USERS
├── CREATE_USERS
└── DELETE_USERS

And:

REPORT_MANAGER
├── VIEW_REPORTS
└── EXPORT_REPORTS

Groups can contain other groups.

For example:

ADMIN
├── USER_MANAGER
│   ├── READ_USERS
│   ├── CREATE_USERS
│   └── DELETE_USERS
│
└── REPORT_MANAGER
    ├── VIEW_REPORTS
    └── EXPORT_REPORTS

So:

Permission
    /       \
Individual   Group
             │
             ├── Permission
             ├── Permission
             └── Group
Requirements

Your system should allow:

admin.allows("READ_USERS")

→ True

admin.allows("EXPORT_REPORTS")

→ True

admin.allows("DELETE_DATABASE")

→ False

And:

report_manager.allows("VIEW_REPORTS")

→ True

The client should not care whether it's asking an individual permission or an entire permission group.

Implement it three ways
Version 1 — Classical

Use:

ABC
abstractmethod
Version 2 — Modern Python

Use:

Protocol

Don't use ABC.

Version 3 — Functional/procedural

No Composite class hierarchy.

You can use:

functions
dicts
lists
sets
recursion
"""

#version 1 classical using ABC

#permission(abc)
from typing import Literal
from abc import ABC,abstractmethod
ACCESS=["READ_USERS","CREATE_USERS",
              "DELETE_USERS","VIEW_REPORTS","EXPORT_REPORTS",]
class Permissions(ABC):
    @abstractmethod
    def allow(self,access:str):
        pass
    @abstractmethod
    def allows(self,access:str)->bool:
        pass
#individual permissions
class IndividualPermission(Permissions):
    def __init__(self,) -> None:

        self.tracker:list[str]=[]
    def allow(self, access: str):
        if access not in ACCESS:
            raise ValueError(f"access can only be one of the following {ACCESS}")
        self.tracker.append(access)

    def allows(self,access:str):
        return access in self.tracker
#group permissions

class Authorizer(Permissions):
    def __init__(self,children:list[Permissions]) -> None:
        self.children=children
    def allow(self,access):
       for child in self.children:
                   child.allow(access)

    def allows(self,access):
        if any([child.allows(access) for child in self.children])==True:
            return True
        else: return False

user1_perm=IndividualPermission()
user1_perm.allow("READ_USERS")
user1_perm.allow("CREATE_USERS")
user1_perm.allow("DELETE_USERS")

user2_perm=IndividualPermission()
user2_perm.allow("VIEW_REPORTS")
user2_perm.allow("EXPORT_REPORTS")

print(user1_perm.allows("READ_USERS"))

admin=Authorizer(children=[user1_perm,user2_perm])
print(admin.allows("READ_USERS"))




###### Version 2  #######   ---pythonic protocol
from typing import Protocol
class Permissions2(Protocol):
    def allow(self,access): ...
    def allows(self,access)->bool: ...

class IndividualPermission2:
    def __init__(self) -> None:
        self.tracker:list[str]=[]

    def allow(self,access:str):
        if access not in ACCESS:
            raise ValueError("incorrect value supplied")
        self.tracker.append(access)

    def allows(self,access:str)->bool:
        return access in self.tracker

class Authorizer2:
    def __init__(self,children:list[Permissions2]) -> None:
        self.children=children

    def allow(self,access):
        for child in self.children:
            child.allow(access) 

    def allows(self,access):
        if any([child.allows(access) for child in self.children])==True:
            return True
        else: return False


### version 3--- functional approach ####
from typing import Any
admins :dict[str,Any]= {"USER_MANAGER": [
                        "READ_USERS",
                        "CREATE_USERS",
                        "DELETE_USERS"],
        "REPORT_MANAGER": [
                        "VIEW_REPORTS",
                        "EXPORT_REPORTS"]
}

#needed recursion pattern