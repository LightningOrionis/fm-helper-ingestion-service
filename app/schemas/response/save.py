from app.schemas.response.base import TimeStampedModel


class SaveResponseModel(TimeStampedModel):
    id: int
    name: str

    model_config = {"from_attributes": True}
