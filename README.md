# FastAPI URL Shortener

A simple URL shortener service built with FastAPI, SQLModel, and SQLite. This project allows you to shorten URLs, retrieve original URLs, track click counts, update, and delete short URLs via a RESTful API.

---

## Table of Contents
- [Features](#features)
- [API Endpoints](#api-endpoints)
- [Database](#database)
- [How to Run the Server](#how-to-run-the-server)
- [How to Run the Frontend (Optional)](#how-to-run-the-frontend-optional)
- [API Usage Examples](#api-usage-examples)
- [Testing](#testing)
- [Keploy API Testing Report](#keploy-api-testing-report)
- [CI/CD Configuration](#cicd-configuration)

---

## Features
- Shorten long URLs to short codes
- Redirect to original URLs using short codes
- Track the number of times a short URL is used
- Update or delete short URLs
- Retrieve information about a short URL

---

## API Endpoints

| Method | Endpoint                | Description                                 |
|--------|-------------------------|---------------------------------------------|
| GET    | `/check`                | Health check endpoint                       |
| POST   | `/shorten`              | Create a new short URL                      |
| GET    | `/{short_code}`         | Redirect to the original URL                |
| GET    | `/info/{short_code}`    | Get info about a short URL                  |
| DELETE | `/delete/{short_code}`  | Delete a short URL                          |
| PUT    | `/update/{short_code}`  | Update the original URL for a short code    |

---

## Database

- **Type:** SQLite
- **File:** `shortener.db` (created automatically in the project root)
- **ORM:** [SQLModel](https://sqlmodel.tiangolo.com/)

### Integration
- The database is initialized at server startup using `init_db()`.
- All database operations (CRUD) are handled via SQLModel ORM models and sessions.
- The main model is `ShortURL` with fields: `id`, `original_url`, `short_code`, `created_at`, and `click_count`.

---

## How to Run the Server

1. **Install dependencies** (preferably in a virtual environment):
   ```bash
   pip install -r requirements.txt
   ```

2. **Start the server:**
   ```bash
   uvicorn app:app --reload
   ```
   The API will be available at [http://127.0.0.1:8000](http://127.0.0.1:8000)

3. **API docs:**
   - Swagger UI: [http://127.0.0.1:8000/docs](http://127.0.0.1:8000/docs)
   - ReDoc: [http://127.0.0.1:8000/redoc](http://127.0.0.1:8000/redoc)

---

## How to Run the Frontend (Optional)

This project does not include a frontend by default. You can use any HTTP client (e.g., Postman, curl, or a custom frontend) to interact with the API.

---

## API Usage Examples

### 1. Health Check
```http
GET /check
```
**Response:**
```json
{"message": "Working Alright"}
```

### 2. Shorten a URL
```http
POST /shorten
Content-Type: application/json

{
  "original_url": "https://www.example.com"
}
```
**Response:**
```json
{
  "id": 1,
  "original_url": "https://www.example.com",
  "short_code": "a1B2c3",
  "created_at": "2024-06-10T12:00:00Z",
  "click_count": 0
}
```

### 3. Redirect to Original URL
```http
GET /a1B2c3
```
- Redirects to `https://www.example.com`.

### 4. Get Info About a Short URL
```http
GET /info/a1B2c3
```
**Response:**
```json
{
  "id": 1,
  "original_url": "https://www.example.com",
  "short_code": "a1B2c3",
  "created_at": "2024-06-10T12:00:00Z",
  "click_count": 5
}
```

### 5. Delete a Short URL
```http
DELETE /delete/a1B2c3
```
**Response:**
```json
{"message": "Deleted successfully"}
```

### 6. Update a Short URL
```http
PUT /update/a1B2c3
Content-Type: application/json

{
  "original_url": "https://www.new-url.com"
}
```
**Response:**
```json
{
  "id": 1,
  "original_url": "https://www.new-url.com",
  "short_code": "a1B2c3",
  "created_at": "2024-06-10T12:00:00Z",
  "click_count": 5
}

```
---

## Testing

| Tool                | Purpose                                 |
|---------------------|-----------------------------------------|
| `pytest`            | Running unit, integration, and API tests|
| `pytest-cov`        | Measuring code coverage                 |
| FastAPI `TestClient`| For API endpoint testing                |
| SQLModel + SQLite   | In-memory test DB interactions          |

---

## Run Commands (Per Test Type)

Each test type can be run separately to generate individual coverage reports.

### Unit Tests

```bash
pytest test/unit --cov=database --cov-report=term-missing
```
### Unit Test Coverage
<img width="1084" alt="unit_test" src="https://github.com/user-attachments/assets/2edda873-b88b-4ceb-b6ff-0b1f1671cdb7" />


### Integration Tests

```bash
pytest test/integration --cov=database --cov-report=term-missing
```
### Integration Test Coverage
<img width="1084" alt="integration_test" src="https://github.com/user-attachments/assets/7559238c-d70c-4fca-90ac-bebccaa918dd" />


### API Tests

```bash
pytest test/api --cov=app --cov-report=term-missing
```

### API Test Coverage
<img width="1084" alt="api_test" src="https://github.com/user-attachments/assets/5713eddc-9758-4fd0-bbb5-94a4c18ffd5a" />

---

## Keploy API Testing Report

<img width="960" alt="dashboard_6" src="https://github.com/user-attachments/assets/787fdde8-de60-4930-bd5e-f6941fc2ae66" />

---

## CI/CD Configuration

GitHub Actions to run the Keploy test suite.
[View CI Workflow](.github/workflows/ci.yml)

