from pydantic import BaseModel
from ..base import TimeStampResponseSchema


class UserResponseSchema(TimeStampResponseSchema):
    email: str
    first_name: str | None = None
    last_name: str | None = None
    disabled: bool | None = None
    role: str | None = None


class TokenResponseSchema(BaseModel):
    access_token: str
    token_type: str
