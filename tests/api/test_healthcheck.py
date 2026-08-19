import pytest
from confluent_kafka import KafkaException
from pytest_mock import MockerFixture
from sqlalchemy.exc import SQLAlchemyError
from starlette.testclient import TestClient


class TestHealthCheckAPI:
    def test_healthcheck_ok(
        self,
        client: TestClient,
    ) -> None:
        response = client.get("/healthcheck")
        data = response.json()

        assert len(data) == 2
        assert data["is_postgres_healthy"]
        assert data["is_kafka_healthy"]

    @pytest.mark.parametrize(
        "mocked_object, side_effect, response_pair",
        [
            ("sqlalchemy.orm.Session.execute", SQLAlchemyError, (True, False)),
            ("app.kafka.producer.KafkaProducer.list_topics", KafkaException, (False, True)),
        ],
    )
    def test_healthcheck_fail(
        self,
        client: TestClient,
        mocker: MockerFixture,
        mocked_object: str,
        side_effect: type,
        response_pair: tuple[bool, bool],
    ) -> None:
        error_mock = mocker.patch(mocked_object, side_effect=side_effect())

        response = client.get("/healthcheck")
        data = response.json()
        is_kafka_healthy = data["is_kafka_healthy"]
        is_postgres_healthy = data["is_postgres_healthy"]

        assert response.status_code == 200
        assert (is_kafka_healthy, is_postgres_healthy) == response_pair

        error_mock.assert_called_once()
