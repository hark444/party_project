from app.api.v1.schema.request.base import TimeStampRequestSchema
from pydantic import validator
from models import get_db
from models.teams import TeamsModel


class TeamsRequestSchema(TimeStampRequestSchema):
    team_name: str = None

    @validator("team_name")
    def validate_team_name_uniqueness(cls, v):
        db = next(get_db())
        teams_obj = db.query(TeamsModel).filter_by(team_name=v.lower()).first()
        if teams_obj:
            raise ValueError(
                f"A team with the same name already exists. "
                f"Please try to create a team with a different name. "
            )
        return v
