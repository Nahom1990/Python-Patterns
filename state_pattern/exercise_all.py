"""
Build a Document Publishing System, similar to what a CMS or content platform might use.

A document can be in these states:

DRAFT
  │
  ├── submit_for_review()
  ▼
IN_REVIEW
  │
  ├── approve()
  ▼
PUBLISHED

There are also rejection paths:

IN_REVIEW
    │
    └── reject()
          ▼
        DRAFT

And archival:

PUBLISHED
    │
    └── archive()
          ▼
       ARCHIVED
Required operations

Your Document should expose:

edit(content)
submit_for_review()
approve()
reject()
publish()
archive()

But whether an operation is allowed depends on the current state.

Rules
📝 DRAFT
edit()                ✅ allowed
submit_for_review()   → IN_REVIEW
approve()             ❌ invalid
reject()              ❌ invalid
publish()             ❌ invalid
archive()             ❌ invalid
🔍 IN_REVIEW
edit()                ❌ invalid
submit_for_review()   ❌ invalid
approve()             → PUBLISHED
reject()              → DRAFT
publish()             ❌ invalid
archive()             ❌ invalid
🌍 PUBLISHED
edit()                ❌ invalid
submit_for_review()   ❌ invalid
approve()             ❌ invalid
reject()              ❌ invalid
publish()             ❌ invalid
archive()             → ARCHIVED
📦 ARCHIVED
All operations ❌ invalid
"""

###version 1

# from abc import ABC,abstractmethod

# class DocumentState(ABC):
#     @abstractmethod
#     def edit(self,doc): pass

#     @abstractmethod
#     def submit_for_review(self,doc): pass

#     @abstractmethod
#     def approve(self,doc): pass

#     @abstractmethod
#     def reject(self,doc): pass

#     @abstractmethod
#     def archive(self,doc): pass

# class Draft(DocumentState):
#     def edit(self,doc):
#         print("editing allowed")

#     def submit_for_review(self, doc):
#         doc.state=InReview()

#     def approve(self,doc):
#         print("draft must be submitted to be reviewed before approval")
    
#     def reject(self,doc):
#         print("draft must be submitted to be reviewed before rejection")

#     def archive(self,doc): 
#         print("draft cant be archived")

# class InReview(DocumentState):

#     def edit(self,doc):
#         print("already submitted for review")

#     def submit_for_review(self, doc):
#         print("already submitted for review")

#     def approve(self,doc):
#         doc.state=Publish()
    
#     def reject(self,doc):
#         doc.state=Draft()

#     def archive(self,doc): 
#         print("must be published before archiving")

# class Publish(DocumentState):

#     def edit(self,doc):
#         print("already aproved")

#     def submit_for_review(self, doc):
#         print("already published")

#     def approve(self,doc):
#         print("already published")
    
#     def reject(self,doc):
#         print("already published")


#     def archive(self,doc): 
#         doc.state=Archive()

# class Archive(DocumentState):

#     def edit(self,doc):
#         print("already archived")

#     def submit_for_review(self, doc):
#         print("already archived")

#     def approve(self,doc):
#         print("already archived")
    
#     def reject(self,doc):
#         print("already archived")

#     def archive(self,doc): 
#         print("already archived")

# class Document:
#     def __init__(self) -> None:
#         self.state=Draft()

#     def edit_it(self):
#         self.state.edit(self)

#     def submit_for_review(self):
#         self.state.submit_for_review(self)

#     def approve_it(self):
#         self.state.approve(self)

#     def reject_it(self):
#         self.state.reject(self)

#     def archive_it(self):
#         self.state.archive(self)

# document1=Document()
# document1.submit_for_review()
# print(document1.state)
# document1.reject_it()
# print(document1.state)
# document1.archive_it()
# print(document1.state)



###############version 2 
from enum import Enum,auto

class DocumentState2(Enum):
    DRAFT=auto()
    INREVIEW=auto()
    PUBLISHED=auto()
    ARCHIVED=auto()

class DocumentProcess:
    def __init__(self) -> None:
        self.state=DocumentState2.DRAFT

    def edit(self):
        match self.state:
            case DocumentState2.DRAFT:
                print("editing ...no state change still draft")
            case DocumentState2.INREVIEW:
                print("submitted draft")
            case DocumentState2.PUBLISHED | DocumentState2.ARCHIVED:
                print("must be approved/ first")

    def submit_for_review(self):
        match self.state:
            case DocumentState2.DRAFT:
                print("document submited for review")
                self.state=DocumentState2.INREVIEW
            case DocumentState2.INREVIEW:
                print("already under review")
            case DocumentState2.PUBLISHED | DocumentState2.ARCHIVED:
                print("must be approved/ first")

    def approve(self):
        match self.state:
            case DocumentState2.DRAFT:
                print("draft must be submitted before approval")
            case DocumentState2.INREVIEW:
                print("document approved ")
                self.state=DocumentState2.PUBLISHED
            case DocumentState2.PUBLISHED:
                print("already approved and Published")
                
            case DocumentState2.ARCHIVED:
                print("already approved and already archived.")

    def archive(self):
        match self.state:
            case DocumentState2.DRAFT:
                print("draft cant be archived")
            case DocumentState2.INREVIEW:
                print("must be approved and oublished to be archived")
            case DocumentState2.PUBLISHED:
                print("Document Archived")
                self.state=DocumentState2.ARCHIVED
            case DocumentState2.ARCHIVED:
                print("already archived")

    def reject(self):
        match self.state:
            case DocumentState2.DRAFT:
                print("must be submited to review first")
            case DocumentState2.INREVIEW:
                print("draft rejected")
                self.state=DocumentState2.DRAFT
            case DocumentState2.PUBLISHED:
                print("published cant be rejected")
            case DocumentState2.ARCHIVED:
                print("archived cant be rejected")
                

