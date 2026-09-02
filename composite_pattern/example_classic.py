#defnition Composite lets clients treat individual objects (leaves) and groups of objects (composites) uniformly through the same interface.
from abc import ABC, abstractmethod


class OrganizationComponent(ABC):

    @abstractmethod
    def get_salary(self) -> float:
        pass

class Employee(OrganizationComponent):

    def __init__(self, name: str, salary: float):
        self.name = name
        self.salary = salary

    def get_salary(self) -> float:
        return self.salary

class Department(OrganizationComponent):

    def __init__(self, name: str):
        self.name = name
        self.children:list[OrganizationComponent] = []

    def add(self, component: OrganizationComponent):
        self.children.append(component)

    def remove(self, component: OrganizationComponent):
        self.children.remove(component)

    def get_salary(self) -> float:
        return sum(
            child.get_salary()
            for child in self.children
        )

"""Notice: self.children
                    can contain:
                        Employee
                        Department
            because both implement:OrganizationComponent
            """

employee1 = Employee("Alice", 5000)
employee2 = Employee("Bob", 6000)

backend = Department("Backend")

backend.add(employee1)
backend.add(employee2)

engineering = Department("Engineering")

engineering.add(backend)
engineering.add(
    Employee("Charlie", 7000)
)

"""
Engineering
│
├── Backend
│   ├── Alice
│   └── Bob
│
└── Charlie
"""

#if we do 
engineering.get_salary() #5000 + 6000 + 7000 for alice, bob,charlie , the recurssion happens automatically

"""
Look at:

def get_salary(self):
    return sum(
        child.get_salary()
        for child in self.children
    )

The Department doesn't care whether a child is:

Employee

or:

Department

It simply says:

"Whatever you are, give me your salary."

That's polymorphism + recursion.

And that's why Composite is so powerful.

Without Composite, you might have:
check if its employee or department at each recursion level then use the appropriate salary method for each 

if isinstance(employee, Employee):
    ...
elif isinstance(employee, Department):
    ...

"""