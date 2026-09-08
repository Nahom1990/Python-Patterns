"""
You have sales:

sales = [
    {
        "product": " Laptop ",
        "category": "Electronics",
        "status": "completed",
        "amount": 1000
    },
    {
        "product": " Mouse ",
        "category": "Electronics",
        "status": "completed",
        "amount": 50
    },
    {
        "product": " Chair ",
        "category": "Furniture",
        "status": "pending",
        "amount": 200
    },
    {
        "product": " Desk ",
        "category": "Furniture",
        "status": "completed",
        "amount": 500
    },
    {
        "product": " Keyboard ",
        "category": "Electronics",
        "status": "completed",
        "amount": 100
    },
    {
        "product": " Sofa ",
        "category": "Furniture",
        "status": "completed",
        "amount": 800
    }
]
Your required pipeline
sales
  ↓
filter(is_completed)
  ↓
map(normalize_sale)
  ↓
reduce(build_summary)
  ↓
FINAL SUMMARY
Step 1 — Predicate

Create:

is_completed(sale)

Keep only:

status == "completed"
Step 2 — Transformation

Create:

normalize_sale(sale)

It should:

Normalize product
" Laptop "
     ↓
"laptop"
Normalize category
"Electronics"
     ↓
"electronics"

Use immutable updates.

Step 3 — The difficult part 🔥

Reduce everything into:

{
    "total_sales": 2450,
    "total_orders": 5,
    "categories": {
        "electronics": {
            "orders": 3,
            "sales": 1150
        },
        "furniture": {
            "orders": 2,
            "sales": 1300
        }
    }
}

Your initial accumulator:

initial = {
    "total_sales": 0,
    "total_orders": 0,
    "categories": {}
}"""
sales = [
    {
        "product": " Laptop ",
        "category": "Electronics",
        "status": "completed",
        "amount": 1000
    },
    {
        "product": " Mouse ",
        "category": "Electronics",
        "status": "completed",
        "amount": 50
    },
    {
        "product": " Chair ",
        "category": "Furniture",
        "status": "pending",
        "amount": 200
    },
    {
        "product": " Desk ",
        "category": "Furniture",
        "status": "completed",
        "amount": 500
    },
    {
        "product": " Keyboard ",
        "category": "Electronics",
        "status": "completed",
        "amount": 100
    },
    {
        "product": " Sofa ",
        "category": "Furniture",
        "status": "completed",
        "amount": 800
    }
]

def  aggregator(accumulator,sale):
    current_category=sale["category"]
    current_sale=sale["amount"]
    category_defaults = {"orders": 0, "sales": 0}

    return {**accumulator,
            "total_sales":accumulator["total_sales"]+current_sale,
            "total_orders":accumulator["total_orders"]+1,
            "categories":
                        {**accumulator["categories"],
                          current_category:
                                            {
                                            "orders":accumulator["categories"].get(current_category,category_defaults)["orders"]+1,
                                            "sales":accumulator["categories"].get(current_category,category_defaults)["sales"]+current_sale}}}

initial_acc={"total_sales":0,
             "total_orders":0,
             "categories":{}}

def is_completed(sale):
    return sale["status"]=="completed"

def normalize_sale(sale):
    return {**sale,"product":sale["product"].lower(),
            "category":sale["category"].lower(),
            }

from functools import reduce
def processor():
    completed=filter(is_completed,sales)
    normalized=map(normalize_sale,completed)
    final=reduce(aggregator,normalized,initial_acc)
    return final

print(processor())