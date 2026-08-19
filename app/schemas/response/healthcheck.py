from pydantic import BaseModel


class HealthcheckResponse(BaseModel):
    is_postgres_healthy: bool
    is_kafka_healthy: bool
