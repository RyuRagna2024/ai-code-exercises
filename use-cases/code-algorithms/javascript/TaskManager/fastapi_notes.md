# Exercise: Getting Started with FastAPI - Part 1 Notes

## Prompt Executed
> **Prompt:** "Create a comprehensive overview of FastAPI covering: What it is compared to Flask and Django, its core concepts, key advantages, and an essential glossary."

---

## 1. What is FastAPI and Comparison

FastAPI is a modern, high-performance web framework for building APIs with Python based on standard Python type hints.

| Feature | FastAPI | Flask | Django |
| :--- | :--- | :--- | :--- |
| **Primary Purpose** | High-performance, Async RESTful APIs | Micro-services, lightweight web apps | Monolithic, full-stack web applications |
| **Architecture** | ASGI native (Async Server Gateway Interface) | WSGI native (Synchronous by default) | WSGI / ASGI (MVT - Model View Template) |
| **Data Validation** | Automatic via Pydantic | Manual or via extensions (e.g., Marshmallow) | Built-in Django Forms / Serializers (DRF) |
| **API Documentation** | Automatic (OpenAPI / Swagger UI / ReDoc) | Requires third-party tools (e.g., Flask-RESTX) | Requires DRF + third-party packages |
| **Batteries Included** | Focused on API tier (Requires ORM setup like SQLAlchemy) | Minimalist (Requires extensions for DB, auth, etc.) | Complete suite (Built-in ORM, Admin UI, Auth) |
| **Performance** | Very High (On par with NodeJS / Go) | Moderate | Moderate / Low under high concurrency |

---

## 2. Core Concepts and Terminology

* **Type Hints (`typing`):** Python standard syntax declaring data types. FastAPI uses these to validate requests, format responses, and auto-generate API documentation.
* **ASGI (Asynchronous Server Gateway Interface):** The modern standard for Python asynchronous web servers (e.g., Uvicorn), enabling high-concurrency handling.
* **Pydantic:** The underlying data validation library. Defines data schemas as Python classes with strict type checking and automatic JSON serialization.
* **Starlette:** The lightweight ASGI framework driving FastAPI's routing, request/response handling, and WebSocket support.
* **Dependency Injection (`Depends`):** A pattern allowing routes to declare prerequisites (like DB sessions, auth tokens, or query parameters) that FastAPI automatically resolves before executing the endpoint handler.

---

## 3. Key Advantages of FastAPI

1. **High Performance:** Utilizes Python's `async`/`await` primitives and Starlette to deliver throughput competitive with NodeJS and Go.
2. **Automatic Interactive Docs:** Generates live, testable Swagger UI (`/docs`) and ReDoc (`/redoc`) endpoints automatically out-of-the-box.
3. **Developer Ergonomics:** Editor auto-completion and static analysis work out-of-the-box thanks to strict Python type hinting.
4. **Data Integrity & Validation:** Automatically validates incoming payload types, throwing standardized HTTP 422 errors when payload validation fails.
5. **Native Dependency System:** Simplifies code reuse, security checks, and database session lifecycles through declarative dependencies.

---

## 4. Essential FastAPI Glossary

* **Path Operation:** The combination of an HTTP method (`GET`, `POST`, `PUT`, `DELETE`) and an endpoint URL path.
* **Path Operation Decorator:** Function decorators like `@app.get("/items")` that register an endpoint with the application instance.
* **Path Parameter:** Dynamic variable segments extracted directly from the URL path (e.g., `/items/{item_id}`).
* **Query Parameter:** Key-value pairs appended after the `?` in a URL string (e.g., `/items?limit=10`).
* **Request Body:** Data transmitted by the client inside the HTTP request payload (typically formatted as JSON).
* **Response Model:** A Pydantic class specified in the route decorator (`response_model=ItemSchema`) to filter and format outgoing payload structures.
* **Uvicorn:** An lightning-fast ASGI web server implementation used to run FastAPI applications in production and development.

