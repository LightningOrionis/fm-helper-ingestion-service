from typing import Annotated

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.dependencies import get_db
from app.schemas.request.save import SaveCreateRequestModel
from app.schemas.response.save import SaveResponseModel
from app.services.save import SaveService

save_router = APIRouter()
PostgreSQLSession = Annotated[Session, Depends(get_db)]


@save_router.post("/", status_code=201, response_model=SaveResponseModel)
def create_save(
    db: PostgreSQLSession,
    save_data: SaveCreateRequestModel,
) -> SaveResponseModel:
    return SaveService().create(db, save_data)


@save_router.get("/{save_id}", response_model=SaveResponseModel)
def get_save(
    save_id: int,
    db: PostgreSQLSession,
) -> SaveResponseModel:
    return SaveService().get(db, save_id)


@save_router.get("/", response_model=list[SaveResponseModel])
def list_saves(db: PostgreSQLSession) -> list[SaveResponseModel]:
    return SaveService().list(db)
