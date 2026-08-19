from app.services.fm_import import ImportService
from app.services.healthcheck import HealthcheckService
from app.services.save import SaveService


def get_save_service() -> SaveService:
    return SaveService()


def get_import_service() -> ImportService:
    return ImportService()


def get_healthcheck_service() -> HealthcheckService:
    return HealthcheckService()
