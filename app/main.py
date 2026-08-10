from fastapi import FastAPI, Request
from starlette.responses import JSONResponse

from app.api.v1 import (
    healthcheck_router,
    import_router,
    save_router,
)
from app.exceptions.item_not_found import ItemNotFoundError

app = FastAPI()
app.include_router(healthcheck_router, prefix="/healthcheck")
app.include_router(import_router, prefix="/import")
app.include_router(save_router, prefix="/save")


@app.exception_handler(ItemNotFoundError)
async def item_not_found_handler(
    request: Request,
    exc: ItemNotFoundError,
):
    return JSONResponse(
        status_code=404,
        content={
            "detail": str(exc),
        },
    )
