from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    DATABASE_URL: str = "sqlite:///./app.db"
    SECRET_KEY: str
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30

    SENDGRID_API_KEY: str
    SENDGRID_FROM_EMAIL: str
    APP_URL: str = "http://localhost:8000"

    class Config:
        env_file = ".env"


settings = Settings()
