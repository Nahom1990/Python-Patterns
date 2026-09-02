from typing import Protocol

#Protocol just removes unnecessary inheritance from the implementation side. and typehinters
class Device(Protocol):

    def enable(self) -> None:
        ...

    def disable(self) -> None:
        ...

    def is_enabled(self) -> bool:
        ...

    def get_volume(self) -> int:
        ...

    def set_volume(self, volume: int) -> None:
        ...

class TV:

    def __init__(self):
        self.enabled = False
        self.volume = 30

    def enable(self):
        self.enabled = True

    def disable(self):
        self.enabled = False

    def is_enabled(self):
        return self.enabled

    def get_volume(self):
        return self.volume

    def set_volume(self, volume):
        self.volume = volume

class Remote:

    def __init__(self, device: Device):
        self.device = device

    def toggle_power(self):

        if self.device.is_enabled():
            self.device.disable()
        else:
            self.device.enable()

class AdvancedRemote(Remote):

    def mute(self):
        self.device.set_volume(0)