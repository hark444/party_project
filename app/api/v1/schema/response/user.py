from pydantic import BaseModel
from ..base import TimestampResponseSchema


class UserResponseSchema(TimestampResponseSchema):
    email: str
    first_name: str | None = None
    last_name: str | None = None
    disabled: bool | None = None
    role: str | None = None

    class Config:
        orm_mode = True


class TokenResponseSchema(BaseModel):
    access_token: str
    token_type: str
