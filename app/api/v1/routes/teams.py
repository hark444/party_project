from fastapi import Depends, APIRouter, HTTPException, status
from models.teams import TeamsModel
from models import get_db
import logging
from sqlalchemy.orm import Session
from app.api.v1.schema.request.teams import TeamsRequestSchema
from app.api.v1.schema.response.teams import TeamsResponseSchema, AllTeamsResponseSchema

team_router = APIRouter(prefix="/teams", tags=["teams"])

logger = logging.getLogger("main")


@team_router.post("", response_model=TeamsResponseSchema)
async def create_team(team: TeamsRequestSchema, db: Session = Depends(get_db)):
    try:
        teams_obj = TeamsModel(
            team_name=team.team_name.lower(), created_on=team.created_on
        )

        db.add(teams_obj)
        db.commit()
        db.refresh(teams_obj)
        logger.info(f"Team object is created with name: {team.team_name}")
        return teams_obj

    except Exception as e:
        logger.exception(f"Team could not be created as : {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e)
        )


@team_router.get("/{team_id}", response_model=TeamsResponseSchema)
async def get_team(
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
