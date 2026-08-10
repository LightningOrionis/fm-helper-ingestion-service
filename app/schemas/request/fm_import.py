from pydantic import BaseModel

from app.enums.fm_import import ImportType


class ImportCreateRequestModel(BaseModel):
    import_type: ImportType
    filename: str
    save_id: int
