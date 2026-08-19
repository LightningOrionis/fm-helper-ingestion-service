from typing import Annotated

from fastapi import APIRouter, Depends, File, Form, UploadFile
from sqlalchemy.orm import Session

from app.dependencies.database import get_db
from app.dependencies.file import get_file_validator, get_storage
from app.dependencies.service import get_import_service
from app.enums.fm_import import ImportType
from app.schemas.request.fm_import import ImportCreateRequestModel
from app.schemas.response.fm_import import ImportResponseModel
from app.services.fm_import import ImportService
from app.storages.base import BaseStorage
from app.utils.validators import FileValidator

import_router = APIRouter()

DatabaseSession = Annotated[Session, Depends(get_db)]
ImportServiceDependency = Annotated[ImportService, Depends(get_import_service)]
FileStorage = Annotated[BaseStorage, Depends(get_storage)]
FileValidatorDependency = Annotated[FileValidator, Depends(get_file_validator)]


@import_router.post("/", status_code=201, response_model=ImportResponseModel)
def upload_import(
    db: DatabaseSession,
    import_service: ImportServiceDependency,
    storage: FileStorage,
    file_validator: FileValidatorDependency,
    import_type: Annotated[ImportType, Form()],
    save_id: Annotated[int, Form()],
    file: UploadFile = File(...),
) -> ImportResponseModel:
    filename = file_validator.validate(file)
    payload = ImportCreateRequestModel(
        save_id=save_id,
        import_type=import_type,
    )

    import_ = import_service.create(db, storage, payload, file.file, filename)

    return ImportResponseModel.model_validate(import_)


@import_router.delete("/{import_id}", status_code=204)
def delete_import(
    db: DatabaseSession,
    import_service: ImportServiceDependency,
    import_id: int,
) -> None:
    import_service.delete(db, import_id)
