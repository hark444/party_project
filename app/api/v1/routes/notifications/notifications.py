from fastapi import Depends, APIRouter, HTTPException, status, Path
from models import get_db
from sqlalchemy.orm import Session
from models.user import UserModel
from models.TeamUser import TeamUserModel
from models.teams import TeamsModel
from app.api.v1.routes.user.auth import get_current_user
from app.api.v1.schema.response.user import UserResponseSchema
from models.notifications import Notifications
from app.api.v1.schema.request.notifications import (
    NotificationCreateSchema,
    NotificationGetSchema,
)
from app.api.v1.schema.response.notifications import (
    NotificationResponseSchema,
    NotificationsResponseSchema,
)
import json


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


@notifications_router.get(
    "",
    response_model=NotificationsResponseSchema,
    response_description="notifications get",
)
async def get_notifications(
    args: NotificationGetSchema = Depends(), db: Session = Depends(get_db)
):
    base_query = db.query(Notifications).filter_by(expired=False)

    if args.user_id:
        base_query = base_query.filter_by(user_id=args.user_id)

    if args.type_id:
        base_query = base_query.filter_by(type_id=args.type_id)

    if args.type:
        base_query = base_query.filter_by(type=args.type)

    count = base_query.count()
    objects = base_query.all()

    return {"data": objects, "total": count}


# currently handling for id only
@notifications_router.put(
    "/{notification_id}", response_model=NotificationResponseSchema
)
async def update_notifications(
    notification_id: int,
    notification: NotificationCreateSchema,
    db: Session = Depends(get_db),
):
    try:
        return update_notifications_sync(notification.json(), notification_id, db)
    except Exception as e:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e)
        )


def update_notifications_sync(notification, notification_id, db):
    notifications_obj = db.query(Notifications).filter_by(id=notification_id).first()
    if not notifications_obj:
        return "No notifications object found for this ID."
    try:
        notification = json.loads(notification)
        for field, value in notification.items():
            setattr(notifications_obj, field, value)

        db.add(notifications_obj)
        db.commit()
        db.refresh(notifications_obj)

        return notifications_obj

    except Exception as e:
        db.rollback()
        return str(e)
