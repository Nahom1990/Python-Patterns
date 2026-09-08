"""
You have:

applications = [
    {
        "user": {
            "name": " Nahom Mekuria ",
            "age": 27
        },
        "service": "VAT Registration",
        "status": "approved",
        "fee": 500,
        "documents_complete": True
    },
    {
        "user": {
            "name": " Abebe Kebede ",
            "age": 16
        },
        "service": "Business License",
        "status": "pending",
        "fee": 300,
        "documents_complete": True
    },
    {
        "user": {
            "name": " Meron Tesfaye ",
            "age": 35
        },
        "service": "VAT Registration",
        "status": "approved",
        "fee": 500,
        "documents_complete": True
    },
    {
        "user": {
            "name": " Sara Ali ",
            "age": 25
        },
        "service": "Business License",
        "status": "approved",
        "fee": 300,
        "documents_complete": False
    },
    {
        "user": {
            "name": " Dawit Bekele ",
            "age": 40
        },
        "service": "Trade License",
        "status": "approved",
        "fee": 200,
        "documents_complete": True
    },
    {
        "user": {
            "name": " Hana Ahmed ",
            "age": 30
        },
        "service": "VAT Registration",
        "status": "rejected",
        "fee": 500,
        "documents_complete": True
    }
]
Your final output should be:
{
    "total_processed": 3,
    "total_fees": 1200,
    "services": {
        "vat_registration": {
            "applications": 2,
            "fees": 1000
        },
        "trade_license": {
            "applications": 1,
            "fees": 200
        }
    },
    "applicants": [
        "Nahom Mekuria",
        "Meron Tesfaye",
        "Dawit Bekele"
    ]
}
Requirements

Your final analytics should only include applications that are:

approved
AND
documents_complete
AND
applicant is an adult
"""

applications = [
    {
        "user": {
            "name": " Nahom Mekuria ",
            "age": 27
        },
        "service": "VAT Registration",
        "status": "approved",
        "fee": 500,
        "documents_complete": True
    },
    {
        "user": {
            "name": " Abebe Kebede ",
            "age": 16
        },
        "service": "Business License",
        "status": "pending",
        "fee": 300,
        "documents_complete": True
    },
    {
        "user": {
            "name": " Meron Tesfaye ",
            "age": 35
        },
        "service": "VAT Registration",
        "status": "approved",
        "fee": 500,
        "documents_complete": True
    },
    {
        "user": {
            "name": " Sara Ali ",
            "age": 25
        },
        "service": "Business License",
        "status": "approved",
        "fee": 300,
        "documents_complete": False
    },
    {
        "user": {
            "name": " Dawit Bekele ",
            "age": 40
        },
        "service": "Trade License",
        "status": "approved",
        "fee": 200,
        "documents_complete": True
    },
    {
        "user": {
            "name": " Hana Ahmed ",
            "age": 30
        },
        "service": "VAT Registration",
        "status": "rejected",
        "fee": 500,
        "documents_complete": True
    }
]

def is_approved(application):
    return application["status"]=="approved"

def document_completed(application):
    return application["documents_complete"]

def is_adult(application):
    return application["user"]["age"]>=18

def normalize_service(application):
    return {**application,"service":"_".join(application["service"].split()).lower()}

def normalize_name(application):
    return {**application,"user":{**application["user"],"name":" ".join(application["user"]["name"].split()).title()}}


def aggregator(accumulator,application):
    current_service=application["service"]
    service_default={"applications":0,"fees":0}
    current_applicant=application["user"]["name"]
    return {**accumulator,
            "total_processed":accumulator["total_processed"]+1,
            "total_fees":accumulator["total_fees"]+application["fee"],
            "services":
                {**accumulator["services"],
                        current_service:{"applications":accumulator["services"].get(current_service,service_default)["applications"]+1,
                                        "fees":accumulator["services"].get(current_service,service_default)["fees"]+application["fee"]}},
            "applicants":[*accumulator["applicants"],current_applicant]}

from functools import reduce

initial={"total_processed":0,
        "total_fees":0,
        "services":{},
        "applicants":[]}

def process():
    approved=filter(is_approved,applications)
    doc=filter(document_completed,approved)
    adult=filter(is_adult,doc)
    normal=map(normalize_service,adult)
    normal_name=map(normalize_name,normal)

    final=reduce(aggregator,normal_name,initial)
    return final

print(process())