===

## Exercise: Getting Started with FastAPI - Part 2 Notes

### Prompts Executed
> **Prompt:** "Generate a basic 'Hello World' example for FastAPI with comments explaining each part, path parameters, query parameters, and how to run/test locally."

---

### Implementation Summary (`main.py`)
* Created an `app = FastAPI(...)` instance with metadata (title, description, version).
* Defined `GET /` returning a simple JSON welcome object.
* Implemented path parameters via `@app.get("/items/{item_id}")` with automatic type validation (`item_id: int`).
* Implemented query parameters via `@app.get("/search/")` using optional arguments and defaults (`q: str = None`, `skip: int = 0`, `limit: int = 10`).

---

### Recommended Production Folder Structure
For real-world scalable applications, transition from single-file `main.py` to a modular layout:

```text
my_fastapi_project/
├── app/
│   ├── __init__.py
│   ├── main.py          # App initialization & middleware
│   ├── config.py        # Environment variables & settings
│   ├── api/             # Endpoint routers
│   │   ├── __init__.py
│   │   └── v1/
│   │       ├── __init__.py
│   │       ├── router.py
│   │       └── endpoints/
│   ├── core/            # Security, database, base configs
│   ├── models/          # ORM models (e.g. SQLAlchemy)
│   └── schemas/         # Pydantic schemas
├── requirements.txt
└── README.md

```
## Exercise: Getting Started with FastAPI - Part 2 Execution Log

