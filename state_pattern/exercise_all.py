"""
Build an Order Lifecycle System.

An order can move through:

PENDING
   ↓
PAID
   ↓
SHIPPED
   ↓
DELIVERED

It can also be:

PENDING → CANCELLED
PAID → CANCELLED

but a shipped or delivered order cannot be cancelled.

The order exposes operations such as:

pay()
ship()
deliver()
cancel()

Each operation should behave differently depending on the order's current state.

For example:

PENDING
 ├── pay()      → PAID
 ├── cancel()   → CANCELLED
 ├── ship()     → reject
 └── deliver()  → reject

PAID
 ├── ship()     → SHIPPED
 ├── cancel()   → CANCELLED
 └── deliver()  → reject

SHIPPED
 ├── deliver()  → DELIVERED
 └── cancel()   → reject
Implement three versions

Version 1 — Classical OOP

ABC
State interface
Concrete state classes
Context

Version 2 — Modern Python

Protocol
No inheritance for concrete states

Version 3 — Pythonic/functional

Functions and/or Enum
Avoid unnecessary classes
"""

###version 1

from abc import ABC,abstractmethod

class States()