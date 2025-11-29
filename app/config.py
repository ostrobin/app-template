"""Application configuration from environment variables."""
from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    """Application settings loaded from environment."""

    # Database
    database_url: str = "postgresql+asyncpg://myapp:password@pgbouncer:5432/myapp"

    # Logging
    log_level: str = "info"
    debug: bool = False

    # Authentik SSO (optional)
    authentik_client_id: str = ""
    authentik_client_secret: str = ""
    authentik_domain: str = ""

    class Config:
        env_file = ".env"
        extra = "ignore"


settings = Settings()
