from confluent_kafka import KafkaError, Message, Producer
from pydantic import BaseModel

from app.config import settings
from app.exceptions.kafka_publish import KafkaPublishError


class KafkaProducer:
    def __init__(self) -> None:
        self._producer = Producer(
            {
                "bootstrap.servers": settings.KAFKA.BOOTSTRAP_SERVERS,
                "client.id": settings.KAFKA.CLIENT_ID,
                "acks": settings.KAFKA.ACKS,
                "request.timeout.ms": settings.KAFKA.REQUEST_TIMEOUT_MS,
                "retry.backoff.ms": settings.KAFKA.RETRY_BACKOFF_MS,
            }
        )

    def publish(
        self,
        topic: str,
        message: BaseModel,
        key: str | None = None,
    ) -> None:
        delivery_error: list[str] = []

        def callback(
            error: KafkaError | None,
            _msg: Message,
        ) -> None:
            if error is not None:
                delivery_error.append(str(error))

        try:
            self._producer.produce(
                topic=topic,
                key=key,
                value=message.model_dump_json(),
                callback=callback,
            )
        except BufferError as exc:
            raise KafkaPublishError("Kafka producer queue is full") from exc

        self._producer.flush()

        if delivery_error:
            raise KafkaPublishError(delivery_error[0])

    def stop(self) -> None:
        self._producer.flush()
