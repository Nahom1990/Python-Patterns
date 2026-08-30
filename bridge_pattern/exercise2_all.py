"""Bridge Project — Report Generation System

You are building a system that generates different kinds of business reports.

The system has two independent dimensions.

Dimension 1: Report type

The application supports:

Sales Report
Inventory Report
Performance Report

Each report has different logic for gathering/preparing its data.

Conceptually:

SalesReport
InventoryReport
PerformanceReport
Dimension 2: Renderer

Each report can be rendered using:

PDF
HTML
JSON

Conceptually:

PDFRenderer
HTMLRenderer
JSONRenderer
The problem

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

But you must decide the details yourself.

Functional requirements

Your application should allow combinations like:

SalesReport(PDFRenderer())
SalesReport(JSONRenderer())
InventoryReport(HTMLRenderer())
PerformanceReport(PDFRenderer())

Every report should be able to work with every renderer.

Each report should have its own data

You don't need a real database.

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