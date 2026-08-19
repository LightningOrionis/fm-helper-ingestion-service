from confluent_kafka import KafkaError, Message, Producer
from pydantic import BaseModel

from app.exceptions.kafka_publish import KafkaPublishError


class KafkaProducer:
    def __init__(
        self,
        bootstrap_servers: str,
        client_id: str,
        acks: str = "all",
        request_timeout_ms: int = 30_000,
        retry_backoff_ms: int = 100,
    ) -> None:
        self._producer = Producer(
            {
                "bootstrap.servers": bootstrap_servers,
                "client.id": client_id,
                "acks": acks,
                "request.timeout.ms": request_timeout_ms,
                "retry.backoff.ms": retry_backoff_ms,
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
