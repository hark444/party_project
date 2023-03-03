from pydantic.schema import datetime
from pydantic import BaseModel
from app.api.v1.schema.request.base import TimeStampRequestSchema
from models.notifications import NotificationTypeEnum


class NotificationsBaseSchema(TimeStampRequestSchema):
    is_read: bool | None = False
    expired: bool | None = False


class NotificationCreateSchema(NotificationsBaseSchema):
    user_id: int
    type: NotificationTypeEnum
    type_id: int


class NotificationGetSchema(NotificationsBaseSchema):
    user_id: int | None
    type: NotificationTypeEnum | None
    type_id: int | None
