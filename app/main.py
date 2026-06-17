from fastapi import FastAPI

from app.api.v1 import (
    healthcheck_router,
    import_router,
)

app = FastAPI()
app.include_router(healthcheck_router, prefix="/healthcheck")
app.include_router(import_router, prefix="/import")
