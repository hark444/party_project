from fastapi import Depends, APIRouter, HTTPException, status
from models.teams import TeamsModel
from models.user import UserModel
from models.TeamUser import TeamUserModel
from models import get_db
import logging
import uuid
from sqlalchemy.orm import Session
from app.api.v1.schema.request.team_user import TeamUserRequestSchema
from app.api.v1.schema.response.TeamUser import TeamUserResponseSchema
from app.api.v1.routes.user.auth import get_current_user
from utils.authorization import ValidatePermissions
from settings import settings

user_team_router = APIRouter(prefix="/user-teams", tags=["user-teams"])

logger = logging.getLogger("main")

allow_change_team = ValidatePermissions(["admin"])

OPT_IN_LINK = settings.API.OPT_IN_LINK


@user_team_router.post(
    "",
    response_model=TeamUserResponseSchema,
    status_code=status.HTTP_201_CREATED,
    dependencies=[Depends(allow_change_team)],
)
async def add_team_to_user(
    team_user: TeamUserRequestSchema,
    db: Session = Depends(get_db),
    curr_user: UserModel = Depends(get_current_user),
):
    try:
        user_obj = db.query(UserModel).filter_by(id=team_user.user_id).first()

        team_obj = db.query(TeamsModel).filter_by(team_name=team_user.team_name).first()

        unique_identifier = str(uuid.uuid4())

        team_user_obj = TeamUserModel(
            uuid=unique_identifier,
            user=user_obj,
            team=team_obj,
            requested_by=curr_user,
        )
        db.add(team_user_obj)
        db.commit()
        db.refresh(team_user_obj)

        opt_in_link = OPT_IN_LINK + unique_identifier
        print(opt_in_link)

        return team_user_obj

    except Exception as e:
        logger.exception(f"Team User could not be created as : {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e)
        )
