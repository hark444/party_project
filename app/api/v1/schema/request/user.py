from pydantic import BaseModel, validator
from typing import Optional
from pydantic.schema import datetime
from app.api.v1.schema.request.base import TimeStampRequestSchema
from models import get_db
from models.user import UserModel
from pydantic import BaseModel


class TokenGenerateSchema(BaseModel):
    email: str
    password: str


class UserRequestSchema(TimeStampRequestSchema):
    first_name: str = None
    last_name: str = None
    disabled: bool = False
    team_id: int = None
    date_of_joining: datetime = None


class UserRequestPostSchema(UserRequestSchema, TokenGenerateSchema):
    @validator("email")
    def validate_email_uniqueness(cls, v):
        db = next(get_db())
        user_obj = db.query(UserModel).filter_by(email=v).first()
        if user_obj:
            raise ValueError(
                f"A user with the same email already exists. "
                f"Please try to login or create a user with a different email"
            )
        return v
