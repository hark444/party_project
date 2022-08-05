from pydantic import BaseModel
from datetime import datetime


class TimestampResponseSchema(BaseModel):
    id: int
    created_on: datetime | None = datetime.now()
    last_modified_on: datetime | None = None
