from fastapi import APIRouter

from app.schemas.response.healthcheck import HealthcheckResponse

healthcheck_router = APIRouter()


@healthcheck_router.get("/", response_model=HealthcheckResponse)
def healthcheck() -> HealthcheckResponse:
    return HealthcheckResponse(healthcheck="ok")
