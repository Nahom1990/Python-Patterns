"""
reduce() doesn't have to produce a number 🔥

This is where things get more interesting.

The accumulator can be:

Integer
Float
String
List
Dictionary
Set"""

from functools import reduce

"""Now we're going to combine everything:

filter()
map()
reduce()
pure functions
immutable updates
lazy pipelines

You have:

applications = [
    {
        "service": "VAT Registration",
        "status": "approved",
        "fee": 500
    },
    {
        "service": "Business License",
        "status": "pending",
        "fee": 300
    },
    {
        "service": "VAT Registration",
        "status": "approved",
        "fee": 500
    },
    {
        "service": "Trade License",
        "status": "approved",
        "fee": 200
    },
    {
        "service": "Business License",
        "status": "approved",
        "fee": 300
    }
]
Your task

Build a pipeline that does this:

Step 1 — Filter approved applications

Create:

is_approved(application)
Step 2 — Normalize the service name

Transform:

"VAT Registration"
        ↓
"vat_registration"

Create:

normalize_service(application)
Step 3 — Reduce the applications into a summary dictionary

The final result should look like:

{
    "total_approved": 4,
    "total_fees": 1500,
    "services": {
        "vat_registration": 2,
        "trade_license": 1,
        "business_license": 1
    }
}
Important challenge 🔥

Your accumulator starts as:

{
    "total_approved": 0,
    "total_fees": 0,
    "services": {}
}

For every application, return a new accumulator dictionary.

Do not mutate:

accumulator["total_approved"] += 1

Instead, think about how you've already done immutable nested updates:

{
    **state,
    "nested": {
        **state["nested"],
        ...
    }
}

You should apply the same concept here.

Your architecture should be:
applications
      ↓
filter(is_approved)
      ↓
map(normalize_service)
      ↓
reduce(build_summary)
      ↓
FINAL SUMMARY"""

def is_approved(application):
    return application["status"]=="approved"

def normalize_service_name(application):
    return {**application,"service":"_".join(application["service"].split()).lower()}


applications = [
    {
        "service": "VAT Registration",
        "status": "approved",
        "fee": 500
    },
    {
        "service": "Business License",
        "status": "pending",
        "fee": 300
    },
    {
        "service": "VAT Registration",
        "status": "approved",
        "fee": 500
    },
    {
        "service": "Trade License",
        "status": "approved",
        "fee": 200
    },
    {
        "service": "Business License",
        "status": "approved",
        "fee": 300
    }
]

def aggregating(accumulator,application):
    service=application["service"]
    fee=application["fee"]

    current_service_count=accumulator["services"].get(service,0)
    return {
        **accumulator,"total_approved":accumulator["total_approved"]+1,
        "total_fees":accumulator["total_fees"]+fee,
        "services":{**accumulator["services"],service:current_service_count+1}

    }

initial_accumulator={"total_approved":0,
                     "total_fees":0,
                     "services":{}}

approved_applications=filter(is_approved,applications)
normal=map(normalize_service_name,approved_applications)
final=reduce(aggregating,normal,initial_accumulator)

print(final)
