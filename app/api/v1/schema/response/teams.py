from app.api.v1.schema.response.base import TimeStampResponseSchema
from pydantic import BaseModel
from typing import List


class TeamsResponseSchema(TimeStampResponseSchema):
    team_name: str | None


class AllTeamsResponseSchema(BaseModel):
    data: List[TeamsResponseSchema]
    total: int
