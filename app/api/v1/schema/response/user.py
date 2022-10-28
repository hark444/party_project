from pydantic import BaseModel
from app.api.v1.schema.response.base import TimeStampResponseSchema
import datetime


class UserResponseSchema(TimeStampResponseSchema):
    email: str
    first_name: str | None = None
    last_name: str | None = None
    disabled: bool | None = None
    role: str | None = None
    team: str | None = None
    date_of_joining: datetime.date | None = None


class TokenResponseSchema(BaseModel):
    access_token: str
    token_type: str
    username: str
