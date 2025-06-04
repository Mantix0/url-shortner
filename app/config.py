import os
import random
import string

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    DB_HOST: str = "localhost"
    DB_PORT: int = "5432"
    DB_NAME: str = "link_shortner_db"
    DB_USER: str = "postgres"
    DB_PASSWORD: str = "postgres"
    SECRET_KEY: str = "".join(
        [
            random.choice(string.ascii_letters + string.digits + string.punctuation)
            for n in range(63)
        ]
    )
    ALGORITHM: str = "HS256"
    LINK_EXPIRATION_HOURS: int = 24

    model_config = SettingsConfigDict(
        env_file=os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", ".env")
    )


settings = Settings()


def get_db_url():
    return (
        f"postgresql+asyncpg://{settings.DB_USER}:{settings.DB_PASSWORD}@"
        f"{settings.DB_HOST}:{settings.DB_PORT}/{settings.DB_NAME}"
    )


def get_auth_data():
    return {"secret_key": settings.SECRET_KEY, "algorithm": settings.ALGORITHM}


def get_expiration_hours():
    return settings.LINK_EXPIRATION_HOURS