### Terminal Output Verification
```powershell
(venv) PS C:\...\TaskManager> uvicorn main:app --reload
INFO:     Will watch for changes in directories: ['...']
INFO:     Uvicorn running on [http://127.0.0.1:8000](http://127.0.0.1:8000) (Press CTRL+C to quit)
INFO:     Started reloader process [2872] using StatReload
INFO:     Started server process [13528]
INFO:     Waiting for application startup.
INFO:     Application startup complete.
INFO:     127.0.0.1:50706 - "GET / HTTP/1.1" 200 OK
INFO:     127.0.0.1:60713 - "GET /items/42 HTTP/1.1" 200 OK
INFO:     127.0.0.1:63189 - "GET /search/?q=fastapi&skip=0&limit=5 HTTP/1.1" 200 OK
INFO:     127.0.0.1:58672 - "GET /docs HTTP/1.1" 200 OK
INFO:     127.0.0.1:51221 - "GET /redoc HTTP/1.1" 200 OK

===

## Exercise: Getting Started with FastAPI - Part 3 Verification Log

### Validation & Exception Testing Results
* **POST /items/ (Negative Price Validation):**
  * Payload: `{"name": "Bad Item", "price": -10.0}`
  * Status: `422 Unprocessable Entity`
  * Outcome: Pydantic `gt=0` constraint caught the invalid price prior to route handler execution.

* **GET /items/999 (Custom Exception Handler):**
  * Request: `/items/999`
  * Status: `404 Not Found`
  * Outcome: `ItemNotFoundError` exception handler returned clean JSON payload `{"detail": "Item with ID 999 not found"}`.

* **GET /items/ (Query Filtering & Pagination):**
  * Request: `/items/?skip=0&limit=10&tag=electronics`
  * Status: `200 OK`
  * Outcome: Successfully created an item via POST and queried it using combined tag filtering and pagination constraints.

  ===

  ## Exercise: Getting Started with FastAPI - Part 4 Challenge Notes

### Prompts Executed
> **Prompt:** "Build a complete CRUD FastAPI application for a To-Do list supporting item creation (title, description, due_date), filtering by status (completed/pending), marking items as completed via PATCH, deleting items via DELETE, and returning proper HTTP status codes."

---

### Challenge Implementation Summary

1. **Pydantic Data Schemas (`app/models/todo.py`):**
   * Configured strict field requirements (`title` mandatory, `due_date` parsed as ISO `date`).
   * Decoupled creation requirements (`TodoCreate`) from complete item representations (`TodoResponse`).

2. **Endpoints & HTTP Verbs (`app/routes/todos.py`):**
   * `POST /todos/`: Creates item (HTTP 201 Created).
   * `GET /todos/`: Lists items with optional `completed` boolean query parameter filtering.
   * `PATCH /todos/{todo_id}/complete`: Updates status directly on target resource.
   * `DELETE /todos/{todo_id}`: Removes item returning clean `HTTP 204 No Content`.

3. **Exception Handling (`app/utils/exceptions.py`):**
   * Handled nonexistent resource calls using custom `TodoNotFoundError` (HTTP 404).
   * Schema constraint violations automatically trigger formatted `HTTP 422 Unprocessable Entity` responses.

   ===

# Contextual Learning with FastAPI - Findings & Analysis

## Part 1: Framework Translation Table

| Feature / Concept | Flask | Django | FastAPI Equivalent |
| :--- | :--- | :--- | :--- |
| **Routing / Modules** | `Blueprint` | `app/urls.py` & Apps | `APIRouter` |
| **Request Parsing** | `request.form` / `request.json` | `request.POST` / `Form` | Pydantic Models & `Depends()` |
| **Validation Layer** | Manual (or Marshmallow) | Django Forms / Serializers | Pydantic Schemas (`BaseModel`) |
| **Auth Injection** | `@login_required` decorator | `LoginRequiredMixin` / Middleware | `Depends(get_current_user)` |
| **Server Gateway** | WSGI (Gunicorn / Werkzeug) | WSGI / ASGI (Channels) | ASGI native (Uvicorn / Starlette) |
| **API Docs** | Third-party extension | DRF + `drf-spectacular` | Automatic (Swagger UI / ReDoc) |

---

## Part 2: Design Philosophy Summary

1. **Pydantic Adoption:** FastAPI avoids wheel-reinvention by leveraging Pydantic. Validation occurs entirely at Python runtime using standard type hints.
2. **Type Hints First:** Type declarations act simultaneously as data validation, IDE auto-complete triggers, and automatic OpenAPI schema generators.
3. **ASGI Native & Async:** Built ground-up on Starlette to run on asynchronous event loops, offering performance close to Go/NodeJS under heavy concurrency.
4. **Dependency Injection:** Replaces monolithic middleware or complex subclassing with composable, reusable callables (`Depends`).

---

## Part 3: Applied JWT Authentication Analysis

### Reflection Answers

1. **Framework Comparison:**
   * Unlike Flask requiring extensions (e.g., `Flask-JWT-Extended`) or Django requiring DRF wrappers, FastAPI natively integrates OAuth2 flows into the core framework and OpenAPI specification via `OAuth2PasswordBearer`.

2. **Advantages of Dependency Injection:**
   * Dependencies can be stacked (`get_current_active_user` depends on `get_current_user`). If token validation fails in the inner dependency, route handlers never execute.

3. **Type Hinting for Security:**
   * Defining response models (`response_model=User`) guarantees secret data (like `hashed_password`) is automatically stripped before sending JSON responses back to clients.

4. **Identified Patterns:**
   * The underlying JWT signature creation, password hashing via `passlib` (bcrypt), and Bearer token headers follow universal RFC standards utilized across Node (Express), Python (Flask/Django), and Go.

---

## Part 4: Mental Model Map

```text
Traditional MVC Framework (Flask/Django)
  │
  ├── Request ──► Middleware/Hooks ──► URL Router ──► View / Controller Function
  │                                                        │
  └────── JSON Response ◄── Serializer / Form ◄────────────┘

FastAPI Mental Model
  │
  ├── Request ──► APIRouter ──► Dependency Graph (Depends) ──► Route Handler
  │                                    │                          │
  │                             (Auth, Validation,             (Business Logic)
  │                                DB Sessions)                   │
  │                                    │                          │
  └────── JSON Response ◄────── Pydantic Response Model ◄─────────┘

