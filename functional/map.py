"""
You are going to build a mini version of something very relevant to backend systems and your government assistant.

You receive:

applications = [
    {
        "user": {"name": " nahom mekuria ", "age": 27},
        "service": "VAT Registration",
        "status": "pending"
    },
    {
        "user": {"name": " abebe kebede ", "age": 16},
        "service": "Business License",
        "status": "pending"
    },
    {
        "user": {"name": " meron tesfaye ", "age": 35},
        "service": "VAT Registration",
        "status": "approved"
    }
]


Your task

Create these pure transformation functions:

clean_application_name(application)
add_adult_status(application)
normalize_service(application)


clean_application_name

Should:

" nahom mekuria "
        ↓
"Nahom Mekuria"
add_adult_status

Should add:

"is_adult": True

inside the user dictionary.

normalize_service

Should convert:

"VAT Registration"
        ↓
"vat_registration"

Then use map() to apply each transformation.

You should be able to do something conceptually like:

step1 = map(clean_application_name, applications)

step2 = map(add_adult_status, step1)

step3 = map(normalize_service, step2)

result = list(step3)
Important rules
Don't mutate the original applications.
Every transformation should return a new application.
Handle the nested "user" dictionary immutably.
Remember: each map() returns an iterator."""


applications = [
    {
        "user": {"name": " nahom mekuria ", "age": 27},
        "service": "VAT Registration",
        "status": "pending"
    },
    {
        "user": {"name": " abebe kebede ", "age": 16},
        "service": "Business License",
        "status": "pending"
    },
    {
        "user": {"name": " meron tesfaye ", "age": 35},
        "service": "VAT Registration",
        "status": "approved"
    }
]

def clean_application_name(app):
    return {**app,"user":{**app["user"],"name":" ".join(app["user"]["name"].split()).title()}}

def add_adult_status(app):
    return {**app,"user":{**app["user"],"is_adult":app["user"]["age"]>=18}}

def normalize_service(app):
    return {**app ,"service":"_".join(app["service"].split()).lower()}



def process(applications):
    cleaned_name=map(clean_application_name,applications)
    add_adlt=map(add_adult_status,cleaned_name)
    normalize_ser=map(normalize_service,add_adlt)

    return list(normalize_ser)

print(process(applications))


