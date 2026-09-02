"""Bridge Project — Report Generation System
You are building a system that generates different kinds of business reports.
The system has two independent dimensions.

###  Dimension 1: Report type

The application supports:

1. Sales Report
2. Inventory Report
3. Performance Report
Each report has different logic for gathering/preparing its data.

####Dimension 2: Renderer

Each report can be rendered using:

1. PDF
2. HTML
3. JSON

Without a good design, someone might create:

SalesPDFReport
SalesHTMLReport
SalesJSONReport

InventoryPDFReport
InventoryHTMLReport
InventoryJSONReport

PerformancePDFReport
PerformanceHTMLReport
PerformanceJSONReport

That's:

3 Report Types × 3 Renderers = 9 classes

And if we add more reports or renderers, the number keeps multiplying.

Your job is to design this using Bridge.

The intended conceptual relationship is:

                 REPORT
                    │
                    │ has-a
                    ▼
                 RENDERER


Functional requirements

Your application should allow combinations like:
Every report should be able to work with every renderer.
 
SalesReport(PDFRenderer())
SalesReport(JSONRenderer())
InventoryReport(HTMLRenderer())
PerformanceReport(PDFRenderer())


Each report should have its own data

For example, each report can prepare data differently:

Sales
{
    "total_sales": 100000,
    "orders": 250
}
Inventory
{
    "total_products": 500,
    "low_stock": 12
}
Performance
{
    "uptime": "99.9%",
    "response_time": "120ms"
}

The values themselves don't matter.

The important thing is that each Report owns its own report-specific logic/data.

Each renderer should render generically

The Renderer should not need to know:

"This is a SalesReport"

or:

"This is an InventoryReport"

It should receive data and render it.

Conceptually:

Report
   │
   │ prepares data
   ▼
Renderer
   │
   │ renders data
   ▼
Output
Version 1 — Classical GoF Bridge

Use:

ABC
abstractmethod

Think about creating:

Report              ← Abstraction

SalesReport         ← Refined Abstraction
InventoryReport     ← Refined Abstraction
PerformanceReport   ← Refined Abstraction


Renderer            ← Implementor

PDFRenderer         ← Concrete Implementor
HTMLRenderer        ← Concrete Implementor
JSONRenderer        ← Concrete Implementor

Your Report should hold a Renderer through composition.

Something conceptually like:

self.renderer = renderer

But write the implementation yourself.

Version 2 — Modern Pythonic Bridge

Now solve the same problem using:

Protocol

Rules:

Renderer should be a Protocol.
Concrete renderers should not inherit from the Protocol.
You may still use normal inheritance where genuine specialization makes sense.
Avoid ABC and abstractmethod.

Again, the core Bridge should still be:

Report
   │
   │ has-a
   ▼
Renderer
Version 3 — Functional / Procedural Approach 🔥

Now solve the same problem without designing a Bridge class hierarchy.

You can use:

functions
dictionaries
plain data
callable objects if you want"""




###Version 1 classic Python
from abc import ABC,abstractmethod
class Renderer(ABC):
    @abstractmethod
    def render(self,data):
        pass
class PDFRenderer(Renderer):
    def render(self,data):
        print(f"rendered{data} in PDF")

class HTMLRenderer(Renderer):
    def render(self,data):
        print(f"rendered{data} in HTML")
class JSONRenderer(Renderer):
    def render(self,data):
        print(f"rendered{data} in JSON")


class ReportType:
    def __init__(self,renderer:Renderer) -> None:
        self.renderer=renderer

class SalesReport(ReportType): ##made same to inventory and performance report because ots example but even though they share the report method their operations inside would be different
    def report(self,data):
        self.renderer.render(data=data)

class InventoryReport(ReportType):
    def report(self,data):
        self.renderer.render(data=data)
class PerfomanceReport(ReportType):
    def report(self,data):
        self.renderer.render(data=data)


pdf_report=SalesReport(PDFRenderer())
pdf_report.report(data={
                            "total_sales": 100000,
                            "orders": 250
                        })


#####version 2
from typing import Protocol
class Renderer2(Protocol):
    def render(self,data): ...

class PDFRenderer2:
    def render(self,data):
        print(f"rendering {data} in pdf")

class HTMLRenderer2:
    def render(self,data):
        print(f"rendering {data} in html")

class JSONRenderer2:
    def render(self,data):
        print(f"rendering {data} in json")

class ReportType2:
    def __init__(self,renderer:Renderer2) -> None:
        self.renderer=renderer

class SalesReport2(ReportType2):
    def report(self,data):
        self.renderer.render(data=data)

class InventoryReport2(ReportType2):
    def report(self,data):
        self.renderer.render(data=data)
class PerfomanceReport2(ReportType2):
    def report(self,data):
        self.renderer.render(data=data)


pdf_report=SalesReport2(PDFRenderer2())
pdf_report.report(data={
                            "total_sales": 100000,
                            "orders": 250
                        })


###version 3 functional or procedural 

from typing import Callable,Any,Dict


#pure rendering functions
def render_pdf_fn(data:Any)->None:
    print(f"[functional] rendering PDF: {data}")

def render_html_fn(data:Any)->None:
    print(f"[functional] rendering html")

def render_json_fn(data:Any)-> None:
    print(f"[dunctional] rendering json")

def make_sales_report(renderer:Callable[[Any],None])->Callable[[Dict[str,Any]],None]:
    def report(data:Dict[str,Any])->None:
        report_payload = {
            "title": "Sales Report",
            "total_sales": data.get("total_sales"),
            "orders": data.get("orders")
        }
        renderer(report_payload)
    return report


sales_data={"total_sales":100000,"orders":250}

pdf_sales_repoter=make_sales_report(render_pdf_fn)
pdf_sales_repoter(sales_data)
json_saled_repoter=make_sales_report(render_json_fn)
json_saled_repoter(sales_data)