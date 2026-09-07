"""
Reduce Practice Challenge 1 — Easy/Medium
💰 Transaction Summary

You have:

transactions = [
    {"type": "income", "amount": 5000},
    {"type": "expense", "amount": 1200},
    {"type": "income", "amount": 3000},
    {"type": "expense", "amount": 800},
    {"type": "expense", "amount": 500}
]

Your job is to use only reduce() to produce:

{
    "income": 8000,
    "expense": 2500,
    "balance": 5500
}
Important challenge 🧠

Your initial accumulator should be:

initial = {
    "income": 0,
    "expense": 0,
    "balance": 0
}

Your reducer receives:

def aggregate(accumulator, transaction):

For every transaction:

If it's income:
income increases
balance increases
If it's expense:
expense increases
balance decreases
Rules

✅ Use reduce()
✅ Don't mutate the accumulator
✅ Return a brand new accumulator dictionary every time
✅ No for loop
✅ No filter() or map() for this first challenge

Your mental model should be:
Initial accumulator

{
 income: 0,
 expense: 0,
 balance: 0
}

        │
        ▼

Transaction #1

{
 type: income,
 amount: 5000
}

        │
        ▼

New accumulator

{
 income: 5000,
 expense: 0,
 balance: 5000
}

        │
        ▼

Transaction #2

{
 type: expense,
 amount: 1200
}

        │
        ▼

New accumulator

{
 income: 5000,
 expense: 1200,
 balance: 3800
}"""


transactions = [
    {"type": "income", "amount": 5000},
    {"type": "expense", "amount": 1200},
    {"type": "income", "amount": 3000},
    {"type": "expense", "amount": 800},
    {"type": "expense", "amount": 500}
]



def aggregator(accumulator,transaction):
    income_amount = transaction["amount"] if transaction["type"] == "income" else 0
    expense_amount = transaction["amount"] if transaction["type"] == "expense" else 0

    return {**accumulator,"income":accumulator["income"]+income_amount,
            "expense":accumulator["expense"]+expense_amount,
            "balance":accumulator["balance"]+income_amount-expense_amount}

initial = {
    "income": 0,
    "expense": 0,
    "balance": 0
}
from functools import reduce

item=reduce(aggregator,transactions,initial)
print(item)