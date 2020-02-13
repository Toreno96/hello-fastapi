import os

from pydantic import BaseSettings


class Config(BaseSettings):
    SECRET_KEY: bytes = os.urandom(32)
    SERVER_NAME: str = ""
    SERVER_HOST: str = ""
    BACKEND_CORS_ORIGINS: str
    PROJECT_NAME: str
    SENTRY_DSN: str
    POSTGRES_SERVER: str
    POSTGRES_USER: str
    POSTGRES_PASSWORD: str
    POSTGRES_DB: str

    SMTP_TLS: bool = True
    SMTP_PORT: int = None
    SMTP_HOST: str
    SMTP_USER: str
    SMTP_PASSWORD: str
    EMAILS_FROM_EMAIL: str

    FIRST_SUPERUSER: str
    FIRST_SUPERUSER_PASSWORD: str

    USERS_OPEN_REGISTRATION: bool = False


config = Config()

API_V1_STR = "/api/v1"

ACCESS_TOKEN_EXPIRE_MINUTES = 60 * 24 * 8  # 60 minutes * 24 hours * 8 days = 8 days

SQLALCHEMY_DATABASE_URI = f"postgresql://{config.POSTGRES_USER}:{config.POSTGRES_PASSWORD}@{config.POSTGRES_SERVER}/{config.POSTGRES_DB}"

EMAILS_FROM_NAME = config.PROJECT_NAME
EMAIL_RESET_TOKEN_EXPIRE_HOURS = 48
EMAIL_TEMPLATES_DIR = "/app/app/email-templates/build"
EMAILS_ENABLED = config.SMTP_HOST and config.SMTP_PORT and config.EMAILS_FROM_EMAIL

EMAIL_TEST_USER = "test@example.com"
