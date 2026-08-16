from pydantic_settings import BaseSettings


class PostgreSQLSettings(BaseSettings):
    POSTGRES_URL: str


POSTGRES_SETTINGS = PostgreSQLSettings()
