from pydantic.schema import datetime
from pydantic import BaseModel
from app.api.v1.schema.request.base import TimeStampRequestSchema
from models.notifications import NotificationTypeEnum


class NotificationCreateSchema(TimeStampRequestSchema):
    user_id: int
    type: NotificationTypeEnum
    is_read: bool | None = False
    expired: bool | None = False
