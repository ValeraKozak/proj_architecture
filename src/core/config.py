from functools import lru_cache

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    app_name: str = "Bulletin Board Platform"
    app_env: str = "development"
    database_url: str = "sqlite:///./bulletin_board.db"
    secret_key: str = "development-only-secret-key"
    access_token_expire_minutes: int = 60
    algorithm: str = "HS256"
    log_level: str = "INFO"

    model_config = SettingsConfigDict(env_file=".env", env_prefix="APP_", extra="ignore")


@lru_cache
def get_settings() -> Settings:
    return Settings()
