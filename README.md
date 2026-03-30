# FastAPI Sample

A FastAPI application with user management and email verification.

## Features

- User registration and authentication
- JWT-based authentication
- Password hashing with bcrypt
- Email verification via SendGrid
- SQLAlchemy ORM with SQLite database
- Interactive API documentation (Swagger UI and ReDoc)
- Rate limiting on authentication endpoints

## Tech Stack

- **FastAPI** - Modern Python web framework
- **SQLAlchemy** - SQL ORM
- **Pydantic** - Data validation
- **Python-Jose** - JWT token handling
- **Passlib** - Password hashing
- **SendGrid** - Email service
- **SlowAPI** - Rate limiting

## Requirements

- Python 3.10+
- SendGrid account (optional, for email delivery)

## Installation

```bash
pip install -r requirements.txt
```

## Configuration

Copy `.env.example` to `.env` and configure:

```bash
cp .env.example .env
```

### Required Environment Variables

| Variable | Description | Required |
|----------|-------------|----------|
| `SECRET_KEY` | JWT signing key (use `openssl rand -hex 32`) | Yes |
| `DATABASE_URL` | Database connection string | No (defaults to SQLite) |
| `SENDGRID_API_KEY` | SendGrid API key for emails | No (logs emails if unset) |
| `SENDGRID_FROM_EMAIL` | Sender email address | No |
| `APP_URL` | Application base URL | No |

### Security Configuration

| Variable | Description | Default |
|----------|-------------|---------|
| `CORS_ORIGINS` | Allowed CORS origins (JSON array) | `["http://localhost:3000"]` |
| `CORS_ALLOW_CREDENTIALS` | Allow credentials in CORS | `True` |
| `CORS_ALLOW_METHODS` | Allowed HTTP methods | `["*"]` |
| `CORS_ALLOW_HEADERS` | Allowed HTTP headers | `["*"]` |

> **Security Note**: Never use `["*"]` for `CORS_ORIGINS` in production when `CORS_ALLOW_CREDENTIALS=True`. Browsers reject `Access-Control-Allow-Credentials: true` with wildcard origins.

### Rate Limits

Authentication endpoints have rate limiting:

| Endpoint | Limit |
|----------|-------|
| `/auth/register` | 5 requests/minute |
| `/auth/login` | 10 requests/minute |
| `/auth/verify-email` | 20 requests/minute |
| `/auth/resend-verification` | 3 requests/minute |

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
- `GET /auth/verify-email` - Verify user email
- `POST /auth/resend-verification` - Resend verification email

### Users
- `GET /users/` - List all users
- `GET /users/{user_id}` - Get user by ID
- `PUT /users/{user_id}` - Update user
- `DELETE /users/{user_id}` - Delete user

## License

MIT License