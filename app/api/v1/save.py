from fastapi import APIRouter

save_router = APIRouter()


@save_router.post("/")
def create_save():
    raise NotImplementedError


@save_router.get("/id")
def get_save_by_id():
    raise NotImplementedError


@save_router.get("/")
def get_all_saves():
    raise NotImplementedError
