# Task API

A small backend API for managing a to-do list, built with FastAPI. Supports full CRUD (Create, Read, Update, Delete) on an in-memory list of tasks.

Built as part of the FlyRank AI Fluency internship, Backend AI Engineering track — Week 2 assignment.

## How to run it

**Requirements:** Python 3.10+

1. Clone this repo and move into it:
```
   git clone https://github.com/dishaagowda/task-api.git
   cd task-api
```

2. Install dependencies:
```
   pip3 install fastapi uvicorn
```

3. Run the server:
```
   uvicorn main:app --reload
```

4. The API is now running at `http://localhost:8000`. Interactive docs (Swagger UI) are at `http://localhost:8000/docs`.

## Endpoints

| Method | Path             | Description                          |
|--------|------------------|---------------------------------------|
| GET    | `/`              | API info (name, version, endpoints)  |
| GET    | `/health`        | Health check                         |
| GET    | `/tasks`         | List all tasks                       |
| GET    | `/tasks/{id}`    | Get a single task by ID              |
| POST   | `/tasks`         | Create a new task                    |
| PUT    | `/tasks/{id}`    | Update a task's title                |
| DELETE | `/tasks/{id}`    | Delete a task                        |

## Example request

```
curl -i -X POST http://localhost:8000/tasks -H "Content-Type: application/json" -d '{"title":"Buy milk"}'
```

```
HTTP/1.1 201 Created
content-type: application/json

{"id":4,"title":"Buy milk","done":false}
```

## Swagger UI

Full CRUD tested and working via Swagger UI's "Try it out" feature:

![Swagger UI screenshot](swagger-screenshot.png)

## Notes

Data is stored in memory only — it resets every time the server restarts. A real database will be added in a future stage.