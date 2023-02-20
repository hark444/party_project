from pydantic import BaseModel
from app.api.v1.schema.response.base import TimeStampResponseSchema
from pydantic.schema import date
from app.api.v1.schema.response.teams import TeamsResponseSchema


class UserResponseSchema(TimeStampResponseSchema):
    email: str
    first_name: str | None = None
    last_name: str | None = None
    disabled: bool | None = None
    role: str | None = None
    team_id: int | None = None
    team: TeamsResponseSchema | None = None
    date_of_joining: date | None = None


class TokenResponseSchema(BaseModel):
    access_token: str
    token_type: str
    username: str | None = None
