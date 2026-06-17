from fastapi import APIRouter, Response

healthcheck_router = APIRouter()

@healthcheck_router.get("/")
def healthcheck():
    return {"healthcheck": "ok"}
