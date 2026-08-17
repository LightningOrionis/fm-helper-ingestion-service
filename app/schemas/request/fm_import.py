from typing import Annotated

from pydantic import BaseModel, BeforeValidator, Field

from app.enums.fm_import import ImportType
from app.utils.validators import non_empty_string_validator


class ImportCreateRequestModel(BaseModel):
    import_type: ImportType
    filename: Annotated[
        str,
        BeforeValidator(non_empty_string_validator),
    ]
    save_id: int = Field(gt=0)
