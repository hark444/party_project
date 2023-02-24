from fastapi import Depends, APIRouter, HTTPException, status
from models.teams import TeamsModel
from models.user import UserModel
from models import get_db
import logging
from sqlalchemy.orm import Session
from app.api.v1.schema.request.team_user import TeamUserRequestSchema
from app.api.v1.schema.response.teams import TeamsResponseSchema, AllTeamsResponseSchema
from app.api.v1.routes.auth import get_current_user

user_team_router = APIRouter(prefix="/user-teams", tags=["user-teams"])

logger = logging.getLogger("main")


@user_team_router.post("", status_code=status.HTTP_201_CREATED)
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


@team_router.get("/{team_id}", response_model=TeamsResponseSchema)
async def get_team_by_id(
    team_id: int,
    db: Session = Depends(get_db),
):
    teams_obj = db.query(TeamsModel).filter_by(id=team_id).first()
    if not teams_obj:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="No team with this ID was found.",
        )
    return teams_obj


@team_router.get("", response_model=AllTeamsResponseSchema)
async def get_teams(
    db: Session = Depends(get_db),
):
    teams_obj = db.query(TeamsModel)
    return {"data": teams_obj.all(), "total": teams_obj.count()}


@team_router.put("/{team_id}", response_model=TeamsResponseSchema)
async def update_team(
    team_id: int,
    team: TeamsRequestSchema,
    db: Session = Depends(get_db),
):
    teams_obj = db.query(TeamsModel).filter_by(id=team_id).first()
    if not teams_obj:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="No team with this ID was found.",
        )
    try:
        teams_obj.team_name = team.team_name.lower()
        db.add(teams_obj)
        db.commit()
        db.refresh(teams_obj)
        logger.info(f"Updated team {teams_obj.team_name}")
        return teams_obj
    except Exception as e:
        logger.exception(f"Team could not be updated as : {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e)
        )


@team_router.delete("/{team_id}", status_code=200)
async def delete_team(
    team_id: int,
    db: Session = Depends(get_db),
):
    teams_obj = db.query(TeamsModel).filter_by(id=team_id).first()
    if not teams_obj:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="No team with this ID was found.",
        )
    try:
        db.delete(teams_obj)
        db.commit()
        logger.info(f"Deleted team {teams_obj.team_name}")
        return
    except Exception as e:
        logger.exception(f"Team could not be deleted as : {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e)
        )
