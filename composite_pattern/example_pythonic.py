from typing import Protocol

"""
With Protocol, a class doesn't have to explicitly announce:

"I am an OrganizationComponent."

It just needs to provide:

get_salary()
"""
class OrganizationComponent(Protocol):

    def get_salary(self) -> float:
        ...

class Employee:

    def __init__(self, name: str, salary: float):
        self.name = name
        self.salary = salary

    def get_salary(self) -> float:
        return self.salary

class Department:

    def __init__(self, name: str):
        self.name = name
        self.children: list[OrganizationComponent] = []

    def add(self, component: OrganizationComponent):
        self.children.append(component)

    def remove(self, component: OrganizationComponent):
        self.children.remove(component)

    def get_salary(self) -> float:
        return sum(
            child.get_salary()
            for child in self.children
        )

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