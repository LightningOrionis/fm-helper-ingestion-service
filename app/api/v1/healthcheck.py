from typing import Annotated

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.dependencies.database import get_db
from app.dependencies.kafka import get_kafka_producer
from app.dependencies.service import get_healthcheck_service
from app.kafka.producer import KafkaProducer
from app.schemas.response.healthcheck import HealthcheckResponse
from app.services.healthcheck import HealthcheckService

healthcheck_router = APIRouter()

DatabaseSession = Annotated[Session, Depends(get_db)]
HealthcheckServiceDependency = Annotated[HealthcheckService, Depends(get_healthcheck_service)]
KafkaProducerDependency = Annotated[KafkaProducer, Depends(get_kafka_producer)]


@healthcheck_router.get("/", response_model=HealthcheckResponse)
def healthcheck(
    db: DatabaseSession,
    kafka_producer: KafkaProducer,
    healthcheck_service: HealthcheckServiceDependency,
) -> HealthcheckResponse:
    return healthcheck_service.healthcheck(db, kafka_producer)
