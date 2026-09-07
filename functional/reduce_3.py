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