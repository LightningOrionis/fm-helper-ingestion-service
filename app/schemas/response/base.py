from datetime import datetime

from pydantic import BaseModel


class TimeStampedModel(BaseModel):
    created_at: datetime
    updated_at: datetime
