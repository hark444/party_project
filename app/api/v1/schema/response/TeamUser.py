from app.api.v1.schema.response.base import TimeStampResponseSchema
from pydantic import BaseModel
from typing import List
from app.api.v1.schema.response.user import UserResponseSchema
from app.api.v1.schema.response.teams import TeamsResponseSchema


class TeamUserResponseSchema(TimeStampResponseSchema):
    user: UserResponseSchema
    team: TeamsResponseSchema
    requested_by: UserResponseSchema
    uuid: str
    subscribed: bool
    deleted: bool
