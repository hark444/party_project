from fastapi import Depends, APIRouter, HTTPException, status
from models.user import UserModel
from models import get_db
from models.teams import TeamsModel
import logging
import datetime
from sqlalchemy.orm import Session
from app.api.v1.schema.request.user import (
    UserRequestSchema,
    UserRequestPostSchema,
    GetUserArgs,
)
from app.api.v1.schema.response.user import UserResponseSchema, UsersResponseSchema
from app.api.v1.routes.auth import get_password_hash, get_current_user

user_router = APIRouter(prefix="/users", tags=["users"])

logger = logging.getLogger("main")


@user_router.post(
    "", response_model=UserResponseSchema, status_code=status.HTTP_201_CREATED
)
async def create_user(user: UserRequestPostSchema, db: Session = Depends(get_db)):
    try:
        team_obj = None
        # Getting teams object for the given team name
        if user.team_name:
            team_obj = (
                db.query(TeamsModel).filter_by(team_name=user.team_name.lower()).first()
            )

        user_obj = UserModel(
            hashed_password=get_password_hash(user.password),
            email=user.email,
            first_name=user.first_name,
            last_name=user.last_name,
            team=team_obj,
            date_of_joining=user.date_of_joining,
            role=user.role,
        )

        db.add(user_obj)
        db.commit()
        db.refresh(user_obj)
        logger.info(f"A user is created with email: {user.email}")
        return user_obj

    except Exception as e:
        logger.exception(f"User could not be created as : {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e)
        )


@user_router.get("", response_model=UsersResponseSchema)
async def get_users(
    db: Session = Depends(get_db),
    args: GetUserArgs = Depends(),
):
    try:
        base_query = db.query(UserModel)
        # Evaluating args
        if args.team is not None and not args.team:
            base_query = base_query.filter_by(team=None)

        if args.team_name:
            team_obj = (
                db.query(TeamsModel).filter_by(team_name=args.team_name.lower()).first()
            )
            base_query = base_query.filter_by(team=team_obj)

        if args.doj:
            base_query = base_query.filter_by(date_of_joining=args.doj)

        if args.experience:
            today = datetime.date.today()
            experience_date = today.replace(year=today.year - args.experience)
            base_query = base_query.filter(UserModel.date_of_joining < experience_date)

        user_objects = base_query.all()
        total_objects = base_query.count()

        return {"data": user_objects, "total": total_objects}

    except Exception as e:
        logger.exception(f"User could not be found as : {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e)
        )


@user_router.put("", response_model=UserResponseSchema)
async def update_user(
    user: UserRequestSchema,
    db: Session = Depends(get_db),
    curr_user: UserModel = Depends(get_current_user),
):
    try:
        for field, value in user:
            setattr(curr_user, field, value)

        # Getting teams object for the given team name
        if user.team_name:
            team_obj = (
                db.query(TeamsModel).filter_by(team_name=user.team_name.lower()).first()
            )
            curr_user.team = team_obj

        db.add(curr_user)
        db.commit()
        db.refresh(curr_user)
        logger.info(f"Updated user {curr_user.email}")
        return curr_user
    except Exception as e:
        logger.exception(f"User could not be updated as : {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e)
        )


@user_router.delete("", status_code=200)
async def delete_user(
    db: Session = Depends(get_db),
    curr_user: UserModel = Depends(get_current_user),
):
    try:
        db.delete(curr_user)
        db.commit()
        logger.info(f"Deleted user {curr_user.email}")
        return
    except Exception as e:
        logger.exception(f"User could not be deleted as : {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e)
        )
