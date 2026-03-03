# FastAPI Sample

A FastAPI application with user management and email verification.

## Features

- User registration and authentication
- JWT-based authentication
- Password hashing with bcrypt
- Email verification via SendGrid
- SQLAlchemy ORM with SQLite database
- Interactive API documentation (Swagger UI and ReDoc)

## Tech Stack

- **FastAPI** - Modern Python web framework
- **SQLAlchemy** - SQL ORM
- **Pydantic** - Data validation
- **Python-Jose** - JWT token handling
- **Passlib** - Password hashing
- **SendGrid** - Email service

## Installation

```bash
pip install -r requirements.txt
```

## Running the Application

```bash
uvicorn app.main:app --reload
```

The API will be available at:
- API docs: http://localhost:8000/docs
- ReDoc: http://localhost:8000/redoc
- Health check: http://localhost:8000/health

## API Endpoints

### Authentication
- `POST /auth/register` - Register a new user
- `POST /auth/login` - Login and get access token
- `GET /auth/me` - Get current user info
- `POST /auth/verify-email` - Verify user email

### Users
- `GET /users/` - List all users
- `GET /users/{user_id}` - Get user by ID
- `PUT /users/{user_id}` - Update user
- `DELETE /users/{user_id}` - Delete user
