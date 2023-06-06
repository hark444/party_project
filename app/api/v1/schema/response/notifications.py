from app.api.v1.schema.response.base import TimeStampResponseSchema
from pydantic import BaseModel
from typing import List
from app.api.v1.schema.response.user import UserResponseSchema
from models.notifications import NotificationTypeEnum


class NotificationResponseSchema(TimeStampResponseSchema):
    user: UserResponseSchema
    type: NotificationTypeEnum
    type_id: int
    is_read: bool
    expired: bool


class NotificationsResponseSchema(BaseModel):
    data: List[NotificationResponseSchema]
    total: int
