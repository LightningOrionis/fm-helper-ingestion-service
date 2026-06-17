from fastapi import APIRouter

import_router = APIRouter()


@import_router.post("/")
def upload_save():
    raise NotImplementedError


@import_router.delete("/id")
def delete_save():
    raise NotImplementedError
