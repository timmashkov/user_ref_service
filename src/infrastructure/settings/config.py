from pydantic_settings import BaseSettings
from dotenv import load_dotenv

import os

load_dotenv()


class ServerConfig(BaseSettings):
    DB_HOST: str = os.getenv("DB_HOST")
    DB_PORT: int = os.getenv("DB_PORT")
    DB_NAME: str = os.getenv("DB_HOST")
    DB_USER: str = os.getenv("DB_NAME")
    DB_PASS: str = os.getenv("DB_PASS")

    @property
    def get_db_url(self):
        return f"postgresql+asyncpg://{self.DB_USER}:{self.DB_PASS}@{self.DB_HOST}:{self.DB_PORT}/{self.DB_NAME}"

    echo: bool = False

    SECRET_KEY: str = os.getenv("SECRET_KEY")
    X_API_TOKEN: str = os.getenv("X_API_TOKEN")

    REDIS_HOST: str = os.getenv("REDIS_HOST")
    REDIS_PORT: str = os.getenv("REDIS_PORT")
    EXPIRATION: int = 60

    @property
    def get_redis_url(self):
        return f"redis://{self.REDIS_HOST}:{self.REDIS_PORT}"

    GOOGLE_PASS: str = os.getenv("GOOGLE_PASS")
    MAIL_FROM: str = os.getenv("MAIL_FROM")

    class Config:
        env_file = ".env"


base_config = ServerConfig()
