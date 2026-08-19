from fastapi import Request

from app.kafka.producer import KafkaProducer


def get_kafka_producer(request: Request) -> KafkaProducer:
    return request.app.state.kafka_producer
