"""
Configuration settings for OpenBB Mobile API.
"""
from pydantic_settings import BaseSettings
from functools import lru_cache


class Settings(BaseSettings):
    """Application settings."""

    # API Settings
    APP_NAME: str = "OpenBB Mobile API"
    APP_VERSION: str = "2.0.0"
    API_PREFIX: str = "/api/v2/mobile"

    # CORS Settings
    CORS_ORIGINS: list[str] = ["*"]
    CORS_ALLOW_CREDENTIALS: bool = True
    CORS_ALLOW_METHODS: list[str] = ["*"]
    CORS_ALLOW_HEADERS: list[str] = ["*"]

    # Cache Settings
    REDIS_HOST: str = "localhost"
    REDIS_PORT: int = 6379
    REDIS_DB: int = 0
    REDIS_PASSWORD: str | None = None
    CACHE_ENABLED: bool = True

    # Cache TTL (seconds)
    CACHE_TTL_QUOTE: int = 60  # 1 minute
    CACHE_TTL_SCREENER: int = 900  # 15 minutes
    CACHE_TTL_HISTORICAL: int = 86400  # 24 hours
    CACHE_TTL_PROFILE: int = 604800  # 7 days

    # Pagination
    DEFAULT_PAGE_SIZE: int = 50
    MAX_PAGE_SIZE: int = 200

    # Compression
    GZIP_MIN_SIZE: int = 1000  # bytes

    # OpenBB Settings
    OPENBB_USER_DATA_PATH: str | None = None

    class Config:
        env_file = ".env"
        case_sensitive = True


@lru_cache()
def get_settings() -> Settings:
    """Get cached settings instance."""
    return Settings()


# Export settings
settings = get_settings()
