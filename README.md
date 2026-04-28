# Todo API

A simple Todo REST API built with Django, PostgreSQL, and Docker.

## Tech Stack
- Django + Django REST Framework
- PostgreSQL
- Docker + Docker Compose
- Poetry (dependency management)

## Setup

### Prerequisites
- Docker
- Docker Compose

### Run the app

1. Clone the repo
```bash
   git clone https://github.com/yourusername/todo-api.git
   cd todo-api
```

2. Create `.env` file
```bash
   cp .env.example .env
```
   Fill in your values.

3. Start the containers
```bash
   docker-compose up --build
```

4. Run migrations
```bash
   docker exec todo_web python manage.py migrate
```

5. Visit `http://localhost:8000/api/todos/`

## API Endpoints

| Method | URL | Description |
|--------|-----|-------------|
| GET | `/api/todos/` | List all todos |
| POST | `/api/todos/` | Create a todo |
| GET | `/api/todos/<id>/` | Get one todo |
| PATCH | `/api/todos/<id>/` | Update a todo |
| DELETE | `/api/todos/<id>/` | Delete a todo |
| PATCH | `/api/todos/<id>/toggle/` | Toggle completed |