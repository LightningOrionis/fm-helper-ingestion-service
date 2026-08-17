from pydantic_settings import BaseSettings, SettingsConfigDict


class PostgreSQLSettings(BaseSettings):
    URL: str

    model_config = SettingsConfigDict(
        env_file=".env",
        env_prefix="POSTGRES_",
        extra="ignore",
    )


class TestPostgreSQLSettings(BaseSettings):
    URL: str

    model_config = SettingsConfigDict(
        env_file=".env",
        env_prefix="TEST_POSTGRES_",
        extra="ignore",
    )


class Settings(BaseSettings):
    POSTGRES: PostgreSQLSettings = PostgreSQLSettings()
    TEST_POSTGRES: TestPostgreSQLSettings = TestPostgreSQLSettings()


settings = Settings()
