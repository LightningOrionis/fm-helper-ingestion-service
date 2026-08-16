from sqlalchemy.orm import Session

from app.enums.fm_import import ImportUploadStatus
from app.exceptions.item_not_found import ItemNotFoundError
from app.models.fm_import import Import
from app.models.save import Save
from app.repositories.fm_import import ImportRepository
from app.repositories.save import SaveRepository
from app.schemas.request.fm_import import ImportCreateRequestModel


class ImportService:
    def __init__(self) -> None:
        self._import_repository = ImportRepository()
        self._save_repository = SaveRepository()

    def create(self, db: Session, payload: ImportCreateRequestModel) -> Import:
        save = self._save_repository.get_by_id(db, payload.save_id)
        if not save:
            raise ItemNotFoundError(Save)

        latest_version = (
            self._import_repository.get_latest_version_by_save(db, payload.save_id, payload.import_type) or 0
        )
        current_version = latest_version + 1

        params = payload.model_dump()
        params["version"] = current_version
        params["upload_status"] = ImportUploadStatus.STARTED

        return self._import_repository.create(db, params)

    def delete(self, db: Session, import_id: int) -> bool:
        result = self._import_repository.delete(db, import_id)
        # TODO: run reversionize  # noqa

        if not result:
            raise ItemNotFoundError(Import)

        return result
