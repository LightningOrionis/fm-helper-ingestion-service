from pathlib import Path
from uuid import UUID

import pytest
from pytest_mock import MockerFixture
from sqlalchemy.exc import SQLAlchemyError
from starlette.testclient import TestClient

from app.config import settings
from app.enums.fm_import import ImportType, ImportUploadStatus
from tests.protocols import FileFactory, ImportFactory, SaveFactory


class TestImportAPI:

    def test_create_import_success(
        self,
        client: TestClient,
        save_factory: SaveFactory,
        file_factory: FileFactory,
    ) -> None:
        save = save_factory(name="save1")
        file = file_factory("file.xls", "application/vnd.ms-excel")
        payload = {"import_type": ImportType.SQUAD.value, "save_id": str(save.id)}
        existence_fields = ["id", "import_type"]

        response = client.post("/api/v1/import/", data=payload, files=file)
        data = response.json()
        path = Path(data["path_to_file"])

        assert response.status_code == 201
        assert data["upload_status"] == ImportUploadStatus.STARTED
        assert data["version"] == 1
        assert data["save_id"] == save.id
        assert str(path.parent) == settings.STORAGE.FILE_PATH
        assert UUID(path.stem).version == 4
        assert path.exists()

        for field in existence_fields:
            assert field in data

        path.unlink()

    @pytest.mark.parametrize(
        "filename, filetype, status_code",
        [
            ("file.xls", "application/vnd.ms-excel", 201),
            ("file.xlsx", "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet", 201),
            ("file.csv", "text/csv", 201),
            ("file.txt", "text/plain", 422),
        ],
    )
    def test_create_import_filetypes(
        self,
        client: TestClient,
        save_factory: SaveFactory,
        file_factory: FileFactory,
        filename: str,
        filetype: str,
        status_code: int,
    ) -> None:
        save = save_factory(name="save1")
        file = file_factory(filename, filetype)
        payload = {"import_type": ImportType.SQUAD.value, "save_id": str(save.id)}

        response = client.post("/api/v1/import/", data=payload, files=file)

        assert response.status_code == status_code

        if response.status_code == 201:
            path = Path(response.json()["path_to_file"])
            path.unlink(missing_ok=True)

    @pytest.mark.parametrize(
        "import_type, expected_version",
        [
            (ImportType.SQUAD, 2),
            (ImportType.SHORTLIST, 1),
        ],
    )
    def test_create_import_new_version(
        self,
        client: TestClient,
        save_factory: SaveFactory,
        import_factory: ImportFactory,
        file_factory: FileFactory,
        import_type: ImportType,
        expected_version: int,
    ) -> None:
        save = save_factory(name="save1")
        import_factory(import_type=ImportType.SQUAD, save_id=save.id, version=1)
        file = file_factory("file.xls", "application/vnd.ms-excel")
        payload = {"import_type": import_type.value, "save_id": str(save.id)}

        response = client.post("/api/v1/import/", data=payload, files=file)
        data = response.json()

        assert response.status_code == 201
        assert data["version"] == expected_version

        path = Path(response.json()["path_to_file"])
        path.unlink()

    def test_create_import_version_for_different_save(
        self,
        client: TestClient,
        save_factory: SaveFactory,
        import_factory: ImportFactory,
        file_factory: FileFactory,
    ) -> None:
        save_1 = save_factory(name="save1")
        save_2 = save_factory(name="save2")
        import_factory(import_type=ImportType.SQUAD, save_id=save_1.id, version=1)
        file = file_factory("file.xls", "application/vnd.ms-excel")
        payload = {"import_type": ImportType.SQUAD.value, "save_id": str(save_2.id)}

        response = client.post("/api/v1/import/", data=payload, files=file)
        data = response.json()

        assert response.status_code == 201
        assert data["version"] == 1
        assert data["save_id"] == save_2.id

        path = Path(response.json()["path_to_file"])
        path.unlink()

    def test_create_import_version_with_gap(
        self,
        client: TestClient,
        save_factory: SaveFactory,
        import_factory: ImportFactory,
        file_factory: FileFactory,
    ) -> None:
        save_1 = save_factory(name="save1")
        import_factory(import_type=ImportType.SQUAD, save_id=save_1.id, version=1)
        import_factory(import_type=ImportType.SQUAD, save_id=save_1.id, version=3)
        file = file_factory("file.xls", "application/vnd.ms-excel")
        payload = {"import_type": ImportType.SQUAD.value, "save_id": str(save_1.id)}

        response = client.post("/api/v1/import/", data=payload, files=file)
        data = response.json()

        assert response.status_code == 201
        assert data["version"] == 4
        assert data["save_id"] == save_1.id

        path = Path(response.json()["path_to_file"])
        path.unlink()

    def test_create_import_save_not_found(
        self,
        client: TestClient,
        file_factory: FileFactory,
    ) -> None:
        file = file_factory("file.xls", "application/vnd.ms-excel")
        payload = {"import_type": ImportType.SQUAD.value, "save_id": "123"}

        response = client.post("/api/v1/import/", data=payload, files=file)
        possible_path_to_file = Path(settings.STORAGE.FILE_PATH) / "file.xls"

        assert response.status_code == 404
        assert response.json()["detail"] == "Save not found"
        assert not possible_path_to_file.exists()

    @pytest.mark.parametrize(
        "mocked_method, exception",
        [
            ("app.storages.local.LocalStorage.upload_file", OSError),
            ("app.repositories.fm_import.ImportRepository.create", SQLAlchemyError),
        ],
    )
    def test_create_import_os_error(
        self,
        client: TestClient,
        save_factory: SaveFactory,
        file_factory: FileFactory,
        mocker: MockerFixture,
        mocked_method: str,
        exception: type,
    ) -> None:
        error_mock = mocker.patch(mocked_method, side_effect=exception())

        save = save_factory(name="save1")
        file = file_factory("file.xls", "application/vnd.ms-excel")
        payload = {"import_type": ImportType.SQUAD.value, "save_id": str(save.id)}

        response = client.post("/api/v1/import/", data=payload, files=file)

        assert response.status_code == 503
        assert response.json()["detail"] == "Failed to create import"
        error_mock.asser_called_with()

    def test_delete_import_success(
        self,
        client: TestClient,
        save_factory: SaveFactory,
        import_factory: ImportFactory,
    ) -> None:
        save = save_factory(name="save1")
        import_ = import_factory(save_id=save.id)

        response = client.delete(f"/api/v1/import/{import_.id}/")

        assert response.status_code == 204

    def test_delete_import_failure(
        self,
        client: TestClient,
    ) -> None:
        response = client.delete("/api/v1/import/999/")

        assert response.status_code == 404
        assert response.json()["detail"] == "Import not found"
