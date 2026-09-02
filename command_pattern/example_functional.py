"""The most pythonic way is function.
A function is already:

an object
storable
passable
executable later

So:"""

from typing import Callable


Command = Callable[[], None]

def execute_commands(commands: list[Command]):

    for command in commands:
        command()

commands = [
    lambda: print("Turn light on"),
    lambda: print("Turn fan on"),
]

commands = [
    lambda: print("Turn light on"),
    lambda: print("Turn fan on"),
]