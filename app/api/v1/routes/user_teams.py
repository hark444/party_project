from fastapi import Depends, APIRouter, HTTPException, status
from models.teams import TeamsModel
from models.user import UserModel
from models import get_db
import logging
from sqlalchemy.orm import Session
from app.api.v1.schema.request.team_user import TeamUserRequestSchema
from app.api.v1.schema.response.teams import TeamsResponseSchema
from app.api.v1.routes.auth import get_current_user
from utils.authorization import ValidatePermissions

user_team_router = APIRouter(prefix="/user-teams", tags=["user-teams"])

logger = logging.getLogger("main")

allow_change_team = ValidatePermissions(["admin"])


@user_team_router.post(
    "", status_code=status.HTTP_201_CREATED, dependencies=Depends(allow_change_team)
)
async def add_team_to_user(
    team_user: TeamUserRequestSchema, db: Session = Depends(get_db)
):
    try:
        # user_obj = db.query(UserModel).filter_by(id=team_user.user_id).first()
        #
        team_obj = db.query(TeamsModel).filter_by(team_name=team_user.team_name).first()
        #
        # user_obj.team = team_obj
        #
        # db.add(user_obj)
        # db.commit()
        # db.refresh(user_obj)
        logger.info(f"Team object is created with name: {team.team_name}")
        return teams_obj

    except Exception as e:
        logger.exception(f"Team could not be created as : {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e)
        )
