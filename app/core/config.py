from pydantic_settings.main import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    GITHUB_TOKEN: str
    JWT_SECRET: str = "your-secret-key"
    ENVIRONMENT: str
    DEV_DB_URL: str
    DEV_DB_KEY: str
    PROD_DB_URL: str
    PROD_DB_KEY: str
    GITHUB_USERNAME: str

    model_config = SettingsConfigDict(
        env_file=".env", env_file_encoding="utf-8", extra="ignore"
    )


settings = Settings()
