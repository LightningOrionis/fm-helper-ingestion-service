from pydantic_settings import BaseSettings


class PostgreSQLSettings(BaseSettings):
    POSTGRES_URL: str

    class Config:
        env_file = None


def get_postgresql_settings():
    return PostgreSQLSettings()
