import pytest
from starlette.testclient import TestClient

from tests.protocols import SaveFactory


class TestSaveAPI:

    @pytest.mark.parametrize(
        "payload, expected_name",
        [
            ({"name": "save"}, "save"),
            ({"name": " save "}, "save"),
        ],
    )
    def test_create_save_success(
        self,
        client: TestClient,
        payload: dict[str, str],
        expected_name: str,
    ) -> None:
        existence_fields = ["id", "created_at", "updated_at"]

        response = client.post("/api/v1/save/", json=payload)
        data = response.json()

        assert response.status_code == 201
        assert data["name"] == expected_name
        for field in existence_fields:
            assert field in data

    @pytest.mark.parametrize(
        "payload",
        [{}, {"name": ""}, {"name": "  "}],
    )
    def test_create_save_failed(
        self,
        client: TestClient,
        payload: dict[str, str],
    ) -> None:
        response = client.post("/api/v1/save/", json=payload)

        assert response.status_code == 422

    def test_get_save_success(
        self,
        client: TestClient,
        save_factory: SaveFactory,
    ) -> None:
        create_payload = {"name": "save"}
        save = save_factory(**create_payload)

        get_response = client.get(f"/api/v1/save/{save.id}")
        data = get_response.json()

        assert get_response.status_code == 200
        assert data["id"] == save.id
        assert data["name"] == create_payload["name"]

    def test_get_save_not_found(
        self,
        client: TestClient,
    ) -> None:
        response = client.get("/api/v1/save/999")

        assert response.status_code == 404
        assert response.json()["detail"] == "Save not found"

    def test_list_saves_empty(
        self,
        client: TestClient,
    ) -> None:
        response = client.get("/api/v1/save/")

        assert response.status_code == 200
        assert response.json() == []

    def test_list_saves_with_data(
        self,
        client: TestClient,
        save_factory: SaveFactory,
    ) -> None:
        names = ["Save 1", "Save 2", "Save 3"]
        created_saves = [save_factory(name) for name in names]

        list_response = client.get("/api/v1/save/")
        data = list_response.json()
        returned_ids = {item["id"] for item in data}

        assert list_response.status_code == 200
        assert len(data) == 3
        for save in created_saves:
            assert save.id in returned_ids

    def test_list_saves_contains_all_fields(
        self,
        client: TestClient,
        save_factory: SaveFactory,
    ) -> None:
        payload = {"name": "Full Info Save"}
        save_factory(**payload)

        response = client.get("/api/v1/save/")
        data = response.json()

        assert len(data) > 0

        first_save = data[0]
        existence_fields = {"id", "name", "created_at", "updated_at"}
        for field in existence_fields:
            assert field in first_save
