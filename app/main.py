from contextlib import asynccontextmanager

from fastapi import APIRouter, FastAPI, Request
from starlette.responses import JSONResponse

from app.api.v1 import (
    healthcheck_router,
    import_router,
    save_router,
)
from app.exceptions.import_creation import ImportCreationError
from app.exceptions.incorrect_file import IncorrectFileError
from app.exceptions.item_not_found import ItemNotFoundError
from app.kafka.producer import KafkaProducer


@asynccontextmanager
async def lifespan(app: FastAPI):
    producer = KafkaProducer()
    app.state.kafka_producer = producer

    try:
        yield
    finally:
        producer.stop()


api_v1_router = APIRouter(prefix="/api/v1")
api_v1_router.include_router(import_router, prefix="/import")
api_v1_router.include_router(save_router, prefix="/save")

app = FastAPI(lifespan=lifespan)
app.include_router(api_v1_router)
app.include_router(healthcheck_router, prefix="/healthcheck")


@app.exception_handler(ItemNotFoundError)
async def item_not_found_handler(
    request: Request,
    exc: ItemNotFoundError,
) -> JSONResponse:
    return JSONResponse(
        status_code=404,
        content={
            "detail": str(exc),
        },
    )


@app.exception_handler(IncorrectFileError)
async def incorrect_file_error_handler(
    request: Request,
    exc: IncorrectFileError,
) -> JSONResponse:
    return JSONResponse(
        status_code=422,
        content={
            "detail": str(exc),
        },
    )


@app.exception_handler(ImportCreationError)
async def import_error_handler(
    request: Request,
    exc: ImportCreationError,
) -> JSONResponse:
    return JSONResponse(
        status_code=503,
        content={
            "detail": str(exc),
        },
    )
