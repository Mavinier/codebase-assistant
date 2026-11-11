from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    app_name: str = "Codebase Assistant"
    app_env: str = "development"
    log_level: str = "INFO"

    database_url: str = (
        "postgresql://postgres:postgres@localhost:5432/codebase_assistant"
    )

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore",
    )


settings = Settings()
