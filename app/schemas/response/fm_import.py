from datetime import datetime

from pydantic import BaseModel

from app.enums.fm_import import ImportType, ImportUploadStatus


class ImportResponseModel(BaseModel):
    id: int
    version: int
    upload_date: datetime
    upload_status: ImportUploadStatus
    import_type: ImportType
    filename: str
    save_id: int
