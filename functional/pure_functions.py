"""A function is generally considered pure when it has two properties:

Rule 1: Same input → Same output

If you call it with the same arguments:

calculate_tax(100)

it should always produce the same result:

15

For example:

def calculate_tax(amount):
    return amount * 0.15

This is predictable:

calculate_tax(100)  # 15
calculate_tax(100)  # 15
calculate_tax(100)  # 15

Same input:

100

Same output:

15
Rule 2: No Observable Side Effects

The function should not secretly affect the outside world.

For example:

balance = 1000

def withdraw(amount):
    global balance
    balance -= amount

This is not pure.

Why?

Because calling:

withdraw(100)

does more than return a value.

It changes:

balance

outside the function.

The function has a side effect:

Function
    ↓
Changes external state




Side Effects

A side effect happens when a function interacts with something outside its returned value.

Examples include:

Modifying a global variable
counter = 0

def increment():
    global counter
    counter += 1

❌ Side effect.

Modifying a passed mutable object
def add_user(users, user):
    users.append(user)

❌ The function changes an object outside itself.

The caller's list is different after the function runs.

Printing
def calculate_total(price):
    total = price * 1.15
    print(total)
    return total

Strictly speaking, printing is a side effect.

The function interacts with stdout.

Writing to a database
def create_user(user):
    database.save(user)

❌ Side effect.

Sending a Telegram message
def notify_user(user_id, message):
    telegram.send_message(user_id, message)

❌ Side effect.

Reading the current time
from datetime import datetime

def get_discount():
    if datetime.now().hour < 12:
        return 0.20
    return 0.10

Same function call can produce different results depending on external state: time.

Randomness
import random

def generate_discount():
    return random.randint(1, 50)

Same call:

generate_discount()

Different possible outputs.

So this isn't pure.




"""
application = {
    "age": 15,
    "has_valid_id": True,
    "has_required_document": False
}

def is_adult(age):
    return age>=18

def has_valid_identification(has_valid_id):
    return has_valid_id

def has_required_documents(has_required_document):
    return has_required_document

def determine_eligibility(application):
    adult= is_adult(application["age"])
    id= has_valid_identification(application["has_valid_id"])
    doc=has_required_documents(application["has_required_document"])
    if adult and id and doc:
        return True
    return False

def process_application(application):
    eligibility=determine_eligibility(application)
    print(eligibility)


def determine_missing_requirements(application):

    requirement={"adult":is_adult(application["age"]),
    "id":has_valid_identification(application["has_valid_id"]),
    "doc":has_required_documents(application["has_required_document"])}

    return [i for i,j in requirement.items() if not j]

print(determine_missing_requirements(application))
"""




You're going to design a simplified version of something relevant to your government assistant.

Scenario

A citizen applies for a government service.

The citizen data looks like:

application = {
    "age": 20,
    "has_valid_id": True,
    "has_required_document": False
}
Part 1 — Pure Functions

Create pure functions for:

is_adult(age)

Returns whether the person is at least 18.

has_valid_identification(has_valid_id)

Returns whether the ID is valid.

has_required_documents(has_required_document)

Returns whether the required document exists.

Then create:

determine_eligibility(application)

It should use your other functions and return either:

"eligible"

or:

"not eligible"
Important:

Do not modify the original application.

Do not use global variables.

Do not print inside these pure functions.

Part 2 — The Imperative Shell

Create a separate function that represents the outside world.

Something conceptually like:

def process_application(application):

This function can:

Call your pure determine_eligibility().
Print the result.

The point is to clearly separate:

PURE DECISION

determine_eligibility(application)

from:

SIDE EFFECT

print(...)
Bonus Challenge 🔥

Add another pure function:

determine_missing_requirements(application)

It should return a new list describing what's missing.

For example:

[
    "valid identification",
    "required document"
]

Again:

Don't modify the application.
Return new data."""

