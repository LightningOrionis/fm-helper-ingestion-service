from confluent_kafka import KafkaException
from sqlalchemy import text
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.orm import Session

from app.kafka.producer import KafkaProducer
from app.schemas.response.healthcheck import HealthcheckResponse


class HealthcheckService:
    def _healthcheck_postgres(
        self,
        db: Session,
    ) -> bool:
        try:
            db.execute(text("SELECT 1"))
        except SQLAlchemyError:
            return False
        return True

    def _healthcheck_kafka(
        self,
        producer: KafkaProducer,
    ) -> bool:
        try:
            producer.list_topics()
        except KafkaException:
            return False
        return True

    def healthcheck(
        self,
        db: Session,
        producer: KafkaProducer,
    ) -> HealthcheckResponse:
        return HealthcheckResponse(
            is_kafka_healthy=self._healthcheck_kafka(producer),
            is_postgres_healthy=self._healthcheck_postgres(db),
        )
