from typing import Annotated

from pydantic import BaseModel, BeforeValidator

from app.utils.validators import non_empty_string_validator


class SaveCreateRequestModel(BaseModel):
    name: Annotated[
        str,
        BeforeValidator(non_empty_string_validator),
    ]
