from app.config import settings
from app.enums.storage import StorageType
from app.storages.base import BaseStorage
from app.storages.local import LocalStorage
from app.utils.validators import FileValidator


def get_storage() -> BaseStorage:
    if settings.STORAGE.LOCATION == StorageType.LOCAL:
        return LocalStorage()

    raise NotImplementedError("S3 Storage is not set up yet.")


def get_file_validator() -> FileValidator:
    return FileValidator()
