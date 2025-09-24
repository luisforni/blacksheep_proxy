from pydantic_settings import BaseSettings
from pydantic import AnyUrl

class Settings(BaseSettings):
    APP_NAME: str = "proxy-gw"
    DEBUG: bool = False

    JWT_SECRET: str
    JWT_EXPIRES_MIN: int = 60

    UPSTREAM_BASE_URL: AnyUrl
    FORWARD_AUTHORIZATION: bool = True
    TIMEOUT_SECONDS: float = 15
    RETRY_ATTEMPTS: int = 2
    RETRY_BACKOFF: float = 0.25

    CORS_ALLOW_ORIGINS: str = "*"
    CORS_ALLOW_HEADERS: str = "*"
    CORS_ALLOW_METHODS: str = "*"

    model_config = {"env_file": ".env"}

settings = Settings()
