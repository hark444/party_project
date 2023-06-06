from pydantic.schema import datetime
from pydantic import BaseModel
from app.api.v1.schema.request.base import TimeStampRequestSchema


class PartyRequestCreateSchema(TimeStampRequestSchema):
    reason: str = None
    proposed_date: datetime
    guests_invited: int
    party_date: datetime | None = None
    party_place: str | None = None


class PartyRequestSchema(PartyRequestCreateSchema):
    ratings: float = 0.0
    approved: bool = False


class AllPartyRequestSchema(BaseModel):
    created_by: str | None = None
    party_year: str | None = None
