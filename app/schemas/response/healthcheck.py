from pydantic import BaseModel


class HealthcheckResponse(BaseModel):
    healthcheck: str
