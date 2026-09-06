"""
Aliasing — The Hidden Mutation Problem

Consider:

users = ["Nahom", "Abel"]

backup_users = users

backup_users.append("Sara")

What does this produce?

Many beginners expect:

users:
["Nahom", "Abel"]

backup_users:
["Nahom", "Abel", "Sara"]

But actually:

users:
["Nahom", "Abel", "Sara"]

backup_users:
["Nahom", "Abel", "Sara"]

Why?

Because:

users ────────────────┐
                      ↓
                 LIST OBJECT
                      ↑
backup_users ─────────┘

Mutation happens to the object, not to the variable name.

This is called aliasing.



Suppose your workflow state looks like:

state = {
    "user_id": 123,
    "service": "VAT registration",
    "slots": {
        "tin": None,
        "business_name": "Nahom Trading"
    }
}

You receive the TIN:

TIN = "ET-123456"

An imperative approach might mutate:

state["slots"]["tin"] = "ET-123456"

Now any code holding a reference to state sees the changed version.

A functional approach:

new_state = {
    **state,
    "slots": {
        **state["slots"],
        "tin": "ET-123456"
    }
}


This is another area where immutability becomes powerful.

Imagine two threads sharing:

users = []

Thread A:

users.append("Nahom")

Thread B:

users.append("Abel")

Shared mutable state creates potential synchronization problems.

You may need:

Locks
Synchronization
Coordination

But immutable data can reduce many of these problems.

If data isn't changing:

Thread A ──► reads data

Thread B ──► reads same data

Thread C ──► reads same data

Reading immutable data concurrently is generally much easier to reason about than coordinating mutations."""




"""
You have:

state = {
    "user_id": 123,
    "service": "VAT Registration",
    "status": "pending",
    "slots": {
        "tin": None,
        "business_name": None,
        "address": None
    }
}
Part 1

Create a function:

update_slot(state, slot_name, value)

It must:

Not mutate state.
Return a new state dictionary.
Update only the requested slot.

Example:

new_state = update_slot(
    state,
    "tin",
    "ET-123456"
)

Afterward:

state["slots"]["tin"]

must still be:

None

while:

new_state["slots"]["tin"]

must be:

"ET-123456"
Part 2

Create:

update_status(state, status)

Again:

Don't mutate the original.
Return a new state.
Part 3 — The Interesting Part 🔥

Create:

apply_updates(state, updates)

Where:

updates = [
    ("slot", "tin", "ET-123456"),
    ("slot", "business_name", "Nahom Trading"),
    ("status", "documents_required")
]

Your function should apply these sequentially and produce a final new state.

Conceptually:

Original State
      ↓
Update TIN
      ↓
State Version 2
      ↓
Update Business Name
      ↓
State Version 3
      ↓
Update Status
      ↓
Final State
Important constraint

Do not mutate the original state anywhere.

You should use the functions you created:

update_slot()
update_status()

inside:

apply_updates()"""

state = {
    "user_id": 123,
    "service": "VAT Registration",
    "status": "pending",
    "slots": {
        "tin": None,
        "business_name": None,
        "address": None
    }
}

def update_slot(state,slot_name,value):
    return {**state,
            "slots":{**state["slots"],
                    slot_name:value}}

def update_status(state,status):
    return {**state,
            "status":status}



def apply_updates(state,updates):
    new_state=state
    for update in updates:
        if update[0]=="slots":
            new_state=update_slot(new_state,update[1],update[2])
        elif update[0]=="status":
            new_state=update_status(new_state,update[1])

    return new_state
updates = [
    ("slots", "tin", "ET-123456"),
    ("slots", "business_name", "Nahom Trading"),
    ("status", "documents_required")
]
print(apply_updates(state,updates))
print(state)
        
