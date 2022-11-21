from fastapi import Depends, APIRouter, HTTPException, status
from models.user import UserModel
from models import get_db
import logging
from sqlalchemy.orm import Session
from app.api.v1.schema.request.user import UserRequestSchema
from app.api.v1.schema.response.user import UserResponseSchema
from app.api.v1.routes.auth import get_password_hash, get_current_user

user_router = APIRouter(prefix="/users", tags=["users"])

logger = logging.getLogger('main')


@user_router.post("/create", response_model=UserResponseSchema)
async def create_user(user: UserRequestSchema, db: Session = Depends(get_db)):
    try:
        user_obj = UserModel(
            hashed_password=get_password_hash(user.password),
            email=user.email,
            first_name=user.first_name,
            last_name=user.last_name,
        )

        db.add(user_obj)
        db.commit()
        db.refresh(user_obj)
        logger.info(f"A user is created with email: {user.email}")
        return user_obj

    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e)
        )


@user_router.put("/update", response_model=UserResponseSchema)
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
        return curr_user
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e)
        )
