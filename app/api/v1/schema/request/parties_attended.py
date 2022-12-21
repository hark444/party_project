from pydantic.schema import datetime
from pydantic import BaseModel
from app.api.v1.schema.request.base import TimeStampRequestSchema


class PartiesAttendedRequestSchema(TimeStampRequestSchema):
    party_id: int
    rating: float
    comment: str | None = None


class PartyAttendedArgs(BaseModel):
    party_id: str | None = None
    created_by: bool = False
