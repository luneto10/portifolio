from urllib.parse import quote_plus
from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    APP_ENV: str
    GITHUB_TOKEN: str
    GITHUB_USERNAME: str
    MONGO_HOST: str
    MONGO_USERNAME: str
    MONGO_PASSWORD: str
    MONGO_DATABASE: str
    EXTRA_CONNECT_PARAMS: str
    @property
    def MONGO_URI(self) -> str:
        encoded_username = quote_plus(self.MONGO_USERNAME)
        encoded_password = quote_plus(self.MONGO_PASSWORD)
        return (
            f"mongodb+srv://{encoded_username}:{encoded_password}"
            f"@{self.MONGO_HOST}/"
            f"?{self.EXTRA_CONNECT_PARAMS}"
        )
        
    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"


settings = Settings()
