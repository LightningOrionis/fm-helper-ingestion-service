from typing import Annotated

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.dependencies import get_db
from app.schemas.request.save import SaveCreateRequestModel
from app.services.save import SaveService

save_router = APIRouter()
PostgreSQLSession = Annotated[Session, Depends(get_db)]


@save_router.post("/")
def create_save(
    save_data: SaveCreateRequestModel,
    db: PostgreSQLSession,
):
    SaveService().create(db, save_data)
    # Todo: Return 201


@save_router.get("/{save_id}")
def get_save(
    save_id: int,
    db: PostgreSQLSession,
):
    result = SaveService().get(db, save_id)
    # Todo: Return Response schema + 200


@save_router.get("/")
def list_saves(db: PostgreSQLSession):
    result = SaveService().list(db)
    # Todo: Return Response schema + 200
