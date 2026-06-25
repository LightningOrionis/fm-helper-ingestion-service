from pydantic import BaseModel


class SaveCreateRequestModel(BaseModel):
    name: str
