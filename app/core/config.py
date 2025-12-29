from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    app_name: str = "artifact-scanner-service"
    environment: str = "development"
    database_url: str = "sqlite+aiosqlite:///./app.db"

    class Config:
        env_file = ".env"
        case_sensitive = False


settings = Settings()

