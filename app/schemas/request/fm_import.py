from pydantic import BaseModel, Field

from app.enums.fm_import import ImportType


class ImportCreateRequestModel(BaseModel):
    import_type: ImportType

    save_id: int = Field()
