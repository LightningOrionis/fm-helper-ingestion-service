from typing import Annotated

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.dependencies import get_db

import_router = APIRouter()
PostgreSQLSession = Annotated[Session, Depends(get_db)]


@import_router.get("/")
def some_test(db: PostgreSQLSession):
    raise NotImplementedError


@import_router.post("/")
def upload_save(db: PostgreSQLSession):
    raise NotImplementedError


@import_router.delete("/id")
def delete_save(db: PostgreSQLSession):
    raise NotImplementedError
