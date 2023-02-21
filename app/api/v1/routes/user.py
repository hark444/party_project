from fastapi import Depends, APIRouter, HTTPException, status
from models.user import UserModel
from models import get_db
from models.teams import TeamsModel
import logging
from sqlalchemy.orm import Session
from app.api.v1.schema.request.user import UserRequestSchema, UserRequestPostSchema
from app.api.v1.schema.response.user import UserResponseSchema
from app.api.v1.routes.auth import get_password_hash, get_current_user

user_router = APIRouter(prefix="/users", tags=["users"])

logger = logging.getLogger("main")


@user_router.post(
    "", response_model=UserResponseSchema, status_code=status.HTTP_201_CREATED
)
async def create_user(user: UserRequestPostSchema, db: Session = Depends(get_db)):
    try:
        team_obj = db.query(TeamsModel).filter_by(id=user.team_id).first()
        user_obj = UserModel(
            hashed_password=get_password_hash(user.password),
            email=user.email,
            first_name=user.first_name,
            last_name=user.last_name,
            team=team_obj,
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


@user_router.put("", response_model=UserResponseSchema)
async def update_user(
    user: UserRequestSchema,
    db: Session = Depends(get_db),
    curr_user: UserModel = Depends(get_current_user),
):
    try:
        for field, value in user:
            setattr(curr_user, field, value)

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