####version 3
from dataclasses import dataclass
from enum import Enum, auto
from typing import Literal

class DocumentState(Enum):
    DRAFT = auto()
    IN_REVIEW = auto()
    PUBLISHED = auto()
    ARCHIVED = auto()


Action = Literal["edit", "submit", "approve", "archive", "reject"]


@dataclass(frozen=True)
class Document:
    """Immutable Document state. here for every new state a new instance in memory
      is created because this is immutable because of frozen ,so good for avoiding race coditions
      in multithreaded situations
      """
    title: str = "Untitled"
    state: DocumentState = DocumentState.DRAFT


def transition(doc: Document, action: Action) -> tuple[Document, str]:
    """
    Pure function: Given an immutable Document and an Action, returns a tuple of
    (New Document Instance, Status Message).

    And here all the match cases are not spread around different functions its collected unde one function 
    under transitions so better approach here also, no hunting for each all are available here,

    also the match case is 2 dimensional before we were just matching the state to one of the [DRAFT,INREVIEW,PUBLISHED and ARCHIVED],
    but this one does that and the action [edit,submit,approve,reject,archive] here at the same time so both are cheked at once 
    in a tuple rather then the above approach this is what elped everyting to be collected as is down below.
    """
    match (doc.state, action):
        # --- Edit ---
        case (DocumentState.DRAFT, "edit"):
            return doc, "Editing... no state change, still draft."
        case (DocumentState.IN_REVIEW, "edit"):
            return doc, "Submitted draft - editing locked while under review."
        case (DocumentState.PUBLISHED | DocumentState.ARCHIVED, "edit"):
            return doc, "Cannot edit published or archived documents directly."

        # --- Submit for Review ---
        case (DocumentState.DRAFT, "submit"):
            return Document(title=doc.title, state=DocumentState.IN_REVIEW), "Document submitted for review."
        case (DocumentState.IN_REVIEW, "submit"):
            return doc, "Already under review."
        case (DocumentState.PUBLISHED | DocumentState.ARCHIVED, "submit"):
            return doc, "Cannot submit a published or archived document."

        # --- Approve ---
        case (DocumentState.DRAFT, "approve"):
            return doc, "Draft must be submitted for review before approval."
        case (DocumentState.IN_REVIEW, "approve"):
            return Document(title=doc.title, state=DocumentState.PUBLISHED), "Document approved and published."
        case (DocumentState.PUBLISHED, "approve"):
            return doc, "Already approved and published."
        case (DocumentState.ARCHIVED, "approve"):
            return doc, "Already archived."

        # --- Archive ---
        case (DocumentState.DRAFT, "archive"):
            return doc, "Drafts cannot be archived directly."
        case (DocumentState.IN_REVIEW, "archive"):
            return doc, "Must be approved and published before archiving."
        case (DocumentState.PUBLISHED, "archive"):
            return Document(title=doc.title, state=DocumentState.ARCHIVED), "Document archived."
        case (DocumentState.ARCHIVED, "archive"):
            return doc, "Already archived."

        # --- Reject ---
        case (DocumentState.DRAFT, "reject"):
            return doc, "Must be submitted for review first before rejection."
        case (DocumentState.IN_REVIEW, "reject"):
            return Document(title=doc.title, state=DocumentState.DRAFT), "Draft rejected, returned to DRAFT."
        case (DocumentState.PUBLISHED | DocumentState.ARCHIVED, "reject"):
            return doc, "Published or archived documents cannot be rejected."

        # --- Guard ---
        case _:
            raise ValueError(f"Unhandled action '{action}' for state '{doc.state}'")


def edit(doc: Document) -> tuple[Document, str]: return transition(doc, "edit")
def submit_for_review(doc: Document) -> tuple[Document, str]: return transition(doc, "submit")
def approve(doc: Document) -> tuple[Document, str]: return transition(doc, "approve")
def archive(doc: Document) -> tuple[Document, str]: return transition(doc, "archive")
def reject(doc: Document) -> tuple[Document, str]: return transition(doc, "reject")


doc = Document(title="Q3 Strategy")
print(f"Initial: {doc.state.name}\n" + "-" * 40)

actions = [edit, submit_for_review, approve, archive]

for act in actions:
    doc, msg = act(doc)
    print(f"[{act.__name__.upper()}] -> {msg}")
    print(f"Current State: {doc.state.name}\n" + "-" * 40)