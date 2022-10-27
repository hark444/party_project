from pydantic import BaseModel
from typing import Optional
import datetime
from app.api.v1.schema.request.base import TimeStampRequestSchema


class UserRequestSchema(TimeStampRequestSchema):
    password: str
    email: str
    first_name: str = None
    last_name: str = None
    disabled: bool = False
    team: str = None
    date_of_joining: datetime.date = None
