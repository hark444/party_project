from pydantic import BaseModel, validator, root_validator
from typing import Optional
from pydantic.schema import datetime, date
from app.api.v1.schema.request.base import TimeStampRequestSchema
from models import get_db
from models.user import UserModel
from models.teams import TeamsModel
from fastapi import HTTPException
from models.role import RoleTypeEnum


class TokenGenerateSchema(BaseModel):
    email: str
    password: str


class UserRequestSchema(TimeStampRequestSchema):
    first_name: str = None
    last_name: str = None
    disabled: bool = False
    role: RoleTypeEnum | None = RoleTypeEnum.regular
    team_name: str | None = None
    date_of_joining: date = None

    @validator("team_name")
    def validate_team_must_exist(cls, v):
        db = next(get_db())
        teams_obj = db.query(TeamsModel).filter_by(team_name=v.lower()).first()
        if not teams_obj:
            raise ValueError(f"There is no existing team with this name.")
        return v


class UserRequestPostSchema(UserRequestSchema, TokenGenerateSchema):
    @validator("email")
    def validate_email_uniqueness(cls, v):
        db = next(get_db())
        user_obj = db.query(UserModel).filter_by(email=v).first()
        if user_obj:
            raise ValueError(
                f"A user with the same email already exists. "
                f"Please try to login or create a user with a different email"
            )
        return v


class GetUserArgs(BaseModel):
    team: bool | None = None
    team_name: str | None = None
    doj: str | None = None
    experience: int | None = None

    @root_validator()
    def validate_team_must_exist(cls, values):
        if values.get("team_name"):
            # Checking if team flag is not set as False
            if values.get("team") is False:
                raise HTTPException(
                    422, "The team flag is disabled but the team name is given."
                )

            # Checking if team name exists
            db = next(get_db())
            teams_obj = (
                db.query(TeamsModel)
                .filter_by(team_name=values.get("team_name").lower())
                .first()
            )
            if not teams_obj:
                raise HTTPException(422, "There is no existing team with this name.")
        return values
