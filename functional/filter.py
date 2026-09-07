"""
A predicate function is simply a function that answers a question with:

True
or
False

Examples:

def is_adult(user):
    return user["age"] >= 18
def has_valid_id(application):
    return application["has_valid_id"]
def is_pending(application):
    return application["status"] == "pending"
def has_required_documents(application):
    return application["documents_complete"]
    
    
    
filter() returns an iterator too

Just like map():

adults = filter(is_adult, users)"""





"""
applications = [
    {
        "user": {
            "name": " nahom mekuria ",
            "age": 27
        },
        "service": "VAT Registration",
        "status": "pending",
        "documents_complete": True
    },
    {
        "user": {
            "name": " abebe kebede ",
            "age": 16
        },
        "service": "Business License",
        "status": "pending",
        "documents_complete": False
    },
    {
        "user": {
            "name": " meron tesfaye ",
            "age": 35
        },
        "service": "VAT Registration",
        "status": "approved",
        "documents_complete": True
    },
    {
        "user": {
            "name": " sara ali ",
            "age": 25
        },
        "service": "Business License",
        "status": "pending",
        "documents_complete": True
    }
]
Your task

Build a functional pipeline that:

Step 1 — Filter pending applications

Create:

is_pending(application)


Step 2 — Filter applications with complete documents

Create:

has_complete_documents(application)


Step 3 — Filter adult applicants

Create:

is_adult(application)


Step 4 — Transform the remaining applications

Create:

clean_application_name(application)

Requirements:

" nahom mekuria "
        ↓
"Nahom Mekuria"

Use an immutable nested update.



Step 5 — Normalize the service

Create:

normalize_service(application)





Example:

"VAT Registration"
        ↓
"vat_registration"



Your pipeline should conceptually look like:
applications
      ↓
filter(is_pending)
      ↓
filter(has_complete_documents)
      ↓
filter(is_adult)
      ↓
map(clean_application_name)
      ↓
map(normalize_service)
      ↓
list()
      ↓
FINAL RESULT

Rules

 Don't mutate the original data
 Predicates should return True or False
 Transformations should return new dictionaries
 Keep the pipeline lazy until the final list()
"""




def is_pending(application):
    return application["status"]=="pending"

def has_complete_document(application):
    return application["documents_complete"]==True

def is_adult(application):
    return application["user"]["age"]>=18

def clean_application_names(application):
    return {**application,"user":{**application["user"],"name":" ".join(application["user"]["name"].split()).title()}}

def normalize_service(application):
    return {**application,"service":"_".join(application["service"].split()).lower()}


def pipeline():
    applications = [
    {
        "user": {
            "name": " nahom mekuria ",
            "age": 27
        },
        "service": "VAT Registration",
        "status": "pending",
        "documents_complete": True
    },
    {
        "user": {
            "name": " abebe kebede ",
            "age": 16
        },
        "service": "Business License",
        "status": "pending",
        "documents_complete": False
    },
    {
        "user": {
            "name": " meron tesfaye ",
            "age": 35
        },
        "service": "VAT Registration",
        "status": "approved",
        "documents_complete": True
    },
    {
        "user": {
            "name": " sara ali ",
            "age": 25
        },
        "service": "Business License",
        "status": "pending",
        "documents_complete": True
    }
]
    pending=filter(is_pending,applications)
    completed_docs=filter(has_complete_document,pending)
    cleaned=map(clean_application_names,completed_docs)
    normalize=map(normalize_service,cleaned)

    return list(normalize)

print(pipeline())