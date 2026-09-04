"""
The Repository-Service-Controller (RSC) architecture is a layered pattern used to structure backend applications—most notably in frameworks like Spring Boot, NestJS, ASP.NET Core, and Express/FastAPI.

It enforces a strict Separation of Concerns (SoC) by dividing the lifecycle of an HTTP request into three distinct layers: HTTP handling (Controller), business logic (Service), and data access (Repository).

The Request Flow
[ HTTP Client ]
      │  ▲
 1. Request / 6. Response
      ▼  │
┌─────────────────────────┐
│       CONTROLLER        │  ── Parses HTTP, validates parameters, returns status codes
└────────────┬────────────┘
             │  ▲
 2. DTO Data │  │ 5. Domain Model/Result
             ▼  │
┌─────────────────────────┐
│         SERVICE         │  ── Executes business rules, orchestrates operations, manages transactions
└────────────┬────────────┘
             │  ▲
 3. Query    │  │ 4. Entity Data
             ▼  │
┌─────────────────────────┐
│       REPOSITORY        │  ── Encapsulates database queries (SQL, ORM, Document DBs)
└─────────────────────────┘


Layer Responsibilities

1. Controller Layer (Presentation / Transport)
Role: Acts as the entry point for inbound HTTP requests.

Responsibilities:

    Defines REST routes, HTTP verbs (GET, POST, etc.), and endpoint security.

    Deserializes request payloads into Data Transfer Objects (DTOs) and validates inputs.

    Calls the appropriate Service method.

    Serializes domain outputs and returns HTTP responses with proper status codes (200 OK, 400 Bad Request, 404 Not Found).

    Rule of Thumb: Controllers should be "thin." They should never contain SQL queries or business decisions.

2. Service Layer (Business Logic)
Role: Represents the core domain rules and workflows of your application.

Responsibilities:

    Coordinates business tasks (e.g., calculating discounts, sending emails, verifying user permissions).

    Manages database transactions (e.g., atomic operations across multiple repositories).

    Transforms raw data entities into application domain models or DTOs.

    Rule of Thumb: Services should be completely decoupled from HTTP frameworks. You should be able to trigger a Service function via a CLI script, background queue worker, or gRPC endpoint without modifying its code.

3. Repository Layer (Data Access)
Role: Abstracts data persistence mechanisms behind an interface.

Responsibilities:

    Encapsulates direct database operations (SQL queries, ORM calls, MongoDB aggregations).

    Provides generic CRUD operations alongside specialized query methods (findActiveUsersByTenant).

    Converts raw database records into Domain Entities.

    Rule of Thumb: Repositories shield the rest of the application from database details. Switching from PostgreSQL to MongoDB or upgrading an ORM should only impact this layer.

    
Implementation Example (Python / FastAPI)

Here is how the three layers interact in a production-style application."""