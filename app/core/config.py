from pydantic_settings import BaseSettings
from functools import lru_cache


class Settings(BaseSettings):
    # Database settings
    DB_HOST: str = "stress-prueba1.cna4icyokmxm.us-east-2.rds.amazonaws.com"
    DB_USER: str = "admin1"
    DB_PASSWORD: str = "stressminderprueba1"
    DB_NAME: str = "sensores_db"
    DB_PORT: int = 3306

    # API Settings
    API_V1_STR: str = "/api/v1"
    PROJECT_NAME: str = "StressMinder API"

    # Security
    SECRET_KEY: str = "your-secret-key-here"  # TODO: Change in production
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60 * 24 * 8  # 8 days

    @property
    def ASYNC_DATABASE_URL(self) -> str:
        return f"mysql+aiomysql://{self.DB_USER}:{self.DB_PASSWORD}@{self.DB_HOST}:{self.DB_PORT}/{self.DB_NAME}"

    class Config:
        case_sensitive = True


@lru_cache()
def get_settings() -> Settings:
    return Settings()
