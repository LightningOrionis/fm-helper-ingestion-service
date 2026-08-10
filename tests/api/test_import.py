from starlette.testclient import TestClient

from app.enums.fm_import import ImportType, ImportUploadStatus
from tests.protocols import ImportFactory, SaveFactory


class TestImportAPI:

    def test_create_import_success(self, client: TestClient, save_factory: SaveFactory) -> None:
        save = save_factory(name="save1")
        payload = {"import_type": ImportType.SQUAD, "filename": "path/to/file", "save_id": save.id}
        existence_fields = ["id", "upload_date", "import_type", "filename"]

        response = client.post("/import/", json=payload)
        data = response.json()

        assert response.status_code == 201
        assert data["upload_status"] == ImportUploadStatus.STARTED
        assert data["version"] == 1
        assert data["save_id"] == save.id
        for field in existence_fields:
            assert field in data

    def test_create_import_new_version(
        self, client: TestClient, save_factory: SaveFactory, import_factory: ImportFactory
    ) -> None:
        save = save_factory(name="save1")
        import_factory(import_type=ImportType.SQUAD, save_id=save.id, version=1)
        payload = {"import_type": ImportType.SQUAD, "filename": "path/to/file", "save_id": save.id}

        response = client.post("/import/", json=payload)
        data = response.json()

        assert response.status_code == 201
        assert data["version"] == 2
        assert data["save_id"] == save.id

    def test_create_import_version_for_different_import_type(
        self, client: TestClient, save_factory: SaveFactory, import_factory: ImportFactory
    ) -> None:
        save = save_factory(name="save1")
        import_factory(import_type=ImportType.SHORTLIST, save_id=save.id, version=1)
        payload = {"import_type": ImportType.SQUAD, "filename": "path/to/file", "save_id": save.id}

        response = client.post("/import/", json=payload)
        data = response.json()

        assert response.status_code == 201
        assert data["version"] == 1
        assert data["save_id"] == save.id

    def test_create_import_version_for_different_save(
        self, client: TestClient, save_factory: SaveFactory, import_factory: ImportFactory
    ) -> None:
        save_1 = save_factory(name="save1")
        save_2 = save_factory(name="save2")
        import_factory(import_type=ImportType.SQUAD, save_id=save_1.id, version=1)
        payload = {"import_type": ImportType.SQUAD, "filename": "path/to/file", "save_id": save_2.id}

        response = client.post("/import/", json=payload)
        data = response.json()

        assert response.status_code == 201
        assert data["version"] == 1
        assert data["save_id"] == save_2.id

    def test_create_import_save_not_found(self, client: TestClient) -> None:
        payload = {"import_type": ImportType.SQUAD, "filename": "path/to/file", "save_id": 123}

        response = client.post("/import/", json=payload)

        assert response.status_code == 404
        assert response.json()["detail"] == "Save not found"

    def test_delete_import_success(
        self, client: TestClient, save_factory: SaveFactory, import_factory: ImportFactory
    ) -> None:
        save = save_factory(name="save1")
        import_ = import_factory(save_id=save.id)

        response = client.delete(f"/import/{import_.id}/")

        assert response.status_code == 204

    def test_delete_import_failure(self, client: TestClient) -> None:
        response = client.delete("/import/999/")

        assert response.status_code == 404
        assert response.json()["detail"] == "Import not found"
