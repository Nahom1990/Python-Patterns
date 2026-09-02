"""a behavioral design pattern that turns a request or an action into
 a stand-alone object.
 Instead of executing an operation immediately, you 
 encapsulate all the information needed to perform that action—[the method name,
 the object that owns the method, and any arguments]—into a separate "Command" class.

 By turning actions into objects, you can pass them as arguments to functions, 
 delay their execution, queue them up,store them,retry them or store them in a history stack 
 to implement undo/redo functionality."""

from abc import ABC, abstractmethod

#reciever/ What actually executes
class Light:

    def turn_on(self):
        print("Light turned ON")

    def turn_off(self):
        print("Light turned OFF")

#command abstractbaseclass/interface
class Command(ABC):

    @abstractmethod
    def execute(self): #every command exposes execute()
        pass

#command concrete class1
class TurnOnLightCommand(Command):

    def __init__(self, light):
        self.light = light

    def execute(self):
        self.light.turn_on()

#command concrete class2
class TurnOffLightCommand(Command):

    def __init__(self, light):
        self.light = light

    def execute(self):
        self.light.turn_off()

#invoker/triggers the command
class RemoteControl:

    def __init__(self):
        self.command = None

    def set_command(self, command):
        self.command = command

    def press_button(self):

        if self.command:
            self.command.execute()

"""The RemoteControl doesn't know about:

Light
Fan
Door, just when button pressed executes the command, here the command is not executed ditectly it first is stored
as object in self.command, then when needed/press button we call execute on the stored command.
The power comes from treating actions as objects.
Now the actions can be
    Stored
    Queued
    Scheduled
    Logged
    Retried
    Executed later"""

#usage
light = Light()

command = TurnOnLightCommand(light)

remote = RemoteControl()

remote.set_command(command)

remote.press_button()