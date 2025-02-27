from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    APP_ENV: str
    DB_URL: str
    DB_KEY: str
    GITHUB_TOKEN: str
    GITHUB_USERNAME: str
    DATABASE_URL: str

    class Config:
        env_file = ".env"


settings = Settings()
