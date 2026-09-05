"""You have this order data:

order = {
    "customer": "Nahom",
    "items": [
        {"name": "Laptop", "price": 1000, "quantity": 1},
        {"name": "Mouse", "price": 50, "quantity": 2},
    ]
}

Your program should conceptually perform this pipeline:

Order
  ↓
Calculate item totals
  ↓
Calculate order subtotal
  ↓
Apply discount
  ↓
Apply tax
  ↓
Final result
Requirements
"""
"""
Create separate functions for the transformations.

Your functions should conceptually handle:

Calculating the total price of each item.
Calculating the subtotal of the entire order.
Applying a discount.
Applying a tax.
Producing the final total.
Important Constraints

Try to design the calculation functions so that they:

Take data as arguments.
Return results.
Do not depend on global variables.
Do not print internally.
Do not modify the original order.

The program should have a clear flow that looks conceptually like:

Input
 ↓
Transformation
 ↓
Transformation
 ↓
Transformation
 ↓
Result
Your Discount and Tax Rules

Use:

10% discount
15% tax after the discount

So:

Subtotal
↓
10% discount
↓
Discounted subtotal
↓
15% tax
↓
Final total"""




order = {
    "customer": "Nahom",
    "items": [
        {"name": "Laptop", "price": 1000, "quantity": 1},
        {"name": "Mouse", "price": 50, "quantity": 2},
    ]}

def calculate_item_totals(order):
    for item in order["items"]:
        item["total"]=item["price"]*item["quantity"]

    return order

def calculate_order_subtotal(order):
    return sum(item["total"] for item in order["items"])

def apply_discount(item_total,discount_percent):
    return item_total-(discount_percent*item_total)/100

def apply_tax(total_amount,tax_percent):
    return total_amount + (total_amount*tax_percent)/1000


def main(order):
    order=calculate_item_totals(order)
    subtotal=calculate_order_subtotal(order)
    after_discount=apply_discount(subtotal,15)
    after_tax=apply_tax(after_discount,12)

    return after_tax



###comment the order is being mutated in place which is not good, use copy , from copy import deepcopy, 
#the copy the original dict and do the transformation on it.