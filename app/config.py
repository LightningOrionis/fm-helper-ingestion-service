from pydantic_settings import BaseSettings


class PostgreSQLSettings(BaseSettings):
    POSTGRESQL_URL: str


postgresql_settings = PostgreSQLSettings()
