from pydantic_settings import BaseSettings


class PostgreSQLSettings(BaseSettings):
    POSTGRES_URL: str


postgresql_settings = PostgreSQLSettings()
