"""Challenge 1 — Immutable Data Transformation Pipeline

You are building a customer-processing engine.

customers = [
    {"name": "  nahom mekuria  ", "age": 27, "country": "Ethiopia"},
    {"name": " abebe kebede ", "age": 16, "country": "Ethiopia"},
    {"name": "  john smith", "age": 31, "country": "USA"},
]

Build these pure transformation functions:

clean_names(customers)
mark_adults(customers)
add_country_code(customers)
Requirements

clean_names should:

"  nahom mekuria  "
        ↓
"nahom mekuria"

mark_adults should add:

"is_adult": True

or:

"is_adult": False

add_country_code should add:

"country_code": "ET"

for Ethiopia and:

"country_code": "US"

for USA.

Then implement:

pipe(*functions)

so that this works:

pipeline = pipe(
    clean_names,
    mark_adults,
    add_country_code
)

result = pipeline(customers)
Important constraints
Do not mutate customers.
Do not mutate the dictionaries inside customers.
Every transformation must return new data.
pipe() must return a function.
pipe() must work with any number of transformations.
Do not hardcode the transformations inside pipe.
No global mutable state.
Bonus

Implement:

compose(*functions)

and demonstrate that you understand the difference between:

pipe(...)

and:

compose(...)
Challenge 2 — Functional Government Application Engine

Now let's make it closer to your government-assistant architecture.

You receive this application:

application = {
    "user": {
        "name": " Nahom Mekuria ",
        "age": 27
    },
    "service": "VAT Registration",
    "slots": {
        "tin": "ET-123456",
        "business_name": None,
        "address": "Addis Ababa"
    },
    "documents": {
        "national_id": True,
        "business_license": False
    },
    "status": "pending"
}

Build a pure functional application-processing engine.

Part 1 — Validation functions

Create independent functions:

is_adult(application)
has_tin(application)
has_business_name(application)
has_address(application)
has_national_id(application)
has_business_license(application)

Each should return a boolean.

Part 2 — Higher-order validation

Create:

validate(application, rule)

It should accept a validation function.

For example:

validate(application, is_adult)

Then create:

rules = [
    is_adult,
    has_tin,
    has_business_name,
    has_address,
    has_national_id,
    has_business_license
]

Build a function that determines which requirements failed.

Part 3 — Immutable state updates

Create:

update_slot(application, slot_name, value)
update_status(application, status)

These must return new application objects.

This must be true:

updated = update_slot(
    application,
    "business_name",
    "Nahom Trading"
)

while:

application["slots"]["business_name"]

must remain:

None
Part 4 — Closure

Create a function:

create_slot_validator(slot_name)

It should return a validation function.

For example:

has_tin = create_slot_validator("tin")
has_business_name = create_slot_validator("business_name")
has_address = create_slot_validator("address")

Now you've created specialized validators from a generic function.

This is deliberately testing whether you understand closures rather than just copying the earlier examples.

Part 5 — Compose the processing

Create a functional pipeline that conceptually does:

Application
      ↓
clean user name
      ↓
add/modify state
      ↓
validate requirements
      ↓
determine status
      ↓
new Application

The business logic should be pure.

You may have a tiny imperative shell such as:

def process_application(application):
    result = ...
    print(result)

But the actual transformations and decisions should not depend on print, databases, network calls, etc.

Challenge 3 — Mini Functional Order Engine

This is the hardest one.

Build a small order-processing engine.

Input:

order = {
    "customer": " Nahom ",
    "items": [
        {"name": "Laptop", "price": 1000, "quantity": 1},
        {"name": "Mouse", "price": 50, "quantity": 2},
    ],
    "country": "Ethiopia"
}

Your engine should eventually produce something conceptually like:

{
    "customer": "Nahom",
    "items": [...],
    "subtotal": 1100,
    "discount": 110,
    "tax": 148.5,
    "total": 1138.5
}

Use a 10% discount and 15% tax.

Part 1 — Pure transformations

Create:

clean_customer_name(order)
calculate_subtotal(order)
calculate_discount(order)
calculate_tax(order)
calculate_total(order)

Each function must return a new order, not mutate the existing one.

Part 2 — Higher-order pricing rules

Create a generic function:

apply_pricing_rule(order, rule)

Then create rules such as:

def ten_percent_discount(order):
    ...

and:

def fifteen_percent_tax(order):
    ...

The important part is that apply_pricing_rule should not know which pricing rule it is executing.

Part 3 — Function registry

Instead of:

if rule_name == "discount":
    ...
elif rule_name == "tax":
    ...

create a dictionary containing behaviors:

pricing_rules = {
    ...
}

Then dynamically select and execute a rule.

This tests your understanding of first-class functions + higher-order functions.

Part 4 — Closures

Create:

create_discount_rule(rate)

It should return a function.

So you can do:

discount_10 = create_discount_rule(0.10)
discount_20 = create_discount_rule(0.20)
discount_30 = create_discount_rule(0.30)

Now you have three different pricing behaviors generated from one function.

Part 5 — Composition / Pipeline

Create:

process_order = pipe(
    clean_customer_name,
    calculate_subtotal,
    calculate_discount,
    calculate_tax,
    calculate_total
)

Then:

result = process_order(order)

The original order must remain unchanged.

Part 6 — Functional Core / Imperative Shell

Separate:

PURE BUSINESS LOGIC
        ↓
Functional Core
        ↓
Imperative Shell
        ↓
print / database / API / etc.

Your business logic should be usable without any print() calls.

For example:

def process_order(order):
    ...

should simply return data.

Then:

def run():
    order = ...
    result = process_order(order)
    print(result)

is allowed."""


