########1 Direct Function Parameter Injection

from typing import Callable

# Dependency type: A function taking two strings and returning None
NotifierFunc = Callable[[str, str], None]

# Concrete dependency functions
def send_email(recipient: str, message: str) -> None:
    print(f"[Email] Sent to {recipient}: {message}")

def send_sms(recipient: str, message: str) -> None:
    print(f"[SMS] Sent to {recipient}: {message}")


# Pure/Decoupled Core Function receiving its dependency via parameter
def process_order(user_id: str, amount: float, notify: NotifierFunc) -> None:
    print(f"Processing order for {user_id} (${amount})...")
    notify(user_id, f"Order of ${amount} confirmed.")


# Usage: Pass functions as values
process_order("user_101", 99.99, notify=send_email)
process_order("user_102", 49.50, notify=send_sms)



#####2 Closure / Partial Application (Currying)
"""If passing notify everywhere gets tedious, use functools.partial or 
closures to create a pre-configured function with dependencies injected upfront."""
from functools import partial
from typing import Callable

# 1. Function factory (Closure) that injects dependencies first
def make_order_processor(notify: Callable[[str, str], None]):
    """Returns a process_order function with 'notify' pre-injected."""
    def process_order(user_id: str, amount: float) -> None:
        print(f"Processing order for {user_id} (${amount})...")
        notify(user_id, f"Order of ${amount} confirmed.")
    return process_order


# --- COMPOSITION ROOT ---

# Bake the dependency in at application setup
process_order_with_email = make_order_processor(send_email)
process_order_with_sms = make_order_processor(send_sms)

# Later in application flow: Call without needing to supply 'notify' repeatedly
process_order_with_email("user_101", 99.99)
process_order_with_sms("user_102", 49.50)


# Alternative using Python's builtin `functools.partial`:
def raw_process_order(notify: NotifierFunc, user_id: str, amount: float) -> None:
    print(f"Processing order for {user_id} (${amount})...")
    notify(user_id, f"Order of ${amount} confirmed.")

# Injected upfront via partial:
configured_process_order = partial(raw_process_order, send_email)
configured_process_order("user_200", 150.00)



