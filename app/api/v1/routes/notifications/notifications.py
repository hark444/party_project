from fastapi import Depends, APIRouter, HTTPException, status, Path
from models import get_db
from sqlalchemy.orm import Session
from models.user import UserModel
from models.TeamUser import TeamUserModel
from models.teams import TeamsModel
from app.api.v1.routes.user.auth import get_current_user
from app.api.v1.schema.response.user import UserResponseSchema
from models.notifications import Notifications
from app.api.v1.schema.request.notifications import NotificationCreateSchema
from app.api.v1.schema.response.notifications import (
    NotificationResponseSchema,
    NotificationsResponseSchema,
)


notifications_router = APIRouter(prefix="/notifications", tags=["notifications"])


@notifications_router.post("", response_model=NotificationResponseSchema)
async def create_notifications(
    notification: NotificationCreateSchema,
    db: Session = Depends(get_db),
):
    try:
        return create_notifications_sync(notification.json(), db)

    except Exception as e:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e)
        )


def create_notifications_sync(notification, db):
    user_obj = db.query(UserModel).filter_by(id=notification.get("user_id")).first()
    notification_obj = Notifications(
        user=user_obj,
        type=notification.get("type"),
        type_id=notification.get("type_id"),
        is_read=notification.get("is_read"),
        expired=notification.get("expired"),
        created_on=notification.get("created_on"),
        last_modified_on=notification.get("last_modified_on"),
    )

    db.add(notification_obj)
    db.commit()
    db.refresh(notification_obj)

    return notification_obj
