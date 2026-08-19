from typing import Annotated

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.dependencies.database import get_db
from app.dependencies.service import get_save_service
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
    save = save_service.create(db, payload)
    return SaveResponseModel.model_validate(save)


@save_router.get("/{save_id}", response_model=SaveResponseModel)
def get_save(
    db: DatabaseSession,
    save_service: SaveServiceDependency,
    save_id: int,
) -> SaveResponseModel:
    save = save_service.get(db, save_id)
    return SaveResponseModel.model_validate(save)


@save_router.get("/", response_model=list[SaveResponseModel])
def list_saves(
    db: DatabaseSession,
    save_service: SaveServiceDependency,
) -> list[SaveResponseModel]:
    saves = save_service.list(db)
    return [SaveResponseModel.model_validate(save) for save in saves]
