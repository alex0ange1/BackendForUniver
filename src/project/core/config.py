#данный файл должен храниться в удаленном месте и хорошо защищенном месте, доступ к нему никто не должен иметь

from pydantic_settings import BaseSettings
from pydantic import SecretStr


class Settings(BaseSettings):
    # TODO убрать значения по умолчанию при переносе приложения в Docker
    ORIGINS: str = "*"
    ROOT_PATH: str = ""
    ENV: str = "DEV"
    LOG_LEVEL: str = "DEBUG"

    POSTGRES_SCHEMA: str = "my_app_schema"
    POSTGRES_HOST: str = "localhost"
    POSTGRES_DB: str = "postgres"
    POSTGRES_PORT: int = 5433
    POSTGRES_USER: SecretStr = "postgres"
    POSTGRES_PASSWORD: SecretStr = "postgres"
    POSTGRES_RECONNECT_INTERVAL_SEC: int = 1

    JWT_SECRET_KEY: SecretStr = "s3cR3t k3y!@#2024$%^&*()_+1234567890abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30
    HASH_ALGORITHM: str = "HS256"
    SECRET_AUTH_KEY: SecretStr = "b46ca661ab495dbfe4d7a9346bb328f8f1c358e92fe468faee4cec6bca06c6b1"
    AUTH_ALGORITHM: str = "HS256"

    @property
    def postgres_url(self) -> str:
        creds = f"{self.POSTGRES_USER.get_secret_value()}:{self.POSTGRES_PASSWORD.get_secret_value()}"
        return f"postgresql+asyncpg://{creds}@{self.POSTGRES_HOST}:{self.POSTGRES_PORT}/{self.POSTGRES_DB}"


settings = Settings()