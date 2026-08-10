from sqlalchemy.orm import Session

from app.enums.fm_import import ImportUploadStatus
from app.exceptions.item_not_found import ItemNotFoundError
from app.models.fm_import import Import
from app.models.save import Save
from app.repositories.fm_import import ImportRepository
from app.schemas.request.fm_import import ImportCreateRequestModel
from app.services.save import SaveService


class ImportService:
    def __init__(self):
        self._repository = ImportRepository()

    def create(self, db: Session, model: ImportCreateRequestModel) -> Import:
        save = SaveService().get(db, save_id=model.save_id)
        if not save:
            raise ItemNotFoundError(Save)

        lastest_version = self._repository.get_latest_version_by_save(db, model.save_id, model.import_type) or 0
        current_version = lastest_version + 1

        params = model.model_dump()
        params["version"] = current_version
        params["upload_status"] = ImportUploadStatus.STARTED
        return self._repository.create(db, params)

    def delete(self, db: Session, import_id: int) -> bool:
        result = self._repository.delete(db, import_id)
        # TODO: run reversionize  # noqa

        if not result:
            raise ItemNotFoundError(Import)

        return result
