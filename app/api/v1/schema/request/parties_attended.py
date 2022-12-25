from pydantic.schema import datetime
from pydantic import BaseModel, validator
from settings.base import env
from app.api.v1.schema.request.base import TimeStampRequestSchema

MAX_PARTY_RATING = env.int("MAX_PARTY_RATING")
MIN_PARTY_RATING = 0


class PartiesAttendedRequestSchema(TimeStampRequestSchema):
    party_id: int
    rating: float
    comment: str | None = None

    @validator("rating")
    def validate_max_rating(cls, v):
        if v > MAX_PARTY_RATING:
            raise ValueError(
                f"Max Party Rating cannot be greater than {MAX_PARTY_RATING}"
            )
        if v < MIN_PARTY_RATING:
            raise ValueError(
                f"Minimum Party Rating cannot be lesser than {MIN_PARTY_RATING}"
            )
        return v


class PartyAttendedArgs(BaseModel):
    party_id: str | None = None
    created_by: bool = False
