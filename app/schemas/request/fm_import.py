from typing import Annotated

from pydantic import BaseModel, Field, StringConstraints

from app.enums.fm_import import ImportType


class ImportCreateRequestModel(BaseModel):
    import_type: ImportType
    filename: Annotated[
        str,
        StringConstraints(strip_whitespace=True, min_length=1),
    ]
    save_id: int = Field(gt=0)
