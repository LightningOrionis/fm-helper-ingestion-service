from app.enums.fm_import import ImportType, ImportUploadStatus
from app.schemas.response.base import TimeStampedModel


class ImportResponseModel(TimeStampedModel):
    id: int
    version: int
    upload_status: ImportUploadStatus
    import_type: ImportType
    filename: str
    save_id: int

    model_config = {"from_attributes": True}