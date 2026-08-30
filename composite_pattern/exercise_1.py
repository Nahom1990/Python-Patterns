"""Write a Protocol-based Composite for:

Task
Project

Requirements:

A Task has a duration.
A Project can contain Tasks and other Projects.
Both must expose:
get_duration() -> int
Project.get_duration() should recursively calculate the total duration.
Use Protocol.
Don't use ABC"""
from typing import Protocol
class TaskProject(Protocol):
    def get_duration(self)->float: ...
class Task:
    def __init__(self,name,duration) -> None:
        self.name=name
        self.duration=duration
    def get_duration(self):
        return self.duration
class Project:
    def __init__(self,name,child:list[TaskProject]) -> None:
        self.name=name
        self.child=child

    def add_task(self,taskproject):
        self.child.append(taskproject)

    def get_duration(self):
        return sum(child.get_duration() for child in self.child) #recursive 
