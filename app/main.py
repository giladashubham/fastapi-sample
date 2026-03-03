from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.api.routes import auth, users
from app.core.config import settings
from app.core.database import engine, Base

Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="User Management API",
    description="A FastAPI application with user management and email verification",
    version="1.0.0",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(auth.router)
app.include_router(users.router)


@app.get("/")
def root():
    return {"message": "User Management API", "docs": "/docs", "redoc": "/redoc"}


@app.get("/health")
def health_check():
    return {"status": "healthy"}
