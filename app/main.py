from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.api.routes import auth, users
from app.core.config import settings
from app.core.database import engine, Base
from app.core.rate_limit import setup_rate_limiting

Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="User Management API",
    description="A FastAPI application with user management and email verification",
    version="1.0.0",
)

setup_rate_limiting(app)

app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.CORS_ORIGINS,
    allow_credentials=settings.CORS_ALLOW_CREDENTIALS,
    allow_methods=settings.CORS_ALLOW_METHODS,
    allow_headers=settings.CORS_ALLOW_HEADERS,
)

app.include_router(auth.router)
app.include_router(users.router)


@app.get("/")
def root():
    return {"message": "User Management API", "docs": "/docs", "redoc": "/redoc"}


@app.get("/health")
def health_check():
    return {"status": "healthy"}
