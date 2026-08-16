from typing import Annotated

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.dependencies.database import get_db
from app.dependencies.services import get_import_service
from app.schemas.request.fm_import import ImportCreateRequestModel
from app.schemas.response.fm_import import ImportResponseModel
from app.services.fm_import import ImportService

import_router = APIRouter()

DatabaseSession = Annotated[Session, Depends(get_db)]
ImportServiceDependency = Annotated[ImportService, Depends(get_import_service)]


@import_router.post("/", status_code=201, response_model=ImportResponseModel)
def upload_import(
    db: DatabaseSession,
    import_service: ImportServiceDependency,
    payload: ImportCreateRequestModel,
) -> ImportResponseModel:
    # TODO: Implement file to local/S3 upload  # noqa
    return import_service.create(db, payload)


@import_router.delete("/{import_id}", status_code=204)
def delete_import(
    db: DatabaseSession,
    import_service: ImportServiceDependency,
    import_id: int,
) -> None:
    import_service.delete(db, import_id)
