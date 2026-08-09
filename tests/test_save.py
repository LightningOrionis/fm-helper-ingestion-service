class TestSaveEndpoints:

    def test_create_save_success(self, client):
        payload = {"name": "My Save"}
        response = client.post("/save/", json=payload)
        data = response.json()
        existence_fields = ["id", "created_at", "updated_at"]

        assert response.status_code == 201
        assert data["name"] == "My Save"
        for field in existence_fields:
            assert field in data

    def test_create_save_with_empty_name(self, client):
        payload = {"name": ""}
        response = client.post("/save/", json=payload)

        assert response.status_code == 422  # Validation error

    def test_create_save_missing_name(self, client):
        payload = {}
        response = client.post("/save/", json=payload)

        assert response.status_code == 422  # Validation error

    def test_get_save_success(self, client):
        create_payload = {"name": "Test Save"}
        create_response = client.post("/save/", json=create_payload)
        save_id = create_response.json()["id"]

        get_response = client.get(f"/save/{save_id}")
        data = get_response.json()

        assert get_response.status_code == 200
        assert data["id"] == save_id
        assert data["name"] == "Test Save"

    def test_get_save_not_found(self, client):
        response = client.get("/save/999")

        assert response.status_code == 404
        assert "Save not found" in response.json()["detail"]

    def test_list_saves_empty(self, client):
        response = client.get("/save/")

        assert response.status_code == 200
        assert response.json() == []

    def test_list_saves_with_data(self, client):
        names = ["Save 1", "Save 2", "Save 3"]
        created_ids = []

        for name in names:
            payload = {"name": name}
            response = client.post("/save/", json=payload)
            created_ids.append(response.json()["id"])

        list_response = client.get("/save/")
        data = list_response.json()
        returned_ids = [item["id"] for item in data]

        assert list_response.status_code == 200
        assert len(data) == 3
        for save_id in created_ids:
            assert save_id in returned_ids

    def test_list_saves_contains_all_fields(self, client):
        payload = {"name": "Full Info Save"}
        client.post("/save/", json=payload)

        response = client.get("/save/")
        data = response.json()

        assert len(data) > 0

        first_save = data[0]
        existence_fields = ["id", "name", "created_at", "updated_at"]
        for field in existence_fields:
            assert field in first_save
