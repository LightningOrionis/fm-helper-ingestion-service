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


class StorageSettings(BaseSettings):
    LOCATION: str
    FILE_PATH: str
    ALLOWED_FILE_SIZE: int

    model_config = SettingsConfigDict(
        env_file=".env",
        env_prefix="STORAGE_",
        extra="ignore",
    )


class KafkaSettings(BaseSettings):
    BOOTSTRAP_SERVERS: str
    CLIENT_ID: str
    ACKS: str
    REQUEST_TIMEOUT_MS: int
    RETRY_BACKOFF_MS: int

    model_config = SettingsConfigDict(
        env_file=".env",
        env_prefix="KAFKA_",
        extra="ignore",
    )


class Settings(BaseSettings):
    POSTGRES: PostgreSQLSettings = PostgreSQLSettings()  # type: ignore
    TEST_POSTGRES: TestPostgreSQLSettings = TestPostgreSQLSettings()  # type: ignore
    STORAGE: StorageSettings = StorageSettings()  # type: ignore
    KAFKA: KafkaSettings = KafkaSettings()  # type: ignore


settings = Settings()
