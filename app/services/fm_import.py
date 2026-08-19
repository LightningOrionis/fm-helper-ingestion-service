import uuid
from pathlib import Path
from typing import BinaryIO

from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.orm import Session

from app.enums.fm_import import ImportUploadStatus
from app.exceptions.import_creation import ImportCreationError
from app.exceptions.item_not_found import ItemNotFoundError
from app.models.fm_import import Import
from app.models.save import Save
from app.repositories.fm_import import ImportRepository
from app.repositories.save import SaveRepository
from app.schemas.request.fm_import import ImportCreateRequestModel
from app.storages.base import BaseStorage


class ImportService:
    def __init__(self) -> None:
        self._import_repository = ImportRepository()
        self._save_repository = SaveRepository()

    def create(
        self,
        db: Session,
        storage: BaseStorage,
        payload: ImportCreateRequestModel,
        file: BinaryIO,
        filename: str,
    ) -> Import:
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

        filename = f"{str(uuid.uuid4())}{Path(filename).suffix.lower()}"
        try:
            path_to_file = storage.upload_file(file, filename)
            params["path_to_file"] = path_to_file
            return self._import_repository.create(db, params)
        except SQLAlchemyError:
            storage.delete_file(filename)
            db.rollback()
            raise ImportCreationError()
        except OSError:
            storage.delete_file(filename)
            raise ImportCreationError()

    def delete(self, db: Session, import_id: int) -> bool:
        result = self._import_repository.delete(db, import_id)
        # TODO: run reversionize

        if not result:
            raise ItemNotFoundError(Import)

        return result
