"""Now anything with:

execute()

can behave as a command."""
from typing import Protocol

class Light:

    def turn_on(self):
        print("Light turned ON")

    def turn_off(self):
        print("Light turned OFF")


class Command(Protocol):

    def execute(self) -> None:
        ...

class TurnOnLightCommand:

    def __init__(self, light):
        self.light = light

    def execute(self):
        self.light.turn_on()

class RemoteControl:

    def __init__(self):
        self.command = None

    def set_command(self, command):
        self.command = command

    def press_button(self):

        if self.command:
            self.command.execute()

light = Light()

command = TurnOnLightCommand(light)

remote = RemoteControl()

remote.set_command(command)

remote.press_button()