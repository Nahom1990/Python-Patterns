"""
Imagine you're building a payment processing system.

You have three payment functions:

Credit Card
Bank Transfer
Mobile Payment

"""
def credit_card_pay(amount):
    return f"charged {amount} using a credit card"

def bank_transfer_pay(amount):
    return f"charged {amount} using bank transfer"

def mobile_bank_pay(amount):
    return f"charged {amount} using mobile payment"

paymeny_methods={'credit_card':credit_card_pay,
 'bank_transfer':bank_transfer_pay,
 "mobile_bank":mobile_bank_pay}


def pay(amount,method):
    if method in paymeny_methods:
        return paymeny_methods[method](amount)
    return "chosen payment method not found"

pay(5,"credit_card")
"""

Your Task

Create three separate functions that process a payment.

For simplicity, each function should:

Receive an amount
Return a descriptive string showing the payment method and amount

For example:

Credit Card payment processed: 500

Then create a dictionary that maps:

"credit_card"

to the function itself.

Likewise:

"bank_transfer"

and:

"mobile_payment"

Then create a function conceptually responsible for:

Receiving a payment method and amount, finding the correct payment function dynamically, and executing it.

Your system should work conceptually like:

User Input

"mobile_payment"
      +
500

       ↓

Payment Dictionary

       ↓

mobile_payment function

       ↓

"Mobile payment processed: 500"
Important Constraints
Do NOT:

Use:

if / elif

to select the payment method.

DO:

Use the dictionary to select the correct function.

Remember:

This:

"credit_card": process_credit_card

stores the function.

While:

"credit_card": process_credit_card()

would call the function immediately."""