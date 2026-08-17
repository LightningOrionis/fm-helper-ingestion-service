from app.services.fm_import import ImportService
from app.services.save import SaveService

save_service = SaveService()
import_service = ImportService()


def get_save_service() -> SaveService:
    return save_service


def get_import_service() -> ImportService:
    return import_service
