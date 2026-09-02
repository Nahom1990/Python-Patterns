"""Dimension A — Messages
AlertMessage
ReminderMessage

Dimension B — Senders
EmailSender
SMSSender

Requirements:

A Message should receive a Sender.
AlertMessage and ReminderMessage should be able to work with either sender.
Do it using Protocol.
No unnecessary ABC inheritance."""

from typing import Protocol
class Sender(Protocol):
    def send(self,message): ...

class EmailSender:
    def send(self,message):
        print(f"Sending EMAIL: {message}")

class SmsSender:
    def send(self,message):
        print(f"Sending SMS: {message}")

class Message:
    def __init__(self,sender:Sender) -> None:
        self.sender=sender


class AlertMessage(Message):
    def message(self):
        self.sender.send(message="this is an alert message")
    
class ReminderMessage(Message):
    def message(self):
        self.sender.send(message="this is an reminder message")
    