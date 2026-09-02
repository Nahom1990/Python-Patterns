from abc import ABC, abstractmethod


class Device(ABC):

    @abstractmethod
    def enable(self) -> None:
        pass

    @abstractmethod
    def disable(self) -> None:
        pass

    @abstractmethod
    def is_enabled(self) -> bool:
        pass

    @abstractmethod
    def get_volume(self) -> int:
        pass

    @abstractmethod
    def set_volume(self, volume: int) -> None:
        pass

class TV(Device):

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

class Radio(Device):

    def __init__(self):
        self.enabled = False
        self.volume = 50

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

class BasicRemote:

    def __init__(self, device: Device):
        self.device = device #the bridge/composition

    def toggle_power(self):

        if self.device.is_enabled():
            self.device.disable()
        else:
            self.device.enable()

    def volume_down(self):
        volume = self.device.get_volume()
        self.device.set_volume(volume - 10)

    def volume_up(self):
        volume = self.device.get_volume()
        self.device.set_volume(volume + 10)

#wee can add new abstractions like this
class AdvancedRemote(BasicRemote):

    def mute(self):
        self.device.set_volume(0)

# we can do 
BasicRemote(TV())
AdvancedRemote(TV())
BasicRemote(Radio())
AdvancedRemote(Radio())

"""
 ABSTRACTION

                  Remote
                    │
           ┌────────┴────────┐
           │                 │
       BasicRemote      AdvancedRemote
           │                 │
           └────────┬────────┘
                    │
                    │ has-a
                    ▼
             IMPLEMENTATION

                  Device
               ┌────┴────┐
               │         │
              TV       Radio"""