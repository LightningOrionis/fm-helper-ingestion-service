from pydantic import BaseModel, Field


class SaveCreateRequestModel(BaseModel):
    name: str = Field(min_length=1)
