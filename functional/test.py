order = {
    "customer": " Nahom ",
    "items": [
        {"name": "Laptop", "price": 1000, "quantity": 1},
        {"name": "Mouse", "price": 50, "quantity": 2},
    ],
    "country": "Ethiopia"
}


def calculate_subtotal(order):
    return {**order,"subtotal": sum([item["price"]*item["quantity"] for item in order["items"]])}

def discount(order,discount_rate):
    return {**order,"discount":order["subtotal"]*discount_rate/100}

def tax(order,tax_rate):
    return {**order,"tax":(order["subtotal"]-order["discount"])*tax_rate/100}

def total(order):
    return {**order,"total":order["subtotal"]-order["discount"]+order["tax"]}


print(total(tax(discount(calculate_subtotal(order),10),15)))