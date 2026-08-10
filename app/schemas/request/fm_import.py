from pydantic import BaseModel

from app.enums.fm_import import ImportType


class ImportCreateRequestModel(BaseModel):
    version: int | None
    import_type: ImportType
    filename: str
    save_id: int
