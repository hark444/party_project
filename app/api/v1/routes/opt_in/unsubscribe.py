from fastapi import Depends, APIRouter, HTTPException, status, Path
from models import get_db
from sqlalchemy.orm import Session
from models.user import UserModel
from models.TeamUser import TeamUserModel
from models.teams import TeamsModel
from app.api.v1.routes.user.auth import get_current_user
from app.api.v1.schema.response.user import UserResponseSchema
from app.api.v1.routes.notifications.notifications import create_notifications_sync
from utils.authorization import ValidatePermissions
from app.api.v1.schema.request.team_user import TeamUserRequestSchema
from app.api.v1.routes.notifications.notifications import create_notifications_sync
from models.notifications import NotificationTypeEnum


unsubscribe_router = APIRouter(prefix="/unsubscribe", tags=["opt_in"])
allow_change_team = ValidatePermissions(["admin", "superadmin"])


@unsubscribe_router.post("", response_model=UserResponseSchema)
async def update_curr_user_team(
    team_user: TeamUserRequestSchema,
    db: Session = Depends(get_db),
    curr_user: UserModel = Depends(get_current_user),
):
    try:
        user_obj = db.query(UserModel).filter_by(id=team_user.user_id).first()

        if user_obj.team.team_name == team_user.team_name:
            user_obj.team = None
            user_obj.team_id = None

            db.add(user_obj)
            db.commit()
            db.refresh(user_obj)

            # Creating notification for the user
            # TODO: remove type_id from this object after notifications.type_id is nullable
            notifications_obj = {
                "user_id": user_obj.id,
                "type": NotificationTypeEnum.UNSUBSCRIBE.value,
                "type_id": user_obj.id,
            }
            create_notifications_sync(notifications_obj, db)

            return curr_user

        else:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="User is subscribed to a different team.",
            )

    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e)
        )
