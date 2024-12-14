from pydantic import SecretStr
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file='.env', env_file_encoding='utf-8', extra='allow'
    )

    DATABASE_URL: str
    LANGCHAIN_TRACING_V2: bool
    LANGCHAIN_ENDPOINT: str
    LANGCHAIN_API_KEY: SecretStr
    LANGCHAIN_PROJECT: str
    COHERE_API_KEY: SecretStr


def get_settings():
    return Settings()  # type: ignore
