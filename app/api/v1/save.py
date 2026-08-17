from typing import Annotated

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.dependencies.database import get_db
from app.dependencies.services import get_save_service
from app.schemas.request.save import SaveCreateRequestModel
from app.schemas.response.save import SaveResponseModel
from app.services.save import SaveService

save_router = APIRouter()

DatabaseSession = Annotated[Session, Depends(get_db)]
SaveServiceDependency = Annotated[SaveService, Depends(get_save_service)]


@save_router.post("/", status_code=201, response_model=SaveResponseModel)
def create_save(
    db: DatabaseSession,
    save_service: SaveServiceDependency,
    payload: SaveCreateRequestModel,
) -> SaveResponseModel:
    return save_service.create(db, payload)


@save_router.get("/{save_id}", response_model=SaveResponseModel)
def get_save(
    db: DatabaseSession,
    save_service: SaveServiceDependency,
    save_id: int,
) -> SaveResponseModel:
    return save_service.get(db, save_id)


@save_router.get("/", response_model=list[SaveResponseModel])
def list_saves(
    db: DatabaseSession,
    save_service: SaveServiceDependency,
) -> list[SaveResponseModel]:
    return save_service.list(db)