customers = [
    {"name": "  nahom mekuria  ", "age": 27, "country": "Ethiopia"},
    {"name": " abebe kebede ", "age": 16, "country": "Ethiopia"},
    {"name": "  john smith", "age": 31, "country": "USA"},
]

def clean_names(customers):
    new_customers=customers
    for customer in new_customers:
        customer["name"]=" ".join(customer["name"].split())
    return new_customers


def mark_adults(customers):
    new_customers=customers
    for customer in new_customers:
        customer["is_adult"]=customer["age"]>=18
    return new_customers

def add_country_code(customers):
    new_customers=customers
    for customer in new_customers:
        customer["country_code"]="ET" if customer["country"]=="Ethiopia" else "US" 
    return new_customers

functions=[clean_names,mark_adults,add_country_code]

def pipe(*functions):
    def piped(customers):
        for func in functions:
            customers=func(customers)
        return customers
    return piped

result=pipe(*functions)
print(result(customers))

def compose(*functions):
    def composed(customers):
        for func in reversed(functions):
            customers=func(customers)
        return customers
    return composed

result=compose(*reversed(functions))

###### challenge 2
application = {
    "user": {
        "name": " Nahom Mekuria ",
        "age": 27
    },
    "service": "VAT Registration",
    "slots": {
        "tin": "ET-123456",
        "business_name": None,
        "address": "Addis Ababa"
    },
    "documents": {
        "national_id": False,
        "business_license": False
    },
    "status": "pending"
}

def is_adult(application):
    return application["user"]["age"]>=18

def has_tin(application):
    return application["slots"]["tin"] is not None

def has_business_name(application):
    return application["slots"]["business_name"] is not None

def has_national_id(application):
    return application["documents"]["national_id"]


def validate(application,rule):
    return rule(application)

rules=[is_adult,has_tin,has_business_name,has_national_id]

def failed(rules,application):
    missing=[]
    for rule in rules:
        if not validate(application,rule):
            missing.append(rule.__name__)

    return missing

print(failed(rules,application,))

def update_slot(application,slot_name,value):
    return {**application,"slots":{**application["slots"],slot_name:value}}

def update_status(application,status):
    return {**application,"status":status}

updated=update_slot(application,"business_name","Nahom Trading")

def create_slot_validator(slot_name):
    def validator(application):
        return application["slots"][slot_name] is not None
    return validator


has_tin=create_slot_validator("business_name")
has_business_name = create_slot_validator("business_name")



def clean_user_name(application):
    return {**application,}