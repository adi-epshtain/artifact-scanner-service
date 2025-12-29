from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    app_name: str = "artifact-scanner-service"
    environment: str = "development"

    class Config:
        env_file = ".env"
        case_sensitive = False


settings = Settings()

