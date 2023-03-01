from app.api.v1.schema.request.base import TimeStampRequestSchema
from pydantic import validator
from models import get_db
from models.teams import TeamsModel
from models.user import UserModel


class TeamUserRequestSchema(TimeStampRequestSchema):
    team_name: str
    user_id: int

    @validator("team_name")
    def validate_team_name_exists(cls, v):
        db = next(get_db())
        teams_obj = db.query(TeamsModel).filter_by(team_name=v)
        if not teams_obj:
            raise ValueError(
                "No teams found with this name. You may create a new team if you are an admin."
            )
        return v

    @validator("user_id")
    def validate_user_exists(cls, v):
        db = next(get_db())
        user_obj = db.query(UserModel).filter_by(id=v)
        if not user_obj:
            raise ValueError("No user found with this ID.")
        return v
