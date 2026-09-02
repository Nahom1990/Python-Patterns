"""
You are building a system that imports employee data from external companies.

The incoming data looks conceptually like this:

{
    "name": "Nahom",
    "email": "nahom@example.com",
    "age": 27,
    "country": "Ethiopia"
}

Before the employee can be imported, the data must pass through a processing pipeline.

Requirements

Create a chain with these handlers:

1. Required Fields Handler

Ensure these fields exist:

name
email
age
country

If any are missing:

STOP the chain
2. Data Validation Handler

Validate:

age >= 18

and ensure the email looks valid—for this exercise, simply check that it contains:

@

If invalid:

STOP the chain
3. Normalization Handler

Normalize the data:

name → strip whitespace and title case

email → strip whitespace and lowercase

country → strip whitespace and title case

Example:

"  NAHOM mekuria  "

becomes:

"Nahom Mekuria"
4. Duplicate Check Handler

Assume you have an existing collection of imported emails.

If the employee's email already exists:

STOP the chain

Otherwise, continue.

5. Import Handler

If the request reaches this handler:

Employee successfully imported

Add the employee to your storage.

Your task

Implement it in three versions, like we've been doing:

Version 1 — Classical OOP

Use:

ABC
Abstract Handler
Concrete Handlers
next_handler
Version 2 — Modern Python

Use whichever Pythonic approach you think is best.

You can use:

Protocol
normal classes
composition

But don't use abstraction just because the classical pattern uses it.

Version 3 — Functional

This is important for you because you've been improving your functional thinking.

Think of:

data
 ↓
function
 ↓
function
 ↓
function
 ↓
function

Each function should either:

continue processing

or:

stop the pipeline
"""

from abc import ABC,abstractmethod
class EmployeeDataProcessor(ABC):
    def __init__(self) -> None:
        self.next_handler=None

    def set_next(self,handler):
        self.next_handler=handler
        return handler
        

    @abstractmethod
    def handle(self,employee_data):
        pass

    def next(self,employee_data):
        if self.next_handler:
            return self.next_handler.handle(employee_data)
        return None

class RequiredFieldHandler(EmployeeDataProcessor):
    required_fields={"name","email","age","country"}

    def handle(self, employee_data):
        if not employee_data:
            raise RuntimeError("nothig supplied")
        actual_fields=set(employee_data.keys())
        missing_fields=self.required_fields-actual_fields

        if missing_fields:
            raise ValueError(f"incomplete fields {missing_fields}")

        return self.next(employee_data)

class DataValidationHandler(EmployeeDataProcessor):
    def handle(self, employee_data):
        if not employee_data["age"]>=18:
            raise ValueError("age cant be less than 18")
        if "@" not in employee_data["email"]:
            raise ValueError("email not valid")

        return self.next(employee_data)

class NormalizationHandler(EmployeeDataProcessor):
    def handle(self, employee_data):
        employee_data["name"]=employee_data["name"].strip().title()
        employee_data["email"]=employee_data["email"].strip().lower()
        employee_data["country"]=employee_data["country"].strip().title()
        print(employee_data)
        return self.next(employee_data)

class DuplicateCheckHandler(EmployeeDataProcessor):  #just demonstration purposes 
    def __init__(self) -> None:
        super().__init__()
        self.emails:set[str]=set()
    def handle(self, employee_data):
        if employee_data["email"] in self.emails:
            raise RuntimeError("duplicated email")
        self.emails.add(employee_data["email"])
        return self.next(employee_data)

class ImportHandler(EmployeeDataProcessor):
    def __init__(self) -> None:
        super().__init__()
        self.storage:list[dict]=[]

    def handle(self, employee_data):
        self.storage.append(employee_data)
        return self.next(employee_data)

## use cases 
required=RequiredFieldHandler()
validation=DataValidationHandler()
normalization=NormalizationHandler()
duplicate_check=DuplicateCheckHandler()
import_handler=ImportHandler()

required.set_next(validation).set_next(normalization).set_next(duplicate_check).set_next(import_handler)
required.handle(employee_data={
    "name": "nahom mekuria   ",
    "email": "  nahom@example.com",
    "age": 27,
    "country": "ethiopia"
})



#### version 2 functional ###########




def required_handler(employee_data):
    required_fields={"name","email","age","country"}
    if not employee_data:
        raise RuntimeError("nothig supplied")
    actual_fields=set(employee_data.keys())
    missing_fields=required_fields-actual_fields

    if missing_fields:
        raise ValueError(f"incomplete fields {missing_fields}")

    return employee_data

def data_handler(employee_data):
    if not employee_data["age"]>=18:
        raise ValueError("age cant be less than 18")
    if "@" not in employee_data["email"]:
        raise ValueError("email not valid")

    return employee_data

def norm_handler(employee_data):
    employee_data["name"]=employee_data["name"].strip().title()
    employee_data["email"]=employee_data["email"].strip().lower()
    employee_data["country"]=employee_data["country"].strip().title()

    return employee_data


def duplicate_handler(employee_data):
    emails=[]
    if employee_data["email"] in emails:
        raise RuntimeError("duplicated email")
    return employee_data

def import_handlers(employee_data):
    storage=[]
    storage.append(employee_data)
    return employee_data

handlers=[required_handler,data_handler,norm_handler,duplicate_handler,import_handlers]
employee_data={
    "name": "nahom mekuria   ",
    "email": "  nahom@example.com",
    "age": 27,
    "country": "ethiopia"
}

def chain(employee_data):
    for handler in handlers:
        handler(employee_data=employee_data)

    return employee_data

chain(employee_data)