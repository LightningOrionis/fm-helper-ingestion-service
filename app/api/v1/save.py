from fastapi import APIRouter

save_router = APIRouter()

@save_router.post("/")
def create_save():
    pass


@save_router.get("/id")
def get_save_by_id():
    pass


@save_router.get("/")
def get_all_saves():
    pass
