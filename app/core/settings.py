import os
from pydantic import BaseSettings


class Settings(BaseSettings):
    DEBUG: bool = False
    PROJECT_NAME: str
    PROJECT_SECRET_KEY: str

    API_V1_STR: str = "v1"

    DB_CONN_STRING: str
    DB_PERMISSIONS_SYNC_REQUIRED: bool = False

    JWT_ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int

    DEFAULT_AUTH_URL: str = "/api/v1/auth/login"

    DEFAULT_ADMIN_USERNAME: str = "Admin"
    DEFAULT_ADMIN_PASSWORD: str

    # Максимальное количество попыток входа
    MAX_RETRIES_COUNT: int = 3

    class Config:
        env_file = os.getenv("ENV_FILE")


settings = Settings() # type: ignore
