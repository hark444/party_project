from fastapi import Depends, APIRouter, HTTPException, status, Path
from models import get_db
from sqlalchemy.orm import Session
from models.user import UserModel
from models.TeamUser import TeamUserModel
from models.teams import TeamsModel
from app.api.v1.routes.user.auth import get_current_user
from app.api.v1.schema.response.user import UserResponseSchema


opt_in_router = APIRouter(prefix="/opt_in", tags=["opt_in"])


@opt_in_router.get("/{unique_identifier}", response_model=UserResponseSchema)
async def get_party_list(
    unique_identifier: str = Path(title="The unique identifier for opt in"),
    db: Session = Depends(get_db),
    curr_user: UserModel = Depends(get_current_user),
):
    try:
        team_user_obj = (
            db.query(TeamUserModel)
            .filter_by(uuid=unique_identifier, user=curr_user)
            .first()
        )
        if not team_user_obj:
            return HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="No Opt-In request for this and user",
            )

        team_obj = db.query(TeamsModel).filter_by(id=team_user_obj.team_id).first()
        curr_user.team = team_obj
        return curr_user

    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e)
        )
