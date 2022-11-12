from pydantic import BaseModel, validator
from typing import Optional
from pydantic.schema import date
from app.api.v1.schema.request.base import TimeStampRequestSchema
from models import get_db
from models.user import UserModel


class UserRequestSchema(TimeStampRequestSchema):
    password: str
    email: str
    first_name: str = None
    last_name: str = None
    disabled: bool = False
    team: str = None
    date_of_joining: date = None

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
