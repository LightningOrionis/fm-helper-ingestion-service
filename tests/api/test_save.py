from starlette.testclient import TestClient

from tests.protocols import SaveFactory


class TestSaveAPI:

    def test_create_save_success(self, client: TestClient) -> None:
        payload = {"name": "My Save"}
        existence_fields = ["id", "created_at", "updated_at"]

        response = client.post("/save/", json=payload)
        data = response.json()

        assert response.status_code == 201
        assert data["name"] == "My Save"
        for field in existence_fields:
            assert field in data

    def test_create_save_with_empty_name(self, client: TestClient) -> None:
        payload = {"name": ""}
        response = client.post("/save/", json=payload)

        assert response.status_code == 422  # Validation error

    def test_create_save_missing_name(self, client: TestClient) -> None:
        payload: dict = {}
        response = client.post("/save/", json=payload)

        assert response.status_code == 422  # Validation error

    def test_get_save_success(
        self,
        client: TestClient,
        save_factory: SaveFactory,
    ) -> None:
        create_payload = {"name": "Test Save"}
        save = save_factory(**create_payload)

        get_response = client.get(f"/save/{save.id}")
        data = get_response.json()

        assert get_response.status_code == 200
        assert data["id"] == save.id
        assert data["name"] == "Test Save"

    def test_get_save_not_found(self, client: TestClient) -> None:
        response = client.get("/save/999")

        assert response.status_code == 404
        assert response.json()["detail"] == "Save not found"

    def test_list_saves_empty(self, client: TestClient):
        response = client.get("/save/")

        assert response.status_code == 200
        assert response.json() == []

    def test_list_saves_with_data(
        self,
        client: TestClient,
        save_factory: SaveFactory,
    ) -> None:
        names = ["Save 1", "Save 2", "Save 3"]
        created_saves = [save_factory(name) for name in names]

        list_response = client.get("/save/")
        data = list_response.json()
        returned_ids = [item["id"] for item in data]

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

        response = client.get("/save/")
        data = response.json()

        assert len(data) > 0

        first_save = data[0]
        existence_fields = ["id", "name", "created_at", "updated_at"]
        for field in existence_fields:
            assert field in first_save
