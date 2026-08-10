from typing import Annotated

from fastapi import APIRouter, Depends, Response
from sqlalchemy.orm import Session

from app.dependencies import get_db
from app.schemas.request.fm_import import ImportCreateRequestModel
from app.schemas.response.fm_import import ImportResponseModel
from app.services.fm_import import ImportService

import_router = APIRouter()
PostgreSQLSession = Annotated[Session, Depends(get_db)]


@import_router.post("/", status_code=201, response_model=ImportResponseModel)
def upload_import(
    db: PostgreSQLSession,
    import_data: ImportCreateRequestModel,
) -> ImportResponseModel:
    # TODO: Implement file to local/S3 upload  # noqa
    return ImportService().create(db, import_data)


@import_router.delete("/{import_id}")
def delete_import(
    db: PostgreSQLSession,
    import_id: int,
) -> Response:
    ImportService().delete(db, import_id)

    return Response(status_code=204)